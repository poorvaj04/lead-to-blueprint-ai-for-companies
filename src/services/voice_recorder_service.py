import threading
import time

import keyboard
import numpy as np
import sounddevice as sd
import soundfile as sf

from src.utils.logger import get_logger


class VoiceRecorderService:
    """
    Records microphone audio.
    """

    def __init__(self):

        self.logger = get_logger("VoiceRecorder")

        self.sample_rate = 16000

        self.channels = 1

        self.audio_frames = []

        self.recording = False

        self.output_file = "temp/recording.wav"

    # --------------------------------------------------

    def _audio_callback(
        self,
        indata,
        frames,
        time,
        status,
    ):

        if self.recording:

            self.audio_frames.append(indata.copy())

    # --------------------------------------------------

    def start_recording(self):

        self.logger.info("Recording Started")

        self.audio_frames.clear()

        self.recording = True

        self.stream = sd.InputStream(

            samplerate=self.sample_rate,

            channels=self.channels,

            callback=self._audio_callback,

        )

        self.stream.start()

    # --------------------------------------------------

    def stop_recording(self):

        self.recording = False

        self.stream.stop()

        self.stream.close()

        audio = np.concatenate(

            self.audio_frames,

            axis=0

        )

        sf.write(

            self.output_file,

            audio,

            self.sample_rate

        )

        self.logger.info("Recording Saved")

        return self.output_file

    # --------------------------------------------------

    def listen(self):

        print()

        print("Hold R to Speak...")

        keyboard.wait("r")

        self.start_recording()

        print("Recording... Release R")

        while keyboard.is_pressed("r"):

            time.sleep(0.01)

        audio_path = self.stop_recording()

        return audio_path