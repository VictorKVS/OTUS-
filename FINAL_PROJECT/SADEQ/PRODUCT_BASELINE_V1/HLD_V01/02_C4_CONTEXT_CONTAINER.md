# HLD-C4-001 — Контекст и контейнеры (C4 L1/L2)
**Status:** proposed. **C4 convention:** system context explains external people/systems and scope; container describes independently runnable applications and stores, not Docker containers.

## C4 L1 — System Context
**System of interest:** SADEQ Platform + UAA + Agent Factory + Qualification Lab; internal offline deployment.
**Persons:** business user, data owner, human approver, security architect, independent examiner, operations/SOC, system administrator.
**External systems at trust boundary:** approved local ERP/CRM/MIS, document repository, event source, local identity directory. There is **no external LLM API** in the OTUS MVP.
**Interactions:** submit evidence, observe status/explanations, propose approved bounded action, qualify/revoke agent versions, import authorized reference data, obtain audit.

## C4 L2 — Logical container view and deployment candidates
| ID | Container | Responsibility | Candidate implementation / deployment | Important dependencies |
|---|---|---|---|---|
| CT-01 | API Edge + Web UI | user workflows, input checking, identity boundary | FastAPI+UI, stateless service | auth, policy, agent runtime |
| CT-02 | Integration & Tool Gateway | allowlisted input and output routing, connectors | internal service/module, hardened transport | policy, sources, tool contracts |
| CT-03 | UAA Application | orchestration, object/events workflow, evidence/decision proposal | initially modular Python application, LangGraph | DB, knowledge, local LLM, policy |
| CT-04 | Policy & Approval | deterministic authorization, human approval, trust state | independently privileged service | identity, audit, qualifier |
| CT-05 | Knowledge & Evidence | ingestion, citations, graph/vector retrieval, sanitization | worker/module with controlled DB access | Qdrant, Neo4j, object store |
| CT-06 | Factory/Agent Registry | versioned domain agent manifests, training plans, safe build requests | admin application/service | qualification, signed artifact registry |
| CT-07 | Independent Qualification | POLYGON adversarial suite, heldout sets, trust issuance recommendation | logically and privilege-separated process | immutable candidate, QA evidence |
| CT-08 | Persistent data | PostgreSQL objects/events/audit/checkpoints, Qdrant, Neo4j, object storage | separate data stores | backup/restore, ACL |
| CT-09 | Local AI Inference | local LLM, embedding, reranking, model manifest | dedicated GPU serving as needed | pinned model weights, local registry |
| CT-10 | Telemetry & Operations | metrics, logs, tracing, incidents, FinOps | OTel + metrics/log storage | all components (redacted) |

## Four planes
**Control:** CT-04, CT-06, critical release and action state.  
**Data:** CT-02, CT-03, CT-05, CT-08, CT-09.  
**Qualification:** CT-07 must not share candidate agent mutation privileges.  
**Operations:** CT-10; trace and audit are protected data.

## Decisions to postpone
Microservice vs modular monolith, Kafka vs PostgreSQL outbox, Qdrant+Neo4j capacity, model server runtime, GPU node count, API autoscale, DR SLA. These require benchmark or hard separation constraints. C4 diagrams show conceptual containers, **not deployed pods**.
