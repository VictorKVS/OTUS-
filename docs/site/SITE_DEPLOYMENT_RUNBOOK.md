# OPS-02 · SITE DEPLOYMENT RUNBOOK

| Field | Value |
|---|---|
| Document ID | OPS-02 |
| Category | operations |
| Status | BASELINED-DESIGN |
| Owner | DevOps/SRE |
| Approver | Operations |
| Gate | G-SITE-REL |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Deploy, smoke, rollback и owner actions.

## Current baseline

Deployment должен быть воспроизводимым. После deploy — smoke links/data loading; при failure — rollback на известный artifact/commit.

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
