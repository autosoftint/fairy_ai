# -*- coding: utf-8 -*-
# cython: language_level=3
from datetime import datetime
from typing import AsyncGenerator
from abc import ABC, abstractmethod
from config import agent as agent_config

# Construct the System Prompt
LLM_FAIRY_PROMPT_LEN: int = len(agent_config.LLM_AGENT_PROMPT)
LLM_AGENT_PROMPT: str = '\n\n'.join(f"{ii + 1}. {agent_config.LLM_AGENT_PROMPT[ii]}" for ii in range(LLM_FAIRY_PROMPT_LEN))


def runtime_prompt_time() -> str:
    return agent_config.LLM_AGENT_RUNTIME_PROMPT_TIME.format(
        timestamp = datetime.now().strftime(agent_config.LLM_AGENT_RUNTIME_PROMPT_TIME_FORMAT)
    )


LLM_RUNTIME_TOKEN: list = [
    runtime_prompt_time
]


def system_prompt() -> str:
    # Generate the runtime token.
    runtime_prompt: str = '\n\n'.join(f"{LLM_FAIRY_PROMPT_LEN + ii + 1}. {x()}" for ii, x in enumerate(LLM_RUNTIME_TOKEN))
    return f"{LLM_AGENT_PROMPT}\n\n{runtime_prompt}\n\n{agent_config.LLM_AGENT_SUFFIX}"


class LLM(ABC):
    @abstractmethod
    async def chat_completion(self, user_prompt: str) -> AsyncGenerator[str | None]:
        raise NotImplementedError
