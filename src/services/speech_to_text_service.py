import os
import random
import time

from groq import Groq

from src.config.settings import settings
from src.dtos.speech_result import SpeechResult
from src.services.text_normalization_service import (
    TextNormalizationService,
)
from src.utils.logger import get_logger

class SpeechToTextService:
    """
    Records live speech and converts it into text
    using Groq Cloud Whisper API.
    """

    def __init__(self):

        self.logger = get_logger("SpeechToText")

        self.api_keys = settings.GROQ_API_KEYS
        if not self.api_keys:
            self.logger.warning("No Groq API keys found in settings!")

        # Text Normalizer
        self.normalizer = TextNormalizationService()

        self.logger.info("Groq Cloud Whisper API Ready")

    def _get_client(self):
        # Randomly select a key to load-balance across the 4 free tiers
        api_key = random.choice(self.api_keys)
        return Groq(api_key=api_key)

    # --------------------------------------------------

    def transcribe(
        self,
        audio_path: str,
    ) -> SpeechResult:

        start = time.perf_counter()

        try:
            client = self._get_client()
            
            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_path), file.read()),
                    model="whisper-large-v3",
                    response_format="json",
                    language=settings.WHISPER_LANGUAGE,
                )
                
            raw_transcript = transcription.text.strip()
            
        except Exception as e:
            self.logger.error(f"Groq API Error: {str(e)}")
            raw_transcript = ""

        inference_time = (
            time.perf_counter() - start
        )

        transcript = self.normalizer.normalize(
            raw_transcript
        )

        return SpeechResult(
            audio_path=audio_path,
            raw_transcript=raw_transcript,
            transcript=transcript,
            inference_time=inference_time,
        )

    # --------------------------------------------------

    def listen(self) -> SpeechResult:
        from src.services.voice_recorder_service import VoiceRecorderService
        recorder = VoiceRecorderService()
        audio_path = recorder.listen()

        return self.transcribe(
            audio_path
        )