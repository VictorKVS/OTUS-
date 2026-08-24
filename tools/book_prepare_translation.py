from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def split_paragraphs(text: str) -> list[tuple[int, int, str]]:
    results: list[tuple[int, int, str]] = []
    paragraph_re = re.compile(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", re.DOTALL)
    for match in paragraph_re.finditer(text):
        raw = match.group(0)
        leading = len(raw) - len(raw.lstrip())
        trailing = len(raw) - len(raw.rstrip())
        start = match.start() + leading
        end = match.end() - trailing
        if start < end:
            results.append((start, end, text[start:end]))
    return results


def page_for_offset(pages: list[dict], offset: int) -> int | None:
    for page in pages:
        if int(page.get("char_start", 0)) <= offset <= int(page.get("char_end", 0)):
            return page.get("page_number")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare translation units for one extracted private book.")
    parser.add_argument(
        "workspace",
        nargs="?",
        help="Private book workspace; if omitted the newest workspace with extraction_manifest.json is used.",
    )
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    args = parser.parse_args()

    private_root = Path(args.private_root)
    if args.workspace:
        workspace = Path(args.workspace)
    else:
        manifests = sorted(
            private_root.glob("*/extraction_manifest.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not manifests:
            print("ERROR: extraction manifest not found; run book_extract.py first", file=sys.stderr)
            return 2
        workspace = manifests[0].parent

    extraction_manifest_path = workspace / "extraction_manifest.json"
    if not extraction_manifest_path.is_file():
        print(f"ERROR: missing {extraction_manifest_path}", file=sys.stderr)
        return 3

    extraction = json.loads(extraction_manifest_path.read_text(encoding="utf-8"))
    if extraction.get("status") != "TEXT_EXTRACTED":
        print(
            f"ERROR: extraction status is {extraction.get('status')}; translation preparation blocked",
            file=sys.stderr,
        )
        return 4

    text_path = Path(extraction["text_path"])
    pages_path = Path(extraction["pages_path"])
    text = text_path.read_text(encoding="utf-8")
    pages = load_jsonl(pages_path)

    units: list[dict] = []
    for order, (start, end, source_text) in enumerate(split_paragraphs(text), start=1):
        source_hash = sha256_text(source_text)
        unit_id = stable_id(extraction["source_sha256"], str(start), str(end), source_hash)
        start_page = page_for_offset(pages, start)
        end_page = page_for_offset(pages, max(start, end - 1))
        units.append(
            {
                "unit_id": unit_id,
                "order": order,
                "source_char_start": start,
                "source_char_end": end,
                "source_page_start": start_page,
                "source_page_end": end_page,
                "source_text": source_text,
                "source_text_sha256": source_hash,
                "target_language": "ru",
                "translated_text": None,
                "translation_status": "PENDING",
                "translation_method": None,
                "translation_model": None,
                "translation_review": "NOT_REVIEWED",
            }
        )

    if not units:
        print("ERROR: no translation units produced", file=sys.stderr)
        return 5

    units_path = workspace / "translation_units.jsonl"
    with units_path.open("w", encoding="utf-8", newline="\n") as handle:
        for unit in units:
            handle.write(json.dumps(unit, ensure_ascii=False, sort_keys=True) + "\n")

    manifest = {
        "schema_version": "father-book-translation-plan.v0.1",
        "status": "TRANSLATION_UNITS_READY",
        "prepared_at": utc_now(),
        "source_sha256": extraction["source_sha256"],
        "extracted_text_sha256": extraction["extracted_text_sha256"],
        "units": len(units),
        "translated_units": 0,
        "target_language": "ru",
        "units_path": str(units_path),
        "next_stage": "TRANSLATE_UNITS",
        "rules": {
            "preserve_source_text": True,
            "preserve_source_hash": True,
            "translation_must_not_replace_source": True,
            "semantic_analysis_before_translation_complete": False,
        },
    }
    (workspace / "translation_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("status=TRANSLATION_UNITS_READY")
    print(f"units={len(units)}")
    print(f"workspace={workspace}")
    print(f"units_path={units_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
