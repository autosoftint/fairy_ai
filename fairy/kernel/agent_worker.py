# -*- coding: utf-8 -*-
# cython: language_level=3
import json
import asyncio
import importlib
from websockets.asyncio.client import connect
import config


async def start_working() -> None:
    # Check the source is text or from STT.
    async with connect(f"ws://127.0.0.1:{config.AGENT_PORT}") as ws:
        # Fetch the current task.
        await ws.send(json.dumps({"op": "fetch"}))
        records = json.loads(await ws.recv())['records']
    # Check out the current request.
    if 'request' not in records:
        # Seems nothing should do, probably start the mission twice.
        return
    request: dict = records['request']
    # Check out the working mode.
    request_mode: str = request['mode']
    if request_mode == "text":
        user_token: str = request['text']
    else:
        print(f"unknown request mode {request_mode}")
        return
    # Construct the LLM communicator.
    # importlib.import_module(f"driver.llm.{config.LLM_MODULE}")


def main() -> None:
    asyncio.run(start_working())


if __name__ == "__main__":
    main()
