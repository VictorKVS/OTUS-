from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

from providers import EdgeTTSProvider, FasterWhisperSTTProvider
from tracing import Timer, TraceWriter, bool_env

AGENT_ID = "FTH-AG-VBR-001"
ROOT = Path(__file__).resolve().parents[3]
load_dotenv(Path(__file__).with_name('.env'))

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TTS_VOICE = os.getenv("TTS_VOICE", "ru-RU-SvetlanaNeural")
STT_MODEL = os.getenv("STT_MODEL", "small")
STT_DEVICE = os.getenv("STT_DEVICE", "cpu")
STT_COMPUTE_TYPE = os.getenv("STT_COMPUTE_TYPE", "int8")
TRACE_FILE = Path(os.getenv("TRACE_FILE", str(ROOT / "runtime" / "traces" / "telegram-voice-bridge.jsonl")))

trace = TraceWriter(TRACE_FILE, capture_content=bool_env('TRACE_CAPTURE_CONTENT', False))
tts = EdgeTTSProvider(TTS_VOICE)
stt = FasterWhisperSTTProvider(STT_MODEL, STT_DEVICE, STT_COMPUTE_TYPE)
router = Router(name='telegram-voice-bridge')

def message_meta(message: Message) -> dict:
    return {
        "telegram_message_id": message.message_id,
        "chat_type": str(message.chat.type),
        "content_type": str(message.content_type),
    }

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "FATHER Voice Bridge готов.\n"
        "Пришлите текст — верну голос.\n"
        "Пришлите голосовое — верну распознанный текст."
    )

@router.message(F.text)
async def text_to_voice(message: Message) -> None:
    trace_id = trace.new_trace_id()
    text = (message.text or '').strip()
    base = message_meta(message)
    trace.event(trace_id, "telegram.message.received", "PASS", metadata={**base, **trace.text_meta(text)})
    trace.event(trace_id, "route.text_to_voice", "PASS", metadata={"route": "text->tts->voice"})

    if not text:
        trace.event(trace_id, "run.finish", "WARN", metadata={"reason": "empty_text"})
        await message.answer("Пустой текст.")
        return

    try:
        with tempfile.TemporaryDirectory(prefix='father-vbr-') as tmp:
            output = Path(tmp) / "reply.mp3"
            trace.event(trace_id, "tts.edge.start", "START", metadata={"voice": TTS_VOICE})
            with Timer() as timer:
                await tts.synthesize(text, output)
            trace.event(trace_id, "tts.edge.finish", "PASS", duration_ms=timer.duration_ms, metadata={"voice": TTS_VOICE, "bytes": output.stat().st_size})

            trace.event(trace_id, "telegram.voice.send", "START", metadata={"format": "mp3"})
            with Timer() as send_timer:
                await message.answer_voice(FSInputFile(output), caption=f'trace: {trace_id}')
            trace.event(trace_id, "telegram.voice.send", "PASS", duration_ms=send_timer.duration_ms, metadata={"format": "mp3"})

        trace.event(trace_id, "run.finish", "PASS", metadata={"route": "text_to_voice"})
    except Exception as exc:
        trace.event(trace_id, "run.finish", "FAIL", metadata={"error_type": type(exc).__name__, "error": str(exc)[:300]})
        await message.answer(f"Ошибка преобразования. trace: {trace_id}")

@router.message(F.voice)
async def voice_to_text(message: Message, bot: Bot) -> None:
    trace_id = trace.new_trace_id()
    base = message_meta(message)
    trace.event(trace_id, "telegram.message.received", "PASS", metadata={**base, "voice_duration_sec": message.voice.duration, "voice_bytes": message.voice.file_size})
    trace.event(trace_id, "route.voice_to_text", "PASS", metadata={"route": "voice->download->stt->text"})

    try:
        with tempfile.TemporaryDirectory(prefix='father-vbr-') as tmp:
            source = Path(tmp) / "incoming.ogg"
            trace.event(trace_id, "telegram.voice.download", "START", metadata={"file_id_present": True})
            with Timer() as download_timer:
                await bot.download(message.voice, destination=source)
            trace.event(trace_id, "telegram.voice.download", "PASS", duration_ms=download_timer.duration_ms, metadata={"bytes": source.stat().st_size})

            trace.event(trace_id, "stt.whisper.start", "START", metadata={"model": STT_MODEL, "device": STT_DEVICE, "compute_type": STT_COMPUTE_TYPE})
            with Timer() as stt_timer:
                text, language, probability = await stt.transcribe(source)
            trace.event(trace_id, "stt.whisper.finish", "PASS" if text else "WARN", duration_ms=stt_timer.duration_ms, metadata={"model": STT_MODEL, "language": language, "language_probability": probability, **trace.text_meta(text)})

        if not text:
            await message.answer(f"Речь не распознана. trace: {trace_id}")
            trace.event(trace_id, "run.finish", "WARN", metadata={"reason": "empty_transcription"})
            return

        trace.event(trace_id, "telegram.text.send", "START", metadata=trace.text_meta(text))
        with Timer() as send_timer:
            await message.answer(f"{text}\n\ntrace: {trace_id}")
        trace.event(trace_id, "telegram.text.send", "PASS", duration_ms=send_timer.duration_ms, metadata={"text_chars": len(text)})
        trace.event(trace_id, "run.finish", "PASS", metadata={"route": "voice_to_text"})
    except Exception as exc:
        trace.event(trace_id, "run.finish", "FAIL", metadata={"error_type": type(exc).__name__, "error": str(exc)[:300]})
        await message.answer(f"Ошибка распознавания. trace: {trace_id}")

@router.message()
async def unsupported(message: Message) -> None:
    trace_id = trace.new_trace_id()
    trace.event(trace_id, "telegram.message.received", "PASS", metadata=message_meta(message))
    trace.event(trace_id, "route.unsupported", "WARN", metadata={"content_type": str(message.content_type)})
    trace.event(trace_id, "run.finish", "WARN", metadata={"reason": "unsupported_content_type"})
    await message.answer("Пока принимаю только текст и голосовые сообщения.")

async def run() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(run())