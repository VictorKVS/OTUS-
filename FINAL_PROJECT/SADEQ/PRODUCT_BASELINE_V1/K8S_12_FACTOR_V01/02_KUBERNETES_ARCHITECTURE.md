# K8S-ARCH-001 · Подсистемы, размещение и масштабирование
## Deployment alternatives
- **LAB:** Windows/WSL2, 32GB RAM, RTX 3060 12GB; Docker Compose, one machine, no HA/SLA. API contracts and process boundaries Kubernetes-compatible.
- **OTUS K8s lab:** Minikube on Docker driver, 4 vCPU, 6GB memory from prior environment configuration; exercise infrastructure and API Pod, not full GPU/GraphRAG/data complex. Confirm resources at actual boot.
- **Enterprise strict offline:** physical Linux K8s cluster with local registry, mirror, GPU driver/operator, local model server, offline CNI manifests and pinned DB images; no external network route. Cluster API / node hardening and supply-chain update procedure.
- **Cloud K8s:** future commercial variant only; VPC, storage, GPU pools, telemetry and managed services may be priced separately; violates strict air-gap without explicit new approved deployment requirement.

## Node pool sketch
- Edge/API: 2+ replicas on CPU node pool where SLO and redundancy require.
- Control: orchestrator, identity, policy, qualifier controller isolated from candidate agent tool execution.
- GPU: inference + embedding/rerank with requests/limits and distinct scale policy.
- Stateful Data: PostgreSQL, Qdrant, Neo4j, object storage with explicit backup and recovery.
- Ops: metrics, traces, audit storage, alerts, local secrets.

## Security zones
```text
Business User
  → Gateway/Ingress (TLS, auth, rate limit)
  → Policy / Identity service
  → API (stateless Deployment)
  → Orchestrator (stateless Deployment, checkpoint in PostgreSQL)
  → Retrieval service (ACL-filtered) → Qdrant, Neo4j
  → Local LLM serving (GPU Deployment)
  → Action Proposal → Policy decision → human approval → Internal Tool Gateway
  → Durable event+audit → Feedback / Independent Qualification
```
Tenant ACL before retrieval and on graph edge traversal. Kubernetes NetworkPolicy must be enforced by a CNI supporting it; a YAML policy in a cluster without enforcement is not protection. Host and egress boundaries are also controlled by physical network and firewall policy.

## Availability vs throughput
**High Availability:** replica and failure domains, PDB, quorum, failover with actual RTO/RPO testing.  
**Horizontal Throughput:** more API/worker replicas or GPU inference nodes, after measured bottleneck; StatefulSets and database partitions require data-level planning.  
**Multi-tenancy:** namespaces alone don't substitute for DB ACL/row-level security, per-tenant vector/graph access and segregated metrics.

## Kubernetes objects selected
`Namespace`, `ServiceAccount` (automount token disabled unless needed), `Deployment` for API/UAA workers, `Service`, `ConfigMap`, `Secret` (managed), `NetworkPolicy` ingress+egress, `ResourceQuota`, `LimitRange` (future), `PodDisruptionBudget`, `HorizontalPodAutoscaler` where metrics exist, `Job/CronJob` admin and qualification operations; GPU `nvidia.com/gpu` requests on installed device-plugin nodes, `StatefulSet/PVC` for DB if qualified.

## Scaling capacity
`api_replicas = ceil(peak_API_RPS / benchmark_verified_RPS_per_pod / safe_utilization)`  
`gpu_pool = ceil(peak_output_tokens_per_second / benchmark_verified_decode_tokens_per_second_per_GPU / safe_utilization)` (approx; TTFT and prefill/concurrency need full benchmark).  
`cost = server_or_cloud_CAPEX/OPEX + GPU + storage/backup + network + SOC/SRE + independent tests`.  
**Never promise 10,000 LLM RPS on one RTX3060;** 10k RPS might refer only to a cache or health-check API, but design must qualify actual request class.

## Source diagrams
See [diagram.mmd](diagram.mmd). Need validate K8s manifests on real cluster: `kubectl --dry-run=server`, kubeconform, policy tests, conformance of image pull in offline mirror. Not executed.
