import os
from .base import BaseLLMClient
from openai import OpenAI, AsyncOpenAI
from json_standardize import JSONStandardizer 
from exceptions import LLMAPIError

class OpenAIHelper(BaseLLMClient):
    def __init__(self, model: str, api_key:str = None):
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Missing OpenAI API key, either set OPENAI_API_KEY in .env, or add it to the object constructor")
        self.client = OpenAI(api_key = self.api_key)
        self.aclient = AsyncOpenAI(api_key = self.api_key)

    def invoke(self, prompt:str, user_input:str) -> dict:
        try:
            response = self.client.responses.create(
                model = self.model,
                instructions = prompt,
                input = user_input
            )
        except Exception as e:
            raise LLMAPIError(f"OpenAI response generated an error:{e}")

        return JSONStandardizer.openai_response(response.model_dump(), model=self.model)

    async def ainvoke(self, prompt:str, user_input:str) -> dict:
        try:
            response = await self.aclient.responses.create(
                model = self.model,
                instructions = prompt,
                input = user_input
            )
        except Exception as e:
            raise LLMAPIError(f"OpenAI response generated an error:{e}")

        return JSONStandardizer.openai_response(response.model_dump(), model=self.model)

    def invoke_chat(self, messages:list[dict]) -> dict:
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages
            )
        except Exception as e:
            raise LLMAPIError(f"OpenAI response generated an error:{e}")

        return JSONStandardizer.openai_chat(response.model_dump(), model=self.model)

    async def ainvoke_chat(self, messages:list[dict]) -> dict:
        try:
            response = await self.aclient.chat.completions.create(
                model = self.model,
                messages = messages
            )
        except Exception as e:
            raise LLMAPIError(f"OpenAI response generated an error:{e}")
    
        
        return JSONStandardizer.openai_chat(response.model_dump(), model=self.model)