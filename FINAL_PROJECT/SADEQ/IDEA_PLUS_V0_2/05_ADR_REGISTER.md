# ADR register — v0.2 proposal
Все решения **PROPOSED**, не утверждены после экспериментального сравнения.
| ID | Decision | Alternatives | Trade-off / verification |
|---|---|---|---|
| ADR-001 | GraphRAG: Qdrant + Neo4j | vector-only, graph-only | сложная синхронизация и ACL; тесты graph path, grounded QA, data segregation |
| ADR-002 | LangGraph stateful orchestration | linear chain, custom FSM | complexity vs checkpoint/branch/approval; replay integration tests |
| ADR-003 | Deterministic state and numerical forecast | pure LLM reasoning | предметные алгоритмы + backtesting; больше интеграционных контрактов |
| ADR-004 | Central policy and tool gateway | agent self-enforcement | latency/single-point-failure vs strict security and logs |
| ADR-005 | Containerized modular MVP | single process, microservices-per-class | операционная сложность vs требования deployment и масштабирование |
| ADR-006 | Append-only event log + state snapshots | overwrite latest record | storage vs provenance/replay |
| ADR-007 | Local quantized multilingual LLM | remote API; oversize model | offline, quality/latency/VRAM; per checkpoint eval |
| ADR-008 | Independent Qualification Lab | self-scoring agent | cost of benchmark set vs lower false confidence |
| ADR-009 | Human approval for writes | full autonomous writes | slower ops but limited irreversibility and rollback |
| ADR-010 | Read-only / supervised learning in MVP | live model fine-tuning | safer version control, faster implementation |
| ADR-011 | Trust is scoped per version/domain/tool | global reputation score | more tests but avoids privilege transfer |
| ADR-012 | Reusable agent specification | copy-paste standalone agents | platform CAPEX vs lower marginal integration |

Каждый ADR должен быть дополнен экспериментацией: constraints, rationale, disconfirmed alternatives, measured quality, measured cost and decision owner. Новый отказ одной из обязательных проверок означает NOT_APPROVED.
