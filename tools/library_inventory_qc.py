from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def path_depth(value: str) -> int:
    return len(Path(value).parts)


def canonical_member(items: list[dict]) -> dict:
    """Pick a stable human-meaningful path for byte-identical copies.

    Architecture score is deliberately *not* used inside one SHA group because a
    misplaced duplicate can inherit unrelated keywords from the wrong folder and
    appear more relevant than the correctly filed copy.
    """
    eligible = [item for item in items if not str(item.get("file_name", "")).startswith("~$")]
    candidates = eligible or items
    return sorted(
        candidates,
        key=lambda item: (
            path_depth(str(item.get("relative_path", ""))),
            len(str(item.get("relative_path", ""))),
            str(item.get("relative_path", "")).casefold(),
        ),
    )[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="QC and canonicalize the generated local library inventory.")
    parser.add_argument(
        "inventory",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1] / "knowledge" / "library_inventory" / "generated" / "library_inventory.json"),
    )
    parser.add_argument("--prefer-sha", default="", help="Keep a known pilot SHA selected while canonicalizing its path.")
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    if not inventory_path.is_file():
        raise SystemExit(f"inventory not found: {inventory_path}")

    payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    items = list(payload.get("items") or [])

    groups: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        groups[str(item.get("sha256") or "")].append(item)

    canonical_items: list[dict] = []
    duplicate_groups: list[dict] = []
    for sha, members in groups.items():
        canonical = canonical_member(members)
        canonical_items.append(canonical)
        if len(members) > 1:
            duplicate_groups.append(
                {
                    "sha256": sha,
                    "copies": len(members),
                    "canonical_path": canonical.get("relative_path"),
                    "paths": [member.get("relative_path") for member in members],
                }
            )

    temporary_files = [item for item in items if str(item.get("file_name", "")).startswith("~$")]

    # Preserve the already selected book hash by default. QC is allowed to repair
    # the path of a byte-identical duplicate, but not silently switch the pilot to
    # another book after extraction has begun.
    original_pilot = payload.get("pilot_candidate") or {}
    preferred_sha = (args.prefer_sha.strip() or str(original_pilot.get("sha256") or "")).lower()
    pilot = None
    if preferred_sha:
        pilot = next((item for item in canonical_items if str(item.get("sha256", "")).lower() == preferred_sha), None)
    if pilot is None and canonical_items:
        pilot = sorted(
            canonical_items,
            key=lambda item: (
                int(item.get("architecture_score") or 0),
                int(item.get("page_count") or 0),
                str(item.get("normalized_title") or "").casefold(),
            ),
            reverse=True,
        )[0]

    manifest_rewritten = False
    manifest_path = None
    if pilot:
        source_root = Path(str(payload.get("source_root") or inventory_path.parents[3] / "Библиотека"))
        private_root = source_root.parent / "_PRIVATE_BOOK_CORPUS"
        manifest_path = private_root / str(pilot.get("item_id")) / "source_manifest.json"
        if manifest_path.is_file():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            before = str(manifest.get("source_path") or "")
            canonical_source_path = str(source_root / str(pilot.get("relative_path")))
            if before != canonical_source_path:
                manifest["source_path_before_canonicalization"] = before
                manifest["source_path"] = canonical_source_path
                manifest["item"] = pilot
                manifest["canonicalized_at"] = utc_now()
                manifest["canonicalization_rule"] = "same SHA-256; prefer shortest/shallower non-temporary path"
                manifest_path.write_text(
                    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                manifest_rewritten = True

    qc = {
        "schema_version": "father-library-inventory-qc.v0.2",
        "generated_at": utc_now(),
        "inventory_path": str(inventory_path),
        "counters": {
            "files_seen": len(items),
            "unique_sha256": len(groups),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_extra_copies": sum(max(0, len(members) - 1) for members in groups.values()),
            "temporary_files": len(temporary_files),
        },
        "canonical_pilot": pilot,
        "preserved_pilot_sha256": preferred_sha or None,
        "source_manifest_rewritten": manifest_rewritten,
        "source_manifest_path": str(manifest_path) if manifest_path else None,
        "duplicate_groups": duplicate_groups,
        "temporary_files": [item.get("relative_path") for item in temporary_files],
    }

    out = inventory_path.with_name("library_inventory_qc.json")
    out.write_text(json.dumps(qc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("status=QC_READY")
    print(f"files_seen={len(items)}")
    print(f"unique_sha256={len(groups)}")
    print(f"duplicate_groups={len(duplicate_groups)}")
    print(f"duplicate_extra_copies={qc['counters']['duplicate_extra_copies']}")
    print(f"temporary_files={len(temporary_files)}")
    if pilot:
        print(f"canonical_pilot={pilot.get('relative_path')}")
        print(f"canonical_pilot_sha256={pilot.get('sha256')}")
    print(f"source_manifest_rewritten={manifest_rewritten}")
    print(f"output={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
