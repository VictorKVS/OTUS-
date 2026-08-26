from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data" / "gost_ib_tk362_seed.txt"
REPORT_ROOT = ROOT / "reports" / "gost_ib_inventory"
DEFAULT_SOURCE = ROOT / "Библиотека" / "разобрать"
DEFAULT_TARGET = ROOT / "Библиотека" / "Архитектор" / "ИБ" / "ГОСТ"
ALLOWED_EXT = {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt"}
TEXTISH_EXT = {".docx", ".odt", ".rtf", ".txt"}

# Important: ISO/ИСО/GOST/ГОСТ must be lexical markers, not arbitrary substrings.
# This prevents false positives such as HarrISO n, AddISO n and микросервИСОв.
STANDARD_TOKEN_RE = re.compile(
    r"(?<![0-9a-zа-я])(?:гост|gost|iso|iec|исо|мэк)(?=$|[^0-9a-zа-я]|\d)",
    re.IGNORECASE,
)
STANDARD_WORD_RE = re.compile(r"(?<![0-9a-zа-я])стандарт[а-я]*", re.IGNORECASE)
# Generic standard-code candidate used only for REVIEW. It intentionally allows
# superseded years which may no longer be present in the current TK362 seed.
GENERIC_CODE_RE = re.compile(r"(?<!\d)(\d{4,5}(?:\.\d+)*(?:-\d+)*-\d{4})(?!\d)")


def norm(s: str) -> str:
    s = s.casefold().replace("ё", "е").replace("–", "-").replace("—", "-")
    return re.sub(r"[^0-9a-zа-я.-]+", "", s)


def loose_norm(s: str) -> str:
    """Normalization for filenames/text where spaces/underscores/dashes differ."""
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


def has_standard_hint(path: Path) -> bool:
    stem = path.stem.casefold().replace("ё", "е")
    return bool(STANDARD_TOKEN_RE.search(stem) or STANDARD_WORD_RE.search(stem))


def is_reference_list(path: Path) -> bool:
    compact = loose_norm(path.stem)
    return "переченьнациональныхстандарт" in compact


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
    has_hint = has_standard_hint(path)

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
        if len(digits) >= 7 and digits in stem_digits:
            dominated = len(stem_digits) <= len(digits) + 2
            if has_hint or dominated:
                hits.append((200 + len(digits), designation, "CODE_DIGITS_NORMALIZED", "MEDIUM"))

    if not hits:
        return None, "NO_TK362_MATCH", "NONE"
    _, designation, basis, confidence = max(hits, key=lambda item: item[0])
    return designation, basis, confidence


def _decode_rtf(raw: bytes) -> str:
    """Best-effort RTF text recovery for designation discovery only."""
    source = raw.decode("latin-1", errors="ignore")
    cp_match = re.search(r"\\ansicpg(\d+)", source, flags=re.IGNORECASE)
    encoding = f"cp{cp_match.group(1)}" if cp_match else "cp1251"
    try:
        "".encode(encoding)
    except LookupError:
        encoding = "cp1251"

    def hex_run(match: re.Match[str]) -> str:
        values = bytes(int(value, 16) for value in re.findall(r"\\'([0-9a-fA-F]{2})", match.group(0)))
        return values.decode(encoding, errors="replace")

    source = re.sub(r"(?:\\'[0-9a-fA-F]{2})+", hex_run, source)

    def unicode_char(match: re.Match[str]) -> str:
        value = int(match.group(1))
        if value < 0:
            value += 65536
        try:
            return chr(value)
        except ValueError:
            return " "

    source = re.sub(r"\\u(-?\d+)\??", unicode_char, source)
    source = source.replace(r"\{", "{").replace(r"\}", "}").replace(r"\\", "\\")
    source = re.sub(r"\\[A-Za-z]+-?\d* ?", " ", source)
    source = re.sub(r"[{}]", " ", source)
    return source


def read_text_prefix(path: Path, max_bytes: int = 1024 * 1024) -> str:
    """Best-effort local inspection for text-like formats only."""
    suffix = path.suffix.casefold()
    if suffix not in TEXTISH_EXT:
        return ""

    try:
        if suffix == ".docx":
            with zipfile.ZipFile(path) as zf:
                raw = zf.read("word/document.xml")[:max_bytes]
            return raw.decode("utf-8", errors="ignore")
        if suffix == ".odt":
            with zipfile.ZipFile(path) as zf:
                raw = zf.read("content.xml")[:max_bytes]
            return raw.decode("utf-8", errors="ignore")

        raw = path.read_bytes()[:max_bytes]
        if suffix == ".rtf":
            return _decode_rtf(raw)

        return "\n".join(
            raw.decode(enc, errors="ignore") for enc in ("utf-8", "cp1251", "latin-1")
        )
    except (OSError, KeyError, zipfile.BadZipFile):
        return ""


def generic_content_codes(text: str) -> list[str]:
    """Return distinct generic standard-like codes in encounter order."""
    seen: set[str] = set()
    result: list[str] = []
    for match in GENERIC_CODE_RE.finditer(text.replace("–", "-").replace("—", "-")):
        code = match.group(1)
        if code not in seen:
            seen.add(code)
            result.append(code)
    return result


def content_seed_candidate(path: Path, seed: list[str]) -> tuple[str | None, int, str]:
    """Surface a content designation candidate for manual identity review."""
    text = read_text_prefix(path)
    if not text:
        return None, 0, "NONE"

    generic_codes = generic_content_codes(text)
    if generic_codes:
        seed_by_code = {code_key(designation): designation for designation in seed}
        first = generic_codes[0]
        if first in seed_by_code:
            return seed_by_code[first], len(generic_codes), "CONTENT_SEED_CODE_REVIEW"
        return first, len(generic_codes), "CONTENT_GENERIC_CODE_REVIEW"

    compact = loose_norm(text)
    hits: list[tuple[int, str]] = []
    seen: set[str] = set()
    for designation in seed:
        key = loose_norm(code_key(designation))
        if not key:
            continue
        pos = compact.find(key)
        if pos >= 0:
            hits.append((pos, designation))
            seen.add(designation)
    if not hits:
        return None, 0, "NONE"
    hits.sort(key=lambda item: item[0])
    return hits[0][1], len(seen), "CONTENT_CODE_PREFIX_REVIEW"


def find_files(root: Path, seed: list[str]) -> list[dict]:
    out = []
    if not root.exists():
        return out

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in ALLOWED_EXT:
            continue

        matched, match_basis, match_confidence = match_seed(path, seed)
        reference_list = is_reference_list(path)
        hint = has_standard_hint(path)

        content_candidate = None
        content_candidate_count = 0
        content_basis = "NONE"
        if not matched and not reference_list and hint:
            content_candidate, content_candidate_count, content_basis = content_seed_candidate(path, seed)

        if matched:
            record_kind = "TK362_MATCH"
            tag = "ИБ"
            current_status = "NEEDS_CURRENT_STATUS_VERIFICATION"
        elif reference_list:
            record_kind = "REFERENCE_LIST"
            tag = "REFERENCE"
            current_status = "REFERENCE_NOT_A_STANDARD"
        elif hint:
            record_kind = "REVIEW_STANDARD_LIKE"
            tag = "REVIEW"
            current_status = "IDENTITY_REVIEW_REQUIRED"
        else:
            continue

        out.append(
            {
                "path": str(path),
                "name": path.name,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "record_kind": record_kind,
                "designation": matched or "",
                "tk362_seed_match": bool(matched),
                "match_basis": match_basis,
                "match_confidence": match_confidence,
                "content_designation_candidate": content_candidate or "",
                "content_candidate_distinct_codes": content_candidate_count,
                "content_match_basis": content_basis,
                "tag": tag,
                "library_role": "ARCHITECT",
                "current_status": current_status,
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
    target_hashes = {row["sha256"] for row in target_rows if row["record_kind"] == "TK362_MATCH"}

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
            "path", "name", "size_bytes", "sha256", "record_kind",
            "designation", "tk362_seed_match", "match_basis", "match_confidence",
            "content_designation_candidate", "content_candidate_distinct_codes", "content_match_basis",
            "tag", "library_role", "current_status",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    payload = {
        "schema_version": "1.4",
        "mode": "APPLY" if args.apply else "PLAN",
        "source": str(source),
        "target": str(target),
        "seed_total": len(seed),
        "source_candidates_total": len(source_rows),
        "source_standard_like_total": sum(1 for row in source_rows if row["record_kind"] != "REFERENCE_LIST"),
        "source_tk362_matches_total": sum(1 for row in source_rows if row["record_kind"] == "TK362_MATCH"),
        "source_high_confidence_matches_total": sum(1 for row in source_rows if row["match_confidence"] == "HIGH"),
        "source_medium_confidence_matches_total": sum(1 for row in source_rows if row["match_confidence"] == "MEDIUM"),
        "source_content_review_candidates_total": sum(1 for row in source_rows if row["content_designation_candidate"]),
        "source_reference_lists_total": sum(1 for row in source_rows if row["record_kind"] == "REFERENCE_LIST"),
        "source_identity_review_total": sum(1 for row in source_rows if row["record_kind"] == "REVIEW_STANDARD_LIKE"),
        "target_candidates_total": len(target_rows),
        "copy_actions_total": sum(1 for action in actions if action["action"].startswith("COPY")),
        "already_present_exact_total": sum(1 for action in actions if action["action"] == "ALREADY_PRESENT_EXACT"),
        "status": "APPLIED_COPY_ONLY_NO_DELETE" if args.apply else "PLAN_READY_NO_FILE_CHANGES",
        "next_gate": "VERIFY_IDENTITY_THEN_CURRENT_STATUS_AGAINST_ROSSTANDART",
        "note": (
            "Filename titles need not be identical. Matching prioritizes normalized designation/code. "
            "ISO/ИСО/GOST/ГОСТ are lexical markers, not arbitrary substrings. Reference lists are separated. "
            "Text-like content candidates are REVIEW-only and never auto-promoted or copied. "
            "Default intake source is Библиотека/разобрать."
        ),
        "actions": actions,
    }
    json_path = REPORT_ROOT / "LATEST_GOST_IB_INVENTORY.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({k: v for k, v in payload.items() if k != "actions"}, ensure_ascii=False, indent=2))
    print(f"Report: {json_path}")
    print(f"CSV:    {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
