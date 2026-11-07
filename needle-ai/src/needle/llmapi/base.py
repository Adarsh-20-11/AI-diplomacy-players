from abc import ABC, abstractmethod
from typing import Any


class BaseLLMClient(ABC):
    @abstractmethod
    def invoke(self, prompt: str, user_input: str) -> dict[str, Any]:
        pass

    @abstractmethod
    async def ainvoke(self, prompt: str, user_input: str) -> dict[str, Any]:
        pass
