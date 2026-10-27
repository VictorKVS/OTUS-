#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "factory" / "data" / "knowledge-registry-v2.json"
CONTRACT = ROOT / "factory" / "data" / "knowledge-architecture.json"
LIFECYCLE = ROOT / "factory" / "data" / "agent-lifecycle-gates.json"

def fail(msg):
    print(f"FAIL: {msg}")
    return False

def main():
    ok = True
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    lifecycle = json.loads(LIFECYCLE.read_text(encoding="utf-8"))

    common = registry.get("common_core") or {}
    if not common.get("id") or not common.get("version"):
        ok = fail("K0 common core id/version missing") and ok

    common_manifest_path = common.get("manifest_path")
    if not common_manifest_path:
        ok = fail("K0 manifest_path missing") and ok
    else:
        mp = ROOT / common_manifest_path
        if not mp.exists():
            ok = fail(f"K0 manifest not found: {common_manifest_path}") and ok
        else:
            m = json.loads(mp.read_text(encoding="utf-8"))
            if m.get("id") != common.get("id") or m.get("version") != common.get("version"):
                ok = fail("K0 manifest id/version mismatch") and ok

    common_curriculum_path = common.get("curriculum_path")
    if not common_curriculum_path:
        ok = fail("K0 curriculum_path missing") and ok
    else:
        cp = ROOT / common_curriculum_path
        if not cp.exists():
            ok = fail(f"K0 curriculum not found: {common_curriculum_path}") and ok
        else:
            c = json.loads(cp.read_text(encoding="utf-8"))
            if c.get("knowledge_pack_id") != common.get("id") or c.get("version") != common.get("version"):
                ok = fail("K0 curriculum id/version mismatch") and ok
            if not c.get("graduation_gate"):
                ok = fail("K0 graduation_gate missing") and ok

    packs = {x["id"]: x for x in registry.get("specialist_packs", [])}
    contexts = {x["id"]: x for x in registry.get("project_contexts", [])}
    profiles = registry.get("agent_profiles", [])
    required = set(contract.get("agent_knowledge_profile_required_fields", []))

    if not profiles:
        ok = fail("no agent knowledge profiles") and ok

    seen = set()
    for p in profiles:
        aid = p.get("agent_id")
        if not aid:
            ok = fail("profile without agent_id") and ok
            continue
        if aid in seen:
            ok = fail(f"duplicate agent_id {aid}") and ok
        seen.add(aid)

        missing = [x for x in required if x not in p]
        if missing:
            ok = fail(f"{aid}: missing fields {missing}") and ok

        if p.get("common_core_id") != common.get("id"):
            ok = fail(f"{aid}: incompatible common_core_id") and ok
        if p.get("common_core_version") != common.get("version"):
            ok = fail(f"{aid}: incompatible common_core_version") and ok

        ids = p.get("specialist_pack_ids", [])
        vers = p.get("specialist_pack_versions", [])
        if not ids:
            ok = fail(f"{aid}: no K1 specialist pack") and ok
        if len(ids) != len(vers):
            ok = fail(f"{aid}: K1 id/version count mismatch") and ok
        for i, pid in enumerate(ids):
            pack = packs.get(pid)
            if not pack:
                ok = fail(f"{aid}: unknown specialist pack {pid}") and ok
                continue
            if i < len(vers) and vers[i] != pack.get("version"):
                ok = fail(f"{aid}: version mismatch for {pid}") and ok
            if common.get("id") not in pack.get("depends_on", []):
                ok = fail(f"{pid}: missing dependency on K0") and ok
            if pack.get("status") != "PLANNED":
                curriculum_path = pack.get("curriculum_path")
                if not curriculum_path:
                    ok = fail(f"{pid}: active pack has no curriculum_path") and ok
                else:
                    cp = ROOT / curriculum_path
                    if not cp.exists():
                        ok = fail(f"{pid}: curriculum not found: {curriculum_path}") and ok
                    else:
                        c = json.loads(cp.read_text(encoding="utf-8"))
                        if c.get("knowledge_pack_id") != pid or c.get("version") != pack.get("version"):
                            ok = fail(f"{pid}: curriculum id/version mismatch") and ok
                        if not c.get("graduation_gate"):
                            ok = fail(f"{pid}: graduation_gate missing") and ok
            manifest_path = pack.get("manifest_path")
            if not manifest_path:
                ok = fail(f"{pid}: manifest_path missing") and ok
            else:
                mp = ROOT / manifest_path
                if not mp.exists():
                    ok = fail(f"{pid}: manifest not found: {manifest_path}") and ok
                else:
                    m = json.loads(mp.read_text(encoding="utf-8"))
                    if m.get("id") != pid or m.get("version") != pack.get("version"):
                        ok = fail(f"{pid}: manifest id/version mismatch") and ok

        ctx = p.get("project_context_id")
        if ctx and ctx not in contexts:
            ok = fail(f"{aid}: unknown project context {ctx}") and ok

    s3 = next((x for x in lifecycle.get("stages", []) if x.get("id") == "S3"), None)
    if not s3 or not s3.get("knowledge_gate", {}).get("common_core_required"):
        ok = fail("lifecycle S3 does not enforce Common Core") and ok
    if not s3 or not s3.get("knowledge_gate", {}).get("specialist_pack_required"):
        ok = fail("lifecycle S3 does not enforce Specialist Pack") and ok

    if ok:
        print(f"PASS: K0={common['id']}@{common['version']}; K1={len(packs)}; profiles={len(profiles)}; contexts={len(contexts)}")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
