from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="father-dz18")
    args = parser.parse_args()

    if shutil.which("minikube") is None:
        print("ERROR: minikube is not installed or not in PATH.", file=sys.stderr)
        return 2

    status = run("minikube", "status", "-p", args.profile, "--output=json")
    if status.returncode == 0 and '"Host": "Running"' in status.stdout:
        print(f"Minikube profile already running: {args.profile}")
        return 0

    print(f"Starting Minikube profile: {args.profile}")
    started = subprocess.run(
        [
            "minikube", "start",
            "-p", args.profile,
            "--driver=docker",
            "--cpus=2",
            "--memory=4096",
        ],
        check=False,
    )
    return started.returncode


if __name__ == "__main__":
    raise SystemExit(main())
