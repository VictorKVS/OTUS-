# Knowledge Polygon Playbook

## Один проход фазы

```text
PHASE QUESTION
      ↓
PROJECT ARTIFACTS
      ↓
GAP ANALYSIS
      ↓
IMPLEMENT / DOCUMENT
      ↓
TEST / MEASURE
      ↓
EVIDENCE
      ↓
LESSON LEARNED
      ↓
GENERALIZE
      ↓
REUSABLE BLOCK / PATTERN
```

## Пример: Phase 13 Evaluation

В каждом проекте спрашиваем не «есть ли тесты?», а:

1. Какой объект качества измеряем?
2. Какая baseline?
3. Какой dataset/sample?
4. Какова статистическая мощность/доверие, если нужна?
5. Какие failure classes?
6. Какой release gate?
7. Что можно сделать универсальным?

Доменные варианты:
- RAG → faithfulness/retrieval;
- frontend → visual regression/accessibility/performance;
- OSINT → precision/provenance/source reliability;
- security → false positive/false negative/control effectiveness;
- media → perceptual/identity/consistency metrics;
- local LLM → quality/latency/VRAM/throughput.

Общий reusable результат: `FTH-BLK-EVAL-* + Experiment Engine`.

## Правило чисел

Любое число в проекте должно иметь:

```text
VALUE
+ UNIT
+ CONTEXT
+ SOURCE
+ METHOD
+ SAMPLE
+ DATE/VERSION
+ PROVENANCE
```

Без этого число не допускается в blocking production gate.
