# AGENT PASSPORT · Telegram Voice Bridge

| Field | Value |
|---|---|
| Agent ID | FTH-AG-VBR-001 |
| Kit | KIT-TELEGRAM-VOICE-BRIDGE |
| Version | 0.1.0 |
| Status | EXPERIMENTAL |
| Family | COMMUNICATION |
| Runtime | Python + aiogram |
| K0 | KB-K0-FATHER-COMMON @ 0.1.0 · shared_reference |
| K1 | KB-K1-COMMUNICATION-BRIDGE @ 0.1.0 |
| K2 | KB-K2-FATHER |
| Memory | stateless per message |
| Trace | required |

## Role

Минимальный двунаправленный Telegram media bridge.

## Goal

- текст из Telegram → TTS → голос обратно;
- голос из Telegram → STT → текст обратно;
- каждый run получает trace_id.

## Prohibited

- не принимает решений вместо пользователя;
- не изменяет содержание текста;
- не хранит содержимое сообщений в trace по умолчанию;
- не выполняет произвольные внешние действия.