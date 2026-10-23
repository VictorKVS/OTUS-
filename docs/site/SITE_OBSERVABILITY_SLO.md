# OPS-03 · SITE OBSERVABILITY SLO

| Field | Value |
|---|---|
| Document ID | OPS-03 |
| Category | operations |
| Status | BASELINED-DESIGN |
| Owner | SRE |
| Approver | Operations |
| Gate | G-SITE-OBS |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Logs/metrics/traces, SLI/SLO и alerts.

## Current baseline

Наблюдаем минимум availability/static errors/data-load errors/client exceptions и release version. SLO вводится только после measurable runtime.

## Mandatory content

- Preconditions and scope.
- Step-by-step controlled procedure or decision model.
- Owner, approver and escalation path.
- Required evidence/artifacts.
- PASS/WARN/FAIL/BLOCKED rules.
- Rollback/recovery/change-control requirements where applicable.

## Verification

A procedure is not considered ready until it can be followed from versioned artifacts and the expected evidence is produced.

## Evidence

Link exact commit, release, CI run, validator report, deployment artifact, incident/RCA or other applicable proof.

## Change control

Material changes are versioned. Operational changes must preserve a tested rollback/recovery path.
