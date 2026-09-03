# Sequence Diagram — Пользователь запрашивает рекомендацию

```mermaid
sequenceDiagram
    autonumber
    actor U as Analyst / User
    participant FE as Frontend
    participant BE as Backend / Case Service
    participant RC as Recommendation Controller
    participant QN as Query Normalizer
    participant RAG as RAG Manager
    participant VDB as Vector DB
    participant SQL as SQL DB
    participant PTF as Prompt Template Factory
    participant LC as LLM Client
    participant LLM as LLM
    participant CG as Citation Guard
    participant CE as Confidence Evaluator
    participant RF as Recommendation Formatter

    U->>FE: Запрашивает рекомендацию по кейсу
    FE->>BE: POST /cases/{caseId}/recommendation
    BE->>RC: POST /get_recommendation
    RC->>QN: normalize(query, case_id, language)
    QN->>RAG: retrieve context
    par Semantic context
        RAG->>VDB: similarity search
        VDB-->>RAG: approved chunks + ids
    and Structured context
        RAG->>SQL: case/entities/findings
        SQL-->>RAG: structured records
    end
    RAG->>PTF: query + retrieved context
    PTF->>LC: prompt + evidence refs
    LC->>LLM: inference request
    LLM-->>LC: draft recommendation
    LC->>CG: draft + retrieved evidence
    CG->>CE: supported claims + citation status
    CE->>RF: confidence + limitations
    RF-->>RC: RecommendationResponse
    RC-->>BE: 200 recommendation + evidence refs
    BE-->>FE: recommendation DTO
    FE-->>U: Отображает рекомендацию и источники

    alt Недостаточно доказательств
        CG-->>RC: insufficient_evidence
        RC-->>BE: 422 INSUFFICIENT_EVIDENCE
        BE-->>FE: запросить дополнительные данные
        FE-->>U: Показать ограничения / research gap
    end
```

## Связь с C3

Каждый компонент Sequence Diagram присутствует на C3 AI Service: `Recommendation Controller`, `Query Normalizer`, `RAG Manager`, `Prompt Template Factory`, `LLM Client`, `Citation & Evidence Guard`, `Confidence Evaluator`, `Recommendation Formatter`.
