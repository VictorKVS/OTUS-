# DMN-style decision table · SEC-DEC-001
**Decision:** may agent invoke tool? **Hit policy:** FIRST matching row in priority order. **Status:** model, not running DMN engine.

| Priority | ACL / tenant | High-risk/prohibited | Qualified version | Evidence | Requires approval | Human approval | Decision |
|---|---|---|---|---|---|---|---|
| 1 | FAIL | — | — | — | — | — | DENY |
| 2 | PASS | YES | — | — | — | — | BLOCK |
| 3 | PASS | NO | INVALID/EXPIRED | — | — | — | DENY |
| 4 | PASS | NO | VALID | CONFLICTED/INSUFFICIENT | — | — | REVIEW_REQUIRED |
| 5 | PASS | NO | VALID | SUFFICIENT | YES | NO/TIMEOUT | DENY |
| 6 | PASS | NO | VALID | SUFFICIENT | YES | PENDING | APPROVAL_REQUIRED |
| 7 | PASS | NO | VALID | SUFFICIENT | YES | APPROVED | ALLOW |
| 8 | PASS | NO | VALID | SUFFICIENT | NO | — | ALLOW_BOUNDED |
| 9 | OTHER | — | — | — | — | — | DENY |

Interpretation: `BLOCK` and `REVIEW_REQUIRED` never dispatch tool calls. `ALLOW_BOUNDED` means read-only or explicitly allowlisted low-risk reversible actions with per-agent/tenant limits. Assignment of HIGH_RISK is independently governed and cannot be overridden by an agent prompt. Deny on parser errors, missing data, stale policies or engine outage.

**Important safety scope:** autonomous identification of targets or use of force is not supported. Classification ambiguity involving protected civilian objects triggers no action and review, not a numerical risk score override.
