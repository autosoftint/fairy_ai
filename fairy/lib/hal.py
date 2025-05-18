# -*- coding: utf-8 -*-
# cython: language_level=3
from abc import ABC, abstractmethod


class DeviceAbstract(ABC):
    pass


class DeviceCameraImage(DeviceAbstract):
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


class DeviceMicrophone(DeviceAbstract):
    def __init__(self):
        pass
