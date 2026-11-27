# DELIVER-001 — Документы, контрольные версии, комплект для защиты и внедрения
## Required design artifacts
☐ IDEA+ contract and feasibility, previous reuse audit, external prior art;
☐ BABOK Business Case, stakeholders, AS-IS/TO-BE BPMN, value stream, RACI;
☐ UML Use Case / Activity / State, DMN table, C4 L1–L4, data ER, Sequence;
☐ ADR register with decisions, constraints, alternatives, owners;
☐ PRD with user stories, acceptance criteria, NFR, contracts (OpenAPI/JSON Schema);
☐ threat model, regulatory/data map, trust and security role contracts;
☐ model/data licensing, citations, reproducible model checkpoint hashes;
☐ deployment/infra options (airgap/onprem/private cloud/hybrid) + diagrams;
☐ Sizing benchmark and cost formulas, GPU/memory/tokens/sec, p95/TTFT;
☐ SLO/SLI/RTO/RPO, monitoring dashboards, backup/restore, incident/rollback;
☐ qualification curriculum, independent negative tests, evidence and signed release;
☐ product documentation, runbooks, training pack, prospect and defense decks.

## Proof ledger
Every critical claim includes `claim_id, business_requirement, evidence_type, test_id, artifact_sha, environment, version, run_date, reviewer, status`.
**NOW:** documentation only; no certification claims.

## OTUS protection against failure
Strict offline demo, LangGraph stateful branching, real GraphRAG, independent access denial User B, GPU serving demonstration, live traces, deploy/data-flow diagrams and real benchmark numbers. Submit ≥8 days prior to defense; record exact date only when provided. Show a 5–7 minute video and annotated repo.

## Three presentations
**OTUS technical** (architecture, GraphRAG, security, experiments); **CTO commercial** (problem, measured ROI, adoption and risk); **Ops/Security** (deployment, controls, runbooks, cost). Reuse earlier draft slide decks only with statuses explicitly marked; unsupported metrics are placeholders.

## Change/ownership policy
Human-reviewed commits, ADR, SHA-256/attestations, qualified release manifests, SBOM/provenance. Public docs use neutral SADEQ terms; links to personal repos and Git metadata can reveal ownership even without project names.

## Open blockers
Live code tests; end-to-end test; supported model/DB licenses; budget/owner; signed acceptance; real customer interviews; production-ready artifacts; independently measured cost; approved security policy. Therefore status remains `RESEARCH / DESIGN BASELINE`.
