# FATHER Rebuild Lab

## Purpose

FATHER grows by rebuilding proven agents, not by inventing a universal component graph in isolation.

Canonical loop:

```text
WORKING AGENT
  -> GOLDEN FREEZE
  -> DECOMPOSITION
  -> PART / ASSEMBLY / BLOCK / MECHANISM PASSPORTS
  -> REBUILD V1
  -> PARITY TEST
  -> DELTA REPORT
  -> CERTIFICATION
  -> CONTROLLED IMPROVEMENT
  -> NEW GOLDEN VERSION
```

## Rules

1. A working agent remains the reference until parity is demonstrated.
2. Existing source and tests are never silently rewritten to fit FATHER.
3. Every extracted component starts as CANDIDATE, not CERTIFIED.
4. Rebuild must pass the reference behavior contract before improvement work.
5. Improvement and parity are separate phases.
6. No evidence -> no promotion.
7. If a behavior is not covered by the current reference tests, record it as UNVERIFIED rather than assuming parity.

## First case

`PRJ-OSINT-001 / FATHER OSINT / OSINT_TRICOLOR`

Why first:
- real executable `agent.py`;
- real unit tests;
- explicit MVP input/output contract;
- SQLite state and audit trail;
- clear security boundary;
- existing architecture and documentation;
- already harvested into the FATHER ecosystem workspace.
