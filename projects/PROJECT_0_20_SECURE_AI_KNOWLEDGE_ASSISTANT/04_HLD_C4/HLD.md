# HLD Decisions

## Architectural style

Modular service architecture with replaceable blocks behind stable contracts.

## Control planes

| Plane | Purpose |
|---|---|
| Data/Knowledge | ingest, normalize, index, provenance |
| Runtime | query orchestration and model execution |
| Security | authz, PII, secrets, guardrails |
| Quality | golden set, eval, regression |
| Operations | metrics/logs/traces/SLO |
| Delivery | build, release manifest, GitOps, rollback |

## HLD invariants

1. Retrieval receives access context before search result is exposed.
2. Model adapter never decides authorization.
3. Citations come from retrieval evidence, not model free text.
4. Release manifest is immutable.
5. Stable release remains addressable during Canary.
6. Every request has a correlation/trace ID.
