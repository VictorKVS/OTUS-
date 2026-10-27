# FATHER LAB PLAN · Telegram Voice Bridge

## Baseline

v0.1: aiogram + edge-tts + faster-whisper.

## Metrics

- text→voice success rate;
- voice→text success rate;
- STT word/error quality on fixed samples;
- p50/p95 TTS duration;
- p50/p95 STT duration;
- Telegram download/send latency;
- failure rate;
- trace completeness;
- content-redaction correctness.

## Future challengers

- local TTS vs edge-tts;
- faster-whisper model sizes;
- CPU int8 vs GPU profiles;
- alternative STT/TTS providers.

## Hard gates

- no secret in trace;
- raw content absent when capture disabled;
- both primary routes pass;
- cleanup pass;
- regression pass.