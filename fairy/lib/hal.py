# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class DeviceCameraImage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def capture(self):
        raise NotImplementedError

    @abstractmethod
    def wait(self):
        raise NotImplementedError

    @abstractmethod
    def read_buffer(self):
        raise NotImplementedError