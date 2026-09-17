from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    def invoke(self, prompt:str, user_input:str) -> str:
        pass

    @abstractmethod
    async def ainvoke(self, prompt:str, user_input:str) -> str:
        pass
