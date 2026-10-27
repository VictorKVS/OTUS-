# SECURITY · Telegram Voice Bridge

## Assets

- Telegram bot token;
- user text/voice content;
- temporary media files;
- trace/evidence.

## Controls

- token только из environment;
- trace content redacted by default;
- no chat/user identifier retained in default trace;
- temporary directory per run;
- temporary media removed automatically;
- provider exception is not returned to user verbatim;
- least-privilege bot permissions;
- no arbitrary file execution.

## External dependency boundary

`edge-tts` uses an online TTS service, therefore text sent to TTS crosses the local boundary. This limitation must be explicit during LAB/security acceptance. A local TTS provider can replace it later.

## Gate

До production необходимо проверить token handling, trace redaction, provider failure, oversized input policy and Telegram access scope.