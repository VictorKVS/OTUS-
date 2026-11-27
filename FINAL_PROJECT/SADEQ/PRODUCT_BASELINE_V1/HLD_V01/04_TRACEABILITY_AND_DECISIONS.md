# HLD-TRACE-001 — Traceability / security / qualification / gates
## Requirement → block mapping
| Requirement | Responsible block(s) | First qualification test |
|---|---|---|
| IDEA FR-01 / PRD FR-01 | B01 | source+schema intake test |
| IDEA FR-02 / PRD FR-03 | B02 | two channels → one object, different tenants never merged |
| IDEA FR-03/04 / PRD FR-04 | B02 | replay and late event detection |
| IDEA FR-05 / PRD FR-05 | B03+B04 | explain graph path and cite source; compare vector-only |
| IDEA FR-06 / PRD FR-06 | B04 | bounded LangGraph branch/checkpoint/restart |
| IDEA FR-07 / PRD FR-07 | B04 | reproduce baseline + backtest |
| IDEA FR-08 / PRD FR-08 | B05 | forbidden tool stays uncalled |
| IDEA FR-09 / PRD FR-10 | B03+B06+B07 | changed source invalidates qualification |
| IDEA FR-10 / PRD FR-11 | B06+B04 | three profiles, no duplicated core |
| IDEA FR-11 / PRD FR-12 | B06+B07 | Agent 001 patch requires human review |
| IDEA FR-12 / PRD FR-14 | B08 | egress blocked and local completion |
| IDEA FR-13 / PRD FR-08 | B01+B02+B03+B05 | User B cannot access User A in graph/vector/cache/log |
| IDEA FR-14 / PRD FR-15 | B07+B05+B08 | outdated qualification DENY |
| PRD FR-13 | B08+B02+B05 | trace source→event→decision→execution |
| PRD FR-16 | B08 | measured cost per independently accepted outcome |

## Threat assignment (initial, not risk assessment)
- B01: THR-011–015, THR-016–018, THR-021–024.
- B02: THR-071–075, THR-079–080, THR-016.
- B03: THR-031–040, THR-076–079.
- B04: THR-041–060, THR-019–020.
- B05: THR-016–030, THR-045–050.
- B06: THR-051–070, THR-009–010.
- B07: THR-009–010, THR-045–060, THR-094–096.
- B08: THR-061–070, THR-081–100.
Each component's threat profile must subsequently be narrowed by context, not all group threats automatically applicable.

## HLD acceptance gates
HLD-G1 Context C1 identifies all persons/external systems and no external model API in strict offline MVP.
HLD-G2 C2 logical containers and persistence boundaries have unambiguous ownership.
HLD-G3 B01–B08 one responsible owner and no unapproved direct cross-block side effects.
HLD-G4 flows FLOW-01..08 have sender, receiver, purpose, input/output contract to be completed.
HLD-G5 security separation between candidate agent, policy service and independent qualifier.
HLD-G6 architecture options with cost/scale decisions and ADR; no invented benchmarks.
HLD-G7 100-threat catalog assessed for applicability and mapped to components before implementation.
HLD-G8 PRD→blocks→tests trace links accepted; high-risk decisions require human gate.

## Known blockers / unknowns
- Need signed business priority order and initial work capacity.
- Need to inspect exact book edition if user intended another book; book source used for C4/API modelling only.
- Real profile/schema of observation payload is not yet frozen.
- No independently run HLD verification tests or customer architecture signoff.
- No actual cost/throughput baseline for new blocks, cloud excluded from strict offline.

## Next step
1. Review B01/B02 ownership and interface to B03 (risk of conflating source document and observation).
2. Create detailed information contracts FLOW-01/02 (strict nested JSON Schema), error taxonomy and field-owner matrix.
3. Produce C3 component diagrams and Sequence before FastAPI implementation; attach evidence.
