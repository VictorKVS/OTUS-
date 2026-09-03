# C3 Component Diagram — Knowledge Base Filling Agent

```mermaid
flowchart LR
    COL[OSINT Collectors / Screening Factory]
    ANA[Main Analyst]

    subgraph KBAG[Container: Knowledge Base Filling Agent]
      API[Ingest API]
      POL[Policy & Admission Gate]
      VAL[Evidence Validator]
      CHK[Stable Chunk Builder]
      EXT[Candidate Extractor]
      PROV[Provenance Binder]
      ER[Entity Resolution]
      CON[Contradiction Engine]
      REV[Review Queue]
      PUB[Knowledge Publisher]
      AUD[Audit Writer]
    end

    EV[(Evidence Vault)]
    ODB[(Operational DB)]
    GRAPH[(Entity Graph)]
    KB[(Knowledge Base)]
    LOG[(Audit Journal)]

    COL -->|EvidencePackage| API
    API --> POL
    POL -->|admitted| VAL
    POL -->|blocked event| AUD
    VAL -->|raw artifact + hash| EV
    VAL --> CHK
    CHK --> EXT
    EXT --> PROV
    PROV --> ER
    ER --> CON
    CON --> REV
    REV -->|ReviewItem| ANA
    ANA -->|APPROVE / REWORK / REJECT| REV
    REV -->|approved object| PUB
    PUB --> ODB
    PUB --> GRAPH
    PUB --> KB
    API --> AUD
    VAL --> AUD
    CON --> AUD
    REV --> AUD
    PUB --> AUD
    AUD --> LOG
```

## Правило публикации

`Knowledge Publisher` принимает только объект, для которого существует явное human review decision. Компоненты извлечения и анализа не имеют прямой записи в `Knowledge Base`.
