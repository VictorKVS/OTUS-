# UX-01 · SITE INFORMATION ARCHITECTURE
 
| Field | Value |
|---|---|
| Document ID | UX-01 |
| Category | ux |
| Status | BASELINED-DESIGN |
| Owner | UX/Architect |
| Approver | Product Owner |
| Gate | G-SITE-UX |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Информационная архитектура и иерархия разделов сайта.

## Current baseline

Верхний уровень: Production Base / Factory / Projects / Knowledge Center / FATHER LAB / DevOps Environments / Document Conveyor / Development Pack. Внутри проекта — Overview/Architecture/Knowledge/Workflows/LAB/Runs/Evaluation/Deploy/Experience.

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
