# ЭП-004 — Architecture Decision Records / альтернатива и обоснование
**Статус:** DECISIONS PROPOSED; measurements not performed. Each ADR must be signed/reviewed before freeze.

## ADR-EP-001 / P0 delivery architecture
**Context:** один AI operations workflow на персональной лаборатории 32GB RAM/RTX3060 12GB, требование on-prem/офлайн, быстрый E2E.
**Options:** A) modular FastAPI + independent UAG/qualification privileges and DB; B) 8–12 independently deployed microservices + message broker; C) single LLM script without policy/data boundaries.
**Decision proposal:** A. Avoid unnecessary latency/operations overhead until load or privilege separation requires process split. A still requires real authorization isolation; not a single model process approving itself.
**Evidence needed:** isolation/benchmark/restore tests. **Fallback:** extract modules into separate services if load/security requires.

## ADR-EP-002 / RAG phase
**Options:** vector/hybrid with Qdrant baseline; Neo4j graph for all queries from day one; lexical-only.
**Decision proposal:** P0 Qdrant + lexical/hybrid retrieval with source citations and ACL; P1 Neo4j relationship queries with controlled graph paths and paired comparison.
**Reason:** better delivery chance, avoid treating graph as unconditional quality improvement. **Limit:** final OTUS goal still requires real GraphRAG.

## ADR-EP-003 / agent orchestration
**Options:** deterministic one-shot rule tree; LangGraph stateful workflow; open-ended autonomous agent.
**Decision proposal:** LangGraph with typed states, checkpoint and bounded loops, deterministic policy/action boundary. **Evals:** task completion, harmful calls, recovery, telemetry.
**Rejected for P0:** unrestricted autonomous planner.

## ADR-EP-004 / inference & data location
**Options:** external commercial LLM API; local Ollama + pinned weights; private enterprise model service.
**Decision proposal:** local Ollama in P0; enterprise internal managed AI endpoint considered only at pilot under separate legal/security review. **Risk:** GPU saturation/quality and model licenses.
**Evidence:** no-egress test, benchmark across local candidates, Russian-language eval.

## ADR-EP-005 / integration
**Options:** direct DB write into ITSM; mock ITSM adapter + OpenAPI contract; enterprise vendor SDK.
**Decision proposal:** typed adapter via restricted API; never direct DB mutation; mock first. **Evidence:** contract tests, failure/retry/reconciliation.

## ADR-EP-006 / security qualification
**Options:** AI model self-assessment; developer tests only; separately governed POLYGON.
**Decision proposal:** independently administered examiner and holdout tests; no QUALIFIED without exact artifact/evidence hashes; human release approval.
**Evidence:** actor separation, denied candidate test access, invalidation after release-relevant changes.

## ADR-EP-007 / benchmark and market claims
**Options:** reuse vendor marketing percentages as our target; own paired benchmark on same corpus and rule set.
**Decision proposal:** paired baseline (manual + nonagent RAG) and measured success criteria; vendor numbers only qualitative context.
**Evidence:** dataset/metric definitions and reproducible test log.

## Status and owner
All ADRs are `PROPOSED`; no independent review, legal approval, customer signoff, real benchmark or qualification claimed. Method selection grounded in [SEDA](../PRODUCT_BASELINE_V1/ENGINEERING_ALGORITHM_V1/README.md).