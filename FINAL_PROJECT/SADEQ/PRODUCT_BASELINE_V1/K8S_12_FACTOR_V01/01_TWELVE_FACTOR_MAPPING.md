# TF-001 · Все 12 факторов: проектное решение → Kubernetes → проверка → стоимость
Версия v0.1; все статусы PROPOSED до доказательств.

| ID | The Twelve-Factor App | Применение к SADEQ | Средство в Kubernetes | Тест / Evidence | Экономический эффект |
|---|---|---|---|---|---|
| TF-01 | **Codebase** | отдельные логически самостоятельные сервисы из версионированного исходного кода, общая API schema и contracts, source provenance | GitOps manifests/Helm versioned, image digests, labels/annotations commit SHA | rollback с того же commit, reproducible build | меньше divergence и потерь на интеграцию; GitOps overhead |
| TF-02 | **Dependencies** | pinned Python/JS libs и модели, lockfile, SBOM, offline mirror, license scanning | private registry/image pull; immutable digest; init validation | no Internet at run/build, verify digest/SBOM | storage mirror, vulnerability DB refresh, onboarding |
| TF-03 | **Config** | конфигурация в runtime; миссия агента и модель/политики versioned; секреты отдельно от ConfigMap/репо | ConfigMap for nonsecrets; Secret/external secret controller for secrets; sealed storage | config switch no rebuild; secret leak tests | operational secret management |
| TF-04 | **Backing Services** | PostgreSQL, Qdrant, Neo4j, object store, queue as replaceable services, *but* schema/data consistency is explicit | StatefulSet/PVC/operator or external private DB; Service DNS | restore, DB outage, tenant isolation, migrations | disk, backup, replicas, data IOPS |
| TF-05 | **Build, Release, Run** | CI produces signed immutable software+model refs; release manifest binds config/policy/model SHA; no `pip install` on live nodes | CI registry → admission → Deployment/Helm rollout; rollback | attestation, signed artifact promotion, no unsigned runtime | CI and supply chain; reduces uncontrolled drift |
| TF-06 | **Processes** | API, orchestrator, ingestion worker stateless; agent memory/checkpoints in DB, never Pod filesystem | Deployment replicas; separate persistence; volumes limited to cache/tmp | delete Pod during LangGraph run, resume from checkpoint | extra DB IOPS vs no session loss |
| TF-07 | **Port Binding** | FastAPI, policy and serving APIs expose explicit ports and TLS at gateway; internal traffic limited | ClusterIP Service, Gateway/Ingress, mTLS where required | contract and reachability tests; no public exposure of DB or model | internal networking and gateway |
| TF-08 | **Concurrency** | distinct scaling API req/s, queue event/s, GraphRAG query/s, LLM tokens/s and agents; avoid 1 agent=1 GPU | HPA CPU/custom metrics, KEDA queue scaler (optional), GPU node pool, vLLM batching | load test p95/TTFT/tokens/s/GPU VRAM/queue | GPU-hours, oversubscription, autoscaling latency |
| TF-09 | **Disposability** | startup only after dependencies ready; graceful SIGTERM; bounded in-flight work; claim/ack queue after durable result; idempotent tools | startup/readiness/liveness probes, preStop, terminationGracePeriodSeconds, PDB | SIGTERM/POD kill & duplicate-delivery tests | retries, extra replica, continuity |
| TF-10 | **Dev/Prod Parity** | same OpenAPI, DB engines/major versions and model digests; dev is smaller but contract identical | Compose/Minikube vs on-prem Kubernetes, Helm values with controlled deltas | parity tests, contract diff, same image promotion | extra staging infra; lower prod regressions |
| TF-11 | **Logs** | JSON logs to stdout/stderr, trace_id, decision_id, tenant-safe redaction, immutable security audit external | DaemonSet OTel collector / node log agents, log backend, SIEM | log correlation, PII/secret redaction, audit loss test | log volume, retention, SIEM operator |
| TF-12 | **Admin Processes** | DB schema migration, embedding/graph reindex, data repair, model promotion, qualification as one-off controlled jobs | Job/CronJob, RBAC-scoped ServiceAccount, approval/signed artifact | migration forward/rollback, one-off idempotency | CPU/GPU job cost, maintenance windows |

## Особенности AI-систем сверх 12 факторов
TF-06 does **not** mean destroy agent memory; persist it externally and handle state schema versioning. TF-08 does **not** make 10,000 full-answer LLM RPS plausible on one consumer GPU; model prefill/decode throughput is a separate bottleneck. TF-03 is **not** license to place prompts/secrets in a public ConfigMap. TF-09 and EDA depend on at-least-once delivery, so enforce idempotency before tool use. TF-11 excludes unredacted chain-of-thought or secrets from logs. The Twelve-Factor methodology alone cannot guarantee authorization, prompt-injection resistance or agent trust; add independent qualification, scoped policy and continuous monitoring.

## Required platform and product boundaries
**API / UAA workers / event intake:** stateless Deployments, can scale independently.  
**Stateful stores:** StatefulSets/PVC or qualified independent services; never scale stateful data layer only by increasing `replicas`.  
**LLM serving:** model pin + GPU assignment, workload node selectors and taints, dedicated SLO/capacity tests.  
**Policy engine and qualification:** separated from candidate agent and tool implementation, deny-by-default.

## Admission
A factor is VERIFIED only when its independent test has run in a documented environment, captured logs/evidence and human approval. All 12 are currently DESIGN ONLY.
