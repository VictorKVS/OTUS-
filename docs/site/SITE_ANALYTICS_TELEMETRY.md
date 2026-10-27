# QA-06 · SITE ANALYTICS TELEMETRY

| Field | Value |
|---|---|
| Document ID | QA-06 |
| Category | quality |
| Status | BASELINED-DESIGN |
| Owner | Product/SRE |
| Approver | Privacy |
| Gate | G-SITE-OBS |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

События продукта, техническая telemetry и privacy-safe измерения.

## Current baseline

Product analytics отделены от operational telemetry. События не должны включать secrets, raw sensitive prompts или персональные данные без необходимости.

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
