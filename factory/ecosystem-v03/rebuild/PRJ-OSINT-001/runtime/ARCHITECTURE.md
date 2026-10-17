# RB-OSINT-001 · FATHER runtime decomposition

The first rebuild deliberately preserves the reference technology profile: Python standard library + SQLite, offline, no collectors.

```text
father_osint_rebuild.service
        │
        ├── validation
        │   ├── category guard
        │   ├── title guard
        │   └── timezone guard
        │
        ├── url_normalizer
        │   ├── URL parse
        │   ├── tracking parameter filter
        │   └── canonical URL
        │
        ├── fingerprint
        │   └── SHA-256(category | normalized_url)
        │
        ├── storage
        │   ├── findings schema
        │   ├── dedup state
        │   └── audit_log
        │
        └── reporting
            ├── priority ordering
            ├── CASE formatting
            └── mandatory human-review disclaimer
```

## Boundary

This runtime does not add network collection, LLM calls, RAG, SecGraph, autonomous enforcement, or new scoring semantics. Those belong to the improvement phase after parity.

## Evidence

`RUN_PARITY.ps1` first runs the original repository tests, then the FATHER rebuild unit tests, then a side-by-side behavioral comparison. Generated evidence is written under `evidence/generated/` and is intentionally not committed automatically.
