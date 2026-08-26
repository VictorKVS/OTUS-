from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data" / "gost_ib_tk362_seed.txt"
REPORT_ROOT = ROOT / "reports" / "gost_ib_inventory"
DEFAULT_SOURCE = Path.home() / "Downloads"
DEFAULT_TARGET = ROOT / "Библиотека" / "Архитектор" / "ИБ" / "ГОСТ"
ALLOWED_EXT = {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt"}


def norm(s: str) -> str:
    s = s.casefold().replace("ё", "е").replace("–", "-").replace("—", "-")
    return re.sub(r"[^0-9a-zа-я.-]+", "", s)


def code_key(designation: str) -> str:
    m = re.search(r"(\d+(?:\.\d+)*(?:-\d+)*-\d{2,4})", designation)
    return m.group(1) if m else norm(designation)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_seed() -> list[str]:
    return [
        x.strip()
        for x in SEED.read_text(encoding="utf-8").splitlines()
        if x.strip() and not x.startswith("#")
    ]


def match_seed(path: Path, seed: list[str]) -> str | None:
    n = norm(path.stem)
    hits = []
    for designation in seed:
        full = norm(designation)
        key = norm(code_key(designation))
        if full in n or (key and key in n):
            hits.append(designation)
    return max(hits, key=len) if hits else None


def looks_like_standard(path: Path, seed_match: str | None) -> bool:
    if seed_match:
        return True
    n = path.stem.casefold()
    return any(t in n for t in ("гост", "gost", "iso", "iec", "исо", "мэк", "стандарт"))


def find_files(root: Path, seed: list[str]) -> list[dict]:
    out = []
    if not root.exists():
        return out
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in ALLOWED_EXT:
            continue
        matched = match_seed(path, seed)
        if not looks_like_standard(path, matched):
            continue
        out.append(
            {
                "path": str(path),
                "name": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "designation": matched or "",
                "tk362_seed_match": bool(matched),
                "tag": "ИБ" if matched else "REVIEW",
                "library_role": "ARCHITECT",
                "current_status": (
                    "NEEDS_CURRENT_STATUS_VERIFICATION" if matched else "NOT_IN_TK362_SEED"
                ),
            }
        )
    return out


def choose_target(src: Path, target_dir: Path, digest: str) -> tuple[Path, str]:
    dst = target_dir / src.name
    if not dst.exists():
        return dst, "COPY"
    if sha256(dst) == digest:
        return dst, "ALREADY_PRESENT_EXACT"
    alt = target_dir / f"{src.stem}__{digest[:8]}{src.suffix}"
    if alt.exists() and sha256(alt) == digest:
        return alt, "ALREADY_PRESENT_EXACT"
    return alt, "COPY_COLLISION_RENAMED"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory local GOST/ISO files and stage TK362 information-security matches for Architect library."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--target", default=str(DEFAULT_TARGET))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = Path(args.source)
    target = Path(args.target)
    seed = load_seed()
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    source_rows = find_files(source, seed)
    target_rows = find_files(target, seed)
    target_hashes = {row["sha256"] for row in target_rows}

    actions = []
    pending_dir = target / "_CURRENTNESS_PENDING"
    for row in source_rows:
        if not row["tk362_seed_match"]:
            continue
        src = Path(row["path"])
        dst, action = choose_target(src, pending_dir, row["sha256"])
        if row["sha256"] in target_hashes:
            action = "ALREADY_PRESENT_EXACT"
        actions.append({**row, "planned_target": str(dst), "action": action})

    if args.apply:
        pending_dir.mkdir(parents=True, exist_ok=True)
        for row in actions:
            if not row["action"].startswith("COPY"):
                continue
            src = Path(row["path"])
            dst = Path(row["planned_target"])
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            if sha256(dst) != row["sha256"]:
                raise RuntimeError(f"copy hash mismatch: {dst}")

    all_rows = source_rows + target_rows
    csv_path = REPORT_ROOT / "gost_ib_inventory.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        fields = [
            "path",
            "name",
            "size_bytes",
            "sha256",
            "designation",
            "tk362_seed_match",
            "tag",
            "library_role",
            "current_status",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    payload = {
        "schema_version": "1.0",
        "mode": "APPLY" if args.apply else "PLAN",
        "source": str(source),
        "target": str(target),
        "seed_total": len(seed),
        "source_candidates_total": len(source_rows),
        "source_tk362_matches_total": sum(1 for row in source_rows if row["tk362_seed_match"]),
        "target_candidates_total": len(target_rows),
        "copy_actions_total": sum(1 for action in actions if action["action"].startswith("COPY")),
        "already_present_exact_total": sum(1 for action in actions if action["action"] == "ALREADY_PRESENT_EXACT"),
        "review_non_tk362_total": sum(1 for row in source_rows if not row["tk362_seed_match"]),
        "actions": actions,
        "status": "APPLIED_COPY_ONLY_NO_DELETE" if args.apply else "PLAN_READY_NO_FILE_CHANGES",
        "next_gate": "VERIFY_CURRENT_STATUS_AGAINST_ROSSTANDART",
    }
    json_path = REPORT_ROOT / "LATEST_GOST_IB_INVENTORY.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({k: v for k, v in payload.items() if k != "actions"}, ensure_ascii=False, indent=2))
    print(f"Report: {json_path}")
    print(f"CSV:    {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
