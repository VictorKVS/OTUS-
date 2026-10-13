# Release Strategy — Canary

## Цель

Снизить blast radius нового AI-релиза, сохраняя предыдущую stable-версию доступной до полного promotion.

## State machine

```text
CANDIDATE_READY
→ STAGING_VALIDATED
→ CANARY_1
→ CANARY_5
→ CANARY_100
→ PROMOTED
```

Любой blocking failure:

```text
CANARY_* → ROLLBACK → STABLE_RESTORED → RCA
```

## Traffic policy

- 0%: candidate deployed but receives only synthetic/smoke traffic;
- 1%: first production exposure;
- 5%: expanded exposure after gate;
- 100%: full promotion after successful gate.

## Gate classes

- technical: availability, errors, latency;
- AI quality: task success, faithfulness/groundedness;
- security: leakage, secrets, unsafe output;
- economics: cost/request;
- operational: saturation, crash loops, dependency failures.

## Example project thresholds

These thresholds are design assumptions for this homework and are configuration-driven:

- p95 latency regression: <= 20% vs stable;
- AI quality relative degradation: <= 5%;
- cost/request regression: <= 20% unless approved;
- critical security/data-leak findings: 0.

Error-rate threshold should be tied to the service SLO and stable baseline rather than hard-coded globally.

## Rollback

Rollback is traffic-first:

1. send 100% traffic to stable;
2. stop candidate progression;
3. mark candidate FAILED;
4. revert desired deployment state to previous release manifest;
5. keep evidence and telemetry;
6. open RCA;
7. fix and issue a new candidate version.

No rebuild of the previous version is required because the stable release uses immutable references.
