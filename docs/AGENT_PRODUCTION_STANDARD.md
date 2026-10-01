# Agent Production Standard v1

Статус: **ACTIVE DRAFT**

Назначение: единый production contract для каждого нового агента и каждого существенного изменения существующего агента.

## 1. Principle

Агент не считается production-ready как набор `prompt + model + tools`.

Минимальный lifecycle:

`SPEC → SECURITY → KNOWLEDGE/RAG → MODEL/TOOLS → EVAL → OBSERVABILITY → SLO → SIZING → COST → RELEASE → FEEDBACK`

## 2. Mandatory agent passport

```yaml
agent:
  id: ""
  role: ""
  owner: ""

workload:
  avg_tasks_per_minute: null
  peak_tasks_per_minute: null
  burst_factor: null
  concurrent_tasks_target: null

ai_profile:
  avg_input_tokens: null
  avg_output_tokens: null
  rag_queries_per_task: null
  tool_calls_per_task: null
  memory_reads_per_task: null
  memory_writes_per_task: null

security:
  data_classes: []
  pii_sanitizer: true
  prompt_injection_guard: true
  output_guard: true
  tool_policy: strict
  secrets_externalized: true

evaluation:
  golden_dataset: ""
  faithfulness_min: null
  answer_relevancy_min: null
  task_success_min: null
  security_hard_gates: true

slo:
  p95_latency_ms: null
  error_rate_max: null
  availability_target: null

sizing:
  cpu_cores: null
  ram_gb: null
  gpu_profile: null
  vector_count: null
  vector_dimension: null
  data_retention_days: null
  replicas: null
  headroom_factor: null
  benchmark_id: null

cost:
  monthly_budget: null
  max_cost_per_task: null
  onprem_tco: null
  cloud_monthly_estimate: null

release:
  eval_gate: required
  security_gate: required
  slo_gate: required
  capacity_gate: required
  rollback: required
```

## 3. Sizing contract — Lesson 16

Sizing is mandatory before production deployment.

Inputs:

- NFR/SLO;
- average/peak/burst workload;
- measured or conservative service time;
- stateful/stateless classification;
- dataset and vector-store growth;
- retention;
- replicas;
- observability volume;
- cost constraints.

Engineering formulas:

- `Concurrency ≈ RPS × service_time_seconds`;
- CPU based on benchmarked CPU-seconds/request and utilization target;
- RAM = working set + cache + runtime + margin;
- vector raw payload = count × dimensions × bytes/element;
- total storage = raw + metadata/index + replicas + headroom.

Detailed LLM GPU/VRAM sizing is refined by Lesson 17.

## 4. Capacity Gate

Agent release is blocked unless one of two conditions is true:

1. benchmark evidence exists; or
2. conservative capacity estimate is explicitly approved with assumptions and expiry/review date.

Gate checks:

- performance SLO;
- availability/redundancy;
- storage/retention;
- security/audit overhead;
- cost budget;
- scale-up / scale-out path.

## 5. Feedback loop

Production telemetry recalibrates sizing:

`OBSERVABILITY → measured workload → capacity model → forecast → budget → scale decision`

Sizing is not a one-time spreadsheet.

## 6. Common services

Do not deploy a separate monitoring/security/sizing stack per agent. Agents consume shared platform services:

- Security / Policy Plane;
- Evaluation Service;
- Observability Plane;
- SLO / Alerting;
- Resource Sizing & Capacity;
- FinOps / Cost Control.

Per-agent differences live in manifest configuration and evidence.
