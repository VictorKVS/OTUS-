# STEP 09 — Lesson 06: RAG patterns

Статус: **DONE v1**

## Цель

Нормализовать Lesson 06 по visual-first pipeline:

`SCHEMA → VISUAL → OTUS → ARCHITECT PRO → FATHER PRODUCTION → ARTIFACTS → EVIDENCE → TRACEABILITY → MATURITY`

## Фокус

- RAG architecture;
- indexing / chunking / embeddings;
- retrieval;
- vector database;
- query transformation / hybrid retrieval / reranking, если подтверждены материалами;
- grounding / citations;
- quality / evaluation;
- data freshness and provenance.

## Definition of Done

- фактические материалы Lesson 06 разобраны;
- инженерная схема создана;
- visual poster создан;
- detail manifest создан;
- production mapping проверен;
- evidence/GAP зафиксированы;
- status/maturity обновлены только по evidence.


## Source-derived result

Curriculum:

- RAG pipeline;
- reranking;
- hybrid search;
- Self-RAG;
- CRAG;
- Knowledge/Cache Augmented Generation;
- hybrid RAG with Vector DB + Knowledge Graph.

Notebook evidence:

- SentenceTransformer embeddings;
- FAISS vector retrieval;
- BM25 + vector hybrid retrieval;
- CrossEncoder reranking;
- context/prompt construction;
- knowledge update demo.

## Important evidence boundary

Notebook cells are saved without execution outputs. Therefore Lesson 06 is `draft / M1`, not `lab`.

Folder `lesson-06-c4-model` contains C4 materials and is not used as RAG evidence.

## Production mapping

- `FTH-KNW-001 · Knowledge Service`
- `FTH-RAG-001 · Retrieval Gateway`
- `FTH-KGR-001 · Knowledge Graph Service`
- `FTH-CTX-001 · Context Builder`
- `FTH-PRM-001 · Prompt Registry`

## Validation

- 5/5 capability IDs resolved;
- 8 artifacts;
- 7 evidence;
- 5 GAP;
- 8 traceability links;
- visual poster present.

Следующий шаг: **STEP 10 — Lesson 07: AI Agents & Multi-Agent Systems**.
