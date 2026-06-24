from dataclasses import dataclass


@dataclass
class SpeechResult:

    audio_path: str

    raw_transcript: str

    transcript: str

    inference_time: float