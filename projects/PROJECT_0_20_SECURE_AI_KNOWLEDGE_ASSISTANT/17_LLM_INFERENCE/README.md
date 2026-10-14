# 17 · LLM inference sizing

## Задача этапа

VRAM, quantization, batching, latency/throughput, GPU profile.

## Вход

Утверждённые артефакты этапа 16.

## Что делаем

1. Фиксируем решение в versioned artifacts.
2. Связываем требования, риски, решения и evidence.
3. Не объявляем M2/M3 без проверяемого evidence.
4. Передаём результат следующему этапу через явный контракт.

## Выход

`INFERENCE_PROFILE.md · BENCHMARK_PLAN.md`

## Связь со сквозным проектом

Проект один: **Secure AI Knowledge Assistant**. На этом уроке не создаётся новая демонстрационная система; расширяется уже существующая архитектура.

## Status

`DESIGN / M1` до появления runtime/evidence, если отдельный артефакт не доказывает более высокий уровень.
