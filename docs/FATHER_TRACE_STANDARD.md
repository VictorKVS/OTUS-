# FATHER Traceability & Runtime Trace Standard

Статус: **CANONICAL DESIGN v1**

## 1. Purpose

Каждый runtime-run агента получает `trace_id`. Trace связывает вход, маршрутизацию, инструменты/модели, выход, ошибки, duration и evidence.

## 2. Minimal event

~~~text
trace_id
event_id
timestamp
agent_id
event
status = START | PASS | WARN | FAIL
duration_ms
metadata
~~~

## 3. Privacy

По умолчанию trace не хранит содержимое пользовательского сообщения, голос, токены/секреты или лишние персональные данные.

Для текста по умолчанию сохраняется только длина и `content_redacted=true`. Content capture допускается только в изолированном LAB и явной настройкой.

## 4. Trace chain

~~~text
CHANNEL INPUT
→ NORMALIZE
→ ROUTE
→ AGENT
→ TOOL / MODEL
→ RESULT
→ CHANNEL OUTPUT
→ RUN FINISH
~~~

Каждый FAIL должен сохранять `error_type` и безопасное краткое описание ошибки.

## 5. UI

`factory/trace-center.html` является представлением runtime traces. Источник реальных trace — `factory/data/runtime-traces.json`, формируемый экспортёром из runtime JSONL.

Design/sample trace обязан иметь явный статус `DESIGN_SAMPLE` и не может отображаться как реальный запуск.

## 6. Evidence

Trace является runtime evidence, но сам по себе не заменяет тест, LAB evaluation или acceptance.