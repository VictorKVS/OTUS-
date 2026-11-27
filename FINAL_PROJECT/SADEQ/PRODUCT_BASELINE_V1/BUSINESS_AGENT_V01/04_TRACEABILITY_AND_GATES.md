# QUAL-BUS-001 — требования / этапы / угрозы / тесты / доказательства
| ALG | Requirements | Block | Threat register references | Qualification test | Status |
|---|---|---|---|---|---|
| ALG-01 | FR-01, FR-02 | B01 | THR-011, THR-012, THR-021 | NEG-SCHEMA-01 forged/extra | NOT_RUN |
| ALG-02 | FR-02, FR-04 | B01/B02 | THR-020, THR-074 | NEG-DEDUPE-02 duplicate event | NOT_RUN |
| ALG-03 | FR-03 | B02 | THR-016, THR-073 | NEG-ER-03 foreign tenant/ambiguous | NOT_RUN |
| ALG-04 | FR-04, FR-13 | B02 | THR-076, THR-080 | EVT-APPEND-04 crash/consistency | NOT_RUN |
| ALG-05 | FR-04 | B02 | THR-075, THR-080 | STATE-REPLAY-05 hash equality | NOT_RUN |
| ALG-06 | FR-07 | B02 | THR-073, THR-075 | CHANGE-BOUND-06 threshold | NOT_RUN |
| ALG-07 | FR-05, FR-08 | B03 | THR-031–040 | RAG-ACL-07 poisoning/retrieval | NOT_RUN |
| ALG-08 | FR-09 | B04 | THR-036, THR-053 | HYP-EVIDENCE-08 contradiction | NOT_RUN |
| ALG-09 | FR-07 | B04 | THR-053, THR-058 | FORECAST-09 baseline/holdout | NOT_RUN |
| ALG-10 | FR-07, FR-09 | B04/B05 | THR-019, THR-045 | DMN-DECISION-10 negative rule | NOT_RUN |
| ALG-11 | FR-08, FR-15 | B05 | THR-016–030, THR-047 | POLICY-RECHECK-11 approval stale | NOT_RUN |
| ALG-12 | FR-13, FR-16 | B02/B05/B08 | THR-050, THR-091–100 | VERIFY-RESULT-12 mismatched receipt | NOT_RUN |

**Requirement mapping note:** PRD FR-07 forecast, FR-09 ABSTAIN, FR-13 audit; at detailed LLD each ID must reference exact PRD revision and not conflate similarly numbered IDEA+ FR IDs. Above is preliminary and needs SA review.

## Acceptance gates
- G-BPM-01: business process actor, start/end, decision ownership reviewed by BA and data owner.
- G-BPM-02: each ALG has input/output state, failure and owner.
- G-BPM-03: each flow has exact sender/receiver/source and security boundary.
- G-BPM-04: threshold/example records and reference dataset accepted as synthetic fixtures.
- G-BPM-05: POLYGON executes negative and integration tests against exact build.
- G-BPM-06: real qualified release requires deployment tests and human approval.

## Open questions / risk of overdesign
A) Whether observation is an absolute stock count or a delta. B) Multi-source trust policy and conflict resolution. C) Approval authority for action types. D) Minimum viable knowledge source & graph path for stock case. E) Event ordering and time clocks. All must be decided before production implementation.

## Next design step
Refine B01→B02 `SourceMessage/ValidatedObservation` in a closed JSON Schema, create business DMN decision table and BPMN 2.0 XML with graphical DI if visual model exchange is needed, then implement one happy path plus negative tests; no assertion of completed behavior yet.
