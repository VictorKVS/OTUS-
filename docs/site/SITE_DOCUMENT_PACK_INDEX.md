# SD-00 · SITE DOCUMENT PACK INDEX
 
| Field | Value |
|---|---|
| Document ID | SD-00 |
| Category | governance |
| Status | BASELINED-DESIGN |
| Owner | Site Documentation Owner |
| Approver | FATHER Architect |
| Gate | G-SITE-DOC |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Индекс полного Site Dossier и состояние каждого документа.

## Current baseline

Сайт уже содержит Architecture Cockpit, Production Base, Document Conveyor, Development Pack и Factory screens. Этот индекс становится единым входом в документацию.

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
