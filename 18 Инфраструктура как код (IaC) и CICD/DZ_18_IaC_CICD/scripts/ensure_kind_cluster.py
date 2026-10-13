from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    if shutil.which("kind") is None:
        print("ERROR: kind is not installed or not in PATH.", file=sys.stderr)
        return 2

    config = Path(args.config).resolve()
    if not config.exists():
        print(f"ERROR: kind config not found: {config}", file=sys.stderr)
        return 3

    listed = run("kind", "get", "clusters")
    clusters = {line.strip() for line in listed.stdout.splitlines() if line.strip()}
    if args.name in clusters:
        print(f"Kind cluster already exists: {args.name}")
        return 0

    print(f"Creating Kind cluster: {args.name}")
    created = subprocess.run(
        ["kind", "create", "cluster", "--name", args.name, "--config", str(config)],
        check=False,
    )
    return created.returncode


if __name__ == "__main__":
    raise SystemExit(main())
