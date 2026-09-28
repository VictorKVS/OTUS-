# Interview Competency Matrix

## Шкала

- **L1 — Concept:** понимаю назначение и место в архитектуре.
- **L2 — Working:** могу реализовать типовой сценарий с документацией/инструментами.
- **L3 — Independent:** могу самостоятельно спроектировать, реализовать и защитить решение.

Evidence: `WORK`, `PROJECT`, `LAB`, `KNOWLEDGE`, `VERIFY`.

| Блок | Компетенция | Целевой уровень | Что нужно доказать на интервью |
|---|---|---:|---|
| LLM | LLM integration | L2–L3 | API/local model, выбор модели, latency/cost/privacy trade-offs |
| LLM | Prompt engineering | L2–L3 | system/user/context/examples/constraints/output contract |
| LLM | Structured output | L3 | JSON Schema/Pydantic, validation, retry/fallback |
| LLM | Tool calling | L2–L3 | модель предлагает действие, приложение проверяет и исполняет |
| RAG | Ingestion/parsing | L2–L3 | происхождение документа, структура, IDs, metadata |
| RAG | Chunking | L2–L3 | fixed/semantic/structure-aware, влияние на retrieval |
| RAG | Embeddings/vector search | L2 | semantic search, top-k, similarity basics |
| RAG | Hybrid retrieval | L2 | vector + lexical/BM25 |
| RAG | Reranking | L2 | candidate retrieval → reranker → context |
| RAG | Grounding/traceability | L3 | answer → chunk → section → source |
| Graph | Knowledge Graph / GraphRAG | L1–L2 | сущности, связи, traversal, когда граф оправдан |
| Agents | Agent pattern | L2–L3 | goal → decide → tool → observe → finish |
| Agents | Multi-agent | L2 | разделение ролей/контекста/прав |
| Agents | Orchestration | L2–L3 | routing, retries, timeout, state, approval |
| Agents | Memory | L2 | short-term / working / long-term |
| Agents | MCP | L1–L2 | client/server/tools, унификация интеграций |
| Quality | Eval dataset | L2–L3 | golden set, expected result/sources/constraints |
| Quality | Regression | L2–L3 | сравнение до/после prompt/model/RAG |
| Quality | RAG metrics | L2 | relevance, recall/precision, groundedness/citations |
| Quality | Tracing | L2–L3 | prompt, retrieval, tools, tokens, latency, errors |
| Secure AI | Prompt injection | L2–L3 | direct/indirect, trusted instructions vs untrusted content |
| Secure AI | Data leakage | L2–L3 | authorization before retrieval, document/chunk ACL |
| Secure AI | Tool security | L2–L3 | least privilege, allowlist, validation, approval, audit |
| Secure AI | Guardrails | L2 | layered controls |
| Backend | Python | L2–L3 | typing, exceptions, modules, classes, generators basics |
| Backend | asyncio | L2 | I/O-bound concurrency и ограничения |
| Backend | FastAPI/REST | L2–L3 | validation, service layer, auth/error handling |
| Backend | PostgreSQL/SQL | L2 | schema, joins, indexes basics, pgvector role |
| Backend | Docker | L2 | image/container/volume/network/env/compose |
| Backend | Git | L2–L3 | branch/commit/merge/PR/conflict |
| Backend | pytest/CI | L2 | unit/integration/regression + pipeline gates |
| AI-assisted | AI-assisted engineering | L3 method | requirement → design → generation → review → tests → integration |
| Compliance | Requirements engineering | L3 | collection, decomposition, IDs, traceability |
| Compliance | Applicability | L3 | что относится к системе/данным/процессу и почему |
| Compliance | Gap analysis | L3 | as-is vs required → remediation |
| Compliance | Control mapping | L2–L3 | requirement → control → system → evidence |
| Security | Asset/data-flow analysis | L3 | что защищаем, где данные, кто владелец, куда передаются |
| Security | Access governance | L2–L3 | RBAC, least privilege, need-to-know, SoD, access matrix |
| Security | Segmentation | L2 | trust zones и controlled flows |
| Security | Backup/recovery | L2 | RPO/RTO, 3-2-1, offline/immutable, restore test |
| Security | DLP/SIEM/EDR/WAF | L2 architecture | назначение, границы и место в общей архитектуре |

## Не заявлять без evidence

`production-grade`, промышленную эксплуатацию AI-систем, точные проценты улучшения качества без воспроизводимых измерений, глубокое администрирование конкретных SIEM/DLP/EDR без hands-on evidence и senior-роль как коммерчески подтверждённую.