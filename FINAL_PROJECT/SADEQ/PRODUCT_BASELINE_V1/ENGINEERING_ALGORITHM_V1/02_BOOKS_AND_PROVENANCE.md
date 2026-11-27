# SOURCE-REG-001 — Библиотека инженерных источников SADEQ
## Verified source card registry (bibliographic details from available user library)
| SRC | Book | Confirmed material inspected | Application | Qualification caveat |
|---|---|---|---|---|
| SRC-001 | James Gough, Daniel Bryant, Matthew Auburn — *Mastering API Architecture: Design, Operate, and Evolve API-Based Systems* | Introduction: API-first/C4 Context, Container, Component; ADR. Ch.1: REST, OpenAPI specification, versioning, validation. Ch.2: Contract and component testing. | C4, contracts and API lifecycle | Edition in library includes early release; pinpoint page from actual edition before formal citation |
| SRC-002 | Suhas Pai — *Designing Large Language Model Applications: A Holistic Approach to LLMs*, O'Reilly, first edition 2025 | Ch.11 Embeddings; Ch.12 RAG pipeline (rewrite/retrieve/rerank), GraphRAG, cost/relationship extraction caveats. | B03 evidence and B04 retrieval architecture | Book discusses methods, not SADEQ-specific performance |
| SRC-003 | Antonio Gulli — *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems* | Ch.1 Prompt Chaining, Ch.2 Routing, Ch.3 Parallelization, Ch.4 Reflection, Ch.5 Tool Use, Ch.8 Memory; discussion of LangGraph and parallel workflow | B04 stateful orchestration, bounded tools, B06 agent patterns | Specific chosen algorithm still must pass independent benchmarks |
| SRC-004 | Chip Huyen — *AI Engineering: Building Applications with Foundation Models* | Inspected excerpt on direct/indirect prompt injection, attacks via tools and retrieved content | Security controls on RAG/tool use; evaluation process needs section-specific recheck | No claim full book or exact evaluation chapter read for this decision |
| SRC-005 | *Building Complex Multi-Agent Systems Using Pattern Prompting* | Appendix on Choreography and RAG Microarchitecture, discussion of event-based pipeline | Event-driven vs orchestration comparison | Need precise book edition/author section reference before formal approval |
| SRC-006 | Bilgin Ibryam, Roland Huß — *Kubernetes Patterns* | Named in prior course source registry; *not specifically re-opened for this package* | Deployment pattern research | UNVERIFIED details; no claims of particular named pattern or page |

## Literature card schema
```yaml
source_id: SRC-002
title: Designing Large Language Model Applications
authors: [Suhas Pai]
edition: "2025 first edition"
chapter: "12 Retrieval-Augmented Generation"
section: "GraphRAG"
page_or_locator: "REVERIFY_WITH_EDITION"
method_name: "graph-based retrieval with entity/relationship extraction"
assumptions:
  - data corpus has meaningful relationships
limitations:
  - initial graph indexing may be expensive
  - extracting relations is harder than extracting entities
what_book_supports: "method and cautions; not specific SADEQ implementation results"
our_application: "B03 Evidence retrieval"
evidence_required: ["graph-path citations", "relation quality check", "vector-only baseline", "index cost benchmark"]
status: SOURCE_TOPIC_VERIFIED
```

## Architectural source-of-truth split
**Book says:** method, mechanism, assumptions, known tradeoff.  
**SADEQ chooses:** our scenario, constraints, design variant, data ownership.  
**POLYGON proves:** whether selected approach works under our test data/SLO/risks.  
Never infer measured improvement just because a pattern is recommended by an author.
