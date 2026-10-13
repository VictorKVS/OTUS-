#!/usr/bin/env python3
"""Reproducible controlled canary calibration.

This is LAB evidence, not production evidence.
No third-party packages are required.
"""
import math
import random
import statistics

SEED = 20261013
N = 10_000

def simulate(n: int, fail_p: float, median_ms: float, sigma: float):
    rows = []
    for _ in range(n):
        ok = random.random() >= fail_p
        latency = random.lognormvariate(math.log(median_ms), sigma)
        rows.append((ok, latency))
    return rows

def percentile(values, p):
    values = sorted(values)
    return values[math.ceil(p * len(values)) - 1]

def summarize(rows):
    n = len(rows)
    success = sum(1 for ok, _ in rows if ok) / n
    lat = [x for _, x in rows]
    return {
        "n": n,
        "success_rate": success,
        "error_rate": 1 - success,
        "mean_ms": statistics.mean(lat),
        "p95_ms": percentile(lat, 0.95),
        "p99_ms": percentile(lat, 0.99),
    }

random.seed(SEED)
stable = simulate(N, fail_p=0.0040, median_ms=180, sigma=0.35)
candidate = simulate(N, fail_p=0.0045, median_ms=185, sigma=0.35)

for name, rows in [("stable", stable), ("candidate", candidate)]:
    print(name, summarize(rows))
