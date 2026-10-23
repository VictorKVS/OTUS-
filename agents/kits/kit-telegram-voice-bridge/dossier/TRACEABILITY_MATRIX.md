# TRACEABILITY MATRIX · Telegram Voice Bridge

| Requirement | Implementation | Trace event | Test/Evidence |
|---|---|---|---|
| VBR-FR-001 | `main.py:text_to_voice` | `telegram.message.received` | text route test |
| VBR-FR-002 | `providers.py:EdgeTTSProvider` | `tts.edge.start/finish` | TTS test |
| VBR-FR-003 | `answer_voice` | `telegram.voice.send` | Telegram integration |
| VBR-FR-004 | `main.py:voice_to_text` | `route.voice_to_text` | voice route test |
| VBR-FR-005 | `bot.download` | `telegram.voice.download` | Telegram integration |
| VBR-FR-006 | `FasterWhisperSTTProvider` | `stt.whisper.start/finish` | STT test |
| VBR-FR-007 | `message.answer` | `telegram.text.send` | Telegram integration |
| VBR-FR-008 | `unsupported` handler | `route.unsupported` | unsupported test |
| VBR-FR-009 | `TraceWriter.new_trace_id` | all events | trace completeness |
| VBR-NFR-002 | `TraceWriter.text_meta` | metadata | privacy test |
| VBR-NFR-003 | `TemporaryDirectory` | run finish | cleanup test |