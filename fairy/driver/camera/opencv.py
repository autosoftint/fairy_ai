# -*- coding: utf-8 -*-
import cv2
from lib.hal import DeviceCameraImage


class Device(DeviceCameraImage):
    def __init__(self):
        super().__init__()
        # Use the default camera.
        self.__camera = cv2.VideoCapture(0)

    def capture(self):
        pass

    def wait(self):
        pass

    def read_buffer(self):
        # Check if the camera opened successfully.
        if not self.__camera.isOpened():
            return b''

        # Save the captured image.
        ret, frame = self.__camera.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        return b''
