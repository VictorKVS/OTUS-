# ДЗ 05 — Многоуровневое проектирование: C4 → API

> ## 📄 Готовый PDF для сдачи
>
> **[Открыть DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf](./DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf)**  
> Контрольная сумма: [`SHA256SUMS.txt`](./SHA256SUMS.txt)  
> PDF автоматически пересобирается GitHub Actions при изменении материалов ДЗ.

## 1. Кейс

Для домашнего задания используется собственный кейс — **OSINT / Due Diligence AI Platform**.

Пользователь работает с делом проверки контрагента/объекта и запрашивает у AI Service рекомендацию, например: можно ли одобрить поставщика, требуется ли углублённая проверка или какие шаги расследования выполнить дальше.

Основной сценарий задания:

```text
Analyst → Frontend → Backend → AI Service → Vector DB / SQL DB → LLM
                                           ↓
                              recommendation + evidence refs
```

AI Service возвращает рекомендацию с доказательствами, confidence и limitations; high-impact решение остаётся за человеком.

---

## 2. Проверка соответствия условию

| Требование ДЗ | Реализация | Статус |
|---|---|---|
| C2 Container Diagram всей системы | [`architecture/C2_SYSTEM_CONTAINERS.svg`](./architecture/C2_SYSTEM_CONTAINERS.svg) + [`C2_SYSTEM_CONTAINERS.md`](./architecture/C2_SYSTEM_CONTAINERS.md) | ✅ |
| На C2 выделить Frontend | `Frontend — React/TypeScript` | ✅ |
| На C2 выделить Backend | `Backend / Case Service — FastAPI` | ✅ |
| На C2 выделить AI Service | `Knowledge & Recommendation Agent` | ✅ |
| На C2 выделить Vector DB | `Vector DB — pgvector/vector index` | ✅ |
| На C2 выделить SQL DB | `SQL DB — PostgreSQL` | ✅ |
| C3 внутри AI Service | [`architecture/C3_KB_AGENT_COMPONENTS.svg`](./architecture/C3_KB_AGENT_COMPONENTS.svg) + [`C3_KB_AGENT_COMPONENTS.md`](./architecture/C3_KB_AGENT_COMPONENTS.md) | ✅ |
| Sequence «Пользователь запрашивает рекомендацию» | [`architecture/SEQUENCE_GET_RECOMMENDATION.md`](./architecture/SEQUENCE_GET_RECOMMENDATION.md) | ✅ |
| API Backend ↔ AI Service | [`api/openapi.yaml`](./api/openapi.yaml) | ✅ |
| Endpoint `/get_recommendation` | `POST /get_recommendation` | ✅ |
| Типы данных | OpenAPI schemas | ✅ |
| Пример request/response | OpenAPI examples | ✅ |
| Коды ошибок | `400/401/404/422/429/500/503` | ✅ |

Точное условие зафиксировано в [`УСЛОВИЕ_ДЗ.md`](./УСЛОВИЕ_ДЗ.md).

---

## 3. C2 — Container Diagram

![C2 — OSINT / Due Diligence AI Platform](./architecture/C2_SYSTEM_CONTAINERS.svg)

### Контейнеры

| Контейнер | Ответственность | Технология |
|---|---|---|
| Frontend | интерфейс аналитика, кейс, запрос и вывод рекомендации | React / TypeScript |
| Backend / Case Service | API gateway, case orchestration, policy, structured data | FastAPI |
| AI Service | RAG, prompt, LLM, citation validation, recommendation | Python / FastAPI |
| Vector DB | semantic retrieval по chunks/knowledge | PostgreSQL + pgvector / vector index |
| SQL DB | cases, entities, findings, sources, review state | PostgreSQL |
| Evidence Vault | originals, evidence lineage, SHA-256 | object storage |

Ключевая интеграция:

```text
Backend → POST /get_recommendation → AI Service
```

---

## 4. C3 — AI Service

![C3 — AI Service](./architecture/C3_KB_AGENT_COMPONENTS.svg)

Внутренние компоненты AI Service:

1. **Recommendation Controller** — endpoint `/get_recommendation`, валидация и orchestration.
2. **Query Normalizer** — нормализует query, language, case context.
3. **RAG Manager** — получает semantic и structured context.
4. **Prompt Template Factory** — формирует prompt нужного типа.
5. **LLM Client** — вызывает LLM через контролируемый gateway.
6. **Citation & Evidence Guard** — проверяет evidence refs и неподтверждённые утверждения.
7. **Confidence Evaluator** — учитывает полноту и противоречия источников.
8. **Recommendation Formatter** — возвращает стабильный JSON contract.
9. **Audit Writer** — сохраняет model/prompt/retrieval versions и execution trail.

### Проверка связности C3 ↔ Sequence

Все основные участники AI Service на Sequence Diagram имеют прямой аналог на C3:

```text
Recommendation Controller
→ Query Normalizer
→ RAG Manager
→ Prompt Template Factory
→ LLM Client
→ Citation & Evidence Guard
→ Confidence Evaluator
→ Recommendation Formatter
```

Это закрывает критерий «компоненты C3 соответствуют шагам Sequence Diagram».

---

## 5. Sequence Diagram — «Пользователь запрашивает рекомендацию»

Исходник и визуализация Mermaid: [`architecture/SEQUENCE_GET_RECOMMENDATION.md`](./architecture/SEQUENCE_GET_RECOMMENDATION.md).

Основная последовательность:

```text
Analyst
  ↓
Frontend
  ↓ POST /cases/{caseId}/recommendation
Backend
  ↓ POST /get_recommendation
Recommendation Controller
  ↓
Query Normalizer
  ↓
RAG Manager
  ├─ Vector DB
  └─ SQL DB / Evidence context
  ↓
Prompt Template Factory
  ↓
LLM Client → LLM
  ↓
Citation & Evidence Guard
  ↓
Confidence Evaluator
  ↓
Recommendation Formatter
  ↓
Backend → Frontend → Analyst
```

При недостатке доказательств AI Service возвращает `422 INSUFFICIENT_EVIDENCE`, а не выдумывает недостающий факт.

---

## 6. OpenAPI 3.1 — Backend ↔ AI Service

Спецификация: **[`api/openapi.yaml`](./api/openapi.yaml)**.

Главный endpoint задания:

```http
POST /get_recommendation
Content-Type: application/json
Authorization: Bearer <JWT>
```

Пример запроса:

```json
{
  "request_id": "REQ-2026-00042",
  "case_id": "CASE-RU-LEGAL-0042",
  "query": "Should the supplier be approved for access to the corporate information system?",
  "recommendation_type": "COUNTERPARTY_RISK",
  "language": "ru",
  "top_k": 8,
  "include_evidence": true
}
```

Пример ответа:

```json
{
  "recommendation_id": "REC-2026-0042",
  "request_id": "REQ-2026-00042",
  "case_id": "CASE-RU-LEGAL-0042",
  "recommendation": "APPROVE_WITH_CONDITIONS",
  "confidence": 0.82,
  "evidence_refs": [
    {
      "source_id": "SRC-FNS-0001",
      "capture_id": "CAP-FNS-20260903-01",
      "chunk_id": "CHK-FNS-17",
      "source_type": "OFFICIAL_REGISTRY"
    }
  ],
  "limitations": ["Beneficial ownership chain is not fully verified."],
  "research_gaps": ["GAP-UBO-0003"]
}
```

Ошибки описаны в OpenAPI:

| HTTP | Код | Значение |
|---:|---|---|
| 400 | `INVALID_REQUEST` | неверный контракт |
| 401 | `UNAUTHORIZED` | ошибка authentication |
| 404 | `CASE_NOT_FOUND` | кейс не найден |
| 422 | `INSUFFICIENT_EVIDENCE` | недостаточно доказательств |
| 429 | `RATE_LIMITED` | превышен лимит |
| 500 | `INTERNAL_ERROR` | ошибка AI Service |
| 503 | `DEPENDENCY_UNAVAILABLE` | LLM/Vector DB недоступны |

---

## 7. Дополнительные архитектурные материалы

Они не заменяют обязательные C2/C3/Sequence/API, а дополняют решение:

- BPMN: [`architecture/BPMN/OSINT_KB_AGENT_BPMN_V1_READABLE.svg`](./architecture/BPMN/OSINT_KB_AGENT_BPMN_V1_READABLE.svg)
- BPMN 2.0 XML: [`architecture/BPMN/OSINT_KB_AGENT_BPMN_V1.bpmn`](./architecture/BPMN/OSINT_KB_AGENT_BPMN_V1.bpmn)
- DFD: [`architecture/DFD/OSINT_KB_AGENT_DFD_V1_READABLE.svg`](./architecture/DFD/OSINT_KB_AGENT_DFD_V1_READABLE.svg)
- Потоки информации: [`docs/OSINT_KB_AGENT_INFORMATION_FLOW_V1.md`](./docs/OSINT_KB_AGENT_INFORMATION_FLOW_V1.md)

---

## 8. Архитектурные ограничения AI Service

- `SOURCE ≠ CLAIM ≠ FACT`.
- recommendation не равна автоматическому управленческому решению.
- LLM не публикует `FACT` напрямую.
- существенные утверждения ответа должны иметь `evidence_refs`.
- при недостатке доказательств возвращается research gap / `422`, а не выдуманный ответ.
- model, prompt и retrieval profile версионируются.
- restricted evidence не экспортируется в публичный контур.

---

## 9. Структура сдачи

```text
ДЗ_05_OSINT_KB_Agent_LLD/
├── README.md
├── УСЛОВИЕ_ДЗ.md
├── DZ05_LLD_OSINT_KB_AGENT_SUBMISSION.pdf
├── SHA256SUMS.txt
├── api/
│   └── openapi.yaml
├── architecture/
│   ├── C2_SYSTEM_CONTAINERS.md
│   ├── C2_SYSTEM_CONTAINERS.svg
│   ├── C3_KB_AGENT_COMPONENTS.md
│   ├── C3_KB_AGENT_COMPONENTS.svg
│   ├── SEQUENCE_GET_RECOMMENDATION.md
│   ├── BPMN/
│   └── DFD/
├── docs/
└── tools/
```

---

## 10. Автоматическая сборка PDF

Workflow `.github/workflows/dz5-build-submission-pdf.yml` автоматически:

1. собирает PDF;
2. проверяет `%PDF-` и размер;
3. рассчитывает SHA-256;
4. коммитит PDF и `SHA256SUMS.txt` обратно в `main`.

---

## 11. Итог

Работа построена в требуемой последовательности:

```text
C2 SYSTEM
   ↓
C3 AI SERVICE
   ↓
SEQUENCE: USER REQUESTS RECOMMENDATION
   ↓
OPENAPI: POST /get_recommendation
```

Таким образом, архитектурные уровни связаны между собой одним сценарием и одним контрактом интеграции Backend ↔ AI Service.
