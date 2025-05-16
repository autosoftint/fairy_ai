# -*- coding: utf-8 -*-
import os

PATH_LIB: str = os.path.dirname(os.path.abspath(__file__))
PATH_FAIRY: str = os.path.dirname(PATH_LIB)
PATH_KERNEL: str = os.path.join(PATH_FAIRY, "kernel")