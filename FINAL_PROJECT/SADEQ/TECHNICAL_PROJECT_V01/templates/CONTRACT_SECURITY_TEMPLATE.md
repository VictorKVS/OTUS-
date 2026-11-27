# FATHER-CSSC-001 / CONTRACT TEMPLATE — copy per FLOW-ID
**Status:** TEMPLATE ONLY. All TBD must be resolved before approval.

## Identity / purpose
- Contract ID / Version / Owner / Reviewers / Approvers:
- Requirements FR / ALG / CMP / FLOW / TEST / THR / SRC:
- Business purpose and explicit out-of-scope:
- Trusted sender service principal (authentication evidence):
- Trusted recipient service principal (mutual authenticity):
- End user, tenant and delegation chain (origin of authority):
- Resource ownership (source of truth, tenant, field classification):

## Exact behavior
- Preconditions:
- Closed request schema version and maximum body/nesting/list/string constraints:
- Closed response schema and masked fields:
- Invariants (MUST ALWAYS):
- Postcondition / independent authoritative verification:
- Allowed state transitions:
- Allowed tool / resource / destination / egress:
- Typed errors and response status:

## Explicit prohibitions (MUST NOT)
| PROHIBITION_ID | What is strictly prohibited | Enforcement point outside LLM | Negative TEST_ID / expected failure |
|---|---|---|---|
| D-01 | Unknown input/output fields | parser/serializer | |
| D-02 | Impersonation or tenant/user assignment from body | authenticated auth-context | |
| D-03 | Read/write other object or field without policy | per-object/property UAG/ACL | |
| D-04 | Arbitrary tool target/shell/network | allowlisted scoped adapter | |
| D-05 | Tool execution via unapproved action | UAG + human consent gate | |
| D-06 | Replay/stale approval/state races | atomic receipt/TTL/state version | |
| D-07 | Disclosure in logs/errors/citations | redacted log and retrieval ACL | |
| D-08 | Unbounded GPU/CPU/cost/time | budget + quota + cancellation | |
| D-09 | Claim verified result from HTTP status only | authoritative read-after-write | |
| D-10 | Self-qualification / modifying holdout | independent POLYGON | |

## Execution/recovery
- Idempotency key origin, replay window, conflict response:
- Transaction/outbox/locks:
- Rate limit per subject/tenant, body cap, max concurrency/tokens/timeout:
- Retry categories, exponential backoff budget:
- Timeout-after-send reconciliation; EXECUTION_UNKNOWN handling:
- Locking/optimistic compare-and-swap state version:

## Threats and evidence
- OWASP API Top 10 categories and agent-specific attack surfaces:
- STRIDE/threat/risk IDs + compensating controls:
- TLS/mTLS/OIDC/OAuth mode; issuer/audience/expiry/rotation:
- Sensitive data source rights, retention/deletion and redaction:
- Positive TEST IDs:
- Negative TEST IDs (one or more per MUST NOT):
- Fuzz/property/concurrency/load TEST IDs:
- Evidence store, exact build/model/policy/schema/source hashes:
- Reviewer / independent examiner / release authority:
- Decision: DRAFT / REVIEW_REQUIRED / APPROVED_FOR_TEST / IMPLEMENTED / VERIFIED / QUALIFIED.

**Freeze rule:** Blank security source, permission owner, constraint, evidence or control → cannot be labelled contract qualified.
