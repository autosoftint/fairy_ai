# -*- coding: utf-8 -*-
# cython: language_level=3
from typing import AsyncGenerator
from abc import ABC, abstractmethod


class LLM(ABC):
    @abstractmethod
    async def chat_completion(self, payload: dict) -> AsyncGenerator:
        raise NotImplementedError