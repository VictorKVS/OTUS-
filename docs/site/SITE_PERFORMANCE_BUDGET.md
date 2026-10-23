# QA-03 · SITE PERFORMANCE BUDGET

| Field | Value |
|---|---|
| Document ID | QA-03 |
| Category | quality |
| Status | BASELINED-DESIGN |
| Owner | SRE/Frontend |
| Approver | FATHER Architect |
| Gate | G-SITE-PERF |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Бюджет размера, загрузки, latency и rendering.

## Current baseline

Performance budget фиксируется измерением, а не обещанием. До baseline реальные thresholds помечаются TARGET и подтверждаются Lighthouse/browser profiling.

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
