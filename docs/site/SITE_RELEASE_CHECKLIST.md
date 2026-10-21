# OPS-06 · SITE RELEASE CHECKLIST

| Field | Value |
|---|---|
| Document ID | OPS-06 |
| Category | operations |
| Status | BASELINED-DESIGN |
| Owner | Release Manager |
| Approver | Governance |
| Gate | G-SITE-REL |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Передрелизный checklist всех обязательных gates.

## Current baseline

Release запрещён без docs/contract/tests/security/links/accessibility/smoke/rollback evidence согласно применимому профилю.

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
