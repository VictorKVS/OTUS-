# C2 Container Diagram — OSINT / Due Diligence AI Platform

```mermaid
flowchart LR
    U[Analyst / User]
    FE[Frontend\nReact/TypeScript]
    BE[Backend / Case Service\nFastAPI]
    AI[AI Service\nKnowledge & Recommendation Agent]
    VDB[(Vector DB\npgvector / vector index)]
    SQL[(SQL DB\nPostgreSQL)]
    EV[(Evidence Vault\nObject Storage)]
    EXT[External OSINT Sources\nRegistries / Sanctions / Web]

    U -->|HTTPS| FE
    FE -->|REST/JSON| BE
    BE -->|POST /get_recommendation| AI
    BE -->|CRUD cases, jobs, sources| SQL
    AI -->|retrieve context| VDB
    AI -->|read structured case data| SQL
    AI -->|read evidence lineage| EV
    BE -->|capture / source metadata| EV
    BE -->|controlled collection requests| EXT
    EXT -->|public data / documents| BE
    AI -->|recommendation + evidence refs| BE
    BE -->|response| FE
    FE -->|view recommendation| U
```

## Containers

| Container | Responsibility | Technology |
|---|---|---|
| Frontend | analyst workspace, case view, recommendation UI | React / TypeScript |
| Backend / Case Service | case orchestration, policy, source registry, API gateway | FastAPI |
| AI Service | retrieval, prompt assembly, LLM reasoning, recommendation generation, evidence citations | Python / FastAPI |
| Vector DB | semantic retrieval over approved knowledge and case chunks | PostgreSQL + pgvector / vector index |
| SQL DB | cases, entities, sources, jobs, findings, review state | PostgreSQL |
| Evidence Vault | immutable source captures, documents and SHA-256 | object storage |
| External OSINT Sources | public registries, sanctions, web sources | external systems |

The AI Service cannot promote a claim to a verified FACT automatically. It produces a recommendation with evidence references and confidence/limitations for analyst review.
