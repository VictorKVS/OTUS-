"""Deterministic LangGraph prototype for OTUS DZ07 M1.1.

Goals:
- typed LangChain messages via MessagesState;
- explicit agent handoffs via Command(goto=...);
- hybrid RAG retrieval (dense + lexical), dedup, reranking and chunk expansion;
- reproducible offline demo without API keys or network access.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command


ROOT = Path(__file__).resolve().parents[1]
RAG_EVAL_PATH = ROOT / "data" / "rag_eval.json"

POLICY_CHUNKS = [
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-FLIGHT-BASE-001",
        "section": "flights",
        "position": 0,
        "text": "Для поездок по России базовый класс перелёта — эконом.",
    },
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-FLIGHT-BUSINESS-001",
        "section": "flights",
        "position": 1,
        "text": "Бизнес-класс требует согласования руководителя и допускается для перелёта свыше 6 часов.",
    },
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-HOTEL-BASE-001",
        "section": "hotels",
        "position": 0,
        "text": "Базовый лимит гостиницы — 8 000 ₽ за ночь.",
    },
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-HOTEL-CAPITALS-001",
        "section": "hotels",
        "position": 1,
        "text": "Для Москвы и Санкт-Петербурга допускается гостиница до 12 000 ₽ за ночь.",
    },
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-DAILY-001",
        "section": "daily_allowance",
        "position": 0,
        "text": "Суточные для командировок по России — 1 500 ₽ в день.",
    },
]

BUSINESS_TERMS = {
    "перелёт",
    "билет",
    "эконом",
    "бизнес",
    "гостиница",
    "отель",
    "москва",
    "санкт",
    "суточные",
    "лимит",
    "согласование",
}


class TravelState(MessagesState):
    request: dict[str, Any]
    trace: list[str]
    policy_hits: list[dict[str, Any]]
    expanded_policy_chunks: list[dict[str, Any]]
    retrieval_metrics: dict[str, Any]
    flight_options: list[dict[str, Any]]
    hotel_options: list[dict[str, Any]]
    budget: dict[str, Any]
    final_answer: dict[str, Any]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())


def _hash_embedding(text: str, dims: int = 96) -> list[float]:
    """Small deterministic local embedding used only for the offline classroom demo."""
    vector = [0.0] * dims
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dims
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [x / norm for x in vector]


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _dense_score(query: str, text: str) -> float:
    return max(0.0, _cosine(_hash_embedding(query), _hash_embedding(text)))


def _lexical_score(query: str, text: str) -> float:
    q_tokens = set(_tokens(query))
    d_tokens = set(_tokens(text))
    if not q_tokens:
        return 0.0
    return len(q_tokens & d_tokens) / len(q_tokens)


def _business_term_bonus(query: str, text: str) -> float:
    q_tokens = set(_tokens(query)) & BUSINESS_TERMS
    if not q_tokens:
        return 0.0
    d_tokens = set(_tokens(text))
    return len(q_tokens & d_tokens) / len(q_tokens)


def _hybrid_candidates(query: str) -> list[dict[str, Any]]:
    candidates = []
    for chunk in POLICY_CHUNKS:
        dense = _dense_score(query, chunk["text"])
        lexical = _lexical_score(query, chunk["text"])
        business = _business_term_bonus(query, chunk["text"])
        # Offline approximation of dense+sparse hybrid retrieval followed by reranking.
        hybrid = 0.55 * dense + 0.35 * lexical + 0.10 * business
        candidates.append(
            {
                **chunk,
                "dense_score": round(dense, 4),
                "lexical_score": round(lexical, 4),
                "business_term_bonus": round(business, 4),
                "hybrid_score": round(hybrid, 4),
            }
        )
    return candidates


def _deduplicate_by_chunk_id(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    for item in items:
        current = best.get(item["chunk_id"])
        if current is None or item["hybrid_score"] > current["hybrid_score"]:
            best[item["chunk_id"]] = item
    return list(best.values())


def _rerank(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            item["hybrid_score"],
            item["lexical_score"],
            item["dense_score"],
        ),
        reverse=True,
    )


def _expand_chunks(primary_hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add adjacent chunks from the same policy section for context preservation."""
    wanted_ids = {hit["chunk_id"] for hit in primary_hits}
    for hit in primary_hits:
        for chunk in POLICY_CHUNKS:
            if chunk["section"] != hit["section"]:
                continue
            if abs(chunk["position"] - hit["position"]) <= 1:
                wanted_ids.add(chunk["chunk_id"])
    return [chunk for chunk in POLICY_CHUNKS if chunk["chunk_id"] in wanted_ids]


def hybrid_retrieve_policy(query: str, top_k: int = 3) -> dict[str, Any]:
    candidates = _hybrid_candidates(query)
    deduped = _deduplicate_by_chunk_id(candidates)
    reranked = _rerank(deduped)
    primary_hits = reranked[:top_k]
    expanded = _expand_chunks(primary_hits)
    return {
        "query": query,
        "primary_hits": primary_hits,
        "expanded_chunks": expanded,
        "candidate_count": len(candidates),
        "deduped_count": len(deduped),
        "top_k": top_k,
    }


def _load_rag_eval_cases() -> list[dict[str, Any]]:
    return json.loads(RAG_EVAL_PATH.read_text(encoding="utf-8"))


def evaluate_retrieval(top_k: int = 2) -> dict[str, float]:
    cases = _load_rag_eval_cases()
    hits = 0
    reciprocal_rank_sum = 0.0
    for case in cases:
        result = hybrid_retrieve_policy(case["query"], top_k=top_k)
        ids = [item["chunk_id"] for item in result["primary_hits"]]
        expected = case["expected_chunk_id"]
        if expected in ids:
            hits += 1
            reciprocal_rank_sum += 1.0 / (ids.index(expected) + 1)
    total = len(cases) or 1
    return {
        "hit_rate_at_k": round(hits / total, 4),
        "mrr_at_k": round(reciprocal_rank_sum / total, 4),
    }


def _trace(state: TravelState, event: str) -> list[str]:
    return [*state.get("trace", []), event]


def manager_agent(state: TravelState) -> Command:
    request = state["request"]
    return Command(
        goto="policy_rag",
        update={
            "messages": [
                AIMessage(
                    content=(
                        f"Manager: планирую командировку {request['origin']} → "
                        f"{request['destination']}; передаю PolicyRAG задачу проверить правила."
                    ),
                    name="manager",
                )
            ],
            "trace": _trace(
                state,
                "Manager -> PolicyRAG: explicit handoff via Command",
            ),
        },
    )


def policy_rag_agent(state: TravelState) -> Command:
    request = state["request"]
    query = (
        f"перелёт гостиница суточные лимит {request['destination']} "
        "командировка согласование"
    )
    retrieval = hybrid_retrieve_policy(query, top_k=3)
    refs = ", ".join(hit["chunk_id"] for hit in retrieval["primary_hits"])
    metrics = evaluate_retrieval(top_k=2)
    return Command(
        goto="flight_search",
        update={
            "policy_hits": retrieval["primary_hits"],
            "expanded_policy_chunks": retrieval["expanded_chunks"],
            "retrieval_metrics": metrics,
            "messages": [
                AIMessage(
                    content=(
                        "PolicyRAG: hybrid retrieval (dense + lexical) выполнен; "
                        f"reranked refs={refs}; context expanded. Передаю FlightSearch."
                    ),
                    name="policy_rag",
                )
            ],
            "trace": _trace(
                state,
                "PolicyRAG -> FlightSearch: dense+lexical -> dedup -> rerank -> chunk expansion",
            ),
        },
    )


def flight_search_agent(state: TravelState) -> Command:
    req = state["request"]
    options = [
        {
            "id": "FL-001",
            "route": f"{req['origin']}→{req['destination']}",
            "class": "economy",
            "price_rub": 14500,
            "refundable": True,
        },
        {
            "id": "FL-002",
            "route": f"{req['origin']}→{req['destination']}",
            "class": "economy",
            "price_rub": 11900,
            "refundable": False,
        },
    ]
    return Command(
        goto="hotel_search",
        update={
            "flight_options": options,
            "messages": [
                AIMessage(
                    content=f"FlightSearch: найдено {len(options)} read-only вариантов; передаю HotelSearch.",
                    name="flight_search",
                )
            ],
            "trace": _trace(state, "FlightSearch -> HotelSearch: explicit handoff via Command"),
        },
    )


def hotel_search_agent(state: TravelState) -> Command:
    city = state["request"]["destination"]
    options = [
        {"id": "HT-001", "city": city, "price_per_night_rub": 7600, "rating": 4.4},
        {"id": "HT-002", "city": city, "price_per_night_rub": 9800, "rating": 4.8},
    ]
    return Command(
        goto="budget",
        update={
            "hotel_options": options,
            "messages": [
                AIMessage(
                    content=f"HotelSearch: найдено {len(options)} вариантов проживания; передаю BudgetAnalyst.",
                    name="hotel_search",
                )
            ],
            "trace": _trace(state, "HotelSearch -> BudgetAnalyst: explicit handoff via Command"),
        },
    )


def budget_analyst(state: TravelState) -> Command:
    req = state["request"]
    nights = int(req.get("nights", 2))
    days = nights + 1
    flight = min(state["flight_options"], key=lambda x: x["price_rub"])
    hotel = min(state["hotel_options"], key=lambda x: x["price_per_night_rub"])
    daily = 1500 * days
    total = flight["price_rub"] + hotel["price_per_night_rub"] * nights + daily
    hotel_limit = 12000 if req["destination"].lower() in {"москва", "санкт-петербург"} else 8000
    policy_ok = hotel["price_per_night_rub"] <= hotel_limit and flight["class"] == "economy"
    budget = {
        "selected_flight": flight,
        "selected_hotel": hotel,
        "daily_allowance_rub": daily,
        "estimated_total_rub": total,
        "hotel_limit_rub": hotel_limit,
        "policy_ok": policy_ok,
    }
    return Command(
        goto="finalize",
        update={
            "budget": budget,
            "messages": [
                AIMessage(
                    content=(
                        f"BudgetAnalyst: оценка {total} ₽, policy_ok={policy_ok}; "
                        "возвращаю результат Manager."
                    ),
                    name="budget_analyst",
                )
            ],
            "trace": _trace(state, "BudgetAnalyst -> Manager: result handoff via Command"),
        },
    )


def manager_finalize(state: TravelState) -> dict[str, Any]:
    budget = state["budget"]
    evidence_refs = [
        {
            "source_id": hit["source_id"],
            "chunk_id": hit["chunk_id"],
            "score": hit["hybrid_score"],
            "dense_score": hit["dense_score"],
            "lexical_score": hit["lexical_score"],
        }
        for hit in state["policy_hits"]
    ]
    decision = "APPROVE_DRAFT" if budget["policy_ok"] else "REQUIRES_APPROVAL"
    answer = {
        "status": decision,
        "estimated_total_rub": budget["estimated_total_rub"],
        "flight_id": budget["selected_flight"]["id"],
        "hotel_id": budget["selected_hotel"]["id"],
        "evidence_refs": evidence_refs,
        "retrieval_metrics": state["retrieval_metrics"],
        "expanded_context_chunk_ids": [
            chunk["chunk_id"] for chunk in state["expanded_policy_chunks"]
        ],
        "note": (
            "Учебная рекомендация; фактическое бронирование и финансовое "
            "одобрение не выполняются."
        ),
    }
    return {
        "final_answer": answer,
        "messages": [
            AIMessage(
                content=f"Manager: собрал ответы агентов и сформировал {decision}.",
                name="manager",
            )
        ],
        "trace": _trace(state, "Manager: synthesized grounded final recommendation"),
    }


def build_graph():
    graph = StateGraph(TravelState)
    graph.add_node("manager", manager_agent)
    graph.add_node("policy_rag", policy_rag_agent)
    graph.add_node("flight_search", flight_search_agent)
    graph.add_node("hotel_search", hotel_search_agent)
    graph.add_node("budget", budget_analyst)
    graph.add_node("finalize", manager_finalize)

    graph.add_edge(START, "manager")
    graph.add_edge("finalize", END)
    return graph.compile()


def run_demo() -> TravelState:
    app = build_graph()
    initial: TravelState = {
        "request": {
            "employee": "Иван Петров",
            "origin": "Санкт-Петербург",
            "destination": "Москва",
            "nights": 2,
        },
        "messages": [
            SystemMessage(
                content=(
                    "Ты — учебная мультиагентная система оформления командировок. "
                    "Не выполняй реальные покупки и возвращай evidence refs."
                )
            ),
            HumanMessage(
                content="Организуй командировку Санкт-Петербург → Москва на две ночи.",
                name="employee",
            ),
        ],
        "trace": [],
        "policy_hits": [],
        "expanded_policy_chunks": [],
        "retrieval_metrics": {},
        "flight_options": [],
        "hotel_options": [],
        "budget": {},
        "final_answer": {},
    }
    return app.invoke(initial)


def _message_label(message: BaseMessage) -> str:
    name = getattr(message, "name", None)
    return name or message.type


if __name__ == "__main__":
    result = run_demo()
    print("=== TYPED AGENT MESSAGES ===")
    for item in result["messages"]:
        print(f"{item.__class__.__name__} [{_message_label(item)}]: {item.content}")
    print("\n=== FINAL ANSWER ===")
    print(json.dumps(result["final_answer"], ensure_ascii=False, indent=2))
    print("\n=== TRACE / HANDOFFS ===")
    for step in result["trace"]:
        print("-", step)
