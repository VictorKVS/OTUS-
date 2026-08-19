# Testing Demo

Папка с проверками моделей и вспомогательными judge-сценариями.

Все команды ниже предполагают запуск из корня репозитория.

## Что лежит здесь

- `pre_deploy_test.py` — полный pre-deploy прогон нескольких моделей
- `run_ragas_demo_test.py` — одиночный прогон одной модели с метриками `RAGAS`
- `toxic_test.py` — judge-проверка токсичности и грубости
- `publish_model_placeholder.py` — загрузка заглушки в MinIO для уже прошедшей модели
- `check.py` — ручная проверка подключения к Yandex OpenAI-compatible API

## Что использует

- общий `docker-compose.yaml` из корня репозитория
- общий `.env` из корня репозитория
- `MLflow` для артефактов и метрик
- `Langfuse` для трассировки `run_ragas_demo_test.py`, если в `.env` заданы ключи
- `Ollama` для локальных моделей в pre-deploy сценарии

## Команды

Полный pre-deploy прогон:

```bash
./.venv/bin/python -m testing.pre_deploy_test
```

Одиночный `RAGAS`-прогон:

```bash
./.venv/bin/python -m testing.run_ragas_demo_test
```

Проверка токсичности:

```bash
./.venv/bin/python -m testing.toxic_test
```

Ручная проверка доступа к списку моделей Yandex:

```bash
./.venv/bin/python -m testing.check
```

`publish_model_placeholder.py` обычно запускается не вручную, а из workflow после успешного `pre_deploy_test`.

## Примечания

- Эти скрипты не поднимают `docker-compose` стек целиком автоматически. Они используют уже общую среду из корня репозитория.
- `pre_deploy_test.py` внутри себя вызывает `run_ragas_demo_test.py` как модуль, поэтому после реорганизации структура запусков остаётся целостной.
