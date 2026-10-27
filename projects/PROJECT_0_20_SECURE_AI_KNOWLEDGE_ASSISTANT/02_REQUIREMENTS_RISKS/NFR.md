# Non-Functional Requirements

## Provenance labels

- `COURSE_TEMPLATE` — число дано как пример в материалах Lesson 2.
- `DESIGN` — проектное решение, ещё не доказано.
- `LAB` — измерено воспроизводимым экспериментом.
- `PROD` — измерено на production workload.

| ID | Category | Metric | Candidate target | Provenance | Verification |
|---|---|---|---:|---|---|
| NFR-PERF-01 | Performance | TTFT | <1.5 s | COURSE_TEMPLATE | load test |
| NFR-PERF-02 | Performance | E2E p95, response <200 tokens | <5.0 s | COURSE_TEMPLATE | load test |
| NFR-PERF-03 | Performance | throughput | >50 req/s | COURSE_TEMPLATE | Locust/k6 |
| NFR-PERF-04 | Performance | concurrency | 100 sessions | COURSE_TEMPLATE | load test |
| NFR-QLT-01 | Quality | answer relevancy | >0.85 | COURSE_TEMPLATE | RAGAS/DeepEval + golden set |
| NFR-QLT-02 | Quality | faithfulness | >0.90 | COURSE_TEMPLATE | golden-set eval |
| NFR-QLT-03 | Quality | context recall | >0.80 | COURSE_TEMPLATE | retrieval eval |
| NFR-SEC-01 | Security | confirmed critical data leakage | 0 | DESIGN MUST | red-team/regression |
| NFR-SEC-02 | Security | forbidden-document retrieval | 0 | DESIGN MUST | ACL adversarial tests |
| NFR-DATA-01 | DataOps | source citation | required for factual answer | DESIGN MUST | automated check |
| NFR-OPS-01 | Operations | rollback without stable rebuild | required | DESIGN MUST | release drill |

## Decision rule

COURSE_TEMPLATE values are **benchmarks to test**, not contractual production SLO. Lesson 15/16/17 replaces them with measured baselines where evidence supports the change.
