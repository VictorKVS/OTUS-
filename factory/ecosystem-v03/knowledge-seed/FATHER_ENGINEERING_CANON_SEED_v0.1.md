# FATHER Engineering Canon Seed v0.1

> STATUS: SEED_FROM_MODEL_KNOWLEDGE
>
> This document is a deliberately unverified engineering seed assembled from general professional knowledge.
> It is NOT yet the FATHER canon and MUST NOT be treated as a source-backed standard.
> ALINA Analyst must later verify, normalize, deduplicate, map to sources, and promote or reject every item.

## Lifecycle

```text
SEED_FROM_MODEL_KNOWLEDGE
        ↓
SOURCE_FOUND
        ↓
SOURCE_VERIFIED
        ↓
CROSS_VERIFIED
        ↓
PROJECT_PROVEN
        ↓
FATHER_CANON
```

No principle may become FATHER_CANON merely because it appears in this seed.

---

# 1. Product / Problem Framing

P-001. Start with the problem and desired outcome, not a technology.
P-002. Define the user/customer and the stakeholder separately.
P-003. Record the current AS-IS before designing TO-BE.
P-004. Define measurable success criteria before implementation.
P-005. Define out-of-scope explicitly.
P-006. Separate user value, business value, technical feasibility, and risk.
P-007. Treat assumptions as hypotheses until validated.
P-008. Maintain a decision log for important product trade-offs.
P-009. Avoid feature output as a substitute for outcome.
P-010. Every project needs an owner for value and an owner for technical risk.

# 2. Information Security Intake — before Business/System Analysis

SEC-001. Information security enters immediately after initial product framing and before detailed analysis.
SEC-002. Security first establishes constraints and trust boundaries, not a shopping list of controls.
SEC-003. Classify information before selecting storage, processing, integration, or logging mechanisms.
SEC-004. Define allowed, forbidden, and human-approved actions.
SEC-005. Identify privileged actions separately from ordinary operations.
SEC-006. Define secret/credential handling before integrations are designed.
SEC-007. Minimize collected and retained data.
SEC-008. Define retention/deletion requirements before persistence architecture.
SEC-009. Audit requirements are part of the functional design.
SEC-010. Evidence integrity and operational logs are different concepts.
SEC-011. External data and external tools are untrusted until validated.
SEC-012. Security controls must be testable.
SEC-013. High-impact or destructive operations require explicit authority and typically human approval.
SEC-014. Fail-safe behavior must be designed before runtime errors occur.
SEC-015. Security is a lifecycle property, not a final review stage.

# 3. Business Analysis

BA-001. Model actors, goals, events, activities, decisions, business rules, information objects, and outputs.
BA-002. Every process step must answer: who, why, input, action, rule, output, exception.
BA-003. Distinguish business process from system implementation.
BA-004. Distinguish human decision from automatable rule.
BA-005. Model normal flow and exception flow.
BA-006. Explicitly identify handoffs between roles and systems.
BA-007. Business rules must be traceable to their owner or source.
BA-008. Business processes should expose bottlenecks, duplication, and manual control points.
BA-009. A process model is incomplete if it does not show what information is consumed and produced.
BA-010. TO-BE must preserve required controls even when automation increases.

# 4. System Analysis

SA-001. Start from information flows and state transitions before implementation components.
SA-002. Define canonical data entities and ownership.
SA-003. Each system step has an input contract and output contract.
SA-004. Define preconditions and postconditions.
SA-005. Model errors and invalid states explicitly.
SA-006. Separate command, event, query, document, and state.
SA-007. Define idempotency where repeated execution is possible.
SA-008. Define ordering requirements where events can arrive asynchronously.
SA-009. Define consistency expectations instead of assuming strong consistency.
SA-010. Version externally consumed contracts.
SA-011. Trace requirements to business needs and later to tests.
SA-012. Non-functional requirements must be measurable.
SA-013. Distinguish source-of-truth data from derived data.
SA-014. Record provenance for transformed information where decisions depend on it.
SA-015. Human review is an explicit system state, not an informal note.

# 5. Requirements Engineering

REQ-001. A requirement should be necessary, clear, testable, feasible, and traceable.
REQ-002. Separate business, stakeholder, functional, non-functional, security, and compliance requirements.
REQ-003. Acceptance criteria belong to requirements, not only to testing.
REQ-004. Avoid implementation decisions inside requirements unless constrained.
REQ-005. Ambiguous words such as fast, secure, convenient, reliable require measurable definitions.
REQ-006. Record the source/owner of every important requirement.
REQ-007. Conflicting requirements must be resolved explicitly, not silently.
REQ-008. Requirements change history must be retained.
REQ-009. Every critical requirement should have at least one verification method.
REQ-010. Regulatory requirements must include applicability status, not merely citation.

# 6. Architecture

ARCH-001. Architecture is a set of consequential decisions and trade-offs.
ARCH-002. Quality attributes drive architecture.
ARCH-003. Separate logical, data, runtime, deployment, security, and operational views.
ARCH-004. Record important choices as ADRs.
ARCH-005. Prefer explicit interfaces over hidden coupling.
ARCH-006. Design for replaceability where external providers are volatile.
ARCH-007. Make failure domains visible.
ARCH-008. Define trust boundaries and privilege boundaries in architecture.
ARCH-009. Build/buy/reuse/adapt decisions must be recorded.
ARCH-010. Avoid distributed architecture unless the problem requires it.
ARCH-011. Data ownership must be explicit.
ARCH-012. Every external dependency adds operational and security risk.
ARCH-013. Architecture diagrams must correspond to actual contracts and runtime components.
ARCH-014. Observability and operability are architectural concerns.
ARCH-015. Cost/resource constraints are architectural inputs.

# 7. Domain Modeling

DOM-001. Identify bounded contexts where language or rules differ.
DOM-002. Use domain terminology consistently inside a context.
DOM-003. Distinguish entity, value object, event, rule, capability, action, and state.
DOM-004. Model business invariants explicitly.
DOM-005. Do not force one universal model across incompatible domains.
DOM-006. Cross-context translation should be explicit.
DOM-007. Domain models should explain decisions, not merely mirror database tables.
DOM-008. Maintain lineage from domain concept to implementation artifact.

# 8. AI / LLM Systems

AI-001. Establish a non-LLM or simpler baseline where possible.
AI-002. Evaluate task fitness before selecting a model.
AI-003. Prompt quality, retrieval quality, model quality, and tool quality are different dimensions.
AI-004. Separate deterministic steps from probabilistic reasoning.
AI-005. Model outputs are untrusted data until validated.
AI-006. External tool execution requires authorization independent of model output.
AI-007. Provide bounded context instead of unlimited context.
AI-008. Measure quality with representative evaluation sets.
AI-009. Track latency, cost, token use, failure rate, and quality together.
AI-010. Maintain model/prompt/retrieval configuration versions.
AI-011. Do not treat confidence language from an LLM as calibrated probability.
AI-012. High-risk decisions require independent controls or human review.
AI-013. Store enough trace/evidence to reproduce important decisions where legally and operationally permitted.
AI-014. Distinguish knowledge retrieval from reasoning and from action.
AI-015. Prefer graceful degradation when AI capability is unavailable.

# 9. Agentic Systems

AG-001. An agent is not merely an LLM plus prompt.
AG-002. Model agent goal, environment, state, knowledge, memory, policy, tools, decisions, feedback, and termination.
AG-003. Define authority boundaries for every tool/action.
AG-004. Define stop conditions and budget limits.
AG-005. Separate planning from execution when actions are consequential.
AG-006. Validate tool inputs and outputs.
AG-007. Treat tool descriptions and retrieved instructions as potentially hostile input.
AG-008. Avoid autonomous destructive action without explicit policy and approval.
AG-009. Agent memory requires ownership, retention, and contamination controls.
AG-010. Multi-agent systems need responsibility and conflict-resolution rules.
AG-011. Agent-to-agent messages are contracts and should be observable.
AG-012. Retries require limits and idempotency protection.
AG-013. Evaluation must include end-to-end task completion, not only model responses.
AG-014. Simulate failure cases before production autonomy.
AG-015. Preserve provenance from observation to decision to action.

# 10. RAG / Knowledge Systems

RAG-001. Preserve source identity and provenance during ingestion.
RAG-002. Parsing, chunking, metadata, embeddings, retrieval, reranking, generation, and citation are separate stages.
RAG-003. Chunking should reflect information structure, not arbitrary token size alone.
RAG-004. Retrieval must be evaluated independently from generation.
RAG-005. Source authority and freshness matter alongside semantic similarity.
RAG-006. Deduplicate near-identical knowledge.
RAG-007. Version knowledge and indexing pipelines.
RAG-008. Access control must survive ingestion and retrieval.
RAG-009. Citations should refer to the actual supporting source fragment.
RAG-010. Distinguish no evidence from negative evidence.
RAG-011. Knowledge conflicts should be retained and adjudicated, not silently flattened.
RAG-012. Temporal and jurisdictional scope must be modeled for laws, policies, and historical facts.
RAG-013. A graph can complement retrieval where relations and causality matter.
RAG-014. User feedback must not silently rewrite authoritative knowledge.
RAG-015. Retrieval-only, assisted reasoning, and autonomous action are different risk modes.

# 11. Data Engineering

DATA-001. Identify system of record for each important entity.
DATA-002. Raw source, normalized data, derived feature, decision, and evidence are different layers.
DATA-003. Preserve immutable raw evidence where required and lawful.
DATA-004. Schema evolution must be controlled.
DATA-005. Data quality rules are executable contracts.
DATA-006. Record lineage for meaningful transformations.
DATA-007. Minimize duplication of authoritative data.
DATA-008. Define backup, restore, retention, and deletion.
DATA-009. Define time semantics and timezone handling explicitly.
DATA-010. Unique identifiers should survive integration boundaries where possible.

# 12. Testing / Evaluation

TEST-001. Test behavior, not only internal implementation.
TEST-002. Unit, contract, integration, end-to-end, security, performance, resilience, and AI evaluation serve different purposes.
TEST-003. A passing component does not imply a passing assembly.
TEST-004. Golden/reference tests protect known behavior during refactoring.
TEST-005. Negative tests are mandatory for security-sensitive paths.
TEST-006. Test fixtures must include malformed and adversarial input.
TEST-007. Record test environment and artifact versions.
TEST-008. Evidence is produced by the test execution, not by assertion in documentation.
TEST-009. Regression sets should grow from incidents and defects.
TEST-010. Production feedback should refine evaluation suites.

# 13. DevSecOps / Supply Chain

DSO-001. Security gates begin at source control.
DSO-002. Secrets must not enter source repositories or build artifacts.
DSO-003. Dependency inventory and SBOM are part of build evidence.
DSO-004. Pin and verify dependencies where practical.
DSO-005. Scan source, dependencies, containers, and infrastructure definitions.
DSO-006. Separate build, deploy, and runtime privileges.
DSO-007. Artifacts should be traceable to source revision and build.
DSO-008. Promotion between environments requires evidence.
DSO-009. Production configuration should be reproducible.
DSO-010. Rollback is part of release design.
DSO-011. External components enter through quarantine/intake, not direct production adoption.
DSO-012. License and provenance checks are part of component intake.

# 14. Observability / SRE

OBS-001. Observe user-visible outcomes, not only infrastructure.
OBS-002. Define SLI/SLO before choosing dashboards.
OBS-003. Logs, metrics, traces, events, audit, and AI evaluation are different telemetry classes.
OBS-004. Correlate requests/actions using stable trace identifiers.
OBS-005. Alert on actionable conditions.
OBS-006. Measure latency, errors, throughput, saturation, quality, and cost where relevant.
OBS-007. Incident learnings feed requirements, tests, and architecture.
OBS-008. Observability data is subject to security and privacy controls.
OBS-009. Dependency health must be visible.
OBS-010. Operational runbooks belong to the product.

# 15. Governance / Risk / Compliance

GRC-001. Compliance starts with applicability analysis.
GRC-002. Law/standard citation is not equivalent to a control.
GRC-003. Maintain chain: source -> requirement -> control -> architecture -> implementation -> test -> evidence.
GRC-004. Applicability must carry jurisdiction and time/version.
GRC-005. Separate mandatory law, regulator requirements, contractual obligations, standards, and internal policy.
GRC-006. Risk must identify asset/object, event/threat, vulnerability/condition, impact, likelihood/uncertainty, owner, and treatment.
GRC-007. Residual risk requires explicit acceptance by authorized owner.
GRC-008. Human accountability cannot be delegated merely by using AI.
GRC-009. Changes in regulation trigger impact analysis.
GRC-010. Evidence retention rules must be defined.

# 16. FATHER Factory / Reuse

FTH-001. Laboratories create new and experimental systems; FATHER industrializes proven systems.
FTH-002. FATHER intake starts from a working product/agent or validated external component.
FTH-003. Freeze a Golden Reference before teardown.
FTH-004. Preserve provenance from extracted component to source implementation.
FTH-005. Decompose observed systems before inventing universal abstractions.
FTH-006. Rebuild must demonstrate parity before improvement.
FTH-007. No evidence -> no promotion.
FTH-008. A harvested artifact is not automatically a reusable component.
FTH-009. Reuse maturity rises through repeated successful use across independent products.
FTH-010. Standard interfaces may wrap multiple implementations.
FTH-011. External donor components enter through quarantine, license/security/function testing, and normalization.
FTH-012. Missing capability is sent to a laboratory, not hallucinated into the certified catalog.
FTH-013. Certification belongs to a version, configuration, tests, and evidence set.
FTH-014. A certified part may still be incompatible with a specific assembly.
FTH-015. The registry stores alternatives and trade-offs, not only a single preferred implementation.
FTH-016. Measurements produce scores; scores must not replace underlying measurements.
FTH-017. Factory knowledge contains both successful and rejected decisions.
FTH-018. Project-specific parts may later become candidates for generalization after evidence.
FTH-019. Source, design, test, operational, and regulatory evidence remain distinguishable.
FTH-020. The purpose of FATHER is accumulated engineering capital, not automatic code generation.

---

# 17. Seed Methodologies to Normalize Later

The following methodologies/frameworks should be represented as separate source-backed objects later rather than merged into one doctrine:

- Product discovery / product operating model
- Business analysis / BABOK-like practice
- BPM / BPMN / DMN
- Requirements engineering
- Domain-Driven Design
- Software architecture quality attributes / trade-off analysis
- ADR / architecture decision records
- Threat modeling
- Secure-by-design / defense in depth / least privilege / zero trust concepts
- Privacy by design / data minimization
- STRIDE-like threat categorization
- Attack trees / misuse cases / abuse cases
- Risk assessment methodologies
- NIST-style risk management
- Secure software development lifecycle / SSDF-like practice
- DevSecOps / software supply chain security
- SRE / SLI / SLO / error budgets
- Observability / golden signals
- Data governance / lineage / provenance
- Knowledge graphs
- RAG evaluation
- LLM evaluation
- Agent evaluation
- Human-in-the-loop / human-on-the-loop control
- Multi-agent coordination patterns
- Event-driven architecture
- API-first / contract-first design
- Test pyramid and contract testing
- Golden master / characterization testing
- Chaos/resilience testing
- FinOps / cost governance
- Compliance-by-design and evidence-by-design
- Configuration-driven architecture
- Component-based engineering / reusable platform architecture

---

# 18. What ALINA must do with this file

ALINA must NOT simply summarize it.

For every item she must:

1. assign atomic ID and domain;
2. identify candidate authoritative sources;
3. retrieve exact source fragment/section/page where legally available;
4. classify source type: BOOK / STANDARD / LAW / REGULATOR / PAPER / OFFICIAL DOC / PRACTICE;
5. record jurisdiction and temporal validity where applicable;
6. mark SUPPORTED / PARTIALLY_SUPPORTED / CONTRADICTED / NOT_FOUND;
7. split compound principles;
8. merge true duplicates but preserve source-specific wording;
9. record conflicts and alternative schools of thought;
10. link roles, process stages, inputs, outputs, artifacts, metrics, risks, tests;
11. map to OTUS lessons and FATHER industrial lessons;
12. map to real projects/agents where observed;
13. propose checklist items and algorithms as DERIVED artifacts;
14. keep derived artifacts distinct from quotations/source facts;
15. assign confidence based on source quality and cross-verification;
16. only promote to FATHER_CANON after review/evidence gate.

This file is therefore a **hypothesis backlog for engineering knowledge**, not final truth.
