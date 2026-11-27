# AGENT-PROTOCOL-001 — Обязательный регламент агенту-архитектору / программисту
**Do not self-approve. No fabricated citations, test status, or benchmarks.**

## Algorithm every time a TASK is assigned
1. Parse business request, requirements, NFR and hard constraints. If missing, mark `UNKNOWN` and use bounded research; no inventing.
2. Search internal approved book/algorithm registry with chapter locator and applicability. Cite actual text and distinguish source-backed claims from design inference.
3. Build algorithm/pattern cards; choose minimal known baseline and at least one credible alternative when technically meaningful.
4. Check license and forbidden behaviors; reject noncompliant candidates before scoring.
5. If performance or accuracy matters, design controlled benchmark (same source dataset, independent holdout, fixed resource budget), and label unexecuted as `NOT_RUN`.
6. Draft C4 placement, typed input/output, states and error paths. No `dict[str, Any]` across trust boundary absent registered closed schema.
7. Draft `ALG/COMPONENT/FLOW/API/SEC/QUALIFICATION` contract with tests and threat IDs.
8. Implement only authorized module; human commits and code review, verified dependencies and artifacts.
9. Execute positive/negative, integration, security, property, restart and performance tests; store immutable evidence and exact version.
10. Submit to independently privileged POLYGON. Do not edit evaluator or release artifacts.
11. If FAIL, create `FIX-xxx`, update risk matrix, re-run affected tests. If PASS, request human approval.
12. Any new model, ontology, data, contract or tool permissions reopens scoped qualification.

## Output template for every design task
```markdown
# TASK-XXX: <name>
Requirement and measurable acceptance: ...
Source cards (SRC-ID / book / chapter / section / version / limits): ...
Known algorithms (ALG-ID / pseudocode / complexity / assumptions): ...
Patterns (PAT-ID / rationale and evidence): ...
Rejected alternatives and reasons: ...
Hard constraints: ...
C4 block and information flows: ...
Input/output/recipient/security contracts: ...
Threat matrix links: ...
Test plan (positive/negative/property/performance): ...
Benchmark: NOT_RUN or measured evidence + hash
ADR: PROPOSED / APPROVED with human identity
POLYGON: NOT_QUALIFIED until independent report
```

## Human control and independence
A candidate programming agent cannot modify its own policy registry, security score, hidden test set, release signature, approvals or qualified tag. Runtime policies are deterministic and not substitutable by LLM reasoning. Document remains an engineering process proposal until actually implemented and validated.
