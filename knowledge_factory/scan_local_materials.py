from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "knowledge_factory" / "reports"

TEXT_READY = {".txt", ".md", ".markdown", ".html", ".htm", ".ipynb"}
PDF_PENDING = {".pdf"}
CODE_ASSETS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".yaml", ".yml", ".json", ".toml",
    ".ini", ".cfg", ".conf", ".sh", ".ps1", ".cmd", ".bat", ".sql", ".tf",
    ".dockerfile",
}
SKIP_DIRS = {
    ".git", ".github", ".idea", ".vscode", ".venv", "venv", "env", "node_modules",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build",
}


@dataclass(frozen=True, slots=True)
class InventoryRecord:
    material_id: str
    lesson: int | None
    relative_path: str
    file_name: str
    extension: str
    byte_size: int
    sha256: str
    route: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def lesson_from_path(relative: Path) -> int | None:
    if not relative.parts:
        return None
    match = re.match(r"^\s*(\d{1,4})\b", relative.parts[0])
    return int(match.group(1)) if match else None


def route_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_READY:
        return "READY_FOR_COURSE_COMPILER"
    if suffix in PDF_PENDING:
        return "PDF_PARSER_PENDING"
    if suffix in CODE_ASSETS or path.name.lower() == "dockerfile":
        return "CODE_ASSET"
    return "INVENTORIED_OTHER"


def material_id(lesson: int | None, relative: str, digest: str) -> str:
    prefix = f"OTUS-L{lesson:02d}" if lesson is not None else "OTUS-UNMAPPED"
    stable = hashlib.sha256(f"{relative}\x1f{digest}".encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-LOCAL-{stable}"


def scan(repo_root: Path) -> list[InventoryRecord]:
    records: list[InventoryRecord] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(repo_root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if relative.parts and relative.parts[0] == "knowledge_factory" and "reports" in relative.parts:
            continue
        try:
            digest = sha256_file(path)
            size = path.stat().st_size
        except OSError:
            continue
        lesson = lesson_from_path(relative)
        relative_text = relative.as_posix()
        records.append(
            InventoryRecord(
                material_id=material_id(lesson, relative_text, digest),
                lesson=lesson,
                relative_path=relative_text,
                file_name=path.name,
                extension=path.suffix.lower(),
                byte_size=size,
                sha256=digest,
                route=route_for(path),
            )
        )
    return records


def write_outputs(records: list[InventoryRecord], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "local_inventory.jsonl"
    md_path = output_dir / "LOCAL_INVENTORY.md"

    route_counts = Counter(item.route for item in records)
    lesson_counts: dict[int | None, Counter[str]] = defaultdict(Counter)
    lesson_bytes: Counter[int | None] = Counter()
    for item in records:
        lesson_counts[item.lesson][item.route] += 1
        lesson_bytes[item.lesson] += item.byte_size

    with jsonl_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps({
            "record_type": "INVENTORY_SUMMARY",
            "files": len(records),
            "bytes": sum(item.byte_size for item in records),
            "routes": dict(sorted(route_counts.items())),
        }, ensure_ascii=False, sort_keys=True) + "\n")
        for item in records:
            payload = item.to_dict()
            payload["record_type"] = "LOCAL_MATERIAL"
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    lines = [
        "# OTUS local material inventory",
        "",
        "Generated locally. Contains metadata and hashes only; it does not duplicate source files.",
        "",
        "## Summary",
        "",
        f"- files: **{len(records)}**",
        f"- bytes: **{sum(item.byte_size for item in records)}**",
    ]
    for route, count in sorted(route_counts.items()):
        lines.append(f"- `{route}`: **{count}**")

    lines += [
        "",
        "## By lesson",
        "",
        "| Lesson | Files | Bytes | Ready text | PDF pending | Code assets | Other |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for lesson in sorted(lesson_counts, key=lambda value: (value is None, value or 0)):
        counts = lesson_counts[lesson]
        label = str(lesson) if lesson is not None else "unmapped"
        lines.append(
            f"| {label} | {sum(counts.values())} | {lesson_bytes[lesson]} | "
            f"{counts['READY_FOR_COURSE_COMPILER']} | {counts['PDF_PARSER_PENDING']} | "
            f"{counts['CODE_ASSET']} | {counts['INVENTORIED_OTHER']} |"
        )

    lines += [
        "",
        "## Routing rule",
        "",
        "- `READY_FOR_COURSE_COMPILER` → FATHER `course-preliminary-v1`;",
        "- `PDF_PARSER_PENDING` → dedicated PDF adapter before semantic extraction;",
        "- `CODE_ASSET` → code/repository analysis lane;",
        "- `INVENTORIED_OTHER` → classify manually before processing.",
        "",
        "No semantic knowledge is promoted by this inventory step.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return {"jsonl": jsonl_path.as_posix(), "markdown": md_path.as_posix()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory OTUS local materials for FATHER Knowledge Factory")
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    records = scan(Path(args.repo_root).resolve())
    outputs = write_outputs(records, Path(args.output).resolve())
    print(json.dumps({
        "status": "PASS",
        "files": len(records),
        "bytes": sum(item.byte_size for item in records),
        "routes": dict(Counter(item.route for item in records)),
        "outputs": outputs,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
