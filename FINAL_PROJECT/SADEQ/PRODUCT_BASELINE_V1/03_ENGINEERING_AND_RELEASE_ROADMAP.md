# ROADMAP-ENG-001 — Разработка, контрольные ворота и выпуски
**Статус:** поэтапный план; календарные даты и бюджеты — UNKNOWN до baseline.

## Фазы с зависимостями
| Фаза | Вход | Действия | Выход | Exit gate |
|---|---|---|---|---|
| R0 IDEA+ | идея, customer need | описание продукта, регистры, feasibility assumptions | IDEA+ baseline | идея документирована, risk recorded |
| R1 Business Discovery | sponsor and process owners | AS-IS BPMN, stakeholder map, interviews, baseline KPI, BMC | Business Case | value hypothesis falsifiable |
| R2 Architecture | PRD | C4 1–4, ER, Sequence, BPMN/DMN/UML, ADR, threat model, contracts | Architecture Decision Pack | independent CTO+security review |
| R3 Offline Infrastructure | architecture | local registry/images/models, Compose, secrets, DB, network deny-all | reproducible deploy | boot offline, SBOM and hashes |
| R4 Universal Core | infrastructure + contracts | adapters, entity resolution, event store, snapshots, state and tool policy | tested UAA runtime | cross-channel/replay/ACL |
| R5 Knowledge & Reason | R4 | source provenance, Qdrant+Neo4j, LangGraph, verified forecast | traceable analysis | real GraphRAG and benchmarks |
| R6 Trust & Training | R5 | curriculum, independent holdouts, review/rollback, monitoring | qualification pipeline | security & AI quality acceptance |
| R7 Factory & Bootstrap | R6 | YAML agent passports, 3 independent configs, Engineer Agent 001 patch in sandbox | demo profiles + agent factory | independent evidence, human signoff |
| R8 Performance & FinOps | R7 | TTFT, p95, GPU VRAM, 40/160/730h costs, TCO | sizing/scale report | capacity and budget bound |
| R9 OTUS Release | R8 | video 5–7min, source/version manifest, diagram and evidence pack | defense artifact | all mandatory criteria; deadline −8 days |
| R10 Enterprise Pilot | agreed business owner | real integration under authority, onboarding, backup, support | controlled pilot | customer success and security acceptance |
| R11 Enterprise Production | qualified pilot | SLA, backup/failover, on-prem/hybrid variants by policy | governed commercial release | measured SLO, TCO, support plan |

## WBS Streams
BUS: discovery / economics. ARCH: contracts / C4 / ADR. CORE: event state machine. KB: GraphRAG. SECURITY: 6 roles and control gates. QAL: independent qualification. OPS: offline deployment / telemetry. FIN: scenario modeling. EDU: 31 OTUS lesson traceability. COM: product packaging / SLA.

## Roadmap horizons — criteria, not promises
**H0 Foundation:** R0–R3; design complete, reproducible offline deployment.  
**H1 MVP:** R4–R9; one completed vertical cycle, 3 profiles, Agent 001, independent tests.  
**H2 Pilot:** R10; 1 design partner; external data connector after permissions.  
**H3 Product:** R11; domain packs, release management and support.  
**H4 Scale:** after unit economics and load traces justify GPU pool, multi-tenancy or clouds.

## Release versioning
v0.1 contracts/prototype; v0.2 complete offline GraphRAG; v0.3 guarded action + evidence; v0.4 factory & three profiles; v1.0 qualified customer pilot. These numbers are **target labels**, no corresponding executable releases currently confirmed.

## Critical path
Verified data rights and source licenses → model fit hardware → entity resolution → evidence-linked graph → independent policy → independent qualification → release. No speed claim before measuring actual critical path.

## OTUS 1–31 coverage
G1 1–3 BUS; G2 4–7 ARCH/KB/Agents; G3 8–10 ADR/CTO debt; G4 11–15 API/Data/QA/Sec/OTel; G5 16–20 sizing/quant/CI/MLOps/deploy; G6 21–27 HA/K8s/EDA/highload/cloud/tenant/privacy; G7 28–31 FinOps/radar/governance/API-product. Detailed lesson-by-lesson matrix: [existing document](../IDEA_PLUS_V0_2/10_OTUS_01_31_TRACEABILITY_MATRIX.md).

## Evidence hierarchy
Not built → Source exists → Tests source present → Tests executed → integration reproduced → independent qualification → human-approved release. No jump between steps.
