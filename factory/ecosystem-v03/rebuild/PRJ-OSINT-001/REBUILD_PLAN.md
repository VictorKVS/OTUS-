# RB-OSINT-001 · Rebuild Plan

## Goal

Rebuild the existing `VictorKVS/OSINT_TRICOLOR` MVP inside FATHER from explicit components, then prove behavioral parity with the original before adding capabilities.

## Reference freeze

Reference artifacts:

- `README.md`
- `AGENT_SPEC.md`
- `agent.py`
- `tests/test_agent.py`
- `PROJECT_REPORT.md`
- `docs/ARCHITECTURE.md`

The current reference remains authoritative for parity. FATHER must adapt to the working agent; the working agent is not rewritten merely to fit the factory model.

## Phase 1 — Capture

Completed at design level:

- input/output contract captured;
- four existing golden behaviors captured;
- safety invariants captured;
- first decomposition into mechanism/block/assembly/part candidates.

Not yet claimed:

- tests have not been executed by the FATHER rebuild;
- no extracted component is certified;
- no parity result exists yet.

## Phase 2 — Extract

Extract implementation behind stable contracts:

```text
URL NORMALIZER
SIGNAL VALIDATOR
FINGERPRINT
STATE REGISTRY
DEDUP TRANSITION
AUDIT WRITER
REPORT BUILDER
```

The first rebuild should preserve simple Python + SQLite behavior. Do not introduce RAG, LLM, graph DB or network collectors during parity work.

## Phase 3 — Reassemble

Target v1:

```text
JSONL INPUT
   ↓
Signal Validator
   ↓
URL Normalizer
   ↓
Fingerprint
   ↓
State Registry
   ├── Dedup Transition
   └── Audit Writer
   ↓
Report Builder
   ↓
SQLite + Markdown OUTPUT
```

## Phase 4 — Parity gate

Run both implementations against the same synthetic fixtures.

Comparison:

| Capability | Reference | Rebuild | Gate |
|---|---|---|---|
| URL normalization | existing unit test | TBD | BLOCKED |
| dedup | existing unit test | TBD | BLOCKED |
| human-review disclaimer | existing unit test | TBD | BLOCKED |
| timezone rejection | existing unit test | TBD | BLOCKED |
| SQLite schema compatibility | source observed | TBD | BLOCKED |
| audit event compatibility | source observed | TBD | BLOCKED |
| report structure | source observed | TBD | BLOCKED |

No improvement work starts until the required parity checks pass.

## Phase 5 — Controlled improvements

Only after parity:

1. immutable evidence hash and custody metadata;
2. source adapters behind explicit permissions;
3. versioned scoring policy;
4. entity resolution;
5. SecGraph integration;
6. ALINA review queue;
7. Legal RAG;
8. observability/evaluation;
9. CI/CD and security gates.

Each improvement creates a new version and must be compared to the previous golden baseline.

## Result

The purpose of RB-OSINT-001 is not merely to refactor OSINT. It is to prove the FATHER manufacturing method itself.

If this cycle works, repeat it for the next already-working agent.
