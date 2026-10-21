#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KIT_REG=ROOT/"factory"/"data"/"agent-kit-registry.json"
KB_REG=ROOT/"factory"/"data"/"knowledge-registry-v2.json"
TEMPLATE=ROOT/"agents"/"templates"/"new-agent-kit.json"

def slug(value):
    return re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-")

def main():
    ap=argparse.ArgumentParser(description="Create a FATHER Agent Kit inheriting shared K0 and selected K1 pack(s).")
    ap.add_argument("--kit-id",required=True)
    ap.add_argument("--agent-id",required=True)
    ap.add_argument("--name",required=True)
    ap.add_argument("--family",required=True)
    ap.add_argument("--role",required=True)
    ap.add_argument("--k1",action="append",required=True)
    ap.add_argument("--project-context",default=None)
    ap.add_argument("--status",default="DESIGN")
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()

    kits=json.loads(KIT_REG.read_text(encoding="utf-8"))
    kb=json.loads(KB_REG.read_text(encoding="utf-8"))
    template=json.loads(TEMPLATE.read_text(encoding="utf-8"))
    pack_ids={x["id"]:x for x in kb["specialist_packs"]}
    for pid in args.k1:
        if pid not in pack_ids:
            raise SystemExit(f"Unknown K1 pack: {pid}")

    if any(x["kit_id"]==args.kit_id for x in kits["kits"]): raise SystemExit(f"Kit already exists: {args.kit_id}")
    if any(x["agent_id"]==args.agent_id for x in kits["kits"]): raise SystemExit(f"Agent already exists: {args.agent_id}")

    common=kb["common_core"]
    m=template
    m["kit_id"]=args.kit_id; m["status"]=args.status
    m["agent"].update({"id":args.agent_id,"name":args.name,"family":args.family,"role":args.role})
    m["inheritance"]["common_core"]={"id":common["id"],"version":common["version"],"mode":"shared_reference"}
    m["inheritance"]["specialist_pack_ids"]=args.k1
    m["inheritance"]["project_context_id"]=args.project_context
    m["known_limitations"]=["new scaffold; complete skills/tools/policies/evaluation before validation"]

    path=Path("agents")/"kits"/slug(args.kit_id)/"manifest.json"
    record={"kit_id":args.kit_id,"agent_id":args.agent_id,"name":args.name,"family":args.family,"status":args.status,"path":str(path).replace(chr(92),"/"),"specialist_pack_ids":args.k1}
    profile={"agent_id":args.agent_id,"name":args.name,"family":args.family,"common_core_id":common["id"],"common_core_version":common["version"],"specialist_pack_ids":args.k1,"specialist_pack_versions":[pack_ids[x]["version"] for x in args.k1],"project_context_id":args.project_context,"retrieval_policy":"K0+K1+optional_K2 evidence-first","access_policy":"DEFINE_ME","citation_provenance_policy":"required","freshness_policy":"source_type_aware","conflict_policy":"surface_and_escalate"}

    if args.dry_run:
        print(json.dumps({"manifest":m,"registry":record,"knowledge_profile":profile},ensure_ascii=False,indent=2))
        return 0

    target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    kits["kits"].append(record); kb["agent_profiles"].append(profile)
    KIT_REG.write_text(json.dumps(kits,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    KB_REG.write_text(json.dumps(kb,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"CREATED {args.kit_id} -> {path}")
    print("NEXT: complete skills/tools/policies/evaluation, then run validate_agent_kits.py")
    return 0

if __name__=="__main__":
    raise SystemExit(main())