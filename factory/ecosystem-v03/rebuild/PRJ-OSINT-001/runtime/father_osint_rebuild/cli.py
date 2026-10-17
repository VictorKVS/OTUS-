"""CLI for the FATHER OSINT parity rebuild."""

import argparse
import json
from pathlib import Path

from .service import DEFAULT_DB, connect, ingest, report


def main():
    parser = argparse.ArgumentParser(
        description="FATHER rebuild of offline OSINT TRIAGE demo; no network collection"
    )
    parser.add_argument("command", choices=["init", "import", "report"])
    parser.add_argument("path", nargs="?")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    args = parser.parse_args()

    with connect(Path(args.db)) as con:
        if args.command == "init":
            print(f"Initialized: {args.db}")
        elif args.command == "report":
            output = Path(args.db).with_name("report_generated.md")
            output.write_text(report(con), encoding="utf-8")
            print(f"Saved: {output}")
        else:
            if not args.path:
                parser.error("import requires path to JSONL")
            for lineno, line in enumerate(
                Path(args.path).read_text(encoding="utf-8").splitlines(),
                1,
            ):
                if not line.strip():
                    continue
                try:
                    case_id, action = ingest(con, json.loads(line))
                    print(f"line {lineno}: CASE-{case_id:05d} {action}")
                except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
                    print(f"line {lineno}: rejected: {exc}")


if __name__ == "__main__":
    main()
