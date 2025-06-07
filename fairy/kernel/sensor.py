# -*- coding: utf-8 -*-
# cython: language_level=3
import asyncio
import importlib
from types import ModuleType
import websockets
from websockets.asyncio.server import serve, ServerConnection
from lib.hal import DeviceAbstract
from config import driver as driver_config


async def run_server() -> None:
    print("starting sensor manager...", flush=True)
    def __load_device(device_type: str, device_name: str) -> DeviceAbstract:
        # Load the device module.
        device_module: ModuleType = importlib.import_module(f"driver.{device_type}.{device_name}")
        # Create the device instance.
        return device_module.Device()

    # Load the specific driver for the device.
    devices: dict[str, DeviceAbstract] = {}
    if driver_config.CAMERA_ENABLE:
        devices["camera"] = __load_device('camera', driver_config.CAMERA_MODULE)

    async def __handler(websocket: ServerConnection) -> None:
        # Accept the connection.
        async for message in websocket:
            print(message, devices)
            await websocket.send(message)

    # Launch the camera control server.
    while True:
        try:
            async with serve(__handler, "127.0.0.1", driver_config.CAMERA_PORT):
                await asyncio.get_event_loop().create_future()
        except (ConnectionError, OSError, asyncio.CancelledError, websockets.exceptions.WebSocketException):
            pass


def main() -> None:
    # Create the camera communicating server.
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
