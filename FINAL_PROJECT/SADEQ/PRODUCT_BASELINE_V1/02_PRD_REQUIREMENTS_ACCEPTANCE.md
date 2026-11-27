# PRD-001 — Требования к продукту, границы и приемка
**Статус:** проектные критерии; владелец бизнес-риска должен утвердить.

## System actors
Business user, system integrator, data owner, security architect, human approver, independent examiner, operations/SOC, model maintainer, tenant administrator.

## Jobs and functional requirements
| ID | Требование | Evidence |
|---|---|---|
| FR-01 | 2+ независимых канала (API/document/event) | test intake contract |
| FR-02 | Нормализация времени/формата/источника; idempotency key | malformed/duplicate tests |
| FR-03 | Entity resolution: несколько сообщений об одном объекте | goldens same-object/different-object |
| FR-04 | Append-only event store, current state/replay | late-event and replay tests |
| FR-05 | GraphRAG retrieval через узлы/связи с source provenance | graph path + citation visible |
| FR-06 | LangGraph state machine, checkpoint, retry, human approval | state transition trace |
| FR-07 | Проверяемый прогноз отдельным алгоритмом | baseline/backtest and uncertainty |
| FR-08 | Политики ACL/tenant/action before tool execution | User B cannot retrieve User A secret |
| FR-09 | При неопределённости ABSTAIN и REVIEW_REQUIRED | synthetic conflicting claims |
| FR-10 | Feedback changes KB/curriculum only after independent approval | regression suite |
| FR-11 | Declarative agent profile, same core for 3 domains | diff demonstrates no core duplication |
| FR-12 | Agent 001 generates patch+tests from bounded spec | reviewer approval required |
| FR-13 | полный audit of decisions, source and version | trace source→state→action |
| FR-14 | fail-closed offline egress and model loading | packet capture/no cloud calls |
| FR-15 | qualification gates and revocation on change | expired qualification denial |
| FR-16 | metering of inference, storage and accepted results | dashboard, TCO link |

## NFR
Security: least privilege, immutable provenance where needed, encryption at rest/in transit as justified by threat model; Tenant boundaries graph/vector/log/cache. Performance: SLO after measurement, distinct API RPS vs LLM throughput; observe TTFT/p95/tokens/s. Reliability: RTO/RPO by BIA, backups and restore tests. Maintainability: typed APIs, ADR, reproducible dependencies, SBOM, signed releases. Data governance: provenance, deletion/retention by policy, PII minimization, object classifications.

## Scope excluded from MVP
Training base model weights; autonomous critical/lethal decisions; medical diagnosis; 20 independently qualified agents; geographic multi-cloud deployment; guaranteeing zero hallucinations; 10k full LLM RPS. Cloud compute is a future optional enterprise variant, not the air-gapped OTUS deployment.

## Product acceptance
No critical isolation failures in defined adversarial suite; independent examiner records result; raw observations traceable; rerun of test corpus reproducible; 3 contrasting profiles demonstrable; browser shows Neo4j graph, live traces, denied access; written SLO/cost benchmark with measured values.

## Change control
Any change to model, embedding, prompt, ontology, retrieval policy, action tools or permission scopes invalidates applicable qualification until regression.
