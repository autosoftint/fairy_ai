# -*- coding: utf-8 -*-
# cython: language_level=3
import asyncio
import edge_tts

TEXT = "Hello World! 但是有中文哦？"
VOICE = "zh-CN-XiaoyiNeural"
OUTPUT_FILE = "test.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(amain())