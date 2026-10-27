# SEC-02 · SITE SECURITY CONTROLS

| Field | Value |
|---|---|
| Document ID | SEC-02 |
| Category | security |
| Status | BASELINED-DESIGN |
| Owner | Security |
| Approver | Security Lead |
| Gate | G-SITE-SEC |
| Version | 0.1.0 |
| Applies to | FATHER / OSUT site + Factory Control Center |

## Purpose

Контроли CSP, secrets, dependency, content, auth и audit.

## Current baseline

Минимум: no secrets in client/repo, dependency review, content/schema validation, CSP when hosted, least privilege, audit/evidence and safe external links.

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
