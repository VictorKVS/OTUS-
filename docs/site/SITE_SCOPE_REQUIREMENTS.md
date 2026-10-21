# SD-02 · SITE SCOPE REQUIREMENTS
 
| Field | Value |
|---|---|
| Document ID | SD-02 |
| Category | governance |
| Status | BASELINED-DESIGN |
| Owner | ALINA Analyst |
| Approver | FATHER Architect |
| Gate | G-SITE-REQ |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Scope, FR/NFR, acceptance references и ограничения сайта.

## Current baseline

Текущий scope: site/* и factory/*; основные capability views — Projects/Factory/LAB/Knowledge/DevOps/Document Conveyor/Development Pack. Cyber Range остаётся PLANNED.

## Mandatory content

- Назначение и границы документа.
- Текущий baseline и отличия DESIGN/TARGET от реально доказанного состояния.
- Обязательные требования/решения для этой области.
- Проверки и критерии PASS/FAIL/BLOCKED.
- Связь с кодом, registry/data contracts и evidence.
- Правила версионирования и change control.

## Verification

Result model: `PASS / WARN / FAIL / BLOCKED`.

- **PASS** — content exists, is internally consistent and has required evidence.
- **WARN** — non-blocking deviation is recorded with owner/rationale.
- **FAIL** — requirement is violated.
- **BLOCKED** — evidence/dependency is missing, so the document cannot be approved.

## Evidence

Evidence should reference exact page/file/registry/test/commit where applicable. A statement marked TARGET/DESIGN is not production evidence.

## Change control

Any material change is versioned. Architecture/security/data-contract changes must reference an ADR or Change Request and rerun affected site gates.
