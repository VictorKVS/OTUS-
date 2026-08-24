from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_text(value: str) -> str:
    return (
        str(value or "")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\x00", "")
    )


class _HTMLText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data)

    def text(self) -> str:
        return normalize_text("\n".join(self.parts)).strip()


def extract_pdf(path: Path) -> tuple[list[dict], str]:
    errors: list[str] = []

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        pages: list[dict] = []
        for number, page in enumerate(reader.pages, start=1):
            text = normalize_text(page.extract_text() or "").strip()
            pages.append({"page_number": number, "text": text})
        return pages, "PYPDF"
    except Exception as exc:
        errors.append(f"pypdf:{type(exc).__name__}:{exc}")

    try:
        import fitz  # type: ignore

        document = fitz.open(str(path))
        pages = []
        for number, page in enumerate(document, start=1):
            text = normalize_text(page.get_text("text") or "").strip()
            pages.append({"page_number": number, "text": text})
        return pages, "PYMUPDF"
    except Exception as exc:
        errors.append(f"pymupdf:{type(exc).__name__}:{exc}")

    raise RuntimeError("PDF extraction unavailable: " + " | ".join(errors))


def extract_docx(path: Path) -> tuple[list[dict], str]:
    try:
        from docx import Document  # type: ignore
    except Exception as exc:
        raise RuntimeError("python-docx is required for DOCX extraction") from exc

    document = Document(str(path))
    text = "\n\n".join(p.text for p in document.paragraphs if p.text.strip())
    return [{"page_number": None, "text": normalize_text(text).strip()}], "PYTHON_DOCX"


def extract_epub(path: Path) -> tuple[list[dict], str]:
    pages: list[dict] = []
    with ZipFile(path) as archive:
        names = sorted(
            name for name in archive.namelist()
            if name.casefold().endswith((".html", ".xhtml", ".htm"))
        )
        for index, name in enumerate(names, start=1):
            raw = archive.read(name)
            decoded = raw.decode("utf-8", errors="replace")
            parser = _HTMLText()
            parser.feed(decoded)
            text = parser.text()
            if text:
                pages.append({"page_number": index, "source_member": name, "text": text})
    return pages, "EPUB_ZIP_HTML"


def extract_plain(path: Path) -> tuple[list[dict], str]:
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            text = raw.decode(encoding)
            return [{"page_number": None, "text": normalize_text(text).strip()}], f"TEXT_{encoding.upper()}"
        except UnicodeDecodeError:
            continue
    raise RuntimeError("unable to decode text file")


def extract(path: Path) -> tuple[list[dict], str]:
    ext = path.suffix.casefold()
    if ext == ".pdf":
        return extract_pdf(path)
    if ext == ".docx":
        return extract_docx(path)
    if ext == ".epub":
        return extract_epub(path)
    if ext in {".txt", ".md", ".rtf"}:
        return extract_plain(path)
    raise RuntimeError(f"extraction is not implemented for {ext}")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from the selected private book pilot.")
    parser.add_argument(
        "manifest",
        nargs="?",
        help="Path to source_manifest.json. If omitted, newest pilot manifest is selected.",
    )
    parser.add_argument(
        "--private-root",
        default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS",
    )
    args = parser.parse_args()

    private_root = Path(args.private_root)
    if args.manifest:
        manifest_path = Path(args.manifest)
    else:
        candidates = sorted(
            private_root.glob("*/source_manifest.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            print("ERROR: no source_manifest.json found; run library_scan.py first", file=sys.stderr)
            return 2
        manifest_path = candidates[0]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_path = Path(manifest["source_path"])
    workspace = Path(manifest["private_workspace"])
    workspace.mkdir(parents=True, exist_ok=True)

    if not source_path.is_file():
        print(f"ERROR: source file not found: {source_path}", file=sys.stderr)
        return 3

    source_bytes = source_path.read_bytes()
    actual_sha = sha256_bytes(source_bytes)
    expected_sha = manifest.get("item", {}).get("sha256")
    if expected_sha and actual_sha != expected_sha:
        print("ERROR: source SHA-256 changed since inventory scan", file=sys.stderr)
        return 4

    try:
        raw_pages, method = extract(source_path)
    except Exception as exc:
        failure = {
            "status": "EXTRACTION_FAILED",
            "failed_at": utc_now(),
            "error": f"{type(exc).__name__}: {exc}",
            "source_path": str(source_path),
            "source_sha256": actual_sha,
        }
        (workspace / "extraction_manifest.json").write_text(
            json.dumps(failure, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"ERROR: {failure['error']}", file=sys.stderr)
        return 5

    pages: list[dict] = []
    full_parts: list[str] = []
    cursor = 0
    nonempty_pages = 0
    char_count = 0

    for raw_page in raw_pages:
        text = normalize_text(raw_page.get("text", "")).strip()
        if text:
            nonempty_pages += 1
            char_count += len(text)
        if full_parts:
            full_parts.append("\n\n")
            cursor += 2
        start = cursor
        full_parts.append(text)
        cursor += len(text)
        end = cursor
        page = dict(raw_page)
        page.update(
            {
                "char_start": start,
                "char_end": end,
                "text_sha256": sha256_text(text),
                "text_length": len(text),
            }
        )
        pages.append(page)

    full_text = "".join(full_parts)
    page_total = len(pages)
    text_page_ratio = (nonempty_pages / page_total) if page_total else 0.0
    average_chars = (char_count / nonempty_pages) if nonempty_pages else 0.0

    if page_total and (text_page_ratio < 0.60 or average_chars < 120):
        status = "NEEDS_OCR"
    elif not full_text.strip():
        status = "NEEDS_OCR"
    else:
        status = "TEXT_EXTRACTED"

    (workspace / "extracted_text.txt").write_text(full_text, encoding="utf-8")
    write_jsonl(workspace / "pages.jsonl", pages)

    extraction_manifest = {
        "schema_version": "father-book-extraction.v0.1",
        "status": status,
        "extracted_at": utc_now(),
        "source_path": str(source_path),
        "source_sha256": actual_sha,
        "source_size_bytes": len(source_bytes),
        "method": method,
        "page_total": page_total,
        "nonempty_pages": nonempty_pages,
        "text_page_ratio": text_page_ratio,
        "text_length": len(full_text),
        "average_chars_per_nonempty_page": average_chars,
        "extracted_text_sha256": sha256_text(full_text),
        "pages_path": str(workspace / "pages.jsonl"),
        "text_path": str(workspace / "extracted_text.txt"),
        "next_stage": "TRANSLATION_UNIT_PREPARATION" if status == "TEXT_EXTRACTED" else "OCR_REVIEW",
    }
    (workspace / "extraction_manifest.json").write_text(
        json.dumps(extraction_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"status={status}")
    print(f"method={method}")
    print(f"pages={page_total}")
    print(f"nonempty_pages={nonempty_pages}")
    print(f"text_length={len(full_text)}")
    print(f"workspace={workspace}")
    return 0 if status == "TEXT_EXTRACTED" else 6


if __name__ == "__main__":
    raise SystemExit(main())
