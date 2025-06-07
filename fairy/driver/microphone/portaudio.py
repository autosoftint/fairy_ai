# -*- coding: utf-8 -*-
# cython: language_level=3
import wave
import pyaudio
from lib.hal import DeviceMicrophone
from config import driver as driver_config


class Device(DeviceMicrophone):
    def __init__(self):
        super().__init__()
        # Calculate the silence chunks.
        rate: int = 16000
        frames_per_buffer: int = 1024
        silence_chunks: int = int(driver_config.MICROPHONE_SILENCE_SEC * rate / frames_per_buffer)
        # Initial the device.
        self.__audio: pyaudio.PyAudio = pyaudio.PyAudio()
        self.__stream: pyaudio.Stream | None = None
        try:
            self.__stream = self.__audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                frames_per_buffer=frames_per_buffer,
                input=True,
                input_device_index=1,
            )
        except Exception as e:
            print(f"Error happens when initializing microphone: {e}")
