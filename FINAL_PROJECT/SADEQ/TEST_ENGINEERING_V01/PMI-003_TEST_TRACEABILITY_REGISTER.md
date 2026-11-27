# ПМИ-003 — Реестр испытаний от источника до доказательства
**Статус:** MATRIX DRAFT, все EVIDENCE = NOT_RUN по новой ПМИ.

| TEST-ID | Source Req | Contract/Flow | Threat / restriction | Method passport | Expected proof | Execution |
|---|---|---|---|---|---|---|
| API-001 | TZ 4.1.3 / FR-NEW-02/09 | FLOW-01, SI-01/02/03 | BOLA / identity spoof / foreign tenant | [PMI-002](PMI-002_CASE_API001_TENANT_ISOLATION.md) | no data/effect, deny trace | NOT_RUN |
| API-002 | FR-NEW-02 | InboundIncidentV1, SI-04/14 | unknown/duplicate JSON field | TO_WRITE | 422 before event | NOT_RUN |
| API-003 | FR-NEW-01 | InboundIncidentV1 | positive authorized incident ingest | TO_WRITE | schema + receipt | NOT_RUN |
| API-004 | FR-NEW-08 | ActionProposalV1, C09 | invalid tool/params & expected-postcondition mismatch | TO_WRITE | contract/semantic deny | NOT_RUN |
| ACT-001 | FR-NEW-09/10 | ApprovalDecisionV1, SI-09/10 | expired/modified approval and stale state | TO_WRITE | zero unauthorized tool calls | NOT_RUN |
| ACT-002 | FR-NEW-11 | FLOW-09, SI-11 | HTTP200 without correct state | TO_WRITE | MISMATCH + incident | NOT_RUN |
| ACT-003 | FR-NEW-11 | SI-12 | ambiguous tool timeout and retry | TO_WRITE | reconciled with no duplicate effect | NOT_RUN |
| EVT-001 | FR-NEW-03/04 | B02 ALG-02..05 | duplicate and inconsistent state | TO_WRITE | one event/state replay hash | NOT_RUN |
| RAG-001 | FR-NEW-05/06 | B03, SI-03/07 | foreign tenant chunk and malicious SOP | TO_WRITE | no leak, cited answer | NOT_RUN |
| SEC-API-04 | TZ 4.1.7 / SI-13 | C17 | body/rate/token exhaustion | TO_WRITE | bounded limits | NOT_RUN |
| SEC-API-07 | SI-08 | C12 | SSRF/unregistered tool host | TO_WRITE | deny egress/tool | NOT_RUN |
| QUAL-001 | FR-NEW-13 | B07, SI-18 | agent self-qualifies / tamper holdout | TO_WRITE | access denied and report | NOT_RUN |

## Milestones
- M-TEST-DESIGN: complete all mandatory passports, source clause verification, fixed expected HTTP/status/state and evidence rules.
- M-TEST-IMPLEMENT: develop executable tests **after** reviewed passports; no changing expected result solely to match code.
- M-TEST-EXECUTE: record raw evidence and findings.
- M-QUALIFY: independent security/POLYGON re-execution with precise artifact hashes and human release signoff.
