# -*- coding: utf-8 -*-
# cython: language_level=3
import json
import asyncio
import websockets
from websockets.asyncio.server import serve, ServerConnection
from lib import process, history
import config

# Prepare an agent worker thread.
agent_worker: process.Proc = None


async def run_server() -> None:
    global agent_worker

    print("starting agent manager...", flush=True)
    # Load the LLM history from disk.
    records: dict = await history.load_records()

    async def __handler(websocket: ServerConnection) -> None:
        global agent_worker

        async def __reply(content: dict) -> None:
            await websocket.send(json.dumps(content))

        def __is_worker_free() -> bool:
            return agent_worker is None or agent_worker.poll() is not None

        # Accept the connection.
        async for message in websocket:
            # Parse the message.
            try:
                command: dict = json.loads(message)
            except json.decoder.JSONDecodeError:
                await __reply({"code": 400})
                continue
            # Check out the command.
            if "op" not in command:
                await __reply({"code": 400})
                continue
            op: str = command["op"]
            if op == "start":
                # Start the agent worker with the text.
                if __is_worker_free():
                    # Save the current command to record.
                    records["request"] = command
                    # Start the worker process.
                    agent_worker = process.launch_subprocess("agent_worker")
                else:
                    await __reply({"code": 403})
                    continue
                # Handle the message.
                await __reply({"code": 200})
            elif op == "fetch":
                # Give back the current stored records.
                await __reply({"code": 200, "records": records})
            elif op == "stop":
                # Check whether the agent worker is running.
                if not __is_worker_free():
                    # Kill the worker.
                    process.terminate(agent_worker)
                await __reply({"code": 200})
            else:
                await __reply({"code": 404})

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
