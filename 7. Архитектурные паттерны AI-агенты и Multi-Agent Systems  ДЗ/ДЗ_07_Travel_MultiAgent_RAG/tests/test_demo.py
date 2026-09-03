import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from travel_multiagent_demo import run_demo


def test_agents_exchange_messages():
    result = run_demo()
    senders = [m["from"] for m in result["messages"]]
    assert "Manager" in senders
    assert "PolicyRAG" in senders
    assert "FlightSearch" in senders
    assert "HotelSearch" in senders
    assert "BudgetAnalyst" in senders
    assert senders[-1] == "Manager"


def test_result_is_grounded_and_budgeted():
    result = run_demo()
    answer = result["final_answer"]
    assert answer["estimated_total_rub"] > 0
    assert answer["status"] in {"APPROVE_DRAFT", "REQUIRES_APPROVAL"}
    assert answer["evidence_refs"]
    assert all(ref["source_id"] == "TRAVEL-POLICY-001" for ref in answer["evidence_refs"])


def test_trace_shows_delegation():
    result = run_demo()
    trace = "\n".join(result["trace"])
    assert "Manager: decomposed request and delegated" in trace
    assert "PolicyRAG: retrieved and reranked" in trace
    assert "Manager: synthesized final recommendation" in trace
