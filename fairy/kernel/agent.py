# -*- coding: utf-8 -*-
# cython: language_level=3
import json
import asyncio
import websockets
from websockets.asyncio.server import serve, ServerConnection
from lib import process
import config


async def run_server() -> None:
    # Launch the queue.
    print("starting agent manager...", flush=True)

    agent_worker: process.Proc = None

    async def __handler(websocket: ServerConnection) -> None:
        async def __send_response(content: dict) -> None:
            await websocket.send(json.dumps(content))

        # Accept the connection.
        async for message in websocket:
            # Parse the message.
            try:
                command: dict = json.loads(message)
            except json.decoder.JSONDecodeError:
                await __send_response({"code": 400})
                continue
            # Check out the command.
            if "op" not in command:
                await __send_response({"code": 400})
                continue
            op: str = command["op"]
            if op == "start_text":
                if "text" not in command:
                    await __send_response({"code": 400})
                    continue
                # Start the agent worker with the text.
                print(command)
                # Handle the message.
                await __send_response({"code": 200})
            else:
                await __send_response({"code": 404})

    # Loop forever to serve the command sent from html.
    try:
        while True:
            try:
                async with serve(__handler, "127.0.0.1", config.AGENT_PORT):
                    await asyncio.get_event_loop().create_future()
            except (ConnectionError, OSError, asyncio.CancelledError, websockets.exceptions.WebSocketException):
                pass
    except Exception as e:
        raise e
    finally:
        process.terminate(agent_worker)


def main() -> None:
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
