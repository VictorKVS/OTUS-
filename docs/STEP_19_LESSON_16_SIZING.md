# STEP 19 — Lesson 16: Resource Sizing for Applications and Data

Статус: **DONE v1 (normalization)**

## Source boundary

Источник Lesson 16 подтверждает:

- CPU / GPU / RAM / storage forecasting;
- stateless/stateful sizing;
- SQL / NoSQL / Vector DB sizing;
- влияние RPS, quality и financial constraints;
- on-premise TCO;
- детальный расчёт для on-premise и cloud;
- наличие TCO calculator frame;
- преподаватель: Михаил Лебедев;
- дата: 23.09.2026;
- длительность: 90 минут.

В папке также присутствует `megaxls-611826-e95145.xlsx`.

Его наличие подтверждено, но формулы и вычисленные значения в этом проходе не верифицированы.

## Engineering schema

```mermaid
flowchart LR
  A[REQ/NFR/SLO] --> B[Workload model]
  B --> C[RPS / concurrency]
  C --> D[Service / data class]
  D --> E[CPU / RAM / GPU / storage]
  E --> F[Replication / headroom]
  F --> G[Benchmark]
  G --> H[On-prem / Cloud]
  H --> I[TCO]
  I --> J[Capacity Gate]
```

## Architect Pro — engineering extension

Вне буквального текста урока добавлен практический расчётный контракт:

- `Concurrency ≈ RPS × service_time_seconds`;
- CPU sizing from benchmarked CPU-seconds/request and utilization target;
- RAM = working set + cache + runtime overhead + safety margin;
- raw vector payload = vector count × dimension × bytes/element;
- storage adds retention, replication, index overhead and headroom;
- TCO includes full operational costs, not only server price.

Все эти формулы являются **engineering extension**, а не дословной частью source lesson.

## Agent Factory impact

Для любого создаваемого агента вводится обязательный **Sizing & Capacity Contract**.

Минимальные входы:

- peak / average task rate;
- concurrency;
- prompt / output token profile;
- RAG queries per task;
- tool calls per task;
- memory operations;
- data/vector growth;
- observability retention;
- p95 latency / availability SLO;
- cost budget.

Минимальный output:

- CPU/RAM/GPU budget;
- SQL/NoSQL/Vector capacity;
- replicas/headroom;
- benchmark evidence;
- cloud/on-prem option;
- TCO / unit cost;
- Capacity Gate result.

## Production mapping

- `FTH-SIZ-001 · Resource Sizing & Capacity Service`
- `FTH-SLO-001 · SLO / Alerting`
- `FTH-REL-001 · Reliability Plane`
- `FTH-FIN-001 · FinOps / Cost Control`
- `FTH-EST-001 · Estimation & Planning`

## Evidence

- `site/data/lesson-details/16.json`
- `site/assets/lesson-16-sizing-capacity.svg`
- source Lesson 16 text;
- XLSX calculator artifact present.

## Status

Lesson 16 = **draft / M1**.

Это означает: архитектурный sizing-контур спроектирован и имеет исходный calculator artifact, но calculator formulas/outputs и benchmark evidence ещё требуют отдельной проверки.

Следующее: Lesson 17 должен детализировать LLM inference / GPU / VRAM sizing.
