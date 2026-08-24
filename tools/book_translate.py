from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl_atomic(path: Path, rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    source_text: str,
    timeout: int,
) -> str:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    system = (
        "Ты профессиональный технический переводчик литературы по программной и системной архитектуре. "
        "Переводи с английского на русский точно по смыслу. "
        "Не сокращай, не пересказывай и не добавляй объяснений. "
        "Сохраняй термины, имена технологий, аббревиатуры, формулы, списки и структуру. "
        "Если термин принято оставлять на английском, сохрани английский термин и при первом уместном случае дай русский эквивалент. "
        "Верни только перевод переданного фрагмента."
    )
    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": source_text},
        ],
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError("translation endpoint returned no choices")
    content = ((choices[0].get("message") or {}).get("content") or "").strip()
    if not content:
        raise RuntimeError("translation endpoint returned empty content")
    return content


def resolve_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    manifests = sorted(
        private_root.glob("*/translation_manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not manifests:
        raise FileNotFoundError("translation_manifest.json not found; run book_prepare_translation.py first")
    return manifests[0].parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate prepared private book units with checkpointing.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument("--base-url", default=os.getenv("BOOK_LLM_BASE_URL", "http://127.0.0.1:8080/v1"))
    parser.add_argument("--model", default=os.getenv("BOOK_LLM_MODEL", ""))
    parser.add_argument("--api-key", default=os.getenv("BOOK_LLM_API_KEY", ""))
    parser.add_argument("--limit", type=int, default=0, help="0 = translate all remaining units")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    if not args.model.strip():
        print("ERROR: set BOOK_LLM_MODEL or pass --model", file=sys.stderr)
        return 2

    try:
        workspace = resolve_workspace(Path(args.private_root), args.workspace)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    manifest_path = workspace / "translation_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    units_path = Path(manifest["units_path"])
    units = load_jsonl(units_path)

    remaining = [unit for unit in units if unit.get("translation_status") != "DONE"]
    if args.limit > 0:
        remaining = remaining[: args.limit]

    if not remaining:
        print("status=TRANSLATION_ALREADY_COMPLETE")
        return 0

    processed = 0
    errors: list[dict] = []

    for unit in remaining:
        source_text = str(unit.get("source_text") or "").strip()
        if not source_text:
            errors.append({"unit_id": unit.get("unit_id"), "error": "empty source_text"})
            continue

        try:
            translated = chat_completion(
                base_url=args.base_url,
                api_key=args.api_key,
                model=args.model,
                source_text=source_text,
                timeout=args.timeout,
            )
            unit["translated_text"] = translated
            unit["translation_status"] = "DONE"
            unit["translation_method"] = "OPENAI_COMPATIBLE_CHAT_COMPLETIONS"
            unit["translation_model"] = args.model
            unit["translated_at"] = utc_now()
            unit["translation_review"] = "NOT_REVIEWED"
            processed += 1
            write_jsonl_atomic(units_path, units)
            print(f"translated {unit.get('order')} unit_id={unit.get('unit_id')}")
        except (urllib.error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
            unit["translation_status"] = "FAILED"
            unit["translation_error"] = f"{type(exc).__name__}: {exc}"
            errors.append({"unit_id": unit.get("unit_id"), "error": unit["translation_error"]})
            write_jsonl_atomic(units_path, units)
            print(f"FAILED unit_id={unit.get('unit_id')}: {exc}", file=sys.stderr)
            break

        if args.sleep > 0:
            time.sleep(args.sleep)

    translated_total = sum(1 for unit in units if unit.get("translation_status") == "DONE")
    failed_total = sum(1 for unit in units if unit.get("translation_status") == "FAILED")
    total = len(units)
    complete = translated_total == total and total > 0

    manifest.update(
        {
            "status": "TRANSLATION_COMPLETE" if complete else "TRANSLATION_IN_PROGRESS",
            "updated_at": utc_now(),
            "translation_provider": "OPENAI_COMPATIBLE_CHAT_COMPLETIONS",
            "translation_base_url": args.base_url,
            "translation_model": args.model,
            "units": total,
            "translated_units": translated_total,
            "failed_units": failed_total,
            "last_run_processed": processed,
            "last_run_errors": errors,
            "next_stage": "SEMANTIC_STRUCTURE" if complete else "TRANSLATE_UNITS",
        }
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"status={manifest['status']}")
    print(f"translated={translated_total}/{total}")
    print(f"failed={failed_total}")
    return 0 if complete else 7


if __name__ == "__main__":
    raise SystemExit(main())
