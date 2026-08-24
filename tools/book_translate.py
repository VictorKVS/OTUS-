from __future__ import annotations

import argparse
import hashlib
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def http_json(url: str, *, timeout: int, headers: dict[str, str] | None = None) -> dict:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def discover_endpoint_and_model(
    *,
    explicit_base_url: str,
    explicit_model: str,
    api_key: str,
    timeout: int = 4,
) -> tuple[str, str]:
    candidates: list[str] = []
    if explicit_base_url.strip():
        candidates.append(explicit_base_url.strip().rstrip("/"))
    candidates.extend(
        [
            "http://127.0.0.1:8080/v1",
            "http://127.0.0.1:1234/v1",
            "http://127.0.0.1:11434/v1",
        ]
    )

    seen: set[str] = set()
    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for base_url in candidates:
        if base_url in seen:
            continue
        seen.add(base_url)
        try:
            payload = http_json(base_url + "/models", timeout=timeout, headers=headers)
        except Exception:
            continue

        available = []
        for item in payload.get("data") or []:
            model_id = str(item.get("id") or "").strip()
            if model_id:
                available.append(model_id)

        if explicit_model.strip():
            model = explicit_model.strip()
            if not available or model in available:
                return base_url, model
            # Some servers accept aliases not advertised by /models.
            return base_url, model

        if available:
            return base_url, available[0]

    if explicit_base_url.strip() and explicit_model.strip():
        return explicit_base_url.strip().rstrip("/"), explicit_model.strip()

    raise RuntimeError(
        "No OpenAI-compatible local endpoint/model detected. "
        "Start a local server or set BOOK_LLM_BASE_URL and BOOK_LLM_MODEL."
    )


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
        "Сохраняй термины, имена технологий, аббревиатуры, формулы, списки, заголовки и структуру. "
        "Не удаляй примеры и оговорки. "
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


def qc_translation(source_text: str, translated_text: str) -> tuple[str, list[str]]:
    flags: list[str] = []
    source = source_text.strip()
    target = translated_text.strip()
    if not target:
        flags.append("EMPTY_TARGET")
    if source and target.casefold() == source.casefold():
        flags.append("UNCHANGED_FROM_SOURCE")
    if source:
        ratio = len(target) / max(1, len(source))
        if ratio < 0.35:
            flags.append("SUSPICIOUSLY_SHORT")
        if ratio > 2.60:
            flags.append("SUSPICIOUSLY_LONG")
    if "```" in source and source.count("```") != target.count("```"):
        flags.append("CODE_FENCE_COUNT_CHANGED")
    return ("PASS" if not flags else "NEEDS_REVIEW"), flags


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
    parser.add_argument("--base-url", default=os.getenv("BOOK_LLM_BASE_URL", ""))
    parser.add_argument("--model", default=os.getenv("BOOK_LLM_MODEL", ""))
    parser.add_argument("--api-key", default=os.getenv("BOOK_LLM_API_KEY", ""))
    parser.add_argument("--limit", type=int, default=0, help="0 = translate all remaining units")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--probe-only", action="store_true", help="Only detect endpoint/model and exit.")
    args = parser.parse_args()

    try:
        base_url, model = discover_endpoint_and_model(
            explicit_base_url=args.base_url,
            explicit_model=args.model,
            api_key=args.api_key,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"translation_base_url={base_url}")
    print(f"translation_model={model}")
    if args.probe_only:
        print("status=TRANSLATION_ENDPOINT_READY")
        return 0

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
    qc_review_count = 0

    for unit in remaining:
        source_text = str(unit.get("source_text") or "").strip()
        if not source_text:
            errors.append({"unit_id": unit.get("unit_id"), "error": "empty source_text"})
            continue

        try:
            translated = chat_completion(
                base_url=base_url,
                api_key=args.api_key,
                model=model,
                source_text=source_text,
                timeout=args.timeout,
            )
            qc_status, qc_flags = qc_translation(source_text, translated)
            unit["translated_text"] = translated
            unit["translated_text_sha256"] = sha256_text(translated)
            unit["translation_status"] = "DONE"
            unit["translation_method"] = "OPENAI_COMPATIBLE_CHAT_COMPLETIONS"
            unit["translation_model"] = model
            unit["translated_at"] = utc_now()
            unit["translation_review"] = "NOT_REVIEWED"
            unit["translation_qc"] = qc_status
            unit["translation_qc_flags"] = qc_flags
            if qc_status != "PASS":
                qc_review_count += 1
            processed += 1
            write_jsonl_atomic(units_path, units)
            print(
                f"translated {unit.get('order')} "
                f"page={unit.get('source_page_start')} "
                f"qc={qc_status} unit_id={unit.get('unit_id')}"
            )
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
    qc_review_total = sum(1 for unit in units if unit.get("translation_qc") == "NEEDS_REVIEW")
    total = len(units)
    complete = translated_total == total and total > 0

    manifest.update(
        {
            "status": "TRANSLATION_COMPLETE" if complete else "TRANSLATION_IN_PROGRESS",
            "updated_at": utc_now(),
            "translation_provider": "OPENAI_COMPATIBLE_CHAT_COMPLETIONS",
            "translation_base_url": base_url,
            "translation_model": model,
            "units": total,
            "translated_units": translated_total,
            "failed_units": failed_total,
            "qc_needs_review_units": qc_review_total,
            "last_run_processed": processed,
            "last_run_qc_needs_review": qc_review_count,
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
    print(f"qc_needs_review={qc_review_total}")
    return 0 if complete else 7


if __name__ == "__main__":
    raise SystemExit(main())
