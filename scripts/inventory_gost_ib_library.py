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
STANDARD_HINTS = ("гост", "gost", "iso", "iec", "исо", "мэк", "стандарт")


def norm(s: str) -> str:
    s = s.casefold().replace("ё", "е").replace("–", "-").replace("—", "-")
    return re.sub(r"[^0-9a-zа-я.-]+", "", s)


def loose_norm(s: str) -> str:
    """Normalization for filenames where spaces/underscores/dashes differ."""
    s = s.casefold().replace("ё", "е")
    return re.sub(r"[^0-9a-zа-я]+", "", s)


def code_key(designation: str) -> str:
    m = re.search(r"(\d+(?:\.\d+)*(?:-\d+)*-\d{2,4})", designation)
    return m.group(1) if m else norm(designation)


def code_digits(value: str) -> str:
    """Compact numeric signature: 59453.1-2021 -> 5945312021."""
    return "".join(re.findall(r"\d", value))


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


def match_seed(path: Path, seed: list[str]) -> tuple[str | None, str, str]:
    """Match by designation, not by exact local filename.

    Returns (designation, basis, confidence). Strong matches tolerate different
    separators/prefixes. Numeric fallback is deliberately bounded so a random
    short number is not promoted to a TK362 match.
    """
    stem = path.stem
    n = norm(stem)
    loose = loose_norm(stem)
    stem_digits = code_digits(stem)
    has_standard_hint = any(token in stem.casefold() for token in STANDARD_HINTS)

    hits: list[tuple[int, str, str, str]] = []
    for designation in seed:
        full = norm(designation)
        key = norm(code_key(designation))
        key_loose = loose_norm(code_key(designation))
        digits = code_digits(code_key(designation))

        if full and full in n:
            hits.append((400 + len(full), designation, "FULL_DESIGNATION", "HIGH"))
            continue
        if key and key in n:
            hits.append((350 + len(key), designation, "CODE_EXACT", "HIGH"))
            continue
        if key_loose and key_loose in loose:
            hits.append((300 + len(key_loose), designation, "CODE_SEPARATOR_NORMALIZED", "HIGH"))
            continue

        # Handles names such as "56939_2024.pdf" or "ГОСТ 56939 2024.pdf".
        # Require a reasonably distinctive signature and either a standard hint
        # or a filename dominated by the code digits.
        if len(digits) >= 7 and digits in stem_digits:
            dominated = len(stem_digits) <= len(digits) + 2
            if has_standard_hint or dominated:
                hits.append((200 + len(digits), designation, "CODE_DIGITS_NORMALIZED", "MEDIUM"))

    if not hits:
        return None, "NO_TK362_MATCH", "NONE"
    _, designation, basis, confidence = max(hits, key=lambda item: item[0])
    return designation, basis, confidence


def looks_like_standard(path: Path, seed_match: str | None) -> bool:
    if seed_match:
        return True
    n = path.stem.casefold()
    return any(t in n for t in STANDARD_HINTS)


def find_files(root: Path, seed: list[str]) -> list[dict]:
    out = []
    if not root.exists():
        return out
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in ALLOWED_EXT:
            continue
        matched, match_basis, match_confidence = match_seed(path, seed)
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
                "match_basis": match_basis,
                "match_confidence": match_confidence,
                "tag": "ИБ" if matched else "REVIEW",
                "library_role": "ARCHITECT",
                "current_status": (
                    "NEEDS_CURRENT_STATUS_VERIFICATION" if matched else "NOT_IN_TK362_SEED_OR_FILENAME_AMBIGUOUS"
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
            "match_basis",
            "match_confidence",
            "tag",
            "library_role",
            "current_status",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    payload = {
        "schema_version": "1.1",
        "mode": "APPLY" if args.apply else "PLAN",
        "source": str(source),
        "target": str(target),
        "seed_total": len(seed),
        "source_candidates_total": len(source_rows),
        "source_tk362_matches_total": sum(1 for row in source_rows if row["tk362_seed_match"]),
        "source_high_confidence_matches_total": sum(1 for row in source_rows if row["match_confidence"] == "HIGH"),
        "source_medium_confidence_matches_total": sum(1 for row in source_rows if row["match_confidence"] == "MEDIUM"),
        "target_candidates_total": len(target_rows),
        "copy_actions_total": sum(1 for action in actions if action["action"].startswith("COPY")),
        "already_present_exact_total": sum(1 for action in actions if action["action"] == "ALREADY_PRESENT_EXACT"),
        "review_non_tk362_total": sum(1 for row in source_rows if not row["tk362_seed_match"]),
        "actions": actions,
        "status": "APPLIED_COPY_ONLY_NO_DELETE" if args.apply else "PLAN_READY_NO_FILE_CHANGES",
        "next_gate": "VERIFY_CURRENT_STATUS_AGAINST_ROSSTANDART",
        "note": "Filename titles need not be identical. Matching prioritizes normalized designation/code; ambiguous GOST-like files stay in REVIEW and are not discarded.",
    }
    json_path = REPORT_ROOT / "LATEST_GOST_IB_INVENTORY.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({k: v for k, v in payload.items() if k != "actions"}, ensure_ascii=False, indent=2))
    print(f"Report: {json_path}")
    print(f"CSV:    {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
