# UAA-ALG-DETAILED-001 — операционные спецификации ALG-01…ALG-12
**Дата:** 2026-11-27 · **Статус:** DESIGN / NOT_IMPLEMENTED / NOT_TESTED / NOT_QUALIFIED

Этот документ детализирует [первую карту алгоритмов](02_ALGORITHMS_AND_CONTRACTS.md) для SADEQ UAA. Он отделяет детерминированные операции, LLM reasoning и обязательное независимое разрешение действий. Не трактовать эти 12 алгоритмов как исторические «12 правил FATHER».

## ALG-01 — Приём и проверка сообщения (B01)
**Назначение:** приём и проверка сообщения.
**Вход:** `source envelope + authenticated principal + schema registry`.
**Выход:** `ValidatedMessage | REJECT`.
**Действия (непосредственная операционная последовательность):**
1. authenticate principal and verify channel
2. look up schema by source/kind/version
3. reject unknown nested fields, invalid types, sizes and classification
4. check source, recipient and operation policy
5. emit validation receipt and redacted audit

**Негативная проверка / приёмка:** Forged sender/unknown field/unauthorized route -> REJECT before side effects.
**Security / threat mapping:** SEC-04; THR-011/012/021.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-02 — Дедупликация (B01/B02)
**Назначение:** дедупликация.
**Вход:** `validated event + trusted tenant/source context`.
**Выход:** `NEW | DUPLICATE(existing receipt) | CONFLICT`.
**Действия (непосредственная операционная последовательность):**
1. form key tenant/source/external_event_id
2. enforce DB unique constraint inside transaction (not SELECT-then-INSERT race)
3. compare canonical payload hash for conflicting replay
4. return existing receipt without duplicate event
5. preserve side-effect idempotency downstream

**Негативная проверка / приёмка:** 100 concurrent duplicates -> one event; same ID different payload -> conflict.
**Security / threat mapping:** SEC-03; THR-020/074.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-03 — Определение объекта (B02)
**Назначение:** определение объекта.
**Вход:** `normalized verified identity attributes + ACL`.
**Выход:** `ObjectID | CREATED | REVIEW_REQUIRED`.
**Действия (непосредственная операционная последовательность):**
1. normalize identifiers using approved source-specific canonicalization
2. exact match using tenant+namespace+external object ID
3. reject cross-tenant joins
4. register new object only when policy permits
5. ambiguous/fuzzy candidate requires independent review

**Негативная проверка / приёмка:** same ID in another tenant never merges; ambiguous match abstains.
**Security / threat mapping:** SEC-02; THR-016/073.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-04 — Регистрация события (B02)
**Назначение:** регистрация события.
**Вход:** `validated observation + object ID + provenance`.
**Выход:** `EventRef | atomic error`.
**Действия (непосредственная операционная последовательность):**
1. validate event type and domain invariants
2. store event_time and ingestion_time separately
3. transactionally insert append-only event and optional outbox record
4. enforce uniqueness and immutable provenance
5. ack only after durable commit

**Негативная проверка / приёмка:** transaction crash produces no partial state or duplicate side effect.
**Security / threat mapping:** SEC-03; THR-076/080.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-05 — Расчёт состояния (B02)
**Назначение:** расчёт состояния.
**Вход:** `canonical ordered events + previous state`.
**Выход:** `ObjectState(version) | CONFLICT`.
**Действия (непосредственная операционная последовательность):**
1. select ordering/correction policy per domain
2. apply pure reducer R(state,event)
3. persist version and event references
4. snapshot periodically with hash
5. replay event log and compare deterministic state

**Негативная проверка / приёмка:** replay after crash produces identical version/hash; late event follows explicit correction rule.
**Security / threat mapping:** SEC-05; THR-075/080.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-06 — Обнаружение изменения (B02)
**Назначение:** обнаружение изменения.
**Вход:** `previous state + new state + approved business rule`.
**Выход:** `BusinessTrigger | NO_ACTION`.
**Действия (непосредственная операционная последовательность):**
1. identify changed attributes
2. compute legal domain-specific delta or state transition
3. apply typed threshold, debounce/hysteresis where relevant
4. dedupe trigger by object/rule/state_version
5. publish only permitted trigger types

**Негативная проверка / приёмка:** exact boundary 9<10 true, 10<10 false; no repeated trigger on same state.
**Security / threat mapping:** SEC-05; THR-073/075.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-07 — Поиск доказательств (B03)
**Назначение:** поиск доказательств.
**Вход:** `authorized evidence query + object/state refs`.
**Выход:** `EvidenceBundle | ABSTAIN`.
**Действия (непосредственная операционная последовательность):**
1. scope tenant/object ACL before every retrieval
2. query lexical/vector indexes; optionally rewrite query
3. rerank candidates
4. traverse permitted graph paths and validate edge provenance
5. return source/version/path citations; reject unauthenticated/poisoned sources

**Негативная проверка / приёмка:** cross-tenant vector/graph retrieval denied; poisoned source never tool instruction.
**Security / threat mapping:** SEC-04/05; THR-031..040.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-08 — Гипотезы и объяснение (B04)
**Назначение:** гипотезы и объяснение.
**Вход:** `event + state + evidence bundle`.
**Выход:** `HypothesisSet with supported/contradicted/unresolved`.
**Действия (непосредственная операционная последовательность):**
1. separate facts from assumptions and unknowns
2. construct bounded candidate explanations
3. attach support/refutations/source provenance
4. check temporal and logical contradictions
5. mark unresolved when causality not established

**Негативная проверка / приёмка:** inventory decrease never proves theft/sales without independent evidence.
**Security / threat mapping:** SEC-05; THR-036/053.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-09 — Прогнозирование (условно) (B04)
**Назначение:** прогнозирование (условно).
**Вход:** `qualified time series + forecast task`.
**Выход:** `ForecastResult | NOT_AVAILABLE`.
**Действия (непосредственная операционная последовательность):**
1. specify target/horizon/units and data validity
2. establish naive baseline and time-based train/test split
3. compare fit methods only with sufficient history
4. run backtest, error and calibration checks
5. version model, uncertainty and test evidence

**Негативная проверка / приёмка:** 2 observations -> NOT_AVAILABLE; no future-data leakage; reproducible backtest.
**Security / threat mapping:** SEC-05; THR-053/058.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-10 — Выбор реакции (B04/B05)
**Назначение:** выбор реакции.
**Вход:** `state + evidence + available forecast + DMN policy`.
**Выход:** `ActionProposal | NO_ACTION | ABSTAIN | REVIEW_REQUIRED`.
**Действия (непосредственная операционная последовательность):**
1. enumerate allowed action types from registry
2. evaluate deterministic business decision table
3. require adequate evidence for consequential proposal
4. compute declared impact and approval policy
5. return typed proposal with provenance, never execute

**Негативная проверка / приёмка:** unknown rule/missing evidence -> ABSTAIN, not invented permission.
**Security / threat mapping:** SEC-01/04; THR-019/045.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-11 — Авторизация и исполнение (B05)
**Назначение:** авторизация и исполнение.
**Вход:** `typed proposal + user delegation + qualified agent + target state`.
**Выход:** `DENY | APPROVAL_REQUIRED | EXECUTED | EXECUTION_UNKNOWN`.
**Действия (непосредственная операционная последовательность):**
1. evaluate sender→agent→tool→object delegation and ACL
2. verify qualified version, scope, risk and tool allowlist
3. bind human approval to exact params/hash, target version and expiry
4. recheck all policy just before tool execution (TOCTOU)
5. idempotently call scoped tool and durably log receipt

**Негативная проверка / приёмка:** stale object/rights or self-approval blocked; unknown tool outcome not blind-retried.
**Security / threat mapping:** SEC-04; THR-016..030/047.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## ALG-12 — Проверка результата (B02/B05/B08)
**Назначение:** проверка результата.
**Вход:** `execution receipt + authoritative external state + expected postcondition`.
**Выход:** `VERIFIED | MISMATCH | PENDING | INCIDENT`.
**Действия (непосредственная операционная последовательность):**
1. query authoritative system independently of HTTP status
2. compare target identity, expected and actual postcondition
3. reconcile ambiguous remote execution via correlation/idempotency
4. append outcome event and immutable audit
5. allow feedback update only via independently approved knowledge change

**Негативная проверка / приёмка:** HTTP 200 without actual draft/order -> not VERIFIED; no blind retry.
**Security / threat mapping:** SEC-05/06; THR-050/091..100.
**Требование к API:** closed schema, typed result, explicit failure code, owner, version, source provenance, audit trace.
**Evidence:** `NOT_RUN` (до разработки и выполнения независимого теста).

## Исполнение AI / non-AI
- ALG-01/02/04/05/06: детерминированный код; ALG-03: baseline deterministic, AI only untrusted candidate.
- ALG-07: retrieval/reranking can use local embedding/rerank/LLM, but ACL + provenance outside LLM.
- ALG-08: LLM can generate candidate hypotheses; evidence/cause review independent.
- ALG-09: numeric forecast in reproducible code, LLM only explanation.
- ALG-10: deterministic DMN governs allowed proposals; LLM explanation untrusted.
- ALG-11: policy, approval, execution must be non-LLM and separately privileged.
- ALG-12: actual-state reconciliation deterministic; LLM may help explain incident.
- B06 Agent Factory and B07 Independent POLYGON are separate privileged product functions, not hidden sub-steps of one agent.

## Core flow
`VerifiedSource → 01 → 02 → 03 → 04 → 05 → 06 → [no action OR 07→08→09(optional)→10→11→12] → new outcome event → governed feedback`.

## Pre-implementation checklist
- Product/Business/System owner signs exact event semantics; stock count vs stock delta is not interchangeable.
- Register exact JSON Schema per source/kind/version, all nested unknown fields rejected, recipient and tool allowlists.
- Define `tenant_id` only from verified identity, not spoofable business-body field.
- Distinguish observed facts, inferred hypotheses, forecast confidence and policy.
- Recheck action hash/object state/TTL on human approval; return `EXECUTION_UNKNOWN` for ambiguous tool state, never blind repeat.
- Each `ALG` maps to `FR, SRC, CMP, FLOW, THR, TEST, EVIDENCE`, with actual version and independently executed POLYGON tests.
- No external model APIs; local/offline inference only for OTUS MVP.

## Literature provenance / not overclaiming
- Gough/Bryant/Auburn, *Mastering API Architecture*: C4, OpenAPI/ADR, contract test methodology.
- Suhas Pai, *Designing Large Language Model Applications*, Ch.11–12: embeddings, retrieval, GraphRAG, reranking (ALG-07).
- Antonio Gulli, *Agentic Design Patterns*, Ch.1–5, 8: routing, chaining, tools, memory (workflow orchestration).
- Exact entity resolution, event sourcing, causal inference, forecasting and DMN patterns require dedicated bibliographic cards and validation; this specification does not falsely attribute them to one of the books.
- [SEDA methodology](../ENGINEERING_ALGORITHM_V1/README.md) and [Threat matrix lifecycle](../SECURE_SDLC_TOP100_V1/THREAT_MATRIX_LIFECYCLE_POLICY.md).

**Next:** detailed ALG-01 strict schema and ALG-02 atomic idempotency + acceptance fixtures, before any blanket claim of an intelligent agent.
