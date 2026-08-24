from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


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


def compact(text: str, limit: int) -> str:
    value = " ".join(str(text or "").split())
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 1)] + "…"


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview translated book units for human QC.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--chars", type=int, default=700)
    args = parser.parse_args()

    workspace = resolve_workspace(Path(args.private_root), args.workspace)
    manifest = json.loads((workspace / "translation_manifest.json").read_text(encoding="utf-8"))
    units = load_jsonl(Path(manifest["units_path"]))
    done = [unit for unit in units if unit.get("translation_status") == "DONE"][: max(1, args.count)]

    print(f"workspace={workspace}")
    print(f"translation_status={manifest.get('status')}")
    print(f"model={manifest.get('translation_model')}")
    print(f"translated={sum(1 for unit in units if unit.get('translation_status') == 'DONE')}/{len(units)}")
    print()

    if not done:
        print("NO_TRANSLATED_UNITS")
        return 2

    for index, unit in enumerate(done, start=1):
        print("=" * 78)
        print(
            f"#{index} order={unit.get('order')} page={unit.get('source_page_start')} "
            f"qc={unit.get('translation_qc')} flags={unit.get('translation_qc_flags') or []}"
        )
        print("SOURCE:")
        print(compact(str(unit.get("source_text") or ""), args.chars))
        print()
        print("RU:")
        print(compact(str(unit.get("translated_text") or ""), args.chars))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
