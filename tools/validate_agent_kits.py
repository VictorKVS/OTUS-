#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KIT_REG=ROOT/"factory"/"data"/"agent-kit-registry.json"
KB_REG=ROOT/"factory"/"data"/"knowledge-registry-v2.json"

def fail(msg, errors):
    errors.append(msg)
    print("FAIL:", msg)

def main():
    errors=[]
    kits=json.loads(KIT_REG.read_text(encoding="utf-8"))
    kb=json.loads(KB_REG.read_text(encoding="utf-8"))
    common=kb["common_core"]
    packs={x["id"]:x for x in kb.get("specialist_packs",[])}
    profiles={x["agent_id"]:x for x in kb.get("agent_profiles",[])}

    base_ref=kits.get("base_kit",{})
    base_path=ROOT/base_ref.get("path","")
    if not base_path.exists():
        fail(f"base kit missing: {base_ref.get('path')}",errors)
    else:
        base=json.loads(base_path.read_text(encoding="utf-8"))
        if base.get("kit_id")!=base_ref.get("id") or base.get("version")!=base_ref.get("version"):
            fail("base kit registry/manifest mismatch",errors)

    seen_kits=set(); seen_agents=set()
    for item in kits.get("kits",[]):
        kid=item.get("kit_id"); aid=item.get("agent_id")
        if kid in seen_kits: fail(f"duplicate kit_id {kid}",errors)
        if aid in seen_agents: fail(f"duplicate agent_id {aid}",errors)
        seen_kits.add(kid); seen_agents.add(aid)

        path=ROOT/item["path"]
        if not path.exists():
            fail(f"{kid}: manifest missing {item['path']}",errors)
            continue
        m=json.loads(path.read_text(encoding="utf-8"))
        if m.get("kit_id")!=kid: fail(f"{kid}: manifest kit_id mismatch",errors)
        if m.get("agent",{}).get("id")!=aid: fail(f"{kid}: manifest agent id mismatch",errors)
        if m.get("status")!=item.get("status"): fail(f"{kid}: status mismatch registry/manifest",errors)

        inh=m.get("inheritance",{})
        cc=inh.get("common_core",{})
        if cc.get("id")!=common.get("id") or cc.get("version")!=common.get("version"):
            fail(f"{kid}: incompatible K0 common core",errors)
        if cc.get("mode")!="shared_reference":
            fail(f"{kid}: K0 must use shared_reference",errors)

        mids=inh.get("specialist_pack_ids",[])
        if not mids: fail(f"{kid}: no K1 specialist pack",errors)
        if mids!=item.get("specialist_pack_ids",[]): fail(f"{kid}: K1 mismatch registry/manifest",errors)
        for pid in mids:
            p=packs.get(pid)
            if not p:
                fail(f"{kid}: unknown K1 {pid}",errors)
                continue
            for field in ("manifest_path","curriculum_path"):
                pth=p.get(field)
                if not pth or not (ROOT/pth).exists():
                    fail(f"{kid}: {pid} missing {field}",errors)

        for field in ("skills","tools","workflows"):
            if not m.get(field): fail(f"{kid}: empty {field}",errors)
        for field in ("instruction_policy","memory_policy","evaluation_profile","environment_profile","permissions"):
            if not m.get(field): fail(f"{kid}: missing {field}",errors)
        dossier=m.get("dossier",{})
        if not dossier.get("standard") or not (ROOT/dossier["standard"]).exists():
            fail(f"{kid}: dossier standard missing",errors)

        profile=profiles.get(aid)
        if not profile:
            fail(f"{kid}: no knowledge profile for agent {aid}",errors)
        else:
            if profile.get("common_core_id")!=common.get("id") or profile.get("common_core_version")!=common.get("version"):
                fail(f"{kid}: knowledge profile K0 mismatch",errors)
            if profile.get("specialist_pack_ids")!=mids:
                fail(f"{kid}: knowledge profile K1 mismatch",errors)

        if m.get("status")=="CERTIFIED" and not m.get("certificate"):
            fail(f"{kid}: CERTIFIED without certificate evidence",errors)

    print(f"CHECKED: kits={len(kits.get('kits',[]))} errors={len(errors)} common={common['id']}@{common['version']}")
    return 1 if errors else 0

if __name__=="__main__":
    sys.exit(main())