# QA-05 · SITE SEO METADATA

| Field | Value |
|---|---|
| Document ID | QA-05 |
| Category | quality |
| Status | BASELINED-DESIGN |
| Owner | Content/Frontend |
| Approver | Product Owner |
| Gate | G-SITE-SEO |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Title/description/canonical/robots/social metadata и indexing policy.

## Current baseline

Внутренние control-center страницы могут иметь noindex policy; публичные страницы получают уникальные title/description/canonical только после определения deployment URL.

## Mandatory content

- Scope, assumptions and protected assets for this document.
- Required controls/criteria expressed in verifiable terms.
- Explicit distinction between DESIGN/TARGET and measured production evidence.
- Links to affected pages, registries, code, tests and release evidence.
- PASS/WARN/FAIL/BLOCKED decision rules.
- Versioning, owner and change-control requirements.

## Verification

Result model: `PASS / WARN / FAIL / BLOCKED`.

A missing prerequisite or missing evidence produces **BLOCKED**, not PASS.

## Evidence

Evidence references exact file/page/registry/test/commit where applicable. Screenshots or prose alone do not replace executable contract/test evidence when such evidence is available.

## Change control

Material changes require version bump and rerun of affected gates. Security/privacy/data-contract changes require explicit review before release.
