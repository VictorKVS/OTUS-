# SADEQ Contract-first TDD Gate — 2026-11-28
**Status:** TEST_FIRST_EXECUTED_LOCALLY / FULL_P0_NOT_QUALIFIED.

## Decision
From this point, SADEQ API will be written **against pre-agreed security and behavior tests** rather than writing tests retrospectively for the current code. This gate implements the principles in [TP-005](TP-005_CONTRACT_STRICT_SECURITY_STANDARD.md) and [negative test matrix](tests/TP005_API_SECURITY_TEST_MATRIX.md). No automatic reduction of MUST NOT to get a green suite.

## Actual local test execution
A separate ZIP artifact `SADEQ_CONTRACT_FIRST_TDD_V01.zip` was created in the conversation filesystem (not committed as ZIP to GitHub). ZIP SHA256: `8de7e8c727e0c6ff92382bc18acf1b0bf88647b9c5ee2711aec8733aed1776af`; 5 files, 5,604 bytes; archive integrity verified.

Test target: prior prototype `SADEQ_MVP_P0_SLICE_001` (FastAPI/SQLite/synthetic identity headers). Command: `python -m pytest -q -p no:cacheprovider tests/test_contract_green.py` and separately `... tests/test_contract_red.py`.
Observed in current isolated assistant environment (not Windows or POLYGON):
- **4 passed** green baseline tests.
- **5 failed** against new requirements. These are **intentional red tests** documenting current non-compliance, not green evidence.

## First five failing requirements
| RED | Contract / Security Invariant | Observed actual | Expected by contract | Development action |
|---|---|---|---|---|
| R001 | SI-01/02, trusted identity | spoofable `X-Demo-*` accepted (201) | unauthenticated call 401 | replace demo identities with a verified auth provider and secure test fixtures |
| R002 | FLOW-01 InboundIncidentV1 | valid bounded `indicators[]` rejected (422) | 201 | align Pydantic model with approved JSON Schema |
| R003 | SI-14 duplicate JSON keys | duplicate `priority` accepted (201) | 400/422 | strict decoder duplicate-key rejection |
| R004 | FLOW-07 ApprovalDecisionV1 | schema_version/proposal_id/approved_state_version rejected (422) | 200 on valid approved action | align decision schema, verify authoritative version |
| R005 | C09 response version | ingest response lacks schema_version | response schema version present | define and enforce ResponseEnvelopeV1 |

The RED test suite must remain active and must not be marked `XFAIL` for release or silently removed. Passing green tests cannot override a RED security test.

## Traceability
`SRC → REQ → FLOW → SECURITY MUST/MUST NOT → TEST → CODE → EVIDENCE → POLYGON`.
For next release: author all planned negative tests before endpoint implementation, including BOLA, BOPLA, BFLA, SSRF, excessive resource use, TOCTOU, replay, prompt injection, RAG tenant isolation and independent qualification.

## Reproduction notes
- ZIP folder `SADEQ_CONTRACT_FIRST_TDD_V01` should be extracted **as a sibling** of `SADEQ_MVP_P0_SLICE_001` on Windows. This is a TDD suite, not a second API.
- The earlier prototype is DEMO ONLY; local success is not proof of production authentication, encryption, endpoint security or policy qualification.
- The executable tests currently target the first 5 high-priority deficits; the complete TP-005 threat matrix is still planned, NOT_RUN.

## Новый порядок: ПМИ перед TDD
[ПМИ-001](../TEST_ENGINEERING_V01/PMI-001_PROGRAM_AND_METHODS.md) и [заполненный пример API-001](../TEST_ENGINEERING_V01/PMI-002_CASE_API001_TENANT_ISOLATION.md) являются проектной нормативно-методической основой до следующей итерации кода. Предварительные локальные 4 PASS / 5 FAIL — не приёмочные протоколы и не POLYGON evidence.
