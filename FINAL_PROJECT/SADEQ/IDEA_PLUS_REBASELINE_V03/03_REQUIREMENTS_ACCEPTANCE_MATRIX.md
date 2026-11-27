# SADEQ-RTM-003 — матрица требований, стадий и приёмки
**Статус:** DRAFT; expected tests are acceptance design, not completed tests.
| REQ | Phase | ALG/Block | Scenario | Evidence to collect | Status |
|---|---|---|---|---|---|
| FR-NEW-01 | P0 | B01, ALG-01 | API+PDF/DOCX source intake | API requests + document parser fixtures | NOT_RUN |
| FR-NEW-02 | P0 | ALG-01 | unknown nested field | validator logs REJECT, no side effect | NOT_RUN |
| FR-NEW-03 | P0 | ALG-02/03 | concurrent duplicate, tenant duplicate external key | unique row+object ID or review | NOT_RUN |
| FR-NEW-04 | P0 | ALG-04/05 | replay after restart | same state hash/version | NOT_RUN |
| FR-NEW-05 | P0 | B03 | import and chunk provenance | cited source/rights/sha per chunk | NOT_RUN |
| FR-NEW-06 | P0 | ALG-07 | question against approved local corpus | citations, recall evaluation, ACL denial | NOT_RUN |
| FR-NEW-07 | P0 | B04 | retry/restart/loop limit | checkpoint and bounded trace | NOT_RUN |
| FR-NEW-08 | P0 | ALG-10 | typed action draft | strict schema + evidence refs | NOT_RUN |
| FR-NEW-09 | P0 | ALG-11 | stale human approval, cross-tenant attempt | DENY + audit | NOT_RUN |
| FR-NEW-10 | P0 | ALG-11 | create/update mock ticket | one authorized tool receipt | NOT_RUN |
| FR-NEW-11 | P0 | ALG-12 | HTTP 200 but no data state change | MISMATCH and incident | NOT_RUN |
| FR-NEW-12 | P0 | B08 | trace full e2e | metrics+model/build/source hashes | NOT_RUN |
| FR-NEW-13 | P0 | B07 | run POLYGON independent tests | signed report and evidence refs | NOT_RUN |
| FR-NEW-14 | P0 | B08 | no external AI/network use | packet capture/deny egress | NOT_RUN |
| FR-NEW-15 | P1 | B03 | multi-hop graph relation retrieval | verified graph path + vector comparison | NOT_RUN |
| FR-NEW-16 | P1 | B06 | 3 config profiles same core | manifest diff and tests | NOT_RUN |
| FR-NEW-17 | P1 | B08 | K8s rollout/restore | logs/recovery proof | NOT_RUN |
| FR-NEW-18 | P1 | B08 | benchmark and budget | p95/TTFT/VRAM/cost with workload | NOT_RUN |
| FR-NEW-19 | P2 | B06 | patch and tests from sandbox | review + user commit | NOT_RUN |
| FR-NEW-20 | P2 | B03/B04 | reviewed feedback and forecasting | holdout/backtest and approval | NOT_RUN |

## Release gate P0
A qualified P0 candidate demonstrates one end-to-end case **at its exact source/model/config hashes**; no critical data leak, unauthorized action or missing provenance; all P0 test rows completed and independently reviewed. No fabricated test values. Baseline SLO threshold must be agreed before final exam.

## Requirement numbering
FR-NEW avoids accidental collision with FR-01..16 PRD and FR-01..14 IDEA v0.2. For each legacy requirement record `KEEP`, `DEFER`, `CHANGE` in [change matrix](04_CHANGE_IMPACT_V02_TO_V03.md). No silent deletion.
