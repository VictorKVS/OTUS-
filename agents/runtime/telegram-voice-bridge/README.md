# Telegram Voice Bridge · FTH-AG-VBR-001

Первый примитивный сквозной агент FATHER.

## Что делает

- Telegram text → Edge TTS → voice message обратно в Telegram.
- Telegram voice → download → faster-whisper → text обратно в Telegram.
- На каждом шаге пишет privacy-safe JSONL trace.

## Runtime flow

~~~text
TEXT:
telegram.message.received
→ route.text
→ tts.start
→ tts.pass
→ telegram.voice.send
→ run.pass

VOICE:
telegram.message.received
→ route.voice
→ telegram.voice.download
→ stt.start
→ stt.pass
→ telegram.text.send
→ run.pass
~~~

## Environment

Copy `.env.example` to `.env`.

Required:
- TELEGRAM_BOT_TOKEN

Defaults:
- TTS_VOICE=ru-RU-SvetlanaNeural
- STT_MODEL=small
- STT_DEVICE=cpu
- STT_COMPUTE_TYPE=int8
- TRACE_CAPTURE_CONTENT=false

## Start

~~~bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
~~~

Linux activation: `source .venv/bin/activate`.

## Trace

Default file: `runtime/traces/telegram-voice-bridge.jsonl`.

Content is not stored unless `TRACE_CAPTURE_CONTENT=true`.

Export for static FATHER Trace Center:
`python tools/export_voice_bridge_traces.py`.