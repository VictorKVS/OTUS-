# OTUS 01–31 → SADEQ UAA · Матрица сквозной архитектуры и квалификации
**Версия:** 0.3 / 27.11.2026 · **Тип:** Traceability & Delivery Plan · **Статус:** PLANNED / NOT_EXECUTED

## Принцип
Урок — не отдельная домашняя работа, а элемент одного архитектурного продукта. Для каждого урока фиксируем **артефакт + критерий приёмки + доказательство + влияние на стоимость**. Источник названий: структура каталога курса OTUS и ARCHITECTURE_ROADMAP.md. Никакие задания не объявляются сданными без подтверждения OTUS.

| № | Урок (как отражён в репозитории) | Артефакт SADEQ | Контроль / метод | Cost / масштабирование |
|---|---|---|---|---|
| 01 | Пресейл, контракты и требования | Product Vision, заказчики, миссия UAA, stakeholder map | интервью, приоритеты, acceptance | стоимость discovery и обязательств |
| 02 | Оценка проекта, план, риски и смета | WBS, RACI, RAID, Basis of Estimate | источники ставок и сроков; 3 сценария | CAPEX, OPEX, contingency |
| 03 | Стратегия ценности PoC→Production | MVP scope, release roadmap, value stream | hypotheses→PoC→pilot→production gates | стоимость каждого gate |
| 04 | HLD с C4 | C4 Context/Container + trust boundaries | coverage систем, ролей, внешних интеграций | стоимость раздельных сервисов |
| 05 | LLD компонентов | typed I/O contracts; State/Event/Action schemas | тесты чёрного ящика, NFR | reuse vs build |
| 06 | Архитектурные паттерны RAG | GraphRAG: Qdrant+Neo4j, source provenance | vector-only vs graph benchmark; leakage tests | цена индекса/поиска/обновлений |
| 07 | AI Agents / Multi-Agent | UAA LangGraph FSM, profile spec, tool gateways | state checkpoint, loop limits, approval | агентные шаги, токены, tool calls |
| 08 | ADR | обоснования решений local/hosted DB/model, broker, ACL | альтернативы, rollback, decision owner | trade-offs total cost |
| 09 | Архитектурная верификация / CTO challenge | Design Review & objections register | независимый ADR critique и противоречия | изменение архитектуры до CAPEX |
| 10 | Надзор и техдолг | Technical Debt & fitness functions | проверка границ, эволюция контрактов | долг как будущие OPEX |
| 11 | Интеграции и AI-стандарты | OpenAPI, webhooks, MCP adapter (optional), ERP/CRM connectors | contract tests; no direct untrusted tool access | интеграционные адаптеры |
| 12 | Архитектура данных | ER, event sourcing, object identity, CDC, backups | order/idempotency/retention/ACL | storage, IOPS, backup |
| 13 | Качество и тестирование GenAI | QA plan, retrieval eval, groundedness, holdout cases | accuracy/recall@k, no self-grading | cost per qualified outcome |
| 14 | Security by Design | Threat model (STRIDE), RBAC/ABAC, policy, prompt injection | User B → secret must DENY | security staffing and controls |
| 15 | Observability | OTel, Jaeger, Prometheus/Grafana, structured logs | E2E trace, TTFT, tokens/s, redaction | telemetry storage cost |
| 16 | Sizing ресурсов | CPU/RAM/SSD/GPU/network sizing workbook | measured p50/p95, concurrency, disk growth | how many nodes & their price |
| 17 | Оптимизация LLM inference | quantization AWQ/GGUF, batching, KV, model routing | quality/VRAM/TTFT benchmark | efficiency per GPU-hour |
| 18 | IaC, CI/CD | offline Docker compose, Helm, provenance, SBOM, signatures | local mirror + reproducible deploy | engineering and environments |
| 19 | MLOps | model registry, versioning, evaluation & promotion | rollback and requalification | storage and validation |
| 20 | Deployment / Production | rollout, shadow/canary where allowed, rollback | recovery test, artifact signature | downtime, controlled release |
| 21 | HA/DR | SLO/SLI, RTO/RPO, failover, backup and restore | game day, failure injection | duplicate nodes and site |
| 22 | Serverless vs Kubernetes | deployment ADR: compose / K8s / event jobs | operations cost threshold; autoscaling test | control-plane + idle resources |
| 23 | EDA | event bus, source timestamps, outbox and dedup | replay, duplicate & late event tests | broker and message retention |
| 24 | High-load/low latency | API vs LLM latency budget; queue and concurrency | 10k RPS only for scoped API; LLM measured separately | GPU pool/batching capacity |
| 25 | Hybrid/multicloud | on-prem primary; cloud-IaaS analysis as variant | private connectivity, egress, data sovereignty and air-gap decision | 24/7 vs burst tariffs |
| 26 | Multi-tenancy | identity, tenant ACL across graph/vector/logs; quotas | cross-tenant leakage negative tests | dedicated vs pooled tenant cost |
| 27 | Federated learning/privacy preserving | privacy boundary, PII minimization, optional FL research | no training weights in MVP; retention tests | privacy/compliance overhead |
| 28 | FinOps architecture | pricing register, LOW/BASE/HIGH, burn rate, cost/task | real tariff snapshots, price shock +50% | TCO/ROI/break-even |
| 29 | Technology radar | candidate adoption/hold/reject per maturity | expiry triggers, model/DB availability | cost of migration |
| 30 | Ethical AI & Governance | Model Card, trust levels, bias/limitations, audit | unsafe object classification → ABSTAIN; human control | independent QA and liability |
| 31 | API as product | API lifecycle, versioning, quotas, developer documentation | consumer contract acceptance | price/tariff internal API SLA |

## Сквозные проверки
- **Business gate:** задокументирована потребность; baseline AS-IS; target outcomes и financial assumptions.
- **Architecture gate:** C4 1–4, Deployment, Sequence, ER, ADR, DMN/BPMN и журналы риска связаны с REQ.
- **Offline gate:** модели и контейнеры предварительно в локальном зеркале, deny-all egress, нет внешнего API runtime.
- **Security gate:** User B не извлекает User A data через tool, graph, vector, history, log или citation.
- **Scientific gate:** retrieval GraphRAG даёт проверяемые citations; forecast имеет baseline/backtesting; agent learning не изменяет риск-политику автоматически.
- **Scale gate:** измерены независимые `API RPS`, `full answer RPS`, `TTFT`, `p95`, `tokens/s`, `peak VRAM`, `queue depth` и `cost/accepted outcome`.
- **Financial gate:** одинаковый workload и SLO для local/cloud сравнения; инстанс *не* равен полноценной production-системе.

## Уроки 20 и 24
В OTUS существуют *разные* темы: урок 20 — стратегии развёртывания и вывода в Production, урок 24 — High-Load/Low-Latency. Упражнение с 10 000 RPS / <200ms оцениваем отдельно по типу запроса и end-to-end latency; одна RTX 3060 не обязана выполнять 10 000 LLM ответов в секунду.

## Группы сборки
G1: 1–3. G2: 4–7. G3: 8–10. G4: 11–15. G5: 16–20. G6: 21–27. G7: 28–31. Состояние предыдущего реестра: G1 in_progress, остальное pending; здесь **планируемые deliverables**, не утверждение об их готовности.

## Traceability record template
```
BUS-xxx → REQ-xxx → NFR-xxx → RISK-xxx → ADR-xxx → CMP-xxx
  → API/DATA-xxx → CTRL-xxx → TEST-xxx → SLO-xxx → COST-xxx → REL-xxx
```
Каждая запись должна иметь owner, status (PROPOSED/TESTED/APPROVED), commit SHA, evidence path и date. Нет evidence → NOT_QUALIFIED.
