# ADD-001 · Архитектура системы и контракты
## Системный контекст (C4 L1)
Снаружи: пользователь, корпоративные ERP/CRM/МИС, администратор ИБ, эксперт и оператор. Внутри: автономная SADEQ платформа с контролируемым импортом информации. Никакие внешние API моделей не допускаются.

## C4 L2 — Containers
- Frontend & API Gateway;
- Identity, Policy Enforcement Point, Tool Gateway;
- LangGraph Orchestrator / UAA Runtime;
- Agent Factory Registry & Qualification Service;
- Knowledge Ingestion + Retrieval;
- PostgreSQL (events, sessions, audit), Qdrant (embeddings), Neo4j (graph);
- Local LLM serving + local embedding/rerank;
- OTel collector, Jaeger, Prometheus/Grafana.

## C4 L3 — UAA components
ChannelAdapters → Parser/Normalizer → EntityResolver → EventWriter → StateReducer → EventDetector → GraphVectorRetriever → Planner/ForecastAlgorithms → PolicyCheck → ToolExecutor → EvidenceChecker → FeedbackRecorder.

## C4 L4 — типизированный контракт
```yaml
observation:
  observation_id: UUID
  source_id: string
  object_external_key: string
  event_time: datetime
  ingest_time: datetime
  payload: object
  provenance: source_ref
event:
  event_id: UUID
  object_id: UUID
  event_type: string
  observed_from: [observation_id]
  confidence: optional_float
action:
  action_id: UUID
  actor_identity: string
  tool_id: string
  object_id: UUID
  policy_decision: ALLOW|DENY|APPROVAL_REQUIRED
  idempotency_key: string
  audit_ref: string
```

## Deployment — физическая изоляция
DMZ: reverse proxy / API Gateway. Internal service zone: Orchestrator, Policy Service, Integration Gateway. Data zone: PostgreSQL/Qdrant/Neo4j/local object storage. GPU zone: local LLM serving. Secret store, observability zone, backups. Egress-deny defaults. Межсетевые правила по принципу least privilege. Secrets никогда не возвращаются агенту через prompt.

## Sequence — запрос
User → authentication → policy on object → input guardrails → orchestrator → Qdrant candidate retrieval (ACL prefilter) → Neo4j allowed graph traversal → reranker → model/algorithms → tool policy → optional human approval → execution / deny → evidence verification → output guardrails → response and audit. Failure branches fail closed.

## ER — данные
Tenant, Identity, Role, Permission, AgentProfile, Source, Document, Chunk, GraphNode, GraphEdge, Object, Observation, Event, StateSnapshot, Session, ActionProposal, Approval, Execution, Trace, AuditEntry, Feedback, QualificationEvidence. Graph edges inherit/validate classification and authorized traversal; logs and citations are also controlled information.

## Control Plane vs Data Plane
Control Plane owns identities, state transitions, planners, policy, action authorization and governance. Data Plane handles immutable events, document ingestion/storage, retrieval indexes and inference. No direct tool write via untrusted LLM output.

## Design concerns
GraphRAG is not a vector search renamed: it must follow relation graph paths and cite source chunks. Entity resolution cannot merge unrelated tenants. Event replay needs ordering, dedupe and idempotent side effects. Predictive computations must use reproducible algorithms and backtesting; LLM can explain but must not invent metrics. Continuous learning requires change approval and versioned data.
