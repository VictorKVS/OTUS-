# llm-app

Репозиторий с общей локальной средой для трёх отдельных демо-направлений:

- `rag/` — классический локальный RAG на `Qdrant` + `Ollama`
- `testing/` — pre-deploy тестирование моделей, `RAGAS`, judge-проверки и служебные утилиты
- `agent/` — controlled-agent с декомпозицией, mock tool и self-check поверх той же базы знаний

Ноутбуки оставлены на верхнем уровне:

- `practice.ipynb`
- `practice_m2_local_llm.ipynb`

Общие для всего репозитория файлы:

- `docker-compose.yaml` — единый compose-стек
- `requirements.txt` — единый набор зависимостей
- `.env` — единая конфигурация среды

Все команды ниже предполагают запуск из корня репозитория.

## Структура

```text
.
├── rag/
├── testing/
├── agent/
├── docker-compose.yaml
├── requirements.txt
├── practice.ipynb
└── practice_m2_local_llm.ipynb
```

## Общая среда

Что должно быть подготовлено:

- активирован `.venv`
- заполнен `.env`
- запущен `Docker Desktop`
- установлен `Ollama`

Общий compose-стек:

```bash
docker compose up -d
docker compose ps
```

URL:

- `MLflow`: `http://localhost:5001`
- `Langfuse`: `http://localhost:3000`
- `Qdrant`: `http://localhost:6333`

Если нужен только RAG или agent demo, достаточно поднимать только `qdrant`:

```bash
docker compose up -d qdrant
docker compose ps qdrant
```

## Быстрый старт по папкам

`rag/`

- документация: `rag/README.md`
- индексация: `./.venv/bin/python -m rag.seed_qdrant_demo`
- чат: `./.venv/bin/python -m rag.run_rag_chat_demo --reindex`

`testing/`

- документация: `testing/README.md`
- pre-deploy: `./.venv/bin/python -m testing.pre_deploy_test`
- одиночный `RAGAS`: `./.venv/bin/python -m testing.run_ragas_demo_test`
- токсичность: `./.venv/bin/python -m testing.toxic_test`

`agent/`

- документация: `agent/README.md`
- список кейсов: `./.venv/bin/python -m agent.run_agent_credit_demo --list-cases`
- agent demo: `./.venv/bin/python -m agent.run_agent_credit_demo --reindex --case-id C-102`

## Что где пишет

- `rag/` — обычные консольные логи
- `agent/` — обычные консольные логи, без обязательного `Langfuse`
- `testing/` — метрики и артефакты в `MLflow`, а при наличии ключей ещё и трассы в `Langfuse`

## Полезные команды

Остановить локально загруженные модели `Ollama`:

```bash
ollama ps | awk 'NR>1 {print $1}' | xargs -n1 ollama stop
```

Остановить локальные сервисы:

```bash
docker compose down
```

Полный сброс `Langfuse`, `MLflow` и `Qdrant`:

```bash
docker compose down -v
docker compose up -d
```

## CI

В `GitHub Actions` ожидаются те же тестовые entrypoint-ы, только в новой структуре:

```bash
python3 -m testing.pre_deploy_test
python3 -m testing.toxic_test
```

Workflow рассчитан на `self-hosted runner`.
