# ADR-HLD-001 — HLD: modular core, explicit data ownership and independent control
**Status:** PROPOSED / pending architecture and security review.

## Context
The SADEQ wish list requires reusable agents for diverse data sources, event-based state, real GraphRAG, governed actions, independent qualification and strict offline deployment. Single desktop GPU and 32 GB RAM impose practical limits. Independently deployable microservices are not automatically warranted.

## Decision
Define B01–B08 as **logical functional blocks**; map them to C4 runtime containers CT-01..CT-10 only when justified by security, state ownership, GPU isolation, scaling or operational requirements. For MVP prefer a modular Python application for object/event/agent workflow with separate privileged policy, local storage and local AI serving, and logically separated/privileged independent POLYGON environment.
Persist objects/events/checkpoints in PostgreSQL; treat vector+graph indexes as derived projections. For strict offline, local LLM+embedding+rerank and no external inference.

## Reasons
Traceable ownership, controlled dependencies, fewer early distributed failure modes, independent security evaluation, later Kubernetes migration without semantic contract changes.

## Alternatives
A. Single Python script with unrestricted tools and SQLite: REJECT — lacks scoped privileges/independent QA.
B. One microservice per agent/component: HOLD — too costly/complex before traffic measurements.
C. Modular-first with explicit contracts, external persistence, separate policy and qualification: SELECTED FOR REVIEW.
D. Managed cloud model API: REJECT for OTUS offline scope; separate commercial architecture possible with explicit permission.

## Consequences and reevaluation triggers
UAA deploy boundary may change without changing interface semantics. Introduce separate services when real scale, tenant isolation or failure separation demands. Revisit after measured throughput, incident modelling and first customer pilot. No claim of deployment or performance.
