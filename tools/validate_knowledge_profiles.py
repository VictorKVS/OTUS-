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
