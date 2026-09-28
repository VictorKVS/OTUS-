# Visual Reference Library — OTUS / Interview Preparation Lab

## Цель

Собрать источники, из которых можно брать архитектурные идеи, структуру документов, алгоритмы/pipeline, способы визуализации и терминологию.

## Правило использования

1. `REUSE_OK` — переиспользование/адаптация только при соблюдении лицензии и атрибуции.
2. `REDRAW` — изучаем содержание и строим собственную схему; исходную картинку не копируем.
3. `INSPIRE` — только визуальное/структурное вдохновение.
4. Внешняя схема получает source, license/status, retrieved_at, adapted=true/false.
5. Алгоритм/идею реализуем самостоятельно; текст/иллюстрации/screenshots копируем только при явном праве.

## P0 — базовые источники

### NIST AI RMF Playbook
https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook
- Брать: Govern / Map / Measure / Manage, risk workflow, trustworthiness, governance/evidence mapping.
- Визуализировать: risk lifecycle, functions map, control/evidence cards.
- Статус: REUSE_OK_WITH_CREDIT; проверять отдельные third-party/copyrighted элементы.

### OWASP GenAI Security Project
https://genai.owasp.org/llm-top-10/
- Брать: Prompt Injection, Sensitive Information Disclosure, Excessive Agency, Vector/Embedding Weaknesses, mitigations.
- Визуализировать: attack → trust boundary → control → evidence; risk cards; threat matrix.
- Статус: CC/open documentation; проверять конкретный project LICENSE.

### OWASP Agentic AI — Threats and Mitigations
https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/
- Брать: agent threats, autonomy, tool misuse, identity/privilege, mitigations.
- Визуализировать: Agent → Tool → Identity → External System; trust boundaries; approval gates.

### MITRE ATLAS
https://atlas.mitre.org/
- Брать: AI attack tactics, techniques, mitigations, case studies.
- Визуализировать: attack matrix, technique cards, threat-to-control mapping.
- Статус: REDRAW/CITE; лицензию data/artifacts проверять отдельно.

### Google Cloud Architecture Center — RAG
https://docs.cloud.google.com/architecture/rag-reference-architectures
- Брать: ingestion/serving split, vector search, GraphRAG, CI/CD for RAG, managed vs custom deployment.
- Визуализировать: production RAG; ingestion vs serving; evaluation subsystem.
- Статус: CC BY 4.0 там, где это указано на странице; code samples обычно Apache 2.0.

### Microsoft Azure Architecture Center — AI / RAG
https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ai-overview
- Брать: RAG as architecture pattern, context engineering, enterprise patterns.
- Статус: REDRAW/CITE unless page/asset explicitly allows reuse.

### AWS Generative AI Application Builder — Architecture
https://docs.aws.amazon.com/solutions/latest/generative-ai-application-builder-on-aws/architecture-overview.html
- Брать: deployment dashboard, text use case, agent use case, reference deployment patterns.
- Статус: REDRAW/CITE; AWS assets/icons only under AWS terms.

## P0 — Agents / MCP / orchestration

### Anthropic — Building Effective AI Agents
https://resources.anthropic.com/building-effective-ai-agents
- Брать: workflow vs agent, sequential/parallel/evaluator-optimizer, single-agent vs multi-agent.
- Статус: INSPIRE/REDRAW.

### Hugging Face — AI Agents Course
https://huggingface.co/learn/agents-course/
- Брать: Think → Act → Observe, tools/actions, frameworks, agentic RAG, observability/evaluation.
- Статус: REDRAW/CITE unless asset license explicitly allows reuse.

### LangChain / LangGraph Learn
https://docs.langchain.com/oss/python/learn
- Брать: semantic search, RAG agents, SQL agents, subagents, handoffs, routers, memory, context engineering.
- Визуализировать: graph/state workflow, router, subagent patterns.

### Model Context Protocol — Official Spec
https://modelcontextprotocol.io/specification/draft/server/index
- Брать: Prompts / Resources / Tools, client/server boundaries, capability negotiation.
- Визуализировать: Host → Client → MCP Server → Tool/Resource.

## P0 — Retrieval / Search / GraphRAG

### Qdrant — Hybrid Search with Reranking
https://qdrant.tech/documentation/tutorials-basics/reranking-hybrid-search/
- Брать: dense + sparse + late interaction, retrieval/reranking stages.
- Визуализировать: ingestion triple-embedding pipeline; query fan-out; reranker.

### Weaviate — Hybrid Search
https://weaviate.io/developers/weaviate/concepts/search/hybrid-search
- Брать: vector + BM25, fusion, alpha weighting, thresholds.
- Визуализировать: parallel retrieval + fusion.

### Pinecone — RAG Series
https://www.pinecone.io/learn/series/rag/
- Брать: rerankers, embeddings, retrieval patterns, metrics-driven agent development.

### Neo4j — GraphRAG Developer Guide
https://neo4j.com/developer/genai-ecosystem/
- Брать: entity/relation graph, graph builder, GraphRAG retrieval patterns.
- Визуализировать: knowledge graph, vector+graph retrieval, entity expansion.

## P1 — Evaluation / Observability

### Arize Phoenix
https://arize.com/docs/phoenix/
- Брать: traces/spans, prompt playground, datasets, experiments, deterministic + LLM evals.
- Визуализировать: trace waterfall, evaluation dashboard, span tree.
- Статус: INSPIRE/REDRAW; screenshots only if allowed.

## P1 — визуальный стандарт

### C4 Model
https://c4model.com/
- Брать: Context → Container → Component → Deployment/Dynamic; legends, scope, zoom levels.
- Статус: INSPIRE/REDRAW with our own model.

### Structurizr
https://docs.structurizr.com/
- Брать: models-as-code, interactive diagrams, perspectives, docs+diagrams integration.

### Mermaid Architecture Diagrams
https://mermaid.js.org/syntax/architecture
- Брать: architecture-as-code, flowchart, sequence, state, ER.

### ByteByteGo
https://bytebytego.com/guides/a-cheat-sheet-for-system-designs/
- Брать: визуальная плотность, карточки, system-design storytelling.
- Статус: INSPIRE ONLY; изображения не копировать без отдельного права.

## Как переносим в OTUS site

`Source concepts → Normalize terminology → Extract algorithm/pattern → Map to capability IDs → Redraw in our notation → Add source/license → Add interview questions → Add evidence`

### Первые 10 poster-схем

1. Production RAG: Ingestion vs Serving vs Evaluation.
2. Hybrid Search: Dense + Sparse → Fusion → Rerank.
3. GraphRAG: Entity extraction → Graph → Hybrid retrieval → Context.
4. Agent patterns: Sequential / Parallel / Router / Evaluator-Optimizer.
5. Agent Security Boundary: Identity → Policy → Tools → Approval → Audit.
6. MCP: Host → Client → Server → Tools/Resources.
7. LLM Evaluation: Dataset → Run → Traces → Metrics → Regression Gate.
8. Secure RAG: Identity → ACL filter → Retrieval → Context → LLM.
9. Security Requirements: Source → REQ → Applicability → Control → Evidence.
10. C4 zoom: Context → Container → Component → Deployment.

## Литература — второй приоритет

- Martin Kleppmann — Designing Data-Intensive Applications.
- Chip Huyen — AI Engineering.
- Chip Huyen — Designing Machine Learning Systems.
- Mark Richards, Neal Ford — Fundamentals of Software Architecture.
- Neal Ford et al. — Software Architecture: The Hard Parts.
- Adam Shostack — Threat Modeling: Designing for Security.
- Ross Anderson — Security Engineering.

Книги используем для концепций и терминологии; графику на сайте строим заново.