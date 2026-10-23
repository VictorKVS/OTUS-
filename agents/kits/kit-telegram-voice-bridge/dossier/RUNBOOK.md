# RUNBOOK · Telegram Voice Bridge

## Preconditions

- Python 3.12 target environment;
- Telegram bot token;
- network access to Telegram;
- network access to edge-tts service for current TTS provider;
- storage/network availability for first faster-whisper model acquisition.

## Start

1. create virtual environment;
2. install `requirements.txt`;
3. copy `.env.example` to `.env`;
4. set `TELEGRAM_BOT_TOKEN`;
5. run `python main.py` from runtime directory.

## Smoke

- send text `Привет` → receive voice;
- send short voice → receive text;
- verify JSONL trace;
- run trace exporter;
- open `factory/trace-center.html` and verify RUNTIME run appears.

## Failure

- no token → startup blocked;
- Telegram unavailable → keep FAIL evidence; retry after connectivity restored;
- Edge TTS unavailable → user receives conversion error + trace id;
- STT failure → user receives recognition error + trace id.

## Rollback

Return to previous known commit/runtime package. No persistent agent state migration is required in v0.1.