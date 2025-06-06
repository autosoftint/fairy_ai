# -*- coding: utf-8 -*-
# cython: language_level=3
import os

PATH_LIB: str = os.path.dirname(os.path.abspath(__file__))
PATH_FAIRY: str = os.path.dirname(PATH_LIB)
PATH_KERNEL: str = os.path.join(PATH_FAIRY, "kernel")
PATH_WEB: str = os.path.join(PATH_FAIRY, "web")
PATH_WEB_STATIC: str = os.path.join(PATH_WEB, "static")

PATH_STORAGE: str = os.path.join(PATH_FAIRY, "storage")
PATH_STORAGE_TTS: str = os.path.join(PATH_STORAGE, "tts")