# Canary calibration · controlled LAB

Seed: `20261013`  
Sample: 10 000 requests per variant.

| Metric | Stable | Candidate |
|---|---:|---:|
| Success rate | 99.58% | 99.49% |
| Error rate | 0.42% | 0.51% |
| Mean latency | 191.34 ms | 196.79 ms |
| p95 latency | 319.01 ms | 330.78 ms |
| p99 latency | 402.64 ms | 416.47 ms |

Interpretation: candidate is slightly worse in this controlled sample. This file proves the calibration workflow is reproducible; it does **not** prove a production threshold.

Run:
```bash
python LAB/canary_calibration.py
```
