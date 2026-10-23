# C4 Level 2 · Containers

```text
[Web UI]
   ↓
[API Gateway / FastAPI]
   ↓
[Policy & Orchestrator]
   ↓
[Retrieval Service] → [Vector / Search Store]
   ↓
[Context Builder]
   ↓
[Model Adapter]
   ↓
[Output Validator]
   ↓
[Response + Citations]

Side services:
[Ingestion Worker] → [Object Store] → [Index Builder]
[Telemetry SDK] → [Observability]
[Release Manifest] → [Registry]
```

## Containers

| Container | Responsibility | Data |
|---|---|---|
| Web UI | user interaction | question, answer, citations |
| API | request contract, auth context, trace | request metadata |
| Policy/Orchestrator | workflow + access/security policy | identity claims, routing |
| Retrieval | search authorized knowledge | query, doc IDs, scores |
| Context Builder | build bounded prompt context | selected chunks |
| Model Adapter | abstract model provider/runtime | prompt, generation |
| Output Validator | grounding/security/citation checks | draft + evidence |
| Ingestion | normalize source documents | source/version/chunks |
| Vector/Search Store | retrieval index | embeddings + metadata |
| Observability | metrics/logs/traces | telemetry |
