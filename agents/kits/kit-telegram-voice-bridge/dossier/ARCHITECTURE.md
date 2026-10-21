# ARCHITECTURE · Telegram Voice Bridge

## Context

~~~text
Telegram User
   ↕
Telegram Bot API
   ↕
FTH-AG-VBR-001
   ├── EdgeTTSProvider
   ├── FasterWhisperSTTProvider
   └── TraceWriter
~~~

## Route A · text → voice

~~~text
Message(text)
→ route.text_to_voice
→ Edge TTS
→ temporary MP3
→ Telegram sendVoice
→ cleanup
~~~

## Route B · voice → text

~~~text
Message(voice)
→ Telegram download
→ temporary OGG
→ faster-whisper
→ Telegram send text
→ cleanup
~~~

## Runtime files

- `agents/runtime/telegram-voice-bridge/main.py` — channel/router/orchestration.
- `providers.py` — TTS/STT adapters.
- `tracing.py` — privacy-safe trace writer.
- `trace.schema.json` — event contract.

## ADR-001

Для v0.1 LLM не используется. Это намеренно: первый агент проверяет Channel Gateway, tool/provider adapters и traceability без влияния reasoning-модели.