# Business Context

## Пользовательская проблема

Сотруднику нужен точный ответ по внутренним документам без ручного перебора папок и длинных PDF.

## Value hypothesis

```text
CURRENT:
question → search → open documents → read → compare → answer

TARGET:
question → verified AI answer + citations → optional source review
```

## Stakeholders

| Роль | Интерес | Основной риск |
|---|---|---|
| Business Owner | ускорить доступ к знаниям | нет измеримого эффекта |
| End User | получить понятный ответ | неверный/неполный ответ |
| Knowledge Owner | актуальность источников | устаревший документ |
| Security | исключить leakage | неверный ACL/RAG retrieval |
| Platform/DevOps | стабильность | release/runtime failure |
| Support/SRE | диагностика | нет telemetry/evidence |
| Architect | целостность | несвязанные локальные решения |

## Business success model

Число не назначаем заранее. Сначала baseline:

```text
T_manual = время от вопроса до подтверждённого ответа вручную
T_ai     = время от вопроса до принятого ответа с AI
saving   = (T_manual - T_ai) / T_manual
```

Целевое снижение времени утверждается после baseline study. Это позволяет защитить KPI фактическими данными, а не «красивым процентом».
