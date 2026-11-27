# ЭП-005 — трассировка требований, алгоритмов, угроз и испытаний
**Статус:** DRAFT; all test evidence NOT_RUN.

## 1. Первая карта трассировки
| P0 Requirement | UC | Component(s) | Algorithm(s) | Threat family | Verification |
|---|---|---|---|---|---|
| FR-NEW-01/02 | UC001 | B01 | ALG-01 | spoofed source / malformed JSON | N-01, contract test |
| FR-NEW-03/04 | UC002/004 | B02 | ALG-02/03/04/05/06 | duplicate, cross-tenant merge, event corruption | N-02/N-08, replay |
| FR-NEW-05/06 | UC001 | B03 | ALG-07 | malicious docs/poisoning, source leak | citation and N-03/N-04 |
| FR-NEW-07/08 | UC002 | B04 | ALG-08/10 | unsafe proposal, runaway graph | loop bounds, typed draft |
| FR-NEW-09/10 | UC002/003 | B05 | ALG-11 | approval bypass, spoofed tenant | N-03/N-05/N-06 |
| FR-NEW-11 | UC002/004 | B05/B02 | ALG-12 | non-durable operation, ambiguous outcome | N-07; state check |
| FR-NEW-12 | UC005 | B08 | audit + events | untracked action, PII in trace | trace redaction review |
| FR-NEW-13 | UC005 | B07 | POLYGON | self-grant qualification | N-10/N-12 |
| FR-NEW-14 | UC005 | B08 | secure deployment | egress/remote LLM | N-11 + packet test |
| FR-NEW-15..18 | UC006..008 | B03/B06/B08 | GraphRAG / deploy | graph leakage, infra failure | P1 separately |

## 2. Quality gates for concept-to-implementation
**DG-01 (IDEA/TZ):** baseline scope, risk owner, acceptance definitions, no fictional KPIs.
**DG-02 (ЭП):** approved scenario, C4 context, trust boundaries, viable on-prem topology, all P0 linked to ALG/TEST.
**DG-03 (ТП):** final JSON Schemas/OpenAPI/ALG/data contracts, threat assignments, adversarial corpus, model decision ADR.
**DG-04 (Implementation):** code+build+SBOM+provenance, unit/contract/integration tests.
**DG-05 (Preliminary testing):** independent positive+negative+offline+recovery, evidence.
**DG-06 (Pilot readiness):** qualified version, approved users/document scope, rollback and SOC runbook.
**DG-07 (Customer acceptance):** formal tests and customer signatures only if actual engagement.

## 3. Independent evidence rules
Each actual evidence artifact requires `REQ/ALG/THR/TEST IDs, code commit, model digest, dataset SHA, policy revision, run ID, environment, expected vs actual, timestamp, reviewer`.
**No source files or tests executed by writing this document.**

## 4. Relationship to global analogs
[Benchmark memo](../IDEA_PLUS_REBASELINE_V03/08_WORLD_ANALOGS_AND_BENCHMARKS.md) offers definitions and hypotheses; independent vendor comparisons may only be claimed after paired test on identical task population and measurement definitions.

## 5. Next steps
Before full LLD: draft production-realistic synthetic corpus, freeze precise business event semantics, define policy role matrix, OpenAPI and Idempotency contracts, then create actual test fixtures.