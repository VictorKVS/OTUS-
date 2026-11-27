# SADEQ-TRACE-001 — OTUS → книга → ГОСТ → документ → испытание
**Это карта внутренних учебных тем и проектных результатов, а не официальный учебный план или заявление о сдаче уроков.** Основание: [31-урочная матрица OTUS](../../IDEA_PLUS_V0_2/10_OTUS_01_31_TRACEABILITY_MATRIX.md).

| OTUS | Метод / книга | ГОСТ / подход | Документ SADEQ | Проверка |
|---|---|---|---|---|
| 01–03 требования/планирование | IDEA+, PM, BA, бизнес-анализ | ГОСТ Р 59793; 34.602 | DOC-001..011 | согласование задачи, BIA, acceptance |
| 04 HLD | Gough/Bryant/Auburn, C4 | 34.201, проектные документы | DOC-012..017 | C4 coverage, trust boundaries |
| 05 LLD | API-first, SEDA, алгоритмы | ЕСПД 19.402/19.701 | DOC-018..029 | инварианты, строгие contracts, ALG tests |
| 06 RAG | Suhas Pai, retrieval/reranking/GraphRAG | 34.201 + security addendum | DOC-032 | recall/groundedness/ACL |
| 07 Agents | Antonio Gulli, orchestration/tool use | 19.402 + проектные контрактные схемы | DOC-021/029/032 | replay, bounded loops, human gate |
| 08–10 ADR/review/technical debt | C4/ADR, SEDA | разработка и контроль изменений | DOC-016/023/052 | independent review, regression |
| 11–12 Integration & Data | Mastering API Architecture, event sourcing | 19.402/34.201 | DOC-025..030 | schema, BOLA, idempotency, outbox |
| 13–15 QA/security/observability | AI Engineering, OWASP, NIST | ГОСТ Р 56939; 34.603 | DOC-031/042..048 | adversarial evaluation, audit, SLO |
| 16–17 Sizing & inference | Suhas Pai, AI Engineering | НФТ в 34.602, ПМИ | DOC-034/048 | p95, tokens/s, peak VRAM |
| 18–20 CI/CD MLOps Production | DevSecOps, SLSA | ГОСТ Р 56939; ЕСПД | DOC-036..040/051 | SBOM, signatures, release/rollback |
| 21–24 HA/DR, K8s, EDA, high load | Kubernetes Patterns (точные разделы ещё проверить) | 34.602/34.603 | DOC-033..035/048 | restore, egress, RPO/RTO, p95 |
| 25–27 hybrid, tenant, privacy | Security design/architecture | 34.602; ГОСТ Р 56939 | DOC-009/030..035 | isolation, privacy, cloud exclusion |
| 28–31 FinOps, radar, governance, API | API as product, SEDA | 34.602 + project annexes | DOC-003/011/023/026/056 | measured TCO, model governance, API acceptance |

## Библиотека решений
`SRC-001 Mastering API Architecture`, `SRC-002 Suhas Pai`, `SRC-003 Agentic Design Patterns`, `SRC-004 Chip Huyen`, `SRC-005 Complex Multiagent`, `SRC-006 Kubernetes Patterns (точные страницы пока не подтверждены)`. Разделы/издание/страницы на уровне отдельного `ALG` должны быть подтверждены первоисточником.

## Отдельная таблица каждого задания
```yaml
otus_lesson: "05"
document_id: DOC-021
requirement_id: FR-01
component_id: B01
algorithm_id: ALG-01
source_id: SRC-001
threat_ids: [THR-011, THR-021]
test_ids: [NEG-SCHEMA-01]
result: NOT_RUN
approved_by: null
```

## Финальная оценка
Для итоговой защиты требуется не только наличие документа, но и measured quality, workload/cost, independent tests, deployment, risk treatment and signed evidence. Нормативная форма документа не доказывает выполнение продукта.
