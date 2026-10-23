# FATHER Engineering: reference + tracing + audit UI contract

Implementation status: **DESIGN ONLY**. This does not claim a working backend, FSTEC certification or protected audit storage.

## Navigation and screens
- Command center: project/lesson/task/run/agent/security status; distinguish planned and observed.
- Action panel: purpose, prerequisites, rights, risks, regulatory notes, expected results, approval and rollback.
- Timeline: trace_id across frontend, API, runner, CI, GitHub, Kubernetes; real event states.
- Evidence browser: source commits, tests, output, hashes, screenshots, reports.
- Security register: requirement -> risk -> control -> test -> evidence and coverage gaps.
- Decision & incident journal: error classification, root cause, approved remediation, retest and lessons learned.
- Memory and knowledge: source-linked agent notes distinct from append-only logs.

## Safety
No arbitrary commands. Predeclared operations only, server-side RBAC, audited approvals, redaction, immutable evidence policies, correlation IDs, least privilege, protected log retention and backups. UI must never simulate real execution success.

## Integration
Canonical specification: https://github.com/VictorKVS/OTUS_Kibirnetes/blob/feature/devsecops-github-baseline/docs/FATHER_AUDIT_TRACE_MEMORY_SPEC.md

Target entry point: factory/index.html on this branch. First implementation: local-read-only runner healthcheck for the existing Minikube problem; unit tests and safety approval gates before mutating actions.
