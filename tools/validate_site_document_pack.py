#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "site" / "data" / "site-document-pack.json"

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Current baseline",
    "## Mandatory content",
    "## Verification",
    "## Evidence",
    "## Change control",
]

def fail(msg, errors):
    errors.append(msg)
    print("FAIL:", msg)

def main():
    errors = []
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    docs = data.get("required_documents", [])
    if not docs:
        fail("registry has no required_documents", errors)

    ids = set()
    paths = set()
    categories = set()

    for doc in docs:
        did = doc.get("id")
        path_str = doc.get("path")
        categories.add(doc.get("category"))
        if not did or not path_str:
            fail(f"registry item missing id/path: {doc}", errors)
            continue
        if did in ids:
            fail(f"duplicate document id: {did}", errors)
        if path_str in paths:
            fail(f"duplicate document path: {path_str}", errors)
        ids.add(did); paths.add(path_str)

        for field in ("category","owner","approver","gate","purpose","status"):
            if not doc.get(field):
                fail(f"{did}: registry field missing: {field}", errors)

        path = ROOT / path_str
        if not path.exists():
            fail(f"{did}: file missing: {path_str}", errors)
            continue

        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 400:
            fail(f"{did}: document too small to be controlled documentation", errors)
        for needle in (f"| Document ID | {did} |", f"| Owner | {doc['owner']} |", f"| Approver | {doc['approver']} |", f"| Gate | {doc['gate']} |"):
            if needle not in text:
                fail(f"{did}: metadata mismatch: {needle}", errors)
        for section in REQUIRED_SECTIONS:
            if section not in text:
                fail(f"{did}: missing section {section}", errors)
        if re.search(r"\b(TODO|TBD)\b|\?\?\?", text):
            fail(f"{did}: unresolved placeholder found", errors)

    required_categories={"governance","ux","architecture","security","quality","operations"}
    missing_categories=required_categories-categories
    if missing_categories:
        fail(f"missing document categories: {sorted(missing_categories)}", errors)

    print(f"CHECKED: documents={len(docs)} categories={len(categories)} errors={len(errors)}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
