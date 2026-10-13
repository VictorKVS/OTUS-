# Traceability 0–20

| Lesson | Input | Engineering decision | Output | Feeds |
|---:|---|---|---|---|
| 00 | Идея | Идея и паспорт проекта: Защищённый AI‑ассистент по корпоративной базе знаний с RAG, цитатами, аудитом и контролем доступа. | PROJECT_CHARTER.md · PROJECT_ID · границы | 01 |
| 01 | Outputs 00 | Бизнес-контекст: Пользователи, ценность, ограничения, stakeholders, критерии успеха. | BUSINESS_CONTEXT.md · SUCCESS_CRITERIA.md | 02 |
| 02 | Outputs 01 | Требования, оценка и риски: Функциональные требования, NFR, риски, оценка объёма и сроков. | REQ.md · NFR.md · RISK_REGISTER.md | 03 |
| 03 | Outputs 02 | Поставка ценности: PoC → MVP → Production; критерии перехода между стадиями. | DELIVERY_ROADMAP.md · STAGE_GATES.md | 04 |
| 04 | Outputs 03 | HLD / C4: Контекст и контейнеры системы: UI/API, RAG, registry, observability, security. | C4_CONTEXT.md · C4_CONTAINER.md | 05 |
| 05 | Outputs 04 | LLD и контракты: Компоненты, sequence, OpenAPI, data contracts, ошибки и таймауты. | LLD.md · OPENAPI.yaml · SEQUENCE.md | 06 |
| 06 | Outputs 05 | RAG: Ingestion, chunking, embeddings, hybrid retrieval, reranking, citations. | RAG_SPEC.md · RETRIEVAL_POLICY.md | 07 |
| 07 | Outputs 06 | AI‑агент: Agent/Supervisor workflow, tools, handoff, memory boundaries. | AGENT_SPEC.md · WORKFLOW.md | 08 |
| 08 | Outputs 07 | ADR: Фиксация ключевых архитектурных решений и trade-offs. | ADR-*.md | 09 |
| 09 | Outputs 08 | Архитектурная проверка: CTO challenge / ATAM-подобная проверка качественных атрибутов и рисков. | ARCH_REVIEW.md · GAP_REGISTER.md | 10 |
| 10 | Outputs 09 | Надзор и техдолг: Governance, exceptions, technical debt, ownership. | GOVERNANCE.md · TECH_DEBT.md | 11 |
| 11 | Outputs 10 | Интеграции: API, events, tools/MCP, retries, idempotency, boundary security. | INTEGRATIONS.md · INTERFACE_CATALOG.md | 12 |
| 12 | Outputs 11 | Архитектура данных: Источники, классификация, storage, vector DB, lineage и retention. | DATA_ARCHITECTURE.md · DATA_CLASSIFICATION.md | 13 |
| 13 | Outputs 12 | Evaluation: Golden set, RAG/LLM metrics, regression gates, статистический дизайн экспериментов. | EVAL_PLAN.md · GOLDEN_SET_SPEC.md | 14 |
| 14 | Outputs 13 | Security by Design: Threat model, PII, secrets, IAM, guardrails, tool policy, security tests. | THREAT_MODEL.md · SECURITY_CONTROLS.md | 15 |
| 15 | Outputs 14 | Observability: Metrics/logs/traces, AI telemetry, SLI/SLO, alerting, release correlation. | OBSERVABILITY.md · SLO.md | 16 |
| 16 | Outputs 15 | Sizing: RPS, CPU/RAM/storage/vector DB, replicas, headroom и capacity model. | SIZING.md · CAPACITY_MODEL.md | 17 |
| 17 | Outputs 16 | LLM inference sizing: VRAM, quantization, batching, latency/throughput, GPU profile. | INFERENCE_PROFILE.md · BENCHMARK_PLAN.md | 18 |
| 18 | Outputs 17 | IaC + CI/CD + DevSecOps: Terraform, Docker, tests, SBOM, SAST/SCA, scans, staging. | PIPELINE.md · IAC.md · SECURITY_GATES.md | 19 |
| 19 | Outputs 18 | MLOps: Dataset/knowledge change → validation → retrain/reindex → eval → registry → release trigger. | MLOPS_PIPELINE.md · MODEL_REGISTRY.md | 20 |
| 20 | Outputs 19 | Production release: GitOps + Argo CD + Canary 1% → 5% → 100%, readiness и rollback. | DZ20_REPORT.md · CANARY_POLICY.md · ROLLBACK_PLAN.md | Production / feedback |

## Сквозной release identity

Каждый production release связывает четыре независимо меняющихся объекта:

```text
APP IMAGE DIGEST
+ MODEL VERSION / DIGEST
+ RAG INDEX VERSION
+ PROMPT / CONFIG VERSION
= RELEASE_ID
```

Это позволяет воспроизводить, сравнивать и откатывать релиз без угадывания «какая модель тогда стояла».
