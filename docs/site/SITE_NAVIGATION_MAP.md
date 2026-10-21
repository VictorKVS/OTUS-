# UX-02 · SITE NAVIGATION MAP
 
| Field | Value |
|---|---|
| Document ID | UX-02 |
| Category | ux |
| Status | BASELINED-DESIGN |
| Owner | UX/Architect |
| Approver | Product Owner |
| Gate | G-SITE-UX |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Карта навигации, входы, cross-links и правила глубины.

## Current baseline

Навигация должна давать путь к ключевому рабочему экрану максимум за несколько осмысленных переходов и сохранять явные cross-links между проектированием, документами, LAB и эксплуатацией.

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
