# Rollback Plan

Trigger rollback on any blocking gate failure during Canary.

## Immediate action

```text
CANDIDATE FAILURE
→ route 100% traffic to STABLE
→ stop progression
→ restore previous desired state
→ verify stable health
```

## Evidence retained

- release id;
- app image digest;
- model version/digest;
- RAG index version;
- telemetry window;
- failed gates;
- security events;
- deployment diff;
- rollback timestamp.

## Follow-up

```text
FAILURE
→ INCIDENT / RCA
→ REQUIREMENT/RISK/ADR UPDATE when necessary
→ FIX
→ NEW IMMUTABLE CANDIDATE
→ FULL PIPELINE AGAIN
```
