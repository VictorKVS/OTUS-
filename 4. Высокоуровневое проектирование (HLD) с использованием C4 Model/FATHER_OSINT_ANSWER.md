# OTUS Lesson 04 — FATHER OSINT Agent / HLD with C4

**Project:** `VictorKVS/OSINT_deepseek`  
**Status:** `CONDITIONAL_PASS / DOCUMENTATION NORMALIZATION`

Lesson 04 requires C1 Context and C2 Containers. We apply them to the existing OSINT Agent without changing code and without inventing Production infrastructure.

## C1 — System Context

```mermaid
flowchart LR
    REQ[Requester / Project] --> AN[Analyst]
    AN -->|ResearchTask| OS[FATHER OSINT Agent]
    OS --> EXT[External Information Sources]
    EXT -->|Material observations| OS
    OS -->|MaterialPackage + gaps/errors| AN
    AN --> REV[Socrates / Reviewer]
    REV -->|RESEARCH_MORE| AN
    REV -->|PASS| KG[Knowledge Gate — future]
```

## C2 — Logical Containers

```mermaid
flowchart LR
    EXT[External Sources] --> ACQ[Acquisition Boundary]
    ACQ --> ORCH[Research Orchestration]
    ORCH --> STORE[(Evidence Persistence)]
    ORCH --> CONTRACT[ResearchTask / Material / MaterialPackage]
    CONTRACT --> REVIEW[Analysis & Review Harness]
    REVIEW --> FUT[Knowledge Gate / KB — future]
```

## HLD drivers

- preserve provenance independent of payload reuse;
- bounded research and visible stop conditions;
- partial collector failure isolation;
- source/transport replaceability;
- external content treated as untrusted;
- model output never replaces source evidence;
- collection, analysis, review and knowledge promotion remain separate responsibilities;
- DEV and Production scopes remain explicit.

## Deliberately not selected here

- database engine;
- queue/broker;
- vector DB;
- LLM provider;
- Kubernetes/VM/bare-metal deployment;
- Production topology.

Those require downstream NFRs, PoC/measurements and ADR.

## UNKNOWN

Production deployment, SLO/workload, legal/data boundary, LLM provider set and final Knowledge Gate deployment boundary remain open.

## What should be improved

| Priority | Improvement |
|---|---|
| P1 | create one canonical C4-as-code source and render all views from it |
| P1 | trace NFR/quality scenarios directly into architecture drivers |
| P1 | reuse stable trust-boundary IDs in Threat Model |
| P2 | render C1/C2 in the FATHER project site from the same source |

Detailed project pack: `OSINT_deepseek/docs/course_live_reproduction/04_hld_c4/`.

This OTUS file is a course mirror; `OSINT_deepseek` remains the source of truth.
