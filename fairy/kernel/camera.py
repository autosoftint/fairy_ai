# -*- coding: utf-8 -*-
import socket
import asyncio
import importlib
from types import ModuleType
import websockets
from websockets.asyncio.server import serve, ServerConnection
from lib.hal import DeviceCameraImage
import config


async def run_server() -> None:
    print("starting camera server...")
    # Load the camera from driver.
    camera_module: ModuleType = importlib.import_module(f"driver.camera.{config.CAMERA_MODULE}")
    camera: DeviceCameraImage = camera_module.Device()

    async def __handler(websocket: ServerConnection) -> None:
        # Accept the connection.
        async for message in websocket:
            print(message, camera)
            await websocket.send(message)

    # Launch the camera control server.
    while True:
        try:
            async with serve(__handler, "127.0.0.1", config.CAMERA_PORT):
                await asyncio.get_event_loop().create_future()
        except (ConnectionError, OSError, websockets.exceptions.WebSocketException):
            pass


def main() -> None:
    # Create the communicate server.
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
