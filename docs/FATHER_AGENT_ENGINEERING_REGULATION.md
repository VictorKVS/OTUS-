# FATHER Agent Engineering Regulation

Статус: **CANONICAL DESIGN v1**

## 1. Основной принцип

В FATHER агент создаётся дважды:

1. **на бумаге** — как полный, согласованный и проверяемый комплект документов;
2. **на практике** — как реализованный программный компонент, который обязан соответствовать документам и пройти испытания.

Код без утверждённого Agent Dossier не считается промышленным агентом.

~~~text
IDEA
→ PAPER DESIGN
→ DOCUMENT REVIEW
→ DEVELOPMENT PACK
→ PRE-DEV VALIDATION
→ FATHER PROGRAMMER
→ IMPLEMENTATION
→ TECHNICAL VERIFICATION
→ FATHER LAB
→ DEVOPS ENVIRONMENT
→ ACCEPTANCE
→ CERTIFICATION
→ ZOO
→ PRODUCTION
→ EXPERIENCE
→ CHANGE REQUEST
→ NEXT VERSION
~~~

## 2. Этапы

### S0 — Idea / Intake
Owner: Requester + ALINA Analyst.
Документы: PROJECT_PASSPORT, AGENT_INTENT, BUSINESS_CONTEXT, SCOPE, STAKEHOLDERS, SOURCE_REGISTER, CONSTRAINTS, ASSUMPTIONS_OPEN_QUESTIONS, SUCCESS_CRITERIA.
Gate: G-S0-INTAKE.

### S1 — Analysis
Owner: ALINA Analyst.
Документы: AS_IS, TO_BE, USE_CASES, FUNCTIONAL_REQUIREMENTS, NFR, DATA_CATALOG, INTEGRATION_REGISTER, RISK_REGISTER, DOMAIN_GLOSSARY, TRACEABILITY_MATRIX.
Gate: G-S1-ANALYSIS.

### S2 — Agent Concept & Architecture
Owner: FATHER Architect.
Документы: AGENT_PASSPORT, AGENT_ROLE_AND_BOUNDARIES, CAPABILITY_MAP, AGENT_SPEC, C4, SEQUENCE, WORKFLOW_GRAPH, STATE_MODEL, INPUT_OUTPUT_CONTRACTS, TOOL_MCP_POLICY, MODEL_ROUTING, MEMORY_POLICY, KNOWLEDGE_ARCHITECTURE, SECURITY_ARCHITECTURE, ADR.
Gate: G-S2-ARCHITECTURE.

### S3 — Knowledge & Skill Design
Owner: ALINA + Domain Expert.
Документы: KNOWLEDGE_SCOPE, SOURCE_POLICY, KNOWLEDGE_SCHEMA, KNOWLEDGE_GRAPH_SPEC, RAG_SPEC, CITATION_PROVENANCE_POLICY, SKILL_TREE, TRAINING_PROGRAM, LEVEL_MODEL, EXAM_PLAN, GOLDEN_DATASET, REGRESSION_DATASET.
Gate: G-S3-KNOWLEDGE.

### S4 — Quality / Security / Operations Design
Owner: QA + Security + SRE + Architect.
Документы: THREAT_MODEL, SECURITY_CONTROLS, IAM_MATRIX, DLP_PII_POLICY, GUARDRAILS_POLICY, QUALITY_GATES, EVALUATION_PLAN, TEST_STRATEGY, OBSERVABILITY_CONTRACT, SLI_SLO, ALERT_MATRIX, CAPACITY_SIZING, FINOPS_PROFILE, HA_DR, ROLLBACK_REQUIREMENTS.
Gate: G-S4-CROSSCUTTING.

### S5 — Development Pack
Owner: Analyst + Architect.
Комплект определяется DEVELOPMENT_PACK_STANDARD.md.
Gate: G-S5-DEV-PACK. Programmer не принимает задачу без PASS.

### S6 — Implementation
Owner: **FATHER Programmer / FATHER CODEX**.
Вход: validated Development Pack + approved ADR/architecture + immutable requirement/acceptance IDs.
Выход: source code, unit/integration/contract tests, schemas/migrations, configs, telemetry hooks, build scripts, containerization, README, CHANGELOG, implementation evidence, Pull Request.
Gate: G-S6-IMPLEMENTATION.

### S7 — Technical Verification
Owner: CI + QA + Security.
Проверки: build, lint/type, unit/integration/contract, schema, SAST/SCA/secrets, container/IaC, authorization/security, observability, migration/rollback, performance where applicable.
Gate: G-S7-TECH.

### S8 — FATHER LAB
Owner: AI Quality / ALINA Evaluator / Lab.
Обязательные испытания: baseline, A/B/N, multi-LLM where applicable, prompt regression, RAG eval, knowledge algorithm eval, agent trajectory, failure/degraded modes, safety, cost/latency/resources, repeatability, regression.
Выход: EXPERIMENT_MANIFEST, RUN_MANIFESTS, METRIC_REPORT, FAILURE_REPORT, EVALUATOR_REPORT, REGRESSION_REPORT, SAFETY_REPORT, CHAMPION_DECISION.
Gate: G-S8-LAB.

### S9 — Environment / DevOps
Owner: DevOps/SRE.
Документы: ENVIRONMENT_PROFILE, DEPLOYMENT_MANIFEST, IMAGE/SBOM, K8S/IaC, RBAC/NetworkPolicy, secrets contract, resource requests/limits, observability evidence, backup/restore evidence, rollback evidence.
Gate: G-S9-ENV.

### S10 — Acceptance
Independent owners: Analyst, Architect, Security, QA/Lab, SRE.
Документы: ANALYST_ACCEPTANCE, ARCHITECT_ACCEPTANCE, SECURITY_ACCEPTANCE, QUALITY_ACCEPTANCE, OPERATIONS_ACCEPTANCE, WAIVERS, DEBT_REGISTER.
Gate: G-S10-ACCEPTANCE.

### S11 — Certification & Zoo
Owner: Governance / Certification.
Документы: AGENT_CERTIFICATE, COMPATIBILITY_MATRIX, SUPPORTED_MODELS, SUPPORTED_ENVIRONMENTS, KNOWN_LIMITATIONS, RELEASE_MANIFEST, EVIDENCE_INDEX.
Только после этого статус может стать CERTIFIED и компонент может войти в FATHER ZOO.
Gate: G-S11-CERTIFY.

### S12 — Production & Experience
Owner: SRE + Product + ALINA Experience.
Документы: RUNBOOK, INCIDENTS, RCA, USER_FEEDBACK, PRODUCTION_METRICS, FAILURE_CASES, REGRESSION_CASES, EXPERIENCE_RECORDS, CHANGE_REQUESTS, ADR_SUPERSEDE.
Gate: G-S12-FEEDBACK.

## 3. Запрет пропуска этапов

Поздний этап не компенсирует отсутствие обязательного раннего gate.

- успешный код не заменяет требования;
- высокий benchmark не заменяет security review;
- production stability не валидирует задним числом отсутствующую архитектуру;
- один успешный demo не заменяет воспроизводимый LAB.

## 4. Paper ↔ implementation conformance

~~~text
REQ → ARCHITECTURE → COMPONENT → CODE/COMMIT → TEST → LAB RUN → EVIDENCE → ACCEPTANCE → RELEASE → TELEMETRY
~~~

Документ без implementation/evidence link неполон. Реализация без governing requirement/design link считается architectural drift.

## 5. Change control

Изменение role, model, prompt, RAG, knowledge algorithm, skill, tool, workflow, permissions, environment, evaluator или quality threshold создаёт versioned Change Request и определяет набор повторно запускаемых gates.

## 6. Definition of Done for an Agent

Agent DONE только когда: dossier complete; Development Pack validated; implementation traceable; tests PASS; LAB PASS; environment gates PASS; mandatory acceptances signed; certificate issued; Zoo record created; runbook/rollback exist; monitoring enabled; evidence retained.

Всё остальное имеет статус DESIGN / PROTOTYPE / EXPERIMENTAL / CANDIDATE, но не production-ready.