from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {
    ".pdf": "PDF",
    ".epub": "EPUB",
    ".mobi": "MOBI",
    ".azw": "AZW",
    ".azw3": "AZW3",
    ".djvu": "DJVU",
    ".doc": "DOC",
    ".docx": "DOCX",
    ".rtf": "RTF",
    ".txt": "TXT",
    ".md": "MD",
}

ARCHITECTURE_KEYWORDS = {
    "architecture": 8,
    "architect": 7,
    "software architecture": 12,
    "solution architecture": 12,
    "system design": 10,
    "distributed systems": 9,
    "microservices": 8,
    "domain-driven": 8,
    "ddd": 6,
    "patterns": 6,
    "design patterns": 8,
    "data architecture": 8,
    "cloud architecture": 8,
    "enterprise architecture": 9,
    "fundamentals of software architecture": 14,
    "software architecture the hard parts": 16,
    "building evolutionary architectures": 12,
    "designing data-intensive applications": 13,
    "clean architecture": 10,
    "архитектур": 8,
    "проектирован": 6,
    "распределенн": 7,
    "микросервис": 7,
    "паттерн": 5,
}

LOW_PRIORITY_KEYWORDS = {
    "fiction": -10,
    "novel": -10,
    "роман": -10,
    "детектив": -10,
    "фантастика": -8,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_title(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r"[_]+", " ", stem)
    stem = re.sub(r"[-]{2,}", " ", stem)
    stem = re.sub(r"\s+", " ", stem)
    return stem.strip()


def architecture_score(title: str, relative_path: str) -> tuple[int, list[str]]:
    haystack = f" {title} {relative_path} ".casefold()
    score = 0
    matched: list[str] = []
    for keyword, weight in ARCHITECTURE_KEYWORDS.items():
        if keyword.casefold() in haystack:
            score += weight
            matched.append(keyword)
    for keyword, weight in LOW_PRIORITY_KEYWORDS.items():
        if keyword.casefold() in haystack:
            score += weight
            matched.append(keyword)
    return score, matched


def pdf_page_count(path: Path) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    try:
        reader = PdfReader(str(path))
        return len(reader.pages)
    except Exception:
        return None


@dataclass(slots=True)
class LibraryItem:
    item_id: str
    relative_path: str
    file_name: str
    normalized_title: str
    extension: str
    format: str
    size_bytes: int
    modified_at: str
    sha256: str
    page_count: int | None
    architecture_score: int
    matched_keywords: list[str]
    duplicate_group_size: int = 1

    def to_dict(self) -> dict:
        return asdict(self)


def iter_supported_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.casefold() in SUPPORTED_EXTENSIONS:
            yield path


def scan_library(root: Path) -> list[LibraryItem]:
    paths = sorted(iter_supported_files(root), key=lambda p: str(p).casefold())
    rows: list[LibraryItem] = []

    for index, path in enumerate(paths, start=1):
        relative = str(path.relative_to(root))
        digest = sha256_file(path)
        stat = path.stat()
        title = normalize_title(path.name)
        score, matched = architecture_score(title, relative)
        pages = pdf_page_count(path) if path.suffix.casefold() == ".pdf" else None
        item_id = f"BOOK-{digest[:16].upper()}"
        rows.append(
            LibraryItem(
                item_id=item_id,
                relative_path=relative,
                file_name=path.name,
                normalized_title=title,
                extension=path.suffix.casefold(),
                format=SUPPORTED_EXTENSIONS[path.suffix.casefold()],
                size_bytes=stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                sha256=digest,
                page_count=pages,
                architecture_score=score,
                matched_keywords=matched,
            )
        )
        print(f"[{index}/{len(paths)}] {relative}")

    counts: dict[str, int] = {}
    for row in rows:
        counts[row.sha256] = counts.get(row.sha256, 0) + 1
    for row in rows:
        row.duplicate_group_size = counts[row.sha256]
    return rows


def choose_pilot(items: list[LibraryItem]) -> LibraryItem | None:
    if not items:
        return None
    unique: dict[str, LibraryItem] = {}
    for item in items:
        current = unique.get(item.sha256)
        if current is None or item.architecture_score > current.architecture_score:
            unique[item.sha256] = item
    ranked = sorted(
        unique.values(),
        key=lambda item: (
            item.architecture_score,
            item.page_count or 0,
            item.size_bytes,
            item.normalized_title.casefold(),
        ),
        reverse=True,
    )
    return ranked[0] if ranked else None


def write_outputs(root: Path, items: list[LibraryItem], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    pilot = choose_pilot(items)
    duplicate_files = sum(1 for item in items if item.duplicate_group_size > 1)
    unique_hashes = len({item.sha256 for item in items})

    payload = {
        "schema_version": "father-library-inventory.v0.1",
        "generated_at": utc_now(),
        "source_root": str(root),
        "counters": {
            "files": len(items),
            "unique_files": unique_hashes,
            "duplicate_members": duplicate_files,
            "architecture_candidates": sum(1 for item in items if item.architecture_score > 0),
        },
        "pilot_candidate": pilot.to_dict() if pilot else None,
        "items": [item.to_dict() for item in items],
    }
    (output_dir / "library_inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    fields = list(LibraryItem.__dataclass_fields__.keys())
    with (output_dir / "library_inventory.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in items:
            row = item.to_dict()
            row["matched_keywords"] = "; ".join(item.matched_keywords)
            writer.writerow(row)

    ranked = sorted(
        items,
        key=lambda item: (item.architecture_score, item.normalized_title.casefold()),
        reverse=True,
    )
    lines = [
        "# Локальная библиотека архитектора — инвентарь",
        "",
        f"Сканирование: `{utc_now()}`",
        f"Источник: `{root}`",
        "",
        "## Счётчики",
        "",
        f"- файлов: **{len(items)}**",
        f"- уникальных по SHA-256: **{unique_hashes}**",
        f"- членов duplicate-групп: **{duplicate_files}**",
        f"- архитектурных кандидатов: **{sum(1 for item in items if item.architecture_score > 0)}**",
        "",
        "## Первый кандидат",
        "",
    ]
    if pilot:
        lines.extend(
            [
                f"**{pilot.normalized_title}**",
                "",
                f"- path: `{pilot.relative_path}`",
                f"- format: `{pilot.format}`",
                f"- score: `{pilot.architecture_score}`",
                f"- SHA-256: `{pilot.sha256}`",
                f"- pages: `{pilot.page_count if pilot.page_count is not None else 'unknown'}`",
                "",
            ]
        )
    else:
        lines.extend(["Кандидат не найден.", ""])

    lines.extend(
        [
            "## Топ архитектурных материалов",
            "",
            "| # | Score | Format | Pages | Duplicate | Title | Relative path |",
            "|---:|---:|---|---:|---:|---|---|",
        ]
    )
    for index, item in enumerate(ranked[:50], start=1):
        title = item.normalized_title.replace("|", "\\|")
        rel = item.relative_path.replace("|", "\\|")
        lines.append(
            f"| {index} | {item.architecture_score} | {item.format} | "
            f"{item.page_count if item.page_count is not None else ''} | "
            f"{item.duplicate_group_size} | {title} | `{rel}` |"
        )
    (output_dir / "library_inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if pilot:
        private_workspace = root.parent / "_PRIVATE_BOOK_CORPUS" / pilot.item_id
        private_workspace.mkdir(parents=True, exist_ok=True)
        pilot_manifest = {
            "schema_version": "father-book-pilot-local.v0.1",
            "created_at": utc_now(),
            "status": "SOURCE_REGISTERED",
            "source_root": str(root),
            "source_path": str(root / pilot.relative_path),
            "item": pilot.to_dict(),
            "next_stage": "TEXT_EXTRACTION",
            "private_workspace": str(private_workspace),
        }
        (private_workspace / "source_manifest.json").write_text(
            json.dumps(pilot_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory a local private book library.")
    parser.add_argument(
        "root",
        nargs="?",
        default=r"G:\1\OTUS\Библиотека",
        help="Library root. Default: G:\\1\\OTUS\\Библиотека",
    )
    parser.add_argument(
        "--output",
        default=r"G:\1\OTUS\knowledge\library_inventory\generated",
        help="Output directory for metadata-only inventory files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    output = Path(args.output)

    if not root.exists() or not root.is_dir():
        print(f"ERROR: library folder not found: {root}", file=sys.stderr)
        return 2

    items = scan_library(root)
    write_outputs(root, items, output)
    pilot = choose_pilot(items)

    print()
    print(f"files={len(items)}")
    print(f"unique_sha256={len({item.sha256 for item in items})}")
    print(f"output={output}")
    if pilot:
        print(f"pilot={pilot.relative_path}")
        print(f"pilot_id={pilot.item_id}")
        print(f"pilot_score={pilot.architecture_score}")
    else:
        print("pilot=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
