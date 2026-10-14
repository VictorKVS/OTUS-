# STEP 16 — Lesson 13 · Оценка качества и тестирование GenAI-компонентов

Статус: **DONE v1 normalization / LAB M1**.

## 1. Source boundary

Исходный текст Lesson 13 прямо подтверждает:

- цель: метрики и фреймворки оценки качества LLM;
- автоматизированное тестирование GenAI в CI/CD;
- RAG metrics: Faithfulness, Answer Relevancy;
- инструменты: DeepEval, Ragas;
- LLM load testing;
- практика: Test Plan для сравнения двух LLM на RAG-задаче;
- преподаватель: Иван Четвериков;
- дата в источнике: «14 сентября, понедельник в 20:00»;
- длительность: 90 минут.

Источник не задаёт явные acceptance criteria, не указывает год занятия и не подтверждает статус сдачи.

## 2. Repository lab evidence

В `llm-app/` подтверждены:

- local RAG: Qdrant + Ollama;
- testing subsystem;
- controlled-agent demo;
- MLflow;
- Langfuse;
- RAGAS;
- multi-model pre-deploy runner;
- toxicity/rudeness judge;
- GitHub Actions quality gates.

## 3. Engineering pipeline

`REQ/NFR → TEST PLAN → GOLDEN DATASET → MODEL/RAG CANDIDATE → RAGAS/JUDGE → METRICS → QUALITY GATE → CI/CD → EVIDENCE`

## 4. Current lab metrics

`run_ragas_demo_test.py` contains:

- Faithfulness;
- Answer Relevancy (embedding fallback by default);
- Context Precision;
- Context Recall;
- QA semantic correctness.

Thresholds are environment-driven. Current lab defaults/workflow values must not be treated as universal production thresholds.

## 5. FATHER production mapping

Primary capability: `FTH-EVL-001 · Evaluation Service`.

Evaluation contract:

`VERSIONED CANDIDATE + VERSIONED DATASET + EVAL CONFIG → RUN → PER-CASE METRICS → AGGREGATE → GATE → EVIDENCE`

Evaluation must bind at least:

- model/version;
- prompt/version;
- retrieval/index version when RAG is used;
- dataset/version;
- evaluator/version;
- metric thresholds;
- code/commit or release context.

## 6. Evidence vs maturity

The repository contains substantial lab code and CI definitions, therefore Lesson 13 remains **LAB / M1**.

It is not raised to M2/M3 because this normalization pass did not confirm immutable successful run evidence for all candidates or a dedicated load-test report.

## 7. GAP

- no explicit source acceptance criteria;
- source year not explicit;
- course submission status unknown;
- DeepEval runtime evidence not confirmed;
- dedicated reproducible load-test artifact not confirmed;
- successful current CI/eval run evidence not confirmed;
- evaluator calibration evidence not confirmed.

## 8. Output artifacts

- `site/data/lesson-details/13.json`;
- `site/assets/lesson-13-genai-evaluation.svg`;
- universal page: `site/lesson-template.html?id=13`;
- this STEP document.
