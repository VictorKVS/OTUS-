from __future__ import annotations

import asyncio
from pathlib import Path

import edge_tts
from faster_whisper import WhisperModel

class EdgeTTSProvider:
    def __init__(self, voice: str = "ru-RU-SvetlanaNeural") -> None:
        self.voice = voice

    async def synthesize(self, text: str, target: Path) -> None:
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(str(target))

class FasterWhisperSTTProvider:
    def __init__(self, model_name: str = "small", device: str = "cpu", compute_type: str = "int8") -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model: WhisperModel | None = None

    def _model_instance(self) -> WhisperModel:
        if self._model is None:
            self._model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type,
            )
        return self._model

    def _transcribe_sync(self, source: Path) -> tuple[str, str | None, float | None]:
        model = self._model_instance()
        segments, info = model.transcribe(str(source), vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments if segment.text.strip()).strip()
        language = getattr(info, "language", None)
        probability = getattr(info, "language_probability", None)
        return text, language, probability

    async def transcribe(self, source: Path) -> tuple[str, str | None, float | None]:
        return await asyncio.to_thread(self._transcribe_sync, source)