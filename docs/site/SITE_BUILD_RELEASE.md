# OPS-01 · SITE BUILD RELEASE

| Field | Value |
|---|---|
| Document ID | OPS-01 |
| Category | operations |
| Status | BASELINED-DESIGN |
| Owner | FATHER Programmer/DevOps |
| Approver | SRE |
| Gate | G-SITE-REL |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Build, artifact, versioning, release и provenance.

## Current baseline

Каждый release связывается с commit SHA, document pack version, contract validation и release evidence.

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
