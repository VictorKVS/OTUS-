from __future__ import annotations

import argparse
import difflib
import json
import os
import statistics
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from book_translate import alphabet_profile, chat_completion, load_jsonl, qc_translation
from translation_model_policy import rank_model, reject_reason


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Candidate:
    base_url: str
    model: str

    @property
    def key(self) -> str:
        return f"{self.base_url}::{self.model}"


def get_json(url: str, timeout: int = 4) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def discover_candidates(max_models: int) -> list[Candidate]:
    endpoints = []
    explicit = os.getenv("BOOK_LLM_BASE_URL", "").strip()
    if explicit:
        endpoints.append(explicit.rstrip("/"))
    endpoints.extend([
        "http://127.0.0.1:8080/v1",
        "http://127.0.0.1:1234/v1",
        "http://127.0.0.1:11434/v1",
    ])

    discovered: list[Candidate] = []
    seen: set[tuple[str, str]] = set()
    for base_url in endpoints:
        try:
            payload = get_json(base_url + "/models")
        except Exception:
            continue
        for row in payload.get("data") or []:
            model = str(row.get("id") or "").strip()
            if not model or reject_reason(model):
                continue
            identity = (base_url, model)
            if identity in seen:
                continue
            seen.add(identity)
            discovered.append(Candidate(base_url=base_url, model=model))

    discovered.sort(key=lambda item: rank_model(item.model), reverse=True)
    return discovered[:max_models] if max_models > 0 else discovered


def resolve_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    manifests = sorted(
        private_root.glob("*/translation_manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not manifests:
        raise FileNotFoundError("translation_manifest.json not found")
    return manifests[0].parent


def technical_score(text: str) -> int:
    lowered = text.casefold()
    keywords = (
        "architecture", "architectural", "trade-off", "tradeoff", "coupling",
        "cohesion", "distributed", "service", "database", "data", "granularity",
        "transaction", "workflow", "domain", "modular", "communication",
    )
    return sum(1 for keyword in keywords if keyword in lowered)


def choose_samples(units: list[dict], count: int) -> list[dict]:
    eligible = [
        unit for unit in units
        if 350 <= len(str(unit.get("source_text") or "")) <= 3200
    ]
    if not eligible:
        eligible = [unit for unit in units if str(unit.get("source_text") or "").strip()]
    if not eligible:
        return []

    ranked = sorted(
        eligible,
        key=lambda unit: (
            technical_score(str(unit.get("source_text") or "")),
            len(str(unit.get("source_text") or "")),
        ),
        reverse=True,
    )

    chosen: list[dict] = []
    used_orders: set[int] = set()
    # Prefer technical passages, but spread them across the book.
    buckets = max(1, count)
    total_orders = max(int(unit.get("order") or 0) for unit in units)
    for bucket in range(buckets):
        low = int(total_orders * bucket / buckets)
        high = int(total_orders * (bucket + 1) / buckets) + 1
        local = [u for u in ranked if low <= int(u.get("order") or 0) < high]
        if local:
            pick = local[0]
            order = int(pick.get("order") or 0)
            if order not in used_orders:
                chosen.append(pick)
                used_orders.add(order)
    for unit in ranked:
        if len(chosen) >= count:
            break
        order = int(unit.get("order") or 0)
        if order not in used_orders:
            chosen.append(unit)
            used_orders.add(order)
    return sorted(chosen[:count], key=lambda unit: int(unit.get("order") or 0))


def score_translation(source: str, target: str, qc_status: str, flags: list[str]) -> float:
    source = source.strip()
    target = target.strip()
    source_cyr, source_lat, source_letters = alphabet_profile(source)
    target_cyr, target_lat, target_letters = alphabet_profile(target)
    target_cyr_share = target_cyr / max(1, target_letters)
    similarity = difflib.SequenceMatcher(None, source.casefold(), target.casefold()).ratio()
    length_ratio = len(target) / max(1, len(source))

    score = 100.0
    if qc_status != "PASS":
        score -= 40.0
    score -= min(35.0, len(flags) * 12.0)
    score += min(15.0, target_cyr_share * 15.0)
    score -= min(30.0, similarity * 35.0)
    if length_ratio < 0.45 or length_ratio > 2.2:
        score -= 15.0
    elif 0.65 <= length_ratio <= 1.65:
        score += 5.0
    return round(max(0.0, min(120.0, score)), 2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare multiple local translation models on identical book samples.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--max-models", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--auto-select-margin", type=float, default=5.0)
    args = parser.parse_args()

    try:
        workspace = resolve_workspace(Path(args.private_root), args.workspace)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    manifest = json.loads((workspace / "translation_manifest.json").read_text(encoding="utf-8"))
    units = load_jsonl(Path(manifest["units_path"]))
    samples = choose_samples(units, max(3, args.samples))
    if not samples:
        print("ERROR: no benchmark samples found", file=sys.stderr)
        return 3

    candidates = discover_candidates(args.max_models)
    if len(candidates) < 2:
        print("ERROR: translator tournament needs at least 2 suitable text models exposed via OpenAI-compatible endpoints.", file=sys.stderr)
        if candidates:
            print(f"found_only={candidates[0].base_url}::{candidates[0].model}")
        return 4

    results: list[dict] = []
    for candidate in candidates:
        model_rows: list[dict] = []
        print(f"\n=== {candidate.model} @ {candidate.base_url} ===")
        for sample in samples:
            source = str(sample.get("source_text") or "").strip()
            try:
                translated = chat_completion(
                    base_url=candidate.base_url,
                    api_key="",
                    model=candidate.model,
                    source_text=source,
                    timeout=args.timeout,
                )
                qc_status, flags = qc_translation(source, translated)
                score = score_translation(source, translated, qc_status, flags)
                row = {
                    "unit_id": sample.get("unit_id"),
                    "order": sample.get("order"),
                    "page": sample.get("source_page_start"),
                    "source_text": source,
                    "translated_text": translated,
                    "qc": qc_status,
                    "flags": flags,
                    "score": score,
                }
                print(f"order={row['order']} page={row['page']} qc={qc_status} score={score} flags={flags}")
            except Exception as exc:
                row = {
                    "unit_id": sample.get("unit_id"),
                    "order": sample.get("order"),
                    "page": sample.get("source_page_start"),
                    "source_text": source,
                    "translated_text": "",
                    "qc": "FAILED",
                    "flags": [f"{type(exc).__name__}:{exc}"],
                    "score": 0.0,
                }
                print(f"order={row['order']} FAILED {exc}")
            model_rows.append(row)

        scores = [float(row["score"]) for row in model_rows]
        pass_count = sum(1 for row in model_rows if row["qc"] == "PASS")
        results.append({
            "base_url": candidate.base_url,
            "model": candidate.model,
            "samples": model_rows,
            "mean_score": round(statistics.mean(scores), 2) if scores else 0.0,
            "min_score": round(min(scores), 2) if scores else 0.0,
            "pass_count": pass_count,
            "sample_count": len(model_rows),
        })

    results.sort(key=lambda row: (row["pass_count"], row["mean_score"], row["min_score"]), reverse=True)
    winner = results[0]
    runner_up = results[1]
    all_pass = winner["pass_count"] == winner["sample_count"]
    margin = float(winner["mean_score"]) - float(runner_up["mean_score"])
    auto_selected = all_pass and margin >= args.auto_select_margin

    report = {
        "schema_version": "father-book-translator-tournament.v0.1",
        "generated_at": utc_now(),
        "workspace": str(workspace),
        "sample_orders": [sample.get("order") for sample in samples],
        "ranking": results,
        "recommended": {
            "model": winner["model"],
            "base_url": winner["base_url"],
            "mean_score": winner["mean_score"],
            "margin_over_second": round(margin, 2),
            "status": "AUTO_SELECTED" if auto_selected else "HUMAN_REVIEW_REQUIRED",
        },
    }
    report_path = workspace / "translation_tournament.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Translation tournament",
        "",
        "| Rank | Model | Endpoint | PASS | Mean | Min |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for idx, row in enumerate(results, start=1):
        md.append(
            f"| {idx} | `{row['model']}` | `{row['base_url']}` | "
            f"{row['pass_count']}/{row['sample_count']} | {row['mean_score']} | {row['min_score']} |"
        )
    md.extend(["", f"Recommended: **{winner['model']}**", "", f"Decision: **{report['recommended']['status']}**", ""])
    for sample_index, sample in enumerate(samples, start=1):
        md.extend([f"## Sample {sample_index} — order {sample.get('order')} / page {sample.get('source_page_start')}", "", "### Source", "", str(sample.get("source_text") or ""), ""])
        for row in results:
            translated = next(item["translated_text"] for item in row["samples"] if item["unit_id"] == sample.get("unit_id"))
            md.extend([f"### {row['model']}", "", translated, ""])
    (workspace / "translation_tournament_report.md").write_text("\n".join(md), encoding="utf-8")

    if auto_selected:
        selection = {
            "schema_version": "father-book-selected-translator.v0.1",
            "selected_at": utc_now(),
            "selection_method": "TRANSLATOR_TOURNAMENT_AUTO",
            "base_url": winner["base_url"],
            "model": winner["model"],
            "mean_score": winner["mean_score"],
            "report_path": str(report_path),
        }
        (workspace / "translation_selected_model.json").write_text(
            json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print("\n=== LEADERBOARD ===")
    for idx, row in enumerate(results, start=1):
        print(f"{idx}. {row['model']} pass={row['pass_count']}/{row['sample_count']} mean={row['mean_score']} min={row['min_score']}")
    print(f"recommended={winner['model']}")
    print(f"decision={report['recommended']['status']}")
    print(f"report={workspace / 'translation_tournament_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
