# Эволюция API: ДЗ 05 → ДЗ 07

## Зачем это нужно

ДЗ 07 не проектируется с нуля. Оно продолжает архитектуру ДЗ 05 и использует уже разработанный внутренний контракт Backend → AI Service.

В ДЗ 05 был зафиксирован стабильный AI endpoint:

```http
POST /get_recommendation
```

Он принимал `RecommendationRequest` и возвращал `RecommendationResponse` с `evidence_refs`, `confidence`, `limitations` и `research_gaps`.

В ДЗ 07 endpoint **не заменяется**, а расширяется для travel-домена:

- добавляется `recommendation_type = TRAVEL_PLAN`;
- в запросе появляется опциональный `travel_context`;
- в ответе появляется опциональный `domain_result = TripPlanResult`;
- все базовые поля ДЗ 05 остаются совместимыми.

Это показывает эволюцию архитектуры, а не набор несвязанных домашних заданий.

---

## Сквозная API-цепочка

```mermaid
sequenceDiagram
    autonumber
    actor U as Employee
    participant FE as Frontend
    participant BE as Backend / Travel Service
    participant SQL as SQL DB
    participant AI as AI Service
    participant M as Manager Agent
    participant RAG as Policy RAG
    participant VDB as Vector DB
    participant AD as Travel Adapters
    participant EXT as Travel Providers
    participant AUD as Evidence / Audit
    participant H as Human Approval
    participant B as Booking Service
    participant PAY as Payment Gateway

    U->>FE: Создать командировку
    FE->>BE: POST /trip-missions
    BE->>SQL: save TripMission
    SQL-->>BE: mission_id + version
    BE-->>FE: 201 TripMission

    U->>FE: Построить варианты
    FE->>BE: POST /trip-missions/{id}/plan
    BE->>AI: POST /get_recommendation\nrecommendation_type=TRAVEL_PLAN
    AI->>M: TripMission + constraints

    M->>RAG: policy query
    RAG->>VDB: hybrid retrieval
    VDB-->>RAG: policy chunks + ids + scores
    RAG-->>M: rules + evidence_refs

    M->>AD: search providers
    AD->>EXT: air/rail/hotel/taxi/maps
    EXT-->>AD: prices + schedules + availability
    AD->>AUD: API evidence
    AD-->>M: normalized provider results

    M-->>AI: plans A/B/C + policy status + risks
    AI-->>BE: RecommendationResponse + TripPlanResult
    BE->>AUD: decision trace
    BE-->>FE: plan DTO
    FE-->>U: Показать варианты и объяснения

    U->>FE: Выбрать план
    FE->>BE: POST /trip-missions/{id}/approval
    BE->>H: approval request
    H-->>BE: APPROVE / REJECT / REQUEST_CHANGES

    alt APPROVE
        BE->>B: booking request
        B->>PAY: payment intent
        PAY-->>B: payment_ref / status
        B-->>BE: booking_id / status
        BE->>SQL: update mission
        BE-->>FE: booking confirmed
    else REJECT or REQUEST_CHANGES
        BE-->>FE: replan required
    end
```

---

## Две границы API

### 1. Frontend ↔ Backend

Доменные endpoints:

```text
POST /trip-missions
POST /trip-missions/{mission_id}/plan
POST /trip-missions/{mission_id}/approval
```

Они работают с сущностями бизнеса: `TripMission`, `Venue`, `TripPlan`, `Approval`.

### 2. Backend ↔ AI Service

Сохраняется контракт из ДЗ 05:

```text
POST /get_recommendation
```

Он остаётся доменно-независимым AI-контрактом и получает `travel_context` только когда `recommendation_type = TRAVEL_PLAN`.

---

## Почему это архитектурно полезно

1. **Backward compatibility.** Клиенты ДЗ 05 продолжают работать.
2. **Separation of concerns.** Backend хранит бизнес-сущности; AI Service выдаёт evidence-backed recommendation.
3. **Human-in-the-loop.** Approval и payment не выполняются AI-агентом.
4. **Traceability.** Каждая рекомендация сохраняет `request_id`, `trace_id`, `evidence_refs` и версию модели/prompts.
5. **Эволюция курса.** C4/API из ДЗ 05 становятся фундаментом multi-agent/RAG решения ДЗ 07.

---

## Артефакты

- ДЗ 05 OpenAPI: `../../5.../api/openapi.yaml` — исходный контракт `/get_recommendation`.
- ДЗ 07 OpenAPI: [`../api/openapi-travel.yaml`](../api/openapi-travel.yaml) — совместимое расширение v2.1.0.
- ДЗ 07 LangGraph: [`../src/travel_multiagent_demo.py`](../src/travel_multiagent_demo.py).
