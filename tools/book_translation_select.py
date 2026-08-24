from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    reports = sorted(
        private_root.glob("*/translation_tournament.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not reports:
        raise FileNotFoundError("translation_tournament.json not found")
    return reports[0].parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Select one translator from a completed tournament.")
    parser.add_argument("rank", type=int, help="1-based rank from the tournament leaderboard")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    args = parser.parse_args()

    workspace = resolve_workspace(Path(args.private_root), args.workspace)
    report_path = workspace / "translation_tournament.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    ranking = list(report.get("ranking") or [])
    if args.rank < 1 or args.rank > len(ranking):
        raise SystemExit(f"rank must be between 1 and {len(ranking)}")

    selected = ranking[args.rank - 1]
    selection = {
        "schema_version": "father-book-selected-translator.v0.1",
        "selected_at": utc_now(),
        "selection_method": "TRANSLATOR_TOURNAMENT_MANUAL",
        "selected_rank": args.rank,
        "base_url": selected["base_url"],
        "model": selected["model"],
        "mean_score": selected["mean_score"],
        "pass_count": selected["pass_count"],
        "sample_count": selected["sample_count"],
        "report_path": str(report_path),
    }
    output = workspace / "translation_selected_model.json"
    output.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("status=TRANSLATOR_SELECTED")
    print(f"rank={args.rank}")
    print(f"model={selected['model']}")
    print(f"base_url={selected['base_url']}")
    print(f"selection={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
