# SEDA-001 — 12-ступенчатый алгоритм инженерного решения
**Статус:** DESIGN REGULATION (процедура SADEQ, не «12 исторических правил FATHER» и не Twelve-Factor App).

## Вход
`idea_id, business_goal, approved_business_requirements, functional_requirements, NFR, constraints, prohibited_behaviors, source_rights, assets, preliminary_threats, available_resources, evidence_requirements`.

## Процедура
| Шаг | Ответственный | Алгоритмическая операция | Артефакт | Gate |
|---|---|---|---|---|
| 01 Problem definition | PM+BA+SA | выделить один сценарий, требуемый результат, наблюдаемый критерий успеха и отрицательные кейсы | TASK-XXX, BUS/FR/NFR | no measurable outcome → RETURN |
| 02 Requirements and constraints | SA+SEC-01 | классифицировать hard constraints, quality attributes, неизвестные, границы данных | Requirement/Constraint matrix | contradictions → ESCALATE |
| 03 Decomposition | Architect | определить обязанности и owner каждого логического блока; C4 Context/Container; доверенные границы | C4 L1/L2, block map | overlapping source of truth → REWORK |
| 04 Knowledge retrieval | ALINA Knowledge Architect | искать известные алгоритмы и паттерны по предмету; точное издание/глава/section/page, source ID, критерии применимости | SOURCE/ALG/PAT cards | no verified source → RESEARCH |
| 05 Alternative generation | Architect+Engineer | собрать минимум baseline и 1 альтернативу; готовое переиспользование отдельно от собственной реализации | Alternatives register | only one untested option → RESEARCH |
| 06 Suitability filter | SEC+Architect | удалить варианты, нарушающие жёсткие ограничения offline/ACL/rights/safety/VRAM or correctness | Hard constraint matrix | violated HC → REJECT |
| 07 Comparative evaluation | Architect+FinOps+QA | испытать оставшиеся варианты на одном датасете; correctness, p95, throughput, cost, complexity; неизвестные = NOT_MEASURED | Weighted choice score + experiment | missing performance evidence → PROVISIONAL |
| 08 Architecture & ADR | Architect | принять/отложить решение с причиной; C4 L3, component responsibilities, algorithm/pattern IDs | ADR + C4 L3 | security reviewer objection → REWORK |
| 09 Contract definition | SA+SEC | входные/выходные JSON schemas, permitted sender/receiver, state transitions, exception/retry/idempotency, semantically safe behavior | CMP/ALG/FLOW/DATA/SEC contracts | unknown fields/recipient → BLOCK |
| 10 Controlled implementation | Engineer Agent + human | reuse-first code, no additional undocumented flow, pinned dependencies, signed commits, test coverage | source+SHA/SBOM+tests | unapproved scope / supply chain → REWORK |
| 11 Qualification | POLYGON SEC-05 | execute functional, adversarial, cross-tenant, failure, load and end-to-end tests against exact version/environment | evidence ledger + independent report | failed P0 → NOT_QUALIFIED |
| 12 Release & feedback | Human release owner + SEC-06 | approve qualified artifact, rollout/rollback, observe metrics and reopen on drift/change | signed release, monitoring, change request | no sign-off / changed artifact → DENY |

## Decision state machine
`DRAFT → PROBLEM_DEFINED → SOURCES_VERIFIED → ALTERNATIVES_EVALUATED → ADR_PROPOSED → CONTRACTS_APPROVED → IMPLEMENTED → TESTED → QUALIFIED → HUMAN_APPROVED → DEPLOYED`; branches `RESEARCH`, `REWORK`, `BLOCKED`, `REVOKED`.
Neither LLM nor agent can change its own exam criteria, threat priority, scope or permissions.

## Fundamental rules
1. **Source provenance:** exact book, authors, edition/year and locatable chapter/section or document URL. A reference is not a proof of our implementation.
2. **Known technique first:** baseline and alternatives; invent new only if sources or tests cannot satisfy requirement, with ADR.
3. **Hard constraints before scores:** no option with forbidden cloud API or cross-tenant leak can win by speed/cost.
4. **Safe unknowns:** lacking benchmark/requirements, mark `NOT_MEASURED`; perform bounded experiment, don't invent numbers.
5. **No algorithm by prompt only:** LLM can propose/describe; safety-critical access decisions, integrity, idempotency and numerical forecasts require verified deterministic code and relevant tests.
6. **Qualification is integrated:** tests per ALG, CMP, FLOW, API and deployment, not only after coding.

## SEDA step output contract
```yaml
decision_id: ADR-XXX
business_requirement: BUS-XXX
functional_requirement: FR-XXX
candidate_algorithm_ids: [ALG-001, ALG-002]
source_refs: [SRC-001]
candidate_pattern_ids: [PAT-001]
hard_constraints: [HC-01, HC-02]
metrics_expected: [accuracy, p95, cost_per_accepted_result]
benchmark_results: NOT_RUN
decision: PROVISIONAL
risk_ids: [THR-011]
contract_ids: [CMP-001, FLOW-001]
test_ids: [TEST-001]
evidence_refs: []
human_owner: TBD
```

## Verification
A component's public label may be `PROTOTYPE`, `TESTED`, `QUALIFIED` only when supporting level is demonstrated; `DESIGN` is not equivalent. Every step records reason for REJECT and tradeoffs. Risk matrix grows from IDEA+ and is reviewed again at change/release.
