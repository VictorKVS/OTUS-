# ARCH-GOV-001 — Связь бизнеса, моделей и архитектуры
## Единая архитектурная ось
`Business Capability → BPMN value stream → Use Case → PRD → C4 L1/L2 → C4 L3/L4 → Data/ER → DMN Policy → Sequence → Testing → Deployment → FinOps`.

## Основной поток данных UAA
Channels (docs/webhooks/db/sensors) → authenticate → validation → source identification → object resolution → immutable observation/event log → state projection → graph/vector retrieval → deterministic algorithms/model reasoning → policy gate → human approval where needed → tool execute or ABSTAIN → observe result → append feedback → independent evaluation.

## Architecture blocks
**Control plane:** identity, agent registry, LangGraph planner, policy engine, approval, trust, release admission.  
**Data plane:** document/object storage, PostgreSQL events/state, Qdrant vectors, Neo4j knowledge graph, local models, tools.  
**Qualification plane:** isolated evaluator / tests / signed evidence.  
**Operations plane:** OTel/metrics/alerts/backup/release.

## C4 and deployment deliverables
1. L1 context: owners, environments, authorized interfaces, data flow boundaries.
2. L2 containers: API gateway, planner, policy gateway, data servers, GPU and QA.
3. L3 components: channel adapter, normalization, entity resolver, event writer, graph retriever, forecast, tool adapter, feedback.
4. L4 source/typed contracts with input/output and negative cases.
5. Deployment 4 alternatives with DMZ/data/GPU/ops zones.
6. Sequence incl. DENY/APPROVAL/HUMAN_REJECT.
7. ER incl. tenant, source, observation, event, object, state, graph relation, action, approval, evidence and audit.

## Six security roles in business notations
BPMN swimlanes: risk owner & architect; threat modeling; development/DevSecOps; independent examiner; human approver; runtime policy; SOC/monitor. UML actors and DMN decision table linked from [security BA model](../IDEA_PLUS_V0_2/13_SECURITY_ROLES_BUSINESS_ANALYSIS.md).

## Quality gates
- G0 idea: verifiable business hypothesis
- G1 business: customer constraints and AS-IS benchmark
- G2 architecture: ADR review+security
- G3 offline stack: local model/graph/trace without egress
- G4 core functional: cross-channel object & replay
- G5 knowledge: real graph citations, measured retrieval quality
- G6 security: User B denied, prompt injection safe, trust scoped
- G7 qualification: independent suite pass and signature
- G8 finance/scale: 3-year scenario, benchmark, no invented numbers
- G9 release/pilot: human approval, field migration and rollback

## Critical verification
Risk HIGH + insufficient evidence ⇒ ABSTAIN. Prompt never expands ACL. Agent may not change own evaluation. Any rejected human approval ⇒ STOP. Cloud migration requires explicit reconsideration of strict airgap and contract/data sovereignty.
