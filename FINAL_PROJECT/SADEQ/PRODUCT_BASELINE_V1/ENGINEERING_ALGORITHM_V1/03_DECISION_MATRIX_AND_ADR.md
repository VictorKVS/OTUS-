# SEDA-DECISION-001 — Выбор алгоритмов и паттернов
## Rule 1: eliminate hard-constraint failures
`eligible(a) = all(hc(a) == PASS)`. `UNKNOWN` for critical hard constraint means `RESEARCH_REQUIRED`, not PASS.
Hard constraints for SADEQ offline MVP: HC01 no external AI API; HC02 no cross-tenant data; HC03 no autonomous high-risk action; HC04 closed contracts; HC05 independent qualification; HC09 hardware support; HC10 genuine GraphRAG where requirement applies.

## Rule 2: multi-criteria score only when evidenced
For candidates passing hard constraints:
```
score(a) = sum_i weight_i * normalized_metric_i(a)
```
Metrics direction and normalization must be documented: quality higher better, p95 latency lower better, memory lower better, cost per qualified outcome lower better, license/support risk lower better. Weights must sum to 1, be business-approved and recorded in ADR. A NOT_MEASURED criterion cannot be assigned a fictional neutral value; declare scoring incomplete and run an experiment.

## Scored candidate matrix template
| Candidate | Source | HC pass? | Accuracy or Recall | p95 | peak VRAM | cost/outcome | Complexity | Decision |
|---|---|---|---|---|---|---|---|---|
| ALG-001 baseline | SRC-XXX | TO_TEST | NOT_MEASURED | NOT_MEASURED | NOT_MEASURED | NOT_MEASURED | ESTIMATE_ONLY | EXPERIMENT |
| ALG-002 alternative | SRC-YYY | TO_TEST | NOT_MEASURED | NOT_MEASURED | NOT_MEASURED | NOT_MEASURED | ESTIMATE_ONLY | EXPERIMENT |

## Typical alternatives, **not preapproved**
| Problem | Baseline | Candidate alternative | Decision experiment |
|---|---|---|---|
| Object resolution | deterministic exact/normalized ID | blocking + fuzzy entity match | precision of merges, false merges, p95, review cost |
| Retrieval | lexical/vector top-k | hybrid BM25/vector + rerank | recall@k, groundedness, p95, cost |
| Relationships | relational joins/reference path | graph traversal + evidence subgraph | relation quality, path accuracy, indexing |
| Agent flow | deterministic finite state machine | LangGraph with checkpoint/tool bounds | recovery, latency, loops, safeguards |
| Event delivery | Postgres outbox | dedicated event broker | lost/duplicate events, throughput, ops cost |
| Deployment | single-host Compose | Kubernetes + GPU pool | RTO/RPO, SLO, required skills, TCO |
| RAG vs no RAG | verified local structured query | RAG/GraphRAG | relevance, citations, unauthorized retrieval and overall cost |

## ADR submission contract
```yaml
adr_id: ADR-ALG-001
problem_id: TASK-001
requirements: [FR-02, FR-03]
reference_books: [SRC-001, SRC-002]
alternatives: [exact_match, fuzzy_match_with_review]
hard_constraint_results: {HC-01: PASS, HC-02: TO_TEST}
benchmark_evidence: []
reasoning: "proposed; no measured quality"
selected: PROVISIONAL_BASELINE
risk_effect: [THR-073]
fallback: ABSTAIN_ON_AMBIGUOUS_MATCH
revisit_trigger: "false merge or domain growth"
approved_by: null
```

## Qualification criteria
- Exact false-positive/false-negative and ambiguity handling for entity resolution.
- Reproducible transformations, seeded test data, cross-tenant denial.
- Difference between `AGENT PROPOSAL` and `AUTHORIZED TOOL EXECUTION`.
- Human/independent approval before marking `APPROVED`.
