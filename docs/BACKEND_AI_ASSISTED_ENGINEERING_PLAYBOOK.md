# Backend & AI-Assisted Engineering Interview Playbook

## Python

Уверенно объяснять modules/packages, typing, exceptions, classes/dataclasses, iterators/generators basics, context managers basics, virtual environments и зависимости.

## asyncio

`asyncio` полезен для I/O-bound конкурентных задач: API, сеть, БД, файлы. Он не ускоряет CPU-bound вычисления автоматически. Нужны базовые знания `async/await`, tasks, timeout и cancellation.

## FastAPI / REST

Типовая цепочка: `HTTP → Route → Request/Pydantic validation → Service layer → RAG/LLM/DB/Agent → Response model`.

Понимать routes, request/response models, dependencies, exception handling, middleware basics, auth conceptually, async endpoints; в REST — HTTP methods, status codes, idempotency, authentication vs authorization, pagination/error contract.

## PostgreSQL / pgvector

Понимать schema/table/index basics, joins, transactions basics и роль индексов. pgvector добавляет хранение и поиск embeddings; vector search не отменяет relational model.

## Docker

Термины: image, container, Dockerfile, volume, network, environment variables/secrets, compose. Контейнер — не полноценная виртуальная машина.

## Git / pytest / CI

Git: branch, commit, merge/rebase basics, pull request, conflict, revert, tag.

Tests: unit, integration, contract, regression. Pipeline: `commit → lint/static checks → tests → security scans → build → deploy/release gate`.

# AI-assisted development

В резюме: **AI-assisted software development / LLM-assisted engineering**, а не просто «vibe coding».

Рабочий цикл: `Requirement → Decomposition → Architecture/constraints → Small task → AI generation → Human review → Tests → Security/dependency check → Integration → Commit/Evidence`.

Coding agent хорошо подходит для boilerplate, prototype, test scaffolding, refactoring proposal, docs draft, debugging hypotheses и повторяющихся задач.

Без проверки нельзя отдавать архитектурные решения, auth/authz, security-critical code, удаление данных, dependency upgrades, production migrations и любой код, который кандидат сам не может объяснить.

Фраза для интервью: «Я активно использую coding agents, но считаю AI-generated code непроверенным до review и tests. AI ускоряет цикл, ответственность за архитектуру и результат остаётся у инженера».

## Контрольные вопросы

1. Когда async полезен, а когда нет?
2. Что будет при blocking I/O внутри async endpoint?
3. Где держать бизнес-логику FastAPI?
4. Authentication vs authorization?
5. Почему нельзя хранить секреты в Git/Dockerfile?
6. Как тестировать недетерминированный LLM?
7. Как проверяете код coding agent?
8. Когда AI-assisted development повышает риск?