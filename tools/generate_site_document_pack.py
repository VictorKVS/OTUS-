#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "site" / "data" / "site-document-pack.json"

def render(doc):
    title = Path(doc["path"]).stem.replace("_", " ")
    return f"""# {doc['id']} · {title}

| Field | Value |
|---|---|
| Document ID | {doc['id']} |
| Category | {doc['category']} |
| Status | BASELINED-DESIGN |
| Owner | {doc['owner']} |
| Approver | {doc['approver']} |
| Gate | {doc['gate']} |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

{doc['purpose']}

## Current baseline

Generated placeholder baseline. Replace with project-specific facts before approval. Until then the document is BLOCKED.

## Mandatory content

- Scope and assumptions.
- Project-specific decisions and constraints.
- Verification criteria.
- Links to code/data contracts/tests.
- Evidence requirements.
- Change control.

## Verification

Result model: PASS / WARN / FAIL / BLOCKED.

## Evidence

Attach exact page/file/registry/test/commit references.

## Change control

Version all material changes and rerun affected gates.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Only report missing files; do not create them.")
    args = ap.parse_args()

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    missing = []
    for doc in data["required_documents"]:
        path = ROOT / doc["path"]
        if not path.exists():
            missing.append(doc)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(render(doc), encoding="utf-8")
                print(f"CREATED {doc['id']} {doc['path']}")

    if args.check and missing:
        for doc in missing:
            print(f"MISSING {doc['id']} {doc['path']}")
        return 1

    print(f"SITE-DOC-PACK: required={len(data['required_documents'])}; missing={len(missing) if args.check else 0}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
