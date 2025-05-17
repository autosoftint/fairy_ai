# -*- coding: utf-8 -*-
# cython: language_level=3
import json
import asyncio
import aiohttp
import config


async def launch():
    async with aiohttp.ClientSession() as sess:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.LLM_API_KEY}"
        }

        payload = {
            "model": config.LLM_MODEL,
            "messages": [
                {"role": "system", "content": config.LLM_SYSTEM_PROMPT},
                {"role": "user", "content": "你好，你是谁呀？"}
            ],
            "temperature": 0,
            "stream": True
        }
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
                    print(choices['delta']['content'], end="")
                else:
                    print("")



def main():
    asyncio.run(launch())


if __name__ == "__main__":
    main()
