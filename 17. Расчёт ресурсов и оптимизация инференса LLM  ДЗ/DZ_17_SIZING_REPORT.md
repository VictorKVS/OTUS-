# ДЗ 17 — Sizing: Llama-3-70B, 1000 RPM

Статус: **READY FOR SUBMISSION DRAFT**  
Рекомендуемый срок: **06.10.2026**

## 1. Задача

Рассчитать инфраструктуру и стоимость инференса **Llama-3-70B** в FP16 и INT4 под нагрузку **1000 RPM**, сравнить A100/T4/L4, сопоставить два облака и оценить влияние quantization / batching / vLLM.

## 2. Явные допущения

Условие задаёт RPM, но не задаёт длину prompt/output и latency profile. Поэтому расчётная таблица делает допущения изменяемыми:

- workload: 1000 RPM = 16.67 RPS;
- average input: 512 tokens/request;
- average output: 128 tokens/request;
- average E2E: 6 s/request;
- concurrency ≈ RPS × E2E = 100;
- capacity headroom: 20%;
- KV cache dtype: FP16/BF16;
- VRAM runtime reserve: 15%.

При изменении workload-профиля расчёт должен быть пересчитан.

## 3. VRAM

Для Llama-3-70B используем 70B parameters.

### Weights

- FP16: 70B × 2 bytes ≈ 140 GB decimal ≈ **130.39 GiB**.
- INT4: 70B × 0.5 bytes ≈ 35 GB decimal ≈ **32.60 GiB**.

### KV Cache

Для Llama-3-70B config:

- layers = 80;
- KV heads = 8;
- head dimension = 128.

Planning formula:

`KV bytes ≈ batch × active_tokens × layers × 2(K,V) × kv_heads × head_dim × bytes_per_element`.

Для concurrency 100 и active tokens 640:

- KV cache ≈ **19.53 GiB**.

### Total planning VRAM

С 15% reserve:

- FP16 ≈ **172.40 GiB**;
- INT4 ≈ **59.95 GiB**.

## 4. GPU memory-fit

| Precision | A100 80GB | T4 16GB | L4 24GB |
|---|---:|---:|---:|
| FP16 | 4* | 11 | 8 |
| INT4 | 1 | 4 | 3 |

* Для FP16 A100 используем не только арифметический memory-fit, а практический optimized profile NVIDIA: 4×A100 80GB.

**Важно:** T4/L4 значения — только нижняя граница по памяти. Они не доказывают способность обеспечить 1000 RPM.

## 5. Throughput

1000 RPM = 16.67 RPS.

При 128 output tokens/request:

- required output throughput ≈ **2133 tok/s**;
- +20% headroom → **2560 tok/s**.

Публичный benchmark для Llama-3-70B 4-bit на A100 показывает порядок около 700 output tok/s в оптимизированном serving stack при высокой concurrency. Это используется только как **planning anchor**, а не как гарантированный результат vLLM.

Base planning:

`ceil(2560 / 700) = 4 A100`.

Поэтому рекомендуемый initial sizing:

**4×A100 80GB, INT4, shared/load-balanced serving pool**.

## 6. vLLM / batching

Не задаём экономию «процентом по ощущениям».

Экономия определяется измеренным effective throughput:

| Effective throughput / A100 | GPU | Relative compute vs 350 tok/s |
|---:|---:|---:|
| 350 tok/s | 8 | 100% |
| 500 tok/s | 6 | 75% |
| 640 tok/s | 4 | 50% |
| 700 tok/s | 4 | 50% |
| 900 tok/s | 3 | 37.5% |

Таким образом, если serving optimization реально увеличит effective throughput с 350 до 700 tok/s/GPU, sizing снизится с 8 до 4 A100 — около **50% compute saving** в данном workload. Это sensitivity analysis, а не обещание конкретного прироста vLLM.

## 7. Сравнение облаков

### Cloud.ru

A100 NVLink: **353.8 ₽/GPU·h**.

4 GPU:

- 1,415.2 ₽/h;
- ×720 h ≈ **1,018,944 ₽/month**.

### Yandex Cloud

Для gpu-standard-v3, 1 A100:

- GPU: 408.12 ₽/h;
- 28 vCPU × 0.9882 ₽/h;
- 119 GB RAM × 0.3074 ₽/h.

Итого ≈ **472.37 ₽/h per A100 configuration**.

4 GPU:

- ≈1,889.48 ₽/h;
- ×720 h ≈ **1,360,426 ₽/month**.

В core-compute comparison Cloud.ru дешевле примерно на **25.1%**.

Не включены disk/network/egress/support и дополнительные provider-specific charges.

## 8. Рекомендация

Для заданного workload рекомендую:

- **Llama-3-70B INT4**;
- **4×A100 80GB** как initial capacity plan;
- **vLLM + continuous batching**;
- 20% headroom;
- load-balanced serving pool;
- обязательный benchmark на реальном prompt/context workload;
- quality regression test после quantization;
- пересчёт GPU count по фактическим TTFT/p95/tokens-per-second.

T4/L4 могут быть полезны для меньших нагрузок/экспериментов, но для 70B и 1000 RPM их нельзя рекомендовать только на основании memory-fit.

## 9. Источники

- VRAM calculator: https://huggingface.co/spaces/NyxKrage/LLM-Model-VRAM-Calculator
- Llama 3 70B config: https://huggingface.co/NousResearch/Meta-Llama-3-70B-Instruct/blob/main/config.json
- NVIDIA NIM memory guidance: https://docs.nvidia.com/nim/large-language-models/latest/troubleshooting/memory.html
- NVIDIA A100: https://www.nvidia.com/en-us/data-center/a100/
- NVIDIA T4: https://www.nvidia.com/en-us/data-center/tesla-t4/
- NVIDIA L4: https://www.nvidia.com/en-us/data-center/l4/
- vLLM recipe/benchmark guidance: https://github.com/vllm-project/recipes/blob/main/Llama/Llama3.3-70B.md
- Yandex Compute pricing: https://github.com/yandex-cloud/docs/blob/master/md-docs/compute/pricing.md
- Cloud.ru ML Inference tariff: https://cloud.ru/documents/tariffs/evolution/evolution-ml-inference
