# SEDA-EXAMPLE-001 — Применение к B01/B02: идентификация объекта
**Purpose:** demonstrate the procedure without claiming running implementation.

## BUSINESS task
From two independent authorized channels (REST inventory update + imported signed file) determine whether observations refer to one or two business objects, record exactly one canonical identity per genuine object, and recover state from ordered event journal. **Do not merge different tenants even when external IDs coincide.**

## Requirements, risks, constraints
- IDEA FR-01/02/03, PRD FR-01/03/04/08; HC-01/02/04; THR-016 (BOLA), THR-073 (incorrect object merge), THR-074 (duplicate delivery), THR-075 (late event), THR-011/012 (unexpected fields).
- B01 cannot establish canonical object identity and B02 cannot invoke external tool actions.

## Identify candidate algorithms
1. **ALG-ER-001** (baseline): `tenant_id + source namespace + canonical external ID` dictionary lookup using normalized verified keys; deterministic exact match. This is the proposed SADEQ baseline from common database/key techniques, **not represented as a quotation from an inspected book**.
2. **ALG-ER-002** (research): blocking + fuzzy name/attributes match with thresholds and an explicit human review interval. Needs primary literature reference and experiment; **not adopted without evidence**.
3. **ALG-STATE-001**: immutable observations/events, deterministic state reducer with event-time and replay, idempotent acknowledgement; proposed engineering choice subject to test.

## FATHER Contract-Strict draft FLOW-01
```yaml
flow_id: FLOW-01
from: B01
to: B02
message_type: ValidatedStockObservationV1
algorithm_id: ALG-ER-001
required_fields:
  - source_id
  - external_key
  - observed_at
  - stock_count
  - provenance_ref
  - trace_id
identity_context: "trusted verified principal and tenant scope; not freeform request body"
unknown_fields: REJECT
permission: observations.write
on_ambiguous_match: REVIEW_REQUIRED
side_effects: append_observation_only
```

### Example: external source payload
```json
{
  "source_id": "inventory-service",
  "external_key": "sku-25",
  "observed_at": "2026-11-27T14:00:00Z",
  "stock_count": 9,
  "provenance_ref": "SOURCE-001",
  "trace_id": "TRACE-001"
}
```
Fields are illustrative; final API should use signed source context and rigorously typed date/quantity. An unknown `export_all_documents` property or `tenant_id` injected into body is rejected. Distinct tenant identities cannot be merged.

## Flow and test
`SourceA → B01 validate→B02 resolve→append immutable event→state projection`. Then `SourceB → same authorized key→same object`; `SourceC same name but different tenant→separate object or deny`.
**Test matrix:** unknown nested property rejected; same event id duplicate no second action; out-of-order event yields deterministic state; unauthorized cross-tenant access DENY; ambiguous fuzzy match REVIEW_REQUIRED, not auto-merge; authorized event replay yields same state hash.

## Book-based method without overclaim
Gough/Bryant/Auburn informs C4 and API contract process. Suhas Pai and Antonio Gulli will inform retrieval/agent workflow when B03/B04 enter the flow, but **do not specifically validate exact matching algorithm**. This requires separate literature card or engineering benchmark. The decision remains `PROVISIONAL`.

## What next
1. Freeze exact business semantics: stock count vs delta, event ordering/conflicts, source trust.
2. Verify identity assumptions and tenant delegation model.
3. Write strict JSON Schema, schemas for all allowed event kinds and security policy.
4. Run ALG-ER-001 vs candidate match alternatives on 50+ labelled object cases (target sample to design, not observed).
5. Submit evidence to POLYGON before calling this implementation ready.
