from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports" / "gost_ib_inventory"
INVENTORY_JSON = REPORT_ROOT / "LATEST_GOST_IB_INVENTORY.json"
INVENTORY_CSV = REPORT_ROOT / "gost_ib_inventory.csv"
REGISTRY = ROOT / "data" / "gost_ib_currentness_registry_2026-08-27.json"
OUTPUT = REPORT_ROOT / "LATEST_GOST_IB_CURRENT_STAGE.json"
CONFIRM = "COPY_VERIFIED_CURRENT_GOSTS"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*]+', "_", value).strip().rstrip(".")
    return re.sub(r"\s+", " ", value)[:140] or "STANDARD"


def current_designations(registry_path: Path) -> set[str]:
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    return {
        str(row.get("designation") or "").strip()
        for row in payload.get("entries", [])
        if isinstance(row, dict) and row.get("status") == "CURRENT" and str(row.get("designation") or "").strip()
    }


def choose_designation(row: dict[str, str], verified: set[str]) -> str:
    direct = str(row.get("designation") or "").strip()
    if direct in verified:
        return direct
    content = str(row.get("content_designation_candidate") or "").strip()
    if content in verified:
        return content
    return ""


def build_plan(rows: list[dict[str, str]], source_root: Path, verified: set[str]) -> tuple[list[dict], list[dict]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    source_prefix = str(source_root.resolve()).casefold().rstrip("\\/") + "\\"
    for row in rows:
        path_text = str(row.get("path") or "")
        if not path_text.casefold().startswith(source_prefix):
            continue
        designation = choose_designation(row, verified)
        if designation:
            grouped[designation].append(row)

    safe: list[dict] = []
    blocked: list[dict] = []
    for designation in sorted(grouped):
        items = grouped[designation]
        by_hash: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in items:
            digest = str(row.get("sha256") or "").strip().lower()
            if digest:
                by_hash[digest].append(row)
        if len(by_hash) != 1:
            blocked.append({
                "designation": designation,
                "reason": "MULTIPLE_DISTINCT_SHA256" if len(by_hash) > 1 else "NO_SHA256",
                "distinct_sha256_total": len(by_hash),
                "files": [row.get("path") for row in items],
            })
            continue
        digest, same = next(iter(by_hash.items()))
        exemplar = sorted(same, key=lambda row: (len(str(row.get("name") or "")), str(row.get("name") or "")))[0]
        safe.append({
            "designation": designation,
            "sha256": digest,
            "source": exemplar.get("path"),
            "source_name": exemplar.get("name"),
            "local_exact_copies_total": len(same),
        })
    return safe, blocked


def existing_hashes(root: Path) -> set[str]:
    values: set[str] = set()
    if not root.exists():
        return values
    for path in root.rglob("*"):
        if path.is_file():
            try:
                values.add(sha256(path))
            except OSError:
                pass
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan/copy only Rosstandart-verified CURRENT IB standards into Architect library.")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm", default="")
    args = parser.parse_args()

    for required in (INVENTORY_JSON, INVENTORY_CSV, REGISTRY):
        if not required.is_file():
            print(json.dumps({"status": "BLOCKED", "reason": "MISSING_INPUT", "path": str(required)}, ensure_ascii=False, indent=2))
            return 2

    inventory = json.loads(INVENTORY_JSON.read_text(encoding="utf-8"))
    source_root = Path(str(inventory["source"]))
    target_root = Path(str(inventory["target"])) / "CURRENT"
    verified = current_designations(REGISTRY)
    with INVENTORY_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    safe, blocked = build_plan(rows, source_root, verified)
    target_hashes = existing_hashes(Path(str(inventory["target"])))

    actions = []
    for row in safe:
        src = Path(str(row["source"]))
        dst_dir = target_root / safe_name(str(row["designation"]))
        dst = dst_dir / src.name
        action = "ALREADY_PRESENT_EXACT" if row["sha256"] in target_hashes else "COPY"
        actions.append({**row, "target": str(dst), "action": action})

    if args.apply:
        if args.confirm != CONFIRM:
            print(json.dumps({"status": "BLOCKED", "reason": "CONFIRMATION_REQUIRED", "required": CONFIRM}, ensure_ascii=False, indent=2))
            return 3
        if blocked:
            print(json.dumps({"status": "BLOCKED", "reason": "IDENTITY_COLLISIONS_PRESENT", "blocked_total": len(blocked)}, ensure_ascii=False, indent=2))
            return 4
        for row in actions:
            if row["action"] != "COPY":
                continue
            src = Path(str(row["source"]))
            dst = Path(str(row["target"]))
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            actual = sha256(dst)
            if actual != row["sha256"]:
                raise RuntimeError(f"copy hash mismatch: {dst}")
            target_hashes.add(actual)
            row["action"] = "COPIED_VERIFIED"

    payload = {
        "schema_version": "1.0",
        "mode": "APPLY" if args.apply else "PLAN",
        "verified_current_registry": str(REGISTRY.relative_to(ROOT)),
        "verified_current_registry_total": len(verified),
        "safe_unique_designations_total": len(safe),
        "blocked_designations_total": len(blocked),
        "copy_actions_total": sum(1 for row in actions if row["action"] == "COPY"),
        "already_present_exact_total": sum(1 for row in actions if row["action"] == "ALREADY_PRESENT_EXACT"),
        "copied_verified_total": sum(1 for row in actions if row["action"] == "COPIED_VERIFIED"),
        "target": str(target_root),
        "blocked": blocked,
        "actions": actions,
        "source_files_deleted": 0,
        "status": "APPLIED_COPY_ONLY_NO_DELETE" if args.apply else ("PLAN_READY" if not blocked else "PLAN_REVIEW_REQUIRED"),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k not in {"blocked", "actions"}}, ensure_ascii=False, indent=2))
    if blocked:
        print("BLOCKED DESIGNATIONS:")
        for row in blocked:
            print(f"  {row['designation']}: {row['reason']} distinct_sha256={row['distinct_sha256_total']}")
    print(f"Report: {OUTPUT}")
    return 0 if not (args.apply and blocked) else 4


if __name__ == "__main__":
    raise SystemExit(main())
