# OTUS Lesson 09 — FATHER OSINT Agent / CTO Challenge & LLM Hosting ADR

**Project:** `VictorKVS/OSINT_deepseek`  
**Status:** `READY FOR HOMEWORK REVIEW`

## Decision

For the **current PoC/MVP semantic-model phase**, use a **hosted LLM API behind a replaceable Model Gateway** only for data explicitly approved for external processing.

Sensitive or unclassified evidence is blocked from the external-provider path by default. Do not commit to Production self-hosted GPU infrastructure until workload, quality, SLO and TCO are measured.

This is a current-stage policy, not a permanent Production vendor/topology decision.

## Options compared

1. Hosted SaaS/model API.
2. Self-hosted model on cloud GPU.
3. Self-hosted on-prem GPU.
4. Hybrid via provider-neutral gateway.

## Criteria

| Criterion | Current interpretation |
|---|---|
| Cost | final ranking UNKNOWN until measured load/current prices/ops/utilization exist |
| Privacy | on-prem strongest control; hosted allowed only for approved data classes |
| Quality | compare on one eval set; cheap local model cannot win if quality gate fails |
| Latency | hosted has network/provider dependency; local has capacity/serving dependency |
| Support | hosted simplest now; self-hosted moves GPU/runtime/patch/monitoring burden to project |
| Reversibility | hosted behind gateway is highest-learning/low-CAPEX current option |

## TCO formulas

Hosted API:

`Monthly API = requests × ((input_tokens × input_rate) + (output_tokens × output_rate)) / rate_unit + auxiliary + ops`

Cloud GPU:

`Monthly cloud = gpu_hour_rate × gpu_count × active_hours + storage + traffic + operations`

On-prem:

`Monthly on-prem = CAPEX/lifetime + electricity + cooling/facility + maintenance + operations`

Fair comparison requires the same quality and SLO gate.

## ADR summary

### Context

Semantic/RAG/agent capabilities need model access, but Production workload/TCO is not yet baselined and external AI processing of sensitive evidence is a registered security concern.

### Decision

Hosted API for current approved PoC/MVP data behind provider-neutral policy/gateway; blocked/local path for unapproved data; collect telemetry before Production self-hosting decision.

### Positive consequences

- fast PoC/evaluation;
- low initial infrastructure commitment;
- real workload/quality/cost telemetry;
- migration path preserved.

### Negative consequences

- provider/terms/network dependency;
- external data-processing restrictions;
- variable cost;
- gateway discipline adds complexity;
- Production TCO remains unresolved.

## CTO pitch

For the current OSINT/Knowledge Factory PoC/MVP stage, hosted API behind a replaceable Model Gateway is the least-commitment way to measure whether semantic/RAG/agent capabilities produce enough quality and value to justify permanent infrastructure. Sensitive or unclassified evidence is not sent externally, so delivery speed does not override data control. We are not pretending API is the final cheapest Production answer: token volume, concurrency, local-model quality, GPU utilization and operating cost are still unknown. We buy learning and reversibility now, collect comparable telemetry, then create a superseding ADR when privacy, SLO or measured TCO justifies cloud-GPU/on-prem self-hosting.

## Revisit triggers

- external processing prohibited for required data;
- measured API TCO loses to comparable self-hosted option;
- p95/availability fails SLO;
- local model passes same quality/security eval;
- stable load supports credible GPU utilization;
- provider terms/region/security posture changes;
- offline/local operation becomes hard requirement.

## What should be improved

| Priority | Improvement |
|---|---|
| P0 | complete data/legal approval matrix for external LLM processing |
| P1 | collect model/provider/token/latency/quality telemetry |
| P1 | benchmark local model on same eval set |
| P1 | calculate TCO with current quotes and measured workload |
| P1 | formalize Model Gateway contract/compliance tests |
| P1 | independent reviewer sign-off for material ADR |

Detailed pack: `OSINT_deepseek/docs/course_live_reproduction/09_cto_challenge/`.
