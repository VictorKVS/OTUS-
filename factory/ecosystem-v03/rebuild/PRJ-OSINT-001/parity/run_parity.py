"""Behavioral parity harness: original OSINT_TRICOLOR vs FATHER rebuild.

No network access is performed. The original repository is imported read-only.
"""

import argparse
import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
CASE_ROOT = HERE.parents[1]
RUNTIME = CASE_ROOT / "runtime"
sys.path.insert(0, str(RUNTIME))

import father_osint_rebuild as rebuilt

SAMPLE = {
    "url": "https://example.org/demo?utm_source=test",
    "title": "Synthetic example",
    "category": "trademark",
    "observed_at": "2026-10-15T09:00:00+03:00",
    "source": "synthetic",
}

def load_reference(reference_root: Path):
    agent_file = reference_root / "agent.py"
    if not agent_file.exists():
        raise FileNotFoundError(f"Reference agent.py not found: {agent_file}")
    spec = importlib.util.spec_from_file_location("osint_tricolor_reference", agent_file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load reference module: {agent_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def outcome(callable_):
    try:
        return {"kind": "return", "value": callable_()}
    except Exception as exc:
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}

def semantic_db_snapshot(con):
    findings = con.execute(
        "SELECT id,fingerprint,url,category,title,description,observed_at,"
        "source,score,status FROM findings ORDER BY id"
    ).fetchall()
    audit = con.execute(
        "SELECT finding_id,action,details FROM audit_log ORDER BY id"
    ).fetchall()
    schema = {
        "findings": [
            list(row[1:6])
            for row in con.execute("PRAGMA table_info(findings)").fetchall()
        ],
        "audit_log": [
            list(row[1:6])
            for row in con.execute("PRAGMA table_info(audit_log)").fetchall()
        ],
    }
    return {"findings": findings, "audit": audit, "schema": schema}

def _missing_timezone(impl, db_path: Path):
    con = impl.connect(db_path)
    try:
        return impl.ingest(
            con,
            {**SAMPLE, "observed_at": "2026-10-15T09:00:00"},
        )
    finally:
        con.close()

def run_suite(impl, db_path: Path):
    results = {}
    results["GB-001"] = outcome(
        lambda: impl.normalize_url("https://EXAMPLE.org/demo/?utm_source=test")
    )

    con = impl.connect(db_path)
    try:
        first = impl.ingest(con, SAMPLE)
        second = impl.ingest(con, SAMPLE)
        snapshot = semantic_db_snapshot(con)
        report_text = impl.report(con)
    finally:
        con.close()

    results["GB-002"] = {
        "kind": "state",
        "first_action": first[1],
        "second_action": second[1],
        "finding_count": len(snapshot["findings"]),
    }
    results["GB-003"] = {
        "kind": "report",
        "contains_disclaimer": "Human review required" in report_text,
        "text": report_text,
    }
    results["GB-004"] = outcome(
        lambda: _missing_timezone(impl, db_path.with_name("timezone.db"))
    )
    results["DIAG-DB"] = snapshot
    results["DIAG-REPORT"] = report_text
    return results

def compare(reference, candidate):
    checks = []

    def add(check_id, description, ref_value, cand_value, gating=True):
        checks.append(
            {
                "id": check_id,
                "description": description,
                "gating": gating,
                "pass": ref_value == cand_value,
                "reference": ref_value,
                "rebuild": cand_value,
            }
        )

    add("GB-001", "URL normalization", reference["GB-001"], candidate["GB-001"])
    add("GB-002", "Dedup state transition", reference["GB-002"], candidate["GB-002"])
    add(
        "GB-003",
        "Human-review disclaimer and report text",
        reference["GB-003"],
        candidate["GB-003"],
    )
    add(
        "GB-004",
        "Timezone-less observed_at rejection",
        reference["GB-004"],
        candidate["GB-004"],
    )
    add(
        "DIAG-DB",
        "Semantic SQLite rows, audit payloads and schema",
        reference["DIAG-DB"],
        candidate["DIAG-DB"],
        gating=False,
    )
    add(
        "DIAG-REPORT",
        "Full report compatibility",
        reference["DIAG-REPORT"],
        candidate["DIAG-REPORT"],
        gating=False,
    )

    required = [x for x in checks if x["gating"]]
    return checks, all(x["pass"] for x in required)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference-root", required=True)
    parser.add_argument(
        "--output",
        default=str(CASE_ROOT / "evidence" / "generated" / "parity-report.json"),
    )
    args = parser.parse_args()

    reference_root = Path(args.reference_root).resolve()
    reference = load_reference(reference_root)

    with tempfile.TemporaryDirectory(prefix="father-osint-parity-") as tmp:
        tmp = Path(tmp)
        ref_results = run_suite(reference, tmp / "reference.db")
        rebuild_results = run_suite(rebuilt, tmp / "rebuild.db")

    checks, gate_pass = compare(ref_results, rebuild_results)
    report = {
        "schema_version": "father.rebuild.parity-report.v0.1",
        "rebuild_case_id": "RB-OSINT-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reference": {
            "repository": "VictorKVS/OSINT_TRICOLOR",
            "local_root": str(reference_root),
            "entrypoint": "agent.py",
        },
        "rebuild": {
            "implementation": "father_osint_rebuild",
            "runtime_root": str(RUNTIME),
        },
        "gate": {
            "id": "GATE-RB-OSINT-PARITY-001",
            "state": "PASS" if gate_pass else "FAIL",
            "rule": "All GB-* checks must match the reference behavior.",
        },
        "checks": checks,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for check in checks:
        mark = "PASS" if check["pass"] else "FAIL"
        kind = "GATE" if check["gating"] else "DIAG"
        print(f"{mark:4} {kind:4} {check['id']} · {check['description']}")

    print()
    print(f"PARITY GATE: {report['gate']['state']}")
    print(f"EVIDENCE: {output}")
    raise SystemExit(0 if gate_pass else 2)

if __name__ == "__main__":
    main()
