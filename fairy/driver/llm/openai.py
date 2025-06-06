# -*- coding: utf-8 -*-
# cython: language_level=3
import json
import aiohttp
import config
from typing import AsyncGenerator
from aiohttp import ClientConnectorError
from lib.llm import LLM, system_prompt


class Device(LLM):
    def __init__(self):
        self.__payload_base: dict = {
            "model": config.LLM_MODEL,
            "messages": [],
            "stream": True
        }

    async def chat_completion(self, user_prompt: str) -> AsyncGenerator[str | None]:
        # Construct the payload.
        payload: dict = self.__payload_base.copy()
        payload["messages"] = [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user_prompt}
        ]
        # Send the payload to LLM.
        async with aiohttp.ClientSession() as sess:
            headers: dict[str, str] = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.LLM_API_KEY}"
            }
            try:
                async with sess.post(f'{config.LLM_BASE_URL}/chat/completions',
                                     headers=headers,
                                     data=json.dumps(payload)) as response:
                    async for data in response.content:
                        if not data.startswith(b"data: "):
                            continue
                        data = data[6:]
                        if data.startswith(b"[DONE]"):
                            continue
                        choices = json.loads(data)['choices'][0]
                        if choices['finish_reason'] is None:
                            yield choices['delta']['content']
                        else:
                            if 'delta' in choices and 'content' in choices['delta']:
                                yield choices['delta']['content']
                            else:
                                yield None
            except ClientConnectorError:
                yield None
