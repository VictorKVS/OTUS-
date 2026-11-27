# ALG-BUS-001 — двенадцать логических алгоритмов business agent
**Design only; not 12 historical rules of FATHER.** All state and input constraints are conceptual until machine-readable schema v0.2 is implemented.

| ALG | Owner block | Exact step | Input / output | Failure mode | Verification |
|---|---|---|---|---|---|
| ALG-01 Validate | B01 | authenticate principal, check tenant, `source_id + kind + schema_version`, closed fields, exact recipient allowlist | SourceMessage → ValidatedObservation | reject / no side effect | unknown field / forged sender |
| ALG-02 Dedupe | B01/B02 | atomically look up `source_id, external_event_id, tenant`, commit one receipt | ValidatedObservation → NEW or PREVIOUS_RECEIPT | bounded retry | duplicate replays no extra event |
| ALG-03 Entity resolve | B02 | normalize eligible verified ID, compare within tenant namespace, auto-link only exact certified mappings; fuzzy→human | Observation + identity scope → ObjectID or REVIEW | abstain, do not guess | same ID distinct tenants never merge |
| ALG-04 Event append | B02 | transactional append-only journal, unique event ID, source provenance, outbox | ObjectID, observation → EventRef | rollback on DB failure | restart and integrity test |
| ALG-05 State reducer | B02 | deterministic reducer with ordered version/event rule; replay snapshot and verify hash | Events → State(vN) | conflicting event → quarantine | replay equality |
| ALG-06 Change detector | B02 | `change = new_state - prev_state`; evaluate deterministic domain threshold and transition | State(vN-1,vN) → ChangeEvent or NO_OP | unknown rule → no action | threshold boundaries |
| ALG-07 Evidence retrieval | B03 | ACL prefilter → text/vector candidates → rerank → permitted graph traversal → cite nodes+paths | AuthorizedQuery → EvidenceBundle | missing provenance → ABSTAIN | cross tenant and poisoned source |
| ALG-08 Hypothesis analysis | B04 | generate multiple hypotheses from evidence; label each supported/contradicted/unknown, test causal assumptions | EvidenceBundle + state → HypothesisSet | no unsupported certainty | contradiction fixture |
| ALG-09 Forecast | B04 | choose domain baseline, fit/evaluate on time split, forecast + uncertainty, compare backtest | event series → ForecastResult | insufficient history → NOT_AVAILABLE | reproducibility and holdout |
| ALG-10 Business decision | B04/B05 | typed DMN decision table: determine recommended action from threshold, evidence, risk and policy preconditions | State + Evidence + Forecast → ActionProposal or ABSTAIN | missing rule → ABSTAIN | rule table coverage |
| ALG-11 Authorization | B05 | check principal and delegated scopes, object ACL, qualification version, impact and risk, human-bound action hash/TTL, TOCTOU | ActionProposal → DENY / APPROVAL_REQUIRED / ALLOW_BOUNDED; ActionReceipt | fail closed | stale approval + foreign object + expired grant |
| ALG-12 Outcome validation | B02/B05/B08 | tool receipt + query authoritative state, compare expected transition; append audit and human-reviewed feedback | ExecutionReceipt + ObservedState → VERIFIED / MISMATCH | escalation; no blind redo | mismatched receipt triggers incident |

## Four main contract types
1. `SourceMessage`: sender identity outside body, source, schema version, event ID, object external key, timestamp, exact payload schema.
2. `ObjectState`: tenant, object ID, version, event references, deterministic projection and provenance.
3. `EvidenceBundle`: allowed source chunks, graph paths, citations, confidence semantics, retrieval version; never carries authority to change ACL.
4. `ActionProposal`: business reason, exact tool operation/params hash, target object version, user delegation, required approval, validity window, qualified agent version, idempotency token.

## Executable semantics needed later
- `ALG-03`: equality key normalized only by approved source-specific canonicalization; human review cannot be bypassed.
- `ALG-05`: event-time ordering and corrections are **policy-dependent**; late events may require replay/reprojection, not arbitrary sorting.
- `ALG-06`: change detection only as defined by business domain; raw subtraction valid for stock count, not generic document states.
- `ALG-08`: explanation is not causal proof. Causal claims require interventions, controlled comparisons or stated assumptions as applicable.
- `ALG-09`: **no training/forecast** if there is insufficient sample; do not invent thresholds.
- `ALG-11`: human approval of recommendation is not execution without fresh scope check.
- `ALG-12`: external tool retries can create duplicate effects, use idempotency and reconciler.

## Mapping to books
- **Gough/Bryant/Auburn** — C4, ADR, API specification, contract tests; supports interface design but not the exact 12-step business algorithm.
- **Suhas Pai** — vector/retrieval/reranking/GraphRAG (ALG-07); does not prove our graph quality.
- **Antonio Gulli** — bounded chaining/routing/tools and memory for ALG-08/10/11 orchestration.
- **Chip Huyen** — evaluate AI applications, prompt risk literature; exact chapter references pending source card review.
For event sourcing, entity resolution, DMN, causal inference and forecasting algorithms, add independent sources rather than falsely attributing them to these books.

## Threats and source
[FATHER strict contract](https://github.com/VictorKVS/FATHER_CODEX/blob/main/docs/protocols/CONTRACT_STRICT_API_ALGORITHM_BOUND_DATA_FLOW_V1.md), [THR-001...100](../SECURE_SDLC_TOP100_V1/TOP_100_THREATS.md). Matched threat IDs and tests in [traceability](04_TRACEABILITY_AND_GATES.md).
