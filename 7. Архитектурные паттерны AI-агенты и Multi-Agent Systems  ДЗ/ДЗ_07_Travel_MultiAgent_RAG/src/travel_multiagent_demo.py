"""Deterministic LangGraph prototype for OTUS DZ07.

The demo intentionally needs no LLM API key or network access.
It proves agent delegation, message exchange and a small RAG-like policy lookup.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph


POLICY_CHUNKS = [
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-FLIGHT-001",
        "text": "Для поездок по России базовый класс перелёта — эконом. Бизнес-класс требует согласования руководителя и перелёта свыше 6 часов.",
    },
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-HOTEL-001",
        "text": "Базовый лимит гостиницы — 8 000 ₽ за ночь. Для Москвы и Санкт-Петербурга допускается 12 000 ₽ за ночь.",
    },
    {
        "source_id": "TRAVEL-POLICY-001",
        "chunk_id": "POLICY-DAILY-001",
        "text": "Суточные для командировок по России — 1 500 ₽ в день.",
    },
]


class TravelState(TypedDict, total=False):
    request: dict[str, Any]
    messages: list[dict[str, str]]
    trace: list[str]
    policy_hits: list[dict[str, Any]]
    flight_options: list[dict[str, Any]]
    hotel_options: list[dict[str, Any]]
    budget: dict[str, Any]
    final_answer: dict[str, Any]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())


def _hash_embedding(text: str, dims: int = 64) -> list[float]:
    """Small deterministic local embedding for the offline classroom demo."""
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


def retrieve_policy(query: str, top_k: int = 2) -> list[dict[str, Any]]:
    q = _hash_embedding(query)
    scored = []
    for chunk in POLICY_CHUNKS:
        score = _cosine(q, _hash_embedding(chunk["text"]))
        scored.append({**chunk, "score": round(score, 4)})
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def _append_message(state: TravelState, sender: str, text: str) -> list[dict[str, str]]:
    return [*state.get("messages", []), {"from": sender, "text": text}]


def manager_agent(state: TravelState) -> TravelState:
    request = state["request"]
    trace = [*state.get("trace", []), "Manager: decomposed request and delegated policy, flight, hotel and budget tasks"]
    return {
        "messages": _append_message(
            state,
            "Manager",
            f"Планирую командировку {request['origin']} → {request['destination']} и делегирую специализированным агентам.",
        ),
        "trace": trace,
    }


def policy_rag_agent(state: TravelState) -> TravelState:
    request = state["request"]
    query = f"перелёт гостиница суточные {request['destination']} командировка"
    hits = retrieve_policy(query, top_k=3)
    refs = ", ".join(hit["chunk_id"] for hit in hits)
    return {
        "policy_hits": hits,
        "messages": _append_message(state, "PolicyRAG", f"Нашёл правила политики: {refs}"),
        "trace": [*state.get("trace", []), "PolicyRAG: retrieved and reranked policy chunks"],
    }


def flight_search_agent(state: TravelState) -> TravelState:
    req = state["request"]
    options = [
        {"id": "FL-001", "route": f"{req['origin']}→{req['destination']}", "class": "economy", "price_rub": 14500, "refundable": True},
        {"id": "FL-002", "route": f"{req['origin']}→{req['destination']}", "class": "economy", "price_rub": 11900, "refundable": False},
    ]
    return {
        "flight_options": options,
        "messages": _append_message(state, "FlightSearch", f"Найдено {len(options)} варианта перелёта."),
        "trace": [*state.get("trace", []), "FlightSearch: returned mock read-only flight options"],
    }


def hotel_search_agent(state: TravelState) -> TravelState:
    req = state["request"]
    city = req["destination"]
    options = [
        {"id": "HT-001", "city": city, "price_per_night_rub": 7600, "rating": 4.4},
        {"id": "HT-002", "city": city, "price_per_night_rub": 9800, "rating": 4.8},
    ]
    return {
        "hotel_options": options,
        "messages": _append_message(state, "HotelSearch", f"Найдено {len(options)} варианта проживания."),
        "trace": [*state.get("trace", []), "HotelSearch: returned mock read-only hotel options"],
    }


def budget_analyst(state: TravelState) -> TravelState:
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
    return {
        "budget": budget,
        "messages": _append_message(state, "BudgetAnalyst", f"Оценка поездки: {total} ₽; policy_ok={policy_ok}."),
        "trace": [*state.get("trace", []), "BudgetAnalyst: calculated total and checked policy limits"],
    }


def manager_finalize(state: TravelState) -> TravelState:
    budget = state["budget"]
    evidence_refs = [
        {"source_id": hit["source_id"], "chunk_id": hit["chunk_id"], "score": hit["score"]}
        for hit in state["policy_hits"]
    ]
    decision = "APPROVE_DRAFT" if budget["policy_ok"] else "REQUIRES_APPROVAL"
    answer = {
        "status": decision,
        "estimated_total_rub": budget["estimated_total_rub"],
        "flight_id": budget["selected_flight"]["id"],
        "hotel_id": budget["selected_hotel"]["id"],
        "evidence_refs": evidence_refs,
        "note": "Учебная рекомендация; фактическое бронирование и финансовое одобрение не выполняются.",
    }
    return {
        "final_answer": answer,
        "messages": _append_message(state, "Manager", f"Собрал ответ от агентов: {decision}."),
        "trace": [*state.get("trace", []), "Manager: synthesized final recommendation from delegated results"],
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
    graph.add_edge("manager", "policy_rag")
    graph.add_edge("policy_rag", "flight_search")
    graph.add_edge("flight_search", "hotel_search")
    graph.add_edge("hotel_search", "budget")
    graph.add_edge("budget", "finalize")
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
        "messages": [],
        "trace": [],
    }
    return app.invoke(initial)


if __name__ == "__main__":
    result = run_demo()
    print("=== AGENT MESSAGES ===")
    for item in result["messages"]:
        print(f"{item['from']}: {item['text']}")
    print("\n=== FINAL ANSWER ===")
    print(result["final_answer"])
    print("\n=== TRACE ===")
    for step in result["trace"]:
        print("-", step)
