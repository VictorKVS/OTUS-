# Multi-Agent Architecture — Smart Travel Assistant

```mermaid
flowchart LR
    U[Сотрудник] --> M[Manager Agent]

    subgraph MAS[Multi-Agent Travel Assistant]
      M --> P[Policy RAG Agent]
      M --> F[Flight Search Agent]
      M --> H[Hotel Search Agent]
      M --> B[Budget Analyst]
      P --> B
      F --> B
      H --> B
      B --> M
    end

    P --> V[(Vector DB)]
    V --> PC[(Travel Policy Chunks)]
    F --> FS[(Flight Provider / mock)]
    H --> HS[(Hotel Provider / mock)]
    M --> O[(Audit / Agent Trace)]
    M --> R[Trip Recommendation]
    R --> U
```

## Single Responsibility

| Агент | Ответственность | Не делает |
|---|---|---|
| **Manager Agent** | декомпозиция запроса, делегирование, сбор результата | не ищет билеты и не интерпретирует политику напрямую |
| **Policy RAG Agent** | поиск правил корпоративной политики и evidence refs | не бронирует и не рассчитывает итоговый бюджет |
| **Flight Search Agent** | подбор вариантов перелёта | не решает, допустим ли тариф по политике |
| **Hotel Search Agent** | подбор вариантов проживания | не утверждает превышение лимита |
| **Budget Analyst** | суммирование расходов и проверка лимитов | не меняет исходные результаты поиска |

## Паттерн взаимодействия

Используется **иерархическая мультиагентная схема**: Manager координирует специализированных агентов. Для минимального прототипа граф детерминирован и воспроизводим; в production-версии Manager может формировать динамический план и запускать независимые поисковые задачи параллельно.

## Безопасность и управляемость

- tools имеют allow-list;
- внешние поисковые агенты в демо используют mock/read-only источники;
- Policy RAG всегда возвращает `source_id/chunk_id`;
- отсутствие правила даёт `POLICY_GAP`;
- итоговая рекомендация не является автоматическим финансовым одобрением.