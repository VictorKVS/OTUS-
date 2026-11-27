# HLD-DRIVERS-001 — Список желаемого, обязательных ограничений и неизвестных
## Confirmed desirable capabilities — source mapping
| Driver | Wish-list item | Requirement source | Architecture implication |
|---|---|---|---|
| WD-01 | Один универсальный агент, предметные профили вместо копирования | IDEA+ FR-10, PRD FR-11 | UAA Core + profile registry |
| WD-02 | Не менее 2 входных каналов | IDEA+ FR-01, PRD FR-01 | Channel interface + adapters |
| WD-03 | Единая идентичность объекта между каналами | IDEA+ FR-02 | Object registry / resolution |
| WD-04 | История событий и replay | IDEA+ FR-03, PRD FR-04 | Durable event journal + state projection |
| WD-05 | Обнаружение изменений и проверяемые прогнозы | IDEA+ FR-04, FR-07 | Deterministic algorithm layer, backtesting |
| WD-06 | Подлинный GraphRAG c путями и источниками | IDEA+ FR-05 | Local vector+graph retrieval + provenance |
| WD-07 | Нелинейный agent flow, checkpoint, bounded loops | IDEA+ FR-06 | LangGraph runtime with external checkpoint |
| WD-08 | Проверяемые разрешённые реакции | IDEA+ FR-08 | Independent Policy / Tool Gateway |
| WD-09 | Подтверждённая обратная связь и обучение | IDEA+ FR-09 | Knowledge feedback/change review |
| WD-10 | Агент-программист создаёт patch+tests | IDEA+ FR-11 | Agent Factory workspace isolated |
| WD-11 | Независимое тестирование и допуски | IDEA+ FR-14 | Qualification plane POLYGON |
| WD-12 | Инструментальная метрика и экономика | PRD FR-16 | OTel metrics + FinOps reporting |

## Hard constraints (HC) — prohibit architecture violations
| Constraint | Contract | Implication |
|---|---|---|
| HC-01 | Air-gapped/offline MVP; no external AI APIs | self-hosted LLM, embedding, rerank; deny egress; imported offline artifacts |
| HC-02 | No cross-tenant/cross-user leaks | policy before vector and graph traversal, cache/log citations isolated |
| HC-03 | No direct autonomous high-risk operations | action proposal vs action execution; human gate; fail closed |
| HC-04 | Strict input/output/recipient/algorithm contracts | versioned closed schemas; UAG only allowlisted routes |
| HC-05 | No self-qualification or self-release | independent POLYGON, human sign-off |
| HC-06 | Evidence or NOT_QUALIFIED | source hashes, test evidence, release provenance |
| HC-07 | No base model training in MVP | local inference only; curriculum and feedback are governed |
| HC-08 | No 20-agent scale claim in MVP | only 3 differentiated profiles and one Agent 001 demo |
| HC-09 | GPU constraint lab RTX3060 12GB, 32 GB RAM | benchmark before selecting model and service count |
| HC-10 | Scope of MVP includes real Qdrant + Neo4j | vector-only search does not count as real GraphRAG |
| HC-11 | No invented SLA or 10k LLM RPS | SLO only after empirical test |
| HC-12 | No cloud option described as strict airgap | cloud is separate allowed deployment option requiring revised security assumption |

## Architecture quality attributes
Security > verifiability > reliable reproducible state > accuracy/provenance > maintainability > latency/throughput > operations cost (ORDER PROPOSED, needs stakeholder signoff).

## Unknown / assumptions to resolve
Source volumes, number of tenants and events/sec, accuracy goldens for entity matching, model licence and language evaluation, SLO p95, GPU token/s, retention policy, customer data classification, RTO/RPO, realistic cloud/on-prem TCO, investment budget, actual commercial adopter. In no case assert these measured.

## Explicit design boundary
The wish list describes *what*, not an obligation to build 8 independent processes. HLD defines responsibilities and flows, LLD later defines algorithms, contracts and deployment after evidence.
