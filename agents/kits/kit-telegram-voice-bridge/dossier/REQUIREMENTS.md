# REQUIREMENTS · Telegram Voice Bridge

## Functional

- VBR-FR-001: принимать Telegram text message.
- VBR-FR-002: преобразовывать текст в speech artifact.
- VBR-FR-003: отправлять speech artifact обратно в тот же Telegram chat.
- VBR-FR-004: принимать Telegram voice message.
- VBR-FR-005: скачивать voice artifact через Telegram Bot API.
- VBR-FR-006: преобразовывать speech в text.
- VBR-FR-007: отправлять распознанный text обратно в тот же chat.
- VBR-FR-008: unsupported content получает понятный ответ.
- VBR-FR-009: каждый вход создаёт уникальный trace_id.

## NFR

- VBR-NFR-001: TELEGRAM_BOT_TOKEN только через environment.
- VBR-NFR-002: содержание сообщения не логируется по умолчанию.
- VBR-NFR-003: временные media files удаляются после run.
- VBR-NFR-004: provider/runtime ошибки дают FAIL trace и безопасный ответ пользователю.
- VBR-NFR-005: STT/TTS providers заменяемы через adapter layer.

## Acceptance

- AC-01 text→voice успешно проходит end-to-end;
- AC-02 voice→text успешно проходит end-to-end;
- AC-03 trace содержит received/route/provider/send/finish;
- AC-04 TRACE_CAPTURE_CONTENT=false не сохраняет raw text;
- AC-05 missing token блокирует startup.