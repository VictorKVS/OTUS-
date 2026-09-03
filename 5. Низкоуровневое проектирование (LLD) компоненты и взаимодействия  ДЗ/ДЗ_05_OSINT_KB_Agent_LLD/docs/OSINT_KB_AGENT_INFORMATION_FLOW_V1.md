# Агент заполнения баз данных и базы знаний — бизнес-схема v1

## Выбранные нотации

- **BPMN 2.0** — кто и в какой последовательности выполняет работу, где параллельность, шлюзы и возврат на доисследование.
- **DFD Level 1** — какие информационные потоки входят в агент, какие хранилища он заполняет и что передаёт дальше.

## Роль агента

Агент не является сборщиком «всего подряд» и не создаёт FACT самостоятельно. Он получает доказательственный пакет, сохраняет происхождение, преобразует материал в устойчивые объекты, сравнивает их с уже накопленными данными, показывает противоречия и готовит кандидаты для утверждения человеком.

## Что агент записывает

| Хранилище | Содержание | Авторитетность |
|---|---|---|
| Evidence Vault | неизменяемые оригиналы, SHA-256, metadata | первичный доказательственный слой |
| Operational DB | дела, задания, источники, captures, claims, статусы | операционная система учёта |
| Entity Graph | сущности, типизированные связи, даты, evidence refs | производное представление |
| Knowledge Base | утверждённые факты, определения, требования, методы, версии | экспертно проверенный слой |
| Audit Journal | все действия и переходы, hash-chain | аудиторский след |

## BPMN — логика работы

```mermaid
flowchart LR
    S((Старт)) --> A[Цель, scope, основание, доступ]
    A --> G{Допустимо?}
    G -- Нет --> X[BLOCKED + журнал] --> E0((Конец))
    G -- Да --> I[Entity Resolution]
    I --> GI{Объект разрешён?}
    GI -- Нет --> Q[Запрос недостающих идентификаторов] --> H{Решение аналитика}
    GI -- Да --> P[Query Plan + Country Pack]
    P --> F{{Пять параллельных потоков}}
    F --> A1[Entity / Registry]
    F --> B1[Business / Finance / Logistics]
    F --> C1[Digital Footprint]
    F --> D1[Legal / Sanctions / Adverse]
    F --> E1[Source Quality / Counter-search]
    A1 --> J{{Сведение}}
    B1 --> J
    C1 --> J
    D1 --> J
    E1 --> J
    J --> C[Capture + SHA-256]
    C --> R[Parse + stable chunks]
    R --> EX[Entity / Event / Claim / Definition / Requirement / Relation]
    EX --> PR[Provenance binding]
    PR --> N[Normalize + exact dedup + no silent merge]
    N --> CMP[Compare with DB / KB]
    CMP --> SG{Evidence sufficient?}
    SG -- Нет --> GAP[RESEARCH_GAP] --> P
    SG -- Да --> Z[Independent ANALYSIS_OPINION]
    Z --> RT[Red Team]
    RT --> H
    H -- Доработка --> P
    H -- Утверждено --> PUB[Versioned publish: DB + Graph + KB]
    PUB --> REP[Report + Monitoring profile]
    REP --> END((Конец))
```

## DFD — информационные потоки

```mermaid
flowchart LR
    U[Постановщик / аналитик] -->|задача, цель, seed| P1((P1 Приём))
    P1 --> D2[(Case + Job + Audit DB)]
    P1 --> P2((P2 Планирование))
    D1[(Source / Tool Registry)] --> P2
    P2 -->|typed jobs| T[Kali / API / Browser / File adapters]
    T -->|raw output + manifest| P3((P3 Capture))
    P3 --> D3[(Evidence Vault)]
    P3 --> P4((P4 Parse / Normalize))
    P4 --> D4[(Operational normalized DB)]
    P4 --> P5((P5 Extract / Resolve))
    P5 --> D5[(Entity / Relation Graph)]
    P5 --> P6((P6 Verify / Red Team))
    D3 --> P6
    D5 --> P6
    R[Эксперт / Red Team] --> P6
    P6 -->|gaps| P2
    P6 -->|approved finding| P7((P7 Publish / Report / Monitor))
    P7 --> D6[(Knowledge Base)]
    P7 --> D7[(Reports / Monitoring)]
    D7 --> C[Руководитель / доменный агент]
```

## Обязательные выходы одного цикла

1. `SOURCE_CAPTURE` с SHA-256 и исходным locator.
2. Stable chunks с точными границами и ссылкой на оригинал.
3. Кандидаты сущностей, событий, утверждений, определений, требований и связей.
4. Запрет silent merge для тёзок и одноимённых организаций.
5. Реестр противоречий, версий и supersession.
6. `RESEARCH_GAP`, если данных недостаточно.
7. Независимые `ANALYSIS_OPINION`, но не автоматический FACT.
8. Human-approved finding.
9. Версионная запись в Operational DB, Graph и Knowledge Base.
10. Справка, export manifest, monitoring profile и audit event.

## Acceptance gate для ДЗ

ДЗ считается завершённым на уровне архитектуры, когда:

- BPMN показывает роли, параллельные потоки, шлюзы и цикл доисследования;
- DFD показывает все хранилища и направления движения данных;
- определены входные и выходные контракты агента;
- зафиксировано разделение SOURCE / CAPTURE / CLAIM / FACT / INFERENCE / HYPOTHESIS;
- сохранена трассировка до исходного фрагмента;
- предусмотрены contradiction, version и supersession;
- FACT создаётся только после human review;
- предусмотрены отчёт, мониторинг и повторный прогон.
