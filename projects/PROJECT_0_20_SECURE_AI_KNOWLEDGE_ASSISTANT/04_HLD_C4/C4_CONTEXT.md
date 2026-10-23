# C4 Level 1 · System Context

Lesson 4 requires C1/C2. This file is the textual source of truth for C1.

```text
[Employee]
    |
    | asks question / receives cited answer
    v
[Secure AI Knowledge Assistant]
    |
    +--> [Corporate Knowledge Sources]
    |
    +--> [Identity / Access Provider]
    |
    +--> [Model Provider / Local Model Runtime]
    |
    +--> [Observability Platform]
    |
    +--> [Artifact / Model Registry]
```

## External relationships

| External system/person | Flow | Trust concern |
|---|---|---|
| Employee | question/answer | identity, authorization |
| Knowledge Sources | documents/metadata | provenance, freshness |
| Identity Provider | subject/roles/claims | authn/authz |
| Model Runtime | context/request → generation | data boundary |
| Observability | metrics/logs/traces | sensitive-log control |
| Registry | artifacts/versions | immutability/integrity |
