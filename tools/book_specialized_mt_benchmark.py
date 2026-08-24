from __future__ import annotations

import argparse
import gc
import json
import statistics
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from book_translate import qc_translation
from book_translation_tournament import score_translation


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class MTSpec:
    alias: str
    model_id: str
    licence: str
    production_eligible: bool
    kind: str


SPECS = {
    "opus": MTSpec(
        alias="opus",
        model_id="Helsinki-NLP/opus-mt-en-ru",
        licence="Apache-2.0",
        production_eligible=True,
        kind="OPUS_EN_RU",
    ),
    "madlad3b": MTSpec(
        alias="madlad3b",
        model_id="google/madlad400-3b-mt",
        licence="Apache-2.0",
        production_eligible=True,
        kind="MADLAD_400",
    ),
    "nllb1.3b": MTSpec(
        alias="nllb1.3b",
        model_id="facebook/nllb-200-distilled-1.3B",
        licence="CC-BY-NC-4.0",
        production_eligible=False,
        kind="NLLB_200",
    ),
}


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


def sample_rows_from_tournament(tournament: dict) -> list[dict]:
    ranking = list(tournament.get("ranking") or [])
    if not ranking:
        return []
    samples = list(ranking[0].get("samples") or [])
    return [
        {
            "unit_id": row.get("unit_id"),
            "order": row.get("order"),
            "page": row.get("page"),
            "source_text": str(row.get("source_text") or ""),
        }
        for row in samples
        if str(row.get("source_text") or "").strip()
    ]


def load_runtime(spec: MTSpec, *, local_files_only: bool):
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    except Exception as exc:
        raise RuntimeError(
            "Install optional dependencies first: python -m pip install -r requirements-specialized-translation.txt"
        ) from exc

    tokenizer_kwargs = {"local_files_only": local_files_only}
    model_kwargs = {"local_files_only": local_files_only}

    if spec.kind == "NLLB_200":
        tokenizer_kwargs["src_lang"] = "eng_Latn"

    if torch.cuda.is_available():
        model_kwargs.update({"device_map": "auto", "torch_dtype": torch.float16})

    tokenizer = AutoTokenizer.from_pretrained(spec.model_id, **tokenizer_kwargs)
    model = AutoModelForSeq2SeqLM.from_pretrained(spec.model_id, **model_kwargs)

    if not torch.cuda.is_available():
        model = model.to("cpu")
    model.eval()
    return torch, tokenizer, model


def translate_one(spec: MTSpec, tokenizer, model, torch, text: str, max_new_tokens: int) -> str:
    source = text.strip()
    if spec.kind == "MADLAD_400":
        source = "<2ru> " + source

    encoded = tokenizer(
        source,
        return_tensors="pt",
        truncation=True,
        max_length=2048,
    )

    try:
        device = next(model.parameters()).device
        encoded = {key: value.to(device) for key, value in encoded.items()}
    except Exception:
        pass

    generate_kwargs = {
        "max_new_tokens": max_new_tokens,
        "num_beams": 4,
        "do_sample": False,
    }
    if spec.kind == "NLLB_200":
        forced_id = tokenizer.convert_tokens_to_ids("rus_Cyrl")
        generate_kwargs["forced_bos_token_id"] = forced_id

    with torch.inference_mode():
        output = model.generate(**encoded, **generate_kwargs)
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()


def cleanup_runtime(torch, model, tokenizer) -> None:
    del tokenizer
    del model
    gc.collect()
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark specialized EN→RU MT models on the exact samples from the existing translator tournament."
    )
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--private-root", default=r"G:\1\OTUS\_PRIVATE_BOOK_CORPUS")
    parser.add_argument(
        "--candidate",
        action="append",
        choices=sorted(SPECS),
        help="Repeat to benchmark multiple models. Default: opus only (small download).",
    )
    parser.add_argument("--include-noncommercial", action="store_true")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=2048)
    args = parser.parse_args()

    try:
        workspace = resolve_workspace(Path(args.private_root), args.workspace)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    tournament_path = workspace / "translation_tournament.json"
    tournament = json.loads(tournament_path.read_text(encoding="utf-8"))
    samples = sample_rows_from_tournament(tournament)
    if not samples:
        print("ERROR: tournament samples unavailable", file=sys.stderr)
        return 3

    aliases = args.candidate or ["opus"]
    specs: list[MTSpec] = []
    for alias in aliases:
        spec = SPECS[alias]
        if not spec.production_eligible and not args.include_noncommercial:
            print(
                f"SKIP {spec.model_id}: licence={spec.licence}; pass --include-noncommercial for research benchmark",
                file=sys.stderr,
            )
            continue
        specs.append(spec)

    if not specs:
        print("ERROR: no eligible specialized MT candidates selected", file=sys.stderr)
        return 4

    specialized_results: list[dict] = []
    for spec in specs:
        print(f"\n=== SPECIALIZED MT {spec.model_id} licence={spec.licence} ===")
        try:
            torch, tokenizer, model = load_runtime(spec, local_files_only=args.local_files_only)
        except Exception as exc:
            specialized_results.append(
                {
                    "model": spec.model_id,
                    "alias": spec.alias,
                    "licence": spec.licence,
                    "production_eligible": spec.production_eligible,
                    "status": "LOAD_FAILED",
                    "error": f"{type(exc).__name__}: {exc}",
                    "samples": [],
                    "pass_count": 0,
                    "sample_count": len(samples),
                    "mean_score": 0.0,
                    "min_score": 0.0,
                }
            )
            print(f"LOAD_FAILED {exc}", file=sys.stderr)
            continue

        rows: list[dict] = []
        try:
            for sample in samples:
                source = sample["source_text"]
                try:
                    translated = translate_one(
                        spec,
                        tokenizer,
                        model,
                        torch,
                        source,
                        args.max_new_tokens,
                    )
                    qc_status, flags = qc_translation(source, translated)
                    score = score_translation(source, translated, qc_status, flags)
                    row = {
                        **sample,
                        "translated_text": translated,
                        "qc": qc_status,
                        "flags": flags,
                        "score": score,
                    }
                    print(
                        f"order={row['order']} page={row['page']} qc={qc_status} "
                        f"score={score} flags={flags}"
                    )
                except Exception as exc:
                    row = {
                        **sample,
                        "translated_text": "",
                        "qc": "FAILED",
                        "flags": [f"{type(exc).__name__}:{exc}"],
                        "score": 0.0,
                    }
                    print(f"order={row['order']} FAILED {exc}", file=sys.stderr)
                rows.append(row)
        finally:
            cleanup_runtime(torch, model, tokenizer)

        scores = [float(row["score"]) for row in rows]
        pass_count = sum(1 for row in rows if row["qc"] == "PASS")
        specialized_results.append(
            {
                "model": spec.model_id,
                "alias": spec.alias,
                "licence": spec.licence,
                "production_eligible": spec.production_eligible,
                "status": "BENCHMARKED",
                "samples": rows,
                "pass_count": pass_count,
                "sample_count": len(rows),
                "mean_score": round(statistics.mean(scores), 2) if scores else 0.0,
                "min_score": round(min(scores), 2) if scores else 0.0,
            }
        )

    llm_rows = [
        {
            "model": row.get("model"),
            "family": "GENERAL_LLM",
            "licence": "LOCAL_MODEL_REVIEW_REQUIRED",
            "production_eligible": None,
            "pass_count": row.get("pass_count"),
            "sample_count": row.get("sample_count"),
            "mean_score": row.get("mean_score"),
            "min_score": row.get("min_score"),
        }
        for row in tournament.get("ranking") or []
    ]
    mt_rows = [
        {
            "model": row["model"],
            "family": "SPECIALIZED_MT",
            "licence": row["licence"],
            "production_eligible": row["production_eligible"],
            "pass_count": row["pass_count"],
            "sample_count": row["sample_count"],
            "mean_score": row["mean_score"],
            "min_score": row["min_score"],
        }
        for row in specialized_results
    ]
    combined = llm_rows + mt_rows
    combined.sort(
        key=lambda row: (
            int(row.get("pass_count") or 0),
            float(row.get("mean_score") or 0.0),
            float(row.get("min_score") or 0.0),
        ),
        reverse=True,
    )

    report = {
        "schema_version": "father-book-specialized-mt-benchmark.v0.1",
        "generated_at": utc_now(),
        "workspace": str(workspace),
        "specialized_results": specialized_results,
        "combined_ranking": combined,
        "note": "Deterministic scores are rejection/ranking aids, not proof of semantic translation quality; near-ties require blind jury or human review.",
    }
    report_path = workspace / "specialized_mt_benchmark.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Specialized MT vs general LLM benchmark",
        "",
        "| Rank | Family | Model | PASS | Mean | Min | Licence | Production |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for index, row in enumerate(combined, start=1):
        md.append(
            f"| {index} | {row['family']} | `{row['model']}` | "
            f"{row.get('pass_count')}/{row.get('sample_count')} | {row.get('mean_score')} | "
            f"{row.get('min_score')} | {row.get('licence')} | {row.get('production_eligible')} |"
        )
    md.extend([
        "",
        "Deterministic metrics only reject obvious failures and rank candidates; semantic winner selection belongs to blind jury/human review.",
        "",
    ])
    (workspace / "specialized_mt_benchmark_report.md").write_text("\n".join(md), encoding="utf-8")

    print("\n=== COMBINED LEADERBOARD ===")
    for index, row in enumerate(combined, start=1):
        print(
            f"{index}. {row['family']} {row['model']} pass={row.get('pass_count')}/{row.get('sample_count')} "
            f"mean={row.get('mean_score')} min={row.get('min_score')}"
        )
    print(f"report={workspace / 'specialized_mt_benchmark_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
