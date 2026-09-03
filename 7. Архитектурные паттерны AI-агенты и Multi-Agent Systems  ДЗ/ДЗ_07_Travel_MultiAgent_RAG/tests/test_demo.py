import sys
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from travel_multiagent_demo import evaluate_retrieval, hybrid_retrieve_policy, run_demo


def test_typed_messages_and_agent_exchange():
    result = run_demo()
    messages = result["messages"]

    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert all(isinstance(message, (SystemMessage, HumanMessage, AIMessage)) for message in messages)

    names = [getattr(message, "name", None) for message in messages]
    assert "manager" in names
    assert "policy_rag" in names
    assert "flight_search" in names
    assert "hotel_search" in names
    assert "budget_analyst" in names
    assert names[-1] == "manager"


def test_result_is_grounded_and_budgeted():
    result = run_demo()
    answer = result["final_answer"]

    assert answer["estimated_total_rub"] > 0
    assert answer["status"] in {"APPROVE_DRAFT", "REQUIRES_APPROVAL"}
    assert answer["evidence_refs"]
    assert all(ref["source_id"] == "TRAVEL-POLICY-001" for ref in answer["evidence_refs"])
    assert all("dense_score" in ref and "lexical_score" in ref for ref in answer["evidence_refs"])
    assert answer["expanded_context_chunk_ids"]


def test_trace_shows_explicit_command_handoffs():
    result = run_demo()
    trace = "\n".join(result["trace"])

    assert "Manager -> PolicyRAG: explicit handoff via Command" in trace
    assert "PolicyRAG -> FlightSearch" in trace
    assert "FlightSearch -> HotelSearch: explicit handoff via Command" in trace
    assert "HotelSearch -> BudgetAnalyst: explicit handoff via Command" in trace
    assert "BudgetAnalyst -> Manager: result handoff via Command" in trace
    assert "Manager: synthesized grounded final recommendation" in trace


def test_hybrid_retrieval_has_dense_lexical_rerank_and_expansion():
    result = hybrid_retrieve_policy("лимит гостиницы Москва", top_k=2)

    assert result["candidate_count"] >= result["deduped_count"]
    assert result["primary_hits"]
    assert any(hit["chunk_id"] == "POLICY-HOTEL-CAPITALS-001" for hit in result["primary_hits"])
    assert all("dense_score" in hit for hit in result["primary_hits"])
    assert all("lexical_score" in hit for hit in result["primary_hits"])
    assert all("hybrid_score" in hit for hit in result["primary_hits"])
    expanded_ids = {item["chunk_id"] for item in result["expanded_chunks"]}
    assert "POLICY-HOTEL-CAPITALS-001" in expanded_ids
    assert "POLICY-HOTEL-BASE-001" in expanded_ids


def test_rag_eval_quality_gate():
    metrics = evaluate_retrieval(top_k=2)
    assert metrics["hit_rate_at_k"] >= 0.8
    assert metrics["mrr_at_k"] >= 0.7
