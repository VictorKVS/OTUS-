# K8S-GATES-001 · Реализация и подтверждение каждого фактора
## Work plan (no assumed completion)
| Wave | Deliverable | Gate tests | OTUS |
|---|---|---|---|
| K0 | Twelve-factor and C4 mapping | architecture review and registered ADR | 04/05/08 |
| K1 | Reproducible offline image / pinned dependencies | hashes, SBOM, signature, license and no egress | 18/20 |
| K2 | API stateless, external checkpoint and source events | pod restart recovers run; no double side effects | 07/12/23 |
| K3 | Policy/service identity/tenant segregation | user B denied through graph/cache/log; tool blocked | 11/14/26 |
| K4 | real GraphRAG + model serving on GPU | path citations and model benchmarks | 06/13/16/17 |
| K5 | deployment test + observability | startup/readiness/graceful SIGTERM/OTel spans | 15/20 |
| K6 | concurrency and recovery | HPA/queue metrics + PDB + restore; no invented SLA | 21/22/24 |
| K7 | FinOps TCO A/B/C with tariff and price shocks | scenario spreadsheet, input provenance | 25/28 |
| K8 | qualification and go/no-go | independent QA, admission and signed human approval | 09/19/30/31 |

## Minimum contract tests by factor
TF01 Git commit and released image match. TF02 pinned dependency digest & offline pull. TF03 replacement settings without rebuilt image, no secret prints. TF04 kill DB, properly degrade and recover. TF05 deny unapproved image. TF06 kill API/agent pod mid-run → resume checkpoint. TF07 no bypass of gateway. TF08 double requests with HPA → no tenant data crossover, SLO reported. TF09 graceful SIGTERM; replay no double tool call. TF10 staging/production artifact digest identical. TF11 redacted correlated logs external. TF12 once-only migration with prior DB version snapshot and rollback procedure.

## Six Security roles and placement
SEC-01 enters architecture/business gates; SEC-02 validates threat model/C4/NetworkPolicy; SEC-03 owns CI/CD supply-chain; SEC-04 is deterministic policy engine at every tool call; SEC-05 performs independent qualification; SEC-06 owns telemetry, drift, incident and revoke. Full business notation: [security lifecycle BPMN](../../IDEA_PLUS_V0_2/diagrams/security_lifecycle.bpmn).

## Business and financial gate
When moving Compose → K8s, quantify operations complexity, Kubernetes HA/backup, GPU device plugin, inter-node network, capacity reservation; do not call migration a cost saving without baseline. Compare cloud/onprem 40/160/730h and fully allocated TCO; prior tariff register [here](../../IDEA_PLUS_V0_2/11_DEPLOYMENT_CLOUD_FINOPS_RU_2026.md).

## Current status
All factor tests NOT_RUN. The project's presence in GitHub is an architecture deliverable only, not proof of running Kubernetes.
