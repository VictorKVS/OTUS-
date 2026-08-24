from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from translation_model_policy import reject_reason


CRITERIA = ("adequacy", "terminology", "completeness", "fluency", "structure")
WEIGHTS = {
    "adequacy": 0.35,
    "terminology": 0.25,
    "completeness": 0.20,
    "fluency": 0.10,
    "structure": 0.10,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Judge:
    base_url: str
    model: str


def get_json(url: str, timeout: int = 4) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def judge_rank(model: str) -> tuple[int, str]:
    name = model.casefold()
    score = 0
    if "deepseek-r1" in name:
        score += 1000
    elif "deepseek" in name:
        score += 900
    if "qwen2.5" in name and "coder" not in name:
        score += 800
    elif "qwen" in name and "coder" not in name:
        score += 700
    if "mistral" in name:
        score += 650
    if "llama" in name:
        score += 500
    if "coder" in name:
        score -= 120
    if any(size in name for size in (":1b", ":1.5b", "-1b", "-1.5b")):
        score -= 200
    return score, name


def discover_judges(excluded_models: set[str], max_judges: int) -> list[Judge]:
    endpoints: list[str] = []
    explicit = os.getenv("BOOK_LLM_BASE_URL", "").strip()
    if explicit:
        endpoints.append(explicit.rstrip("/"))
    endpoints.extend([
        "http://127.0.0.1:8080/v1",
        "http://127.0.0.1:1234/v1",
        "http://127.0.0.1:11434/v1",
    ])

    found: list[Judge] = []
    seen: set[tuple[str, str]] = set()
    for base_url in endpoints:
        try:
            payload = get_json(base_url + "/models")
        except Exception:
            continue
        for row in payload.get("data") or []:
            model = str(row.get("id") or "").strip()
            if not model or model in excluded_models or reject_reason(model):
                continue
            key = (base_url, model)
            if key in seen:
                continue
            seen.add(key)
            found.append(Judge(base_url=base_url, model=model))

    found.sort(key=lambda item: judge_rank(item.model), reverse=True)
    return found[:max_judges]


def resolve_workspace(private_root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    reports = sorted(
        private_root.glob("*/translation_tournament.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not reports:
        raise FileNotFoundError("translation_tournament.json not found")
    return reports[0].parent


def generic_chat(*, base_url: str, model: str, system: str, user: str, timeout: int) -> str:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError("judge endpoint returned no choices")
    return str(((choices[0].get("message") or {}).get("content") or "")).strip()


def parse_json_object(text: str) -> dict:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("judge did not return a JSON object")
    return json.loads(cleaned[start : end + 1])


def weighted_score(values: dict) -> float:
    total = 0.0
    for criterion in CRITERIA:
        raw = float(values.get(criterion, 0.0))
        bounded = min(10.0, max(0.0, raw))
        total += bounded * WEIGHTS[criterion]
    return round(total * 10.0, 2)


def build_prompt(source: str, labeled_translations: dict[str, str]) -> str:
    parts = [
        "SOURCE EN:",
        source,
        "",
        "CANDIDATE TRANSLATIONS:",
    ]
    for label, text in labeled_translations.items():
        parts.extend([f"[{label}]", text, ""])
    parts.extend([
        "Evaluate every candidate on a 0..10 scale for: adequacy, terminology, completeness, fluency, structure.",
        "Adequacy and completeness are more important than stylistic elegance.",
        "Architectural terminology must preserve the technical meaning of the English source.",
        "Return ONLY JSON in this exact shape:",
        '{"scores":{"A":{"adequacy":0,"terminology":0,"completeness":0,"fluency":0,"structure":0}},"winner":"A","reason":"short reason"}',
        "Include one scores object for every supplied label.",
    ])
    return "\n".join(parts)


def rotate_labels(models: list[dict], shift: int) -> tuple[dict[str, dict], dict[str, str]]:
    ordered = models[shift:] + models[:shift]
    label_to_model: dict[str, dict] = {}
    model_to_label: dict[str, str] = {}
    for index, row in enumerate(ordered):
        label = chr(ord("A") + index)
        label_to_model[label] = row
        model_to_label[str(row["model"])] = label
    return label_to_model, model_to_label


def main() -> int:
    parser = argparse.ArgumentParser(description="Blind multi-model jury for translator tournament finalists.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument("--finalists", type=int, default=2)
    parser.add_argument("--judges", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--auto-select-margin", type=float, default=2.0)
    args = parser.parse_args()

    try:
        workspace = resolve_workspace(Path(args.private_root), args.workspace)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    tournament_path = workspace / "translation_tournament.json"
    tournament = json.loads(tournament_path.read_text(encoding="utf-8"))
    ranking = list(tournament.get("ranking") or [])
    finalist_count = max(2, min(args.finalists, len(ranking)))
    finalists = ranking[:finalist_count]
    if len(finalists) < 2:
        print("ERROR: at least 2 tournament finalists required", file=sys.stderr)
        return 3

    excluded = {str(row.get("model") or "") for row in finalists}
    judges = discover_judges(excluded, max(1, args.judges))
    if not judges:
        print("ERROR: no independent local judge model available", file=sys.stderr)
        return 4

    sample_ids = [row.get("unit_id") for row in finalists[0].get("samples") or []]
    sample_source: dict[object, str] = {
        row.get("unit_id"): str(row.get("source_text") or "")
        for row in finalists[0].get("samples") or []
    }
    translations: dict[tuple[str, object], str] = {}
    for finalist in finalists:
        for sample in finalist.get("samples") or []:
            translations[(str(finalist["model"]), sample.get("unit_id"))] = str(sample.get("translated_text") or "")

    system = (
        "Ты независимый редактор и эксперт по техническому переводу литературы по software/system architecture. "
        "Сравнивай варианты вслепую: не пытайся угадывать модель. "
        "Оценивай точность передачи смысла, корректность архитектурной терминологии, полноту, естественность русского и сохранение структуры. "
        "Не предпочитай буквальный перевод, если он хуже передает технический смысл. "
        "Не выдавай рассуждения по шагам; верни только требуемый JSON и короткую причину."
    )

    evaluations: list[dict] = []
    model_scores: dict[str, list[float]] = {str(row["model"]): [] for row in finalists}
    judge_failures = 0

    for judge_index, judge in enumerate(judges):
        print(f"\n=== JUDGE {judge.model} @ {judge.base_url} ===")
        for sample_index, unit_id in enumerate(sample_ids):
            label_map, _ = rotate_labels(finalists, (judge_index + sample_index) % len(finalists))
            labeled = {
                label: translations[(str(row["model"]), unit_id)]
                for label, row in label_map.items()
            }
            prompt = build_prompt(sample_source[unit_id], labeled)
            try:
                raw = generic_chat(
                    base_url=judge.base_url,
                    model=judge.model,
                    system=system,
                    user=prompt,
                    timeout=args.timeout,
                )
                parsed = parse_json_object(raw)
                score_map = parsed.get("scores") or {}
                scored_models: dict[str, float] = {}
                for label, finalist in label_map.items():
                    if label not in score_map:
                        raise ValueError(f"judge omitted label {label}")
                    model = str(finalist["model"])
                    score = weighted_score(score_map[label])
                    model_scores[model].append(score)
                    scored_models[model] = score
                winner_label = str(parsed.get("winner") or "").strip().upper()
                winner_model = str(label_map[winner_label]["model"]) if winner_label in label_map else None
                evaluations.append({
                    "judge_model": judge.model,
                    "judge_base_url": judge.base_url,
                    "unit_id": unit_id,
                    "scores": scored_models,
                    "winner_model": winner_model,
                    "reason": str(parsed.get("reason") or "")[:400],
                })
                print(f"unit={unit_id} winner={winner_model} scores={scored_models}")
            except Exception as exc:
                judge_failures += 1
                evaluations.append({
                    "judge_model": judge.model,
                    "judge_base_url": judge.base_url,
                    "unit_id": unit_id,
                    "error": f"{type(exc).__name__}: {exc}",
                })
                print(f"unit={unit_id} FAILED {exc}", file=sys.stderr)

    jury_rows: list[dict] = []
    for finalist in finalists:
        model = str(finalist["model"])
        scores = model_scores[model]
        jury_mean = round(statistics.mean(scores), 2) if scores else 0.0
        deterministic = float(finalist.get("mean_score") or 0.0) / 120.0 * 100.0
        combined = round(jury_mean * 0.85 + deterministic * 0.15, 2)
        jury_rows.append({
            "model": model,
            "base_url": finalist["base_url"],
            "jury_mean": jury_mean,
            "deterministic_normalized": round(deterministic, 2),
            "combined_score": combined,
            "jury_scores": scores,
        })

    jury_rows.sort(key=lambda row: (row["combined_score"], row["jury_mean"]), reverse=True)
    winner = jury_rows[0]
    runner_up = jury_rows[1]
    margin = round(float(winner["combined_score"]) - float(runner_up["combined_score"]), 2)
    expected_evaluations = len(judges) * len(sample_ids)
    successful = expected_evaluations - judge_failures
    enough_judges = len(judges) >= 2 and successful >= max(2, int(expected_evaluations * 0.8))
    auto_selected = enough_judges and margin >= args.auto_select_margin

    report = {
        "schema_version": "father-book-translator-jury.v0.1",
        "generated_at": utc_now(),
        "workspace": str(workspace),
        "finalists": [row["model"] for row in finalists],
        "judges": [judge.model for judge in judges],
        "evaluations": evaluations,
        "ranking": jury_rows,
        "judge_failures": judge_failures,
        "successful_evaluations": successful,
        "recommended": {
            "model": winner["model"],
            "base_url": winner["base_url"],
            "margin_over_second": margin,
            "status": "AUTO_SELECTED" if auto_selected else "HUMAN_REVIEW_REQUIRED",
        },
    }
    report_path = workspace / "translation_jury.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Blind translator jury",
        "",
        "| Rank | Model | Jury mean | Deterministic | Combined |",
        "|---:|---|---:|---:|---:|",
    ]
    for index, row in enumerate(jury_rows, start=1):
        md.append(
            f"| {index} | `{row['model']}` | {row['jury_mean']} | "
            f"{row['deterministic_normalized']} | {row['combined_score']} |"
        )
    md.extend([
        "",
        f"Judges: {', '.join(judge.model for judge in judges)}",
        "",
        f"Recommended: **{winner['model']}**",
        "",
        f"Decision: **{report['recommended']['status']}**",
        "",
        f"Margin: **{margin}**",
        "",
    ])
    for evaluation in evaluations:
        md.append(
            f"- judge=`{evaluation.get('judge_model')}` unit=`{evaluation.get('unit_id')}` "
            f"winner=`{evaluation.get('winner_model')}` scores=`{evaluation.get('scores')}` "
            f"reason={evaluation.get('reason', evaluation.get('error', ''))}"
        )
    (workspace / "translation_jury_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    if auto_selected:
        selection = {
            "schema_version": "father-book-selected-translator.v0.1",
            "selected_at": utc_now(),
            "selection_method": "BLIND_MULTI_JUDGE_JURY",
            "base_url": winner["base_url"],
            "model": winner["model"],
            "jury_combined_score": winner["combined_score"],
            "margin_over_second": margin,
            "jury_report_path": str(report_path),
            "tournament_report_path": str(tournament_path),
        }
        (workspace / "translation_selected_model.json").write_text(
            json.dumps(selection, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print("\n=== JURY LEADERBOARD ===")
    for index, row in enumerate(jury_rows, start=1):
        print(
            f"{index}. {row['model']} jury={row['jury_mean']} "
            f"combined={row['combined_score']}"
        )
    print(f"recommended={winner['model']}")
    print(f"margin={margin}")
    print(f"decision={report['recommended']['status']}")
    print(f"report={workspace / 'translation_jury_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
