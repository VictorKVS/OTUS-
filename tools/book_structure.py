from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def looks_like_heading(text: str) -> bool:
    value = " ".join(text.split()).strip()
    if not value or len(value) > 140:
        return False
    if re.match(r"^(chapter|part|section|глава|часть|раздел)\b", value, flags=re.I):
        return True
    if value.isupper() and len(value.split()) <= 14:
        return True
    if re.match(r"^\d+(?:\.\d+)*\s+\S", value) and len(value) <= 120:
        return True
    return False


def block_type(text: str) -> str:
    stripped = text.strip()
    if looks_like_heading(stripped):
        return "HEADING"
    lines = [line for line in stripped.splitlines() if line.strip()]
    if lines and all(re.match(r"^\s*(?:[-*•]|\d+[.)])\s+", line) for line in lines):
        return "LIST"
    if lines and sum(1 for line in lines if re.match(r"^\s{2,}\S", line)) >= max(1, len(lines) // 2):
        return "CODE_OR_EXAMPLE"
    return "PARAGRAPH"


def split_blocks(text: str, *, max_chars: int = 1800) -> list[tuple[int, int, str]]:
    """Split translated page text into reviewable semantic blocks.

    We preserve page-level source provenance. This is intentionally conservative:
    it does not pretend that sub-paragraph translated offsets are byte-exact spans
    in the English original.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = []
    paragraph_re = re.compile(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", re.DOTALL)
    for match in paragraph_re.finditer(normalized):
        raw = match.group(0)
        lead = len(raw) - len(raw.lstrip())
        trail = len(raw) - len(raw.rstrip())
        start = match.start() + lead
        end = match.end() - trail
        if start < end:
            paragraphs.append((start, end, normalized[start:end]))

    if len(paragraphs) <= 1:
        # PDF page extraction often has line breaks but no blank paragraphs.
        # Pack lines into bounded blocks, preferring sentence boundaries.
        paragraphs = []
        cursor = 0
        buffer_start = None
        buffer_lines: list[str] = []
        buffer_len = 0
        for line in normalized.splitlines(keepends=True):
            raw_line = line
            clean = raw_line.strip()
            line_start = cursor
            cursor += len(raw_line)
            if not clean:
                if buffer_lines:
                    joined = " ".join(buffer_lines).strip()
                    paragraphs.append((buffer_start or 0, line_start, joined))
                    buffer_start = None
                    buffer_lines = []
                    buffer_len = 0
                continue

            if buffer_start is None:
                buffer_start = line_start + (len(raw_line) - len(raw_line.lstrip()))

            buffer_lines.append(clean)
            buffer_len += len(clean) + 1

            hard_boundary = looks_like_heading(clean) and len(buffer_lines) == 1
            sentence_boundary = bool(re.search(r"[.!?;:]$", clean))
            if hard_boundary or (buffer_len >= 700 and sentence_boundary) or buffer_len >= max_chars:
                joined = " ".join(buffer_lines).strip()
                paragraphs.append((buffer_start, cursor, joined))
                buffer_start = None
                buffer_lines = []
                buffer_len = 0

        if buffer_lines:
            joined = " ".join(buffer_lines).strip()
            paragraphs.append((buffer_start or 0, len(normalized), joined))

    # Split any oversized paragraph deterministically by sentences.
    results: list[tuple[int, int, str]] = []
    sentence_re = re.compile(r"[^.!?]+(?:[.!?]+|$)", re.MULTILINE)
    for start, end, paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            results.append((start, end, paragraph.strip()))
            continue
        chunk_parts: list[str] = []
        chunk_start = start
        consumed = 0
        for sentence in sentence_re.finditer(paragraph):
            piece = sentence.group(0).strip()
            if not piece:
                continue
            projected = sum(len(part) + 1 for part in chunk_parts) + len(piece)
            if chunk_parts and projected > max_chars:
                text_chunk = " ".join(chunk_parts).strip()
                results.append((chunk_start, min(end, chunk_start + len(text_chunk)), text_chunk))
                chunk_start = start + sentence.start()
                chunk_parts = []
            chunk_parts.append(piece)
            consumed = sentence.end()
        if chunk_parts:
            text_chunk = " ".join(chunk_parts).strip()
            results.append((chunk_start, min(end, start + max(consumed, len(paragraph))), text_chunk))

    return [row for row in results if row[2]]


def resolve_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    manifests = sorted(
        private_root.glob("*/translation_manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not manifests:
        raise FileNotFoundError("translation_manifest.json not found")
    return manifests[0].parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Create semantic book units after translation.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    workspace = resolve_workspace(Path(args.private_root), args.workspace)
    manifest_path = workspace / "translation_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    units = load_jsonl(Path(manifest["units_path"]))

    done = [unit for unit in units if unit.get("translation_status") == "DONE" and str(unit.get("translated_text") or "").strip()]
    if not args.allow_partial and len(done) != len(units):
        raise SystemExit(f"translation incomplete: {len(done)}/{len(units)}; structuring blocked")
    if not done:
        raise SystemExit("no translated units available")

    semantic: list[dict] = []
    current_heading: list[str] = []
    order = 0
    for page_unit in done:
        translated = str(page_unit.get("translated_text") or "")
        for local_start, local_end, text in split_blocks(translated):
            order += 1
            kind = block_type(text)
            if kind == "HEADING":
                current_heading = [" ".join(text.split())]
            semantic_id = stable_id(str(page_unit.get("unit_id")), str(local_start), str(local_end), text)
            semantic.append(
                {
                    "semantic_id": semantic_id,
                    "order": order,
                    "unit_type": kind,
                    "translated_text": text,
                    "translated_char_start_in_unit": local_start,
                    "translated_char_end_in_unit": local_end,
                    "heading_path": list(current_heading),
                    "source_unit_id": page_unit.get("unit_id"),
                    "source_page_start": page_unit.get("source_page_start"),
                    "source_page_end": page_unit.get("source_page_end"),
                    "source_text_sha256": page_unit.get("source_text_sha256"),
                    "source_char_start": page_unit.get("source_char_start"),
                    "source_char_end": page_unit.get("source_char_end"),
                    "translation_model": page_unit.get("translation_model"),
                    "translation_method": page_unit.get("translation_method"),
                    "review_status": "NEEDS_REVIEW",
                }
            )

    output = workspace / "semantic_units.jsonl"
    write_jsonl(output, semantic)

    counts: dict[str, int] = {}
    for row in semantic:
        counts[row["unit_type"]] = counts.get(row["unit_type"], 0) + 1

    structure_manifest = {
        "schema_version": "father-book-semantic-structure.v0.1",
        "status": "SEMANTIC_STRUCTURE_READY" if len(done) == len(units) else "SEMANTIC_STRUCTURE_PARTIAL",
        "generated_at": utc_now(),
        "workspace": str(workspace),
        "source_translation_units": len(units),
        "translated_units_used": len(done),
        "semantic_units": len(semantic),
        "type_counts": counts,
        "semantic_units_path": str(output),
        "provenance_policy": "translated sub-block -> translated page unit -> exact English source page span/hash",
        "next_stage": "KNOWLEDGE_ANALYST",
    }
    (workspace / "structure_manifest.json").write_text(
        json.dumps(structure_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"status={structure_manifest['status']}")
    print(f"translated_units_used={len(done)}/{len(units)}")
    print(f"semantic_units={len(semantic)}")
    for kind, count in sorted(counts.items()):
        print(f"{kind.lower()}={count}")
    print(f"output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
