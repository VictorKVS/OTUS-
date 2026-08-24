from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def resolve_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    selections = sorted(
        private_root.glob("*/translation_selected_model.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not selections:
        raise FileNotFoundError("translation_selected_model.json not found; run tournament/select first")
    return selections[0].parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate book using the selected tournament winner.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    workspace = resolve_workspace(Path(args.private_root), args.workspace)
    selection_path = workspace / "translation_selected_model.json"
    selection = json.loads(selection_path.read_text(encoding="utf-8"))

    script = Path(__file__).resolve().parent / "book_translate.py"
    command = [
        sys.executable,
        str(script),
        str(workspace),
        "--base-url",
        str(selection["base_url"]),
        "--model",
        str(selection["model"]),
        "--timeout",
        str(args.timeout),
    ]
    if args.limit > 0:
        command.extend(["--limit", str(args.limit)])

    print(f"selected_model={selection['model']}")
    print(f"selected_base_url={selection['base_url']}")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
