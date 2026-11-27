# SADEQ HLD v0.1 — Верхнеуровневое проектирование
**Дата:** 2026-11-27. **Статус:** PROPOSED / DESIGN ONLY / NO INTEGRATION TESTS.

## Исходные документы (не менять интерпретацию без ADR)
- [IDEA+ / FR-01...FR-14](../../IDEA_PLUS_V0_2/01_IDEA_CONTRACT.md)
- [Product PRD / FR-01...FR-16](../02_PRD_REQUIREMENTS_ACCEPTANCE.md)
- [Business analysis](../../IDEA_PLUS_V0_2/02_BUSINESS_ANALYSIS.md)
- [Architecture earlier baseline](../../IDEA_PLUS_V0_2/04_ARCHITECTURE.md)
- [Contract strict FATHER](https://github.com/VictorKVS/FATHER_CODEX/blob/main/docs/protocols/CONTRACT_STRICT_API_ALGORITHM_BOUND_DATA_FLOW_V1.md)
- [Threat matrix lifecycle from IDEA+](../SECURE_SDLC_TOP100_V1/THREAT_MATRIX_LIFECYCLE_POLICY.md)
- [Security roles and business notation](../../IDEA_PLUS_V0_2/13_SECURITY_ROLES_BUSINESS_ANALYSIS.md)

## Book-based method and exact provenance
A local library document **James Gough, Daniel Bryant, Matthew Auburn, _Mastering API Architecture: Design, Operate, and Evolve API-Based Systems_** was inspected. Its introductory material discusses C4 system context/container/component diagrams and ADRs; its first chapters cover API-first design, OpenAPI and contract testing. We use these explicitly identified ideas as the **method**, not as an assertion that the book designs SADEQ.
**Previously discussed C4 / Simon Brown** is also an established architecture modelling method; the exact edition of a Simon Brown book was *not* opened during this pass.
We do not assert a particular book is the user's intended exact title without confirmation; this is a grounded working basis based on an accessible book and former methodology. The content below is **SADEQ design**, not quoted from the book.

## Files / modeling order
1. [Wish list and constraints to architecture drivers](01_DRIVERS_AND_CONSTRAINTS.md).
2. [C4 Context and Container](02_C4_CONTEXT_CONTAINER.md).
3. [Block responsibility and interfaces](03_BLOCK_CATALOG.md).
4. [Functional traceability, risks and design gates](04_TRACEABILITY_AND_DECISIONS.md).
5. [C4 Context source](diagrams/c4_context.mmd), [C4 Container source](diagrams/c4_container.mmd).
6. [Data-flow with security boundaries](diagrams/data_flow.mmd).
7. [Initial architectural decision record](ADR-HLD-001.md).

## Critical truth condition
HLD block != microservice != Kubernetes Pod. We choose runtime separation only from evidence of independent scaling, failure isolation, security boundary, specific technology or organization ownership. First deployment may be a modular local monolith + separate stateful DB and local inference; Kubernetes is a *deployment option* after sizing.
