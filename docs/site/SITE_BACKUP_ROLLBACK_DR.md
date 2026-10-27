# OPS-04 · SITE BACKUP ROLLBACK DR

| Field | Value |
|---|---|
| Document ID | OPS-04 |
| Category | operations |
| Status | BASELINED-DESIGN |
| Owner | SRE |
| Approver | Architecture Review |
| Gate | G-SITE-DR |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Backup/restore, rollback, RTO/RPO targets и DR drill.

## Current baseline

Для static site recovery основа — Git history + reproducible deployment artifact; stateful backend/data backup добавляется при появлении соответствующих сервисов.

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
