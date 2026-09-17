import os
from google import genai
from google.genai import types
from exceptions import LLMAPIError
from json_standardize import JSONStandardizer
from .base import BaseLLMClient

class GeminiHelper(BaseLLMClient):
    def __init__(self, model: str, api_key: str = None):
        self.model = model
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Missing Gemini API key. Set GEMINI_API_KEY in your environment or pass it to the constructor."
            )
        self.client = genai.Client(api_key=self.api_key)
        self.aclient = genai.Client(api_key=self.api_key).aio

    def invoke(self, prompt: str, user_input: str) -> dict:
        try:
            config = types.GenerateContentConfig(system_instruction=prompt)
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_input,
                config=config,
            )
        except Exception as e:
            raise LLMAPIError(f"Gemini response generated an error: {e}")

        return JSONStandardizer.gemini(response.model_dump(), model=self.model)

    async def ainvoke(self, prompt: str, user_input: str) -> dict:
        try:
            config = types.GenerateContentConfig(system_instruction=prompt)
            response = await self.aclient.models.generate_content(
                model=self.model,
                contents=user_input,
                config=config,
            )
        except Exception as e:
            raise LLMAPIError(f"Gemini response generated an error: {e}")

        return JSONStandardizer.gemini(response.model_dump(), model=self.model)

    def invoke_chat(self, messages: list[dict]) -> dict:
        try:
            system_instruction = None
            formatted_contents = []

            for msg in messages:
                role = msg.get("role")
                content = msg.get("content", "")
                if role == "system":
                    system_instruction = content
                elif role == "user":
                    formatted_contents.append(types.Content(role="user", parts=[types.Part.from_text(text=content)]))
                elif role in ["assistant", "model"]:
                    formatted_contents.append(types.Content(role="model", parts=[types.Part.from_text(text=content)]))

            config = types.GenerateContentConfig(system_instruction=system_instruction) if system_instruction else None

            response = self.client.models.generate_content(
                model=self.model,
                contents=formatted_contents,
                config=config,
            )
        except Exception as e:
            raise LLMAPIError(f"Gemini chat response generated an error: {e}")

        return JSONStandardizer.gemini(response.model_dump(), model=self.model)

    async def ainvoke_chat(self, messages: list[dict]) -> dict:
        try:
            system_instruction = None
            formatted_contents = []

            for msg in messages:
                role = msg.get("role")
                content = msg.get("content", "")
                if role == "system":
                    system_instruction = content
                elif role == "user":
                    formatted_contents.append(types.Content(role="user", parts=[types.Part.from_text(text=content)]))
                elif role in ["assistant", "model"]:
                    formatted_contents.append(types.Content(role="model", parts=[types.Part.from_text(text=content)]))

            config = types.GenerateContentConfig(system_instruction=system_instruction) if system_instruction else None

            response = await self.aclient.models.generate_content(
                model=self.model,
                contents=formatted_contents,
                config=config,
            )
        except Exception as e:
            raise LLMAPIError(f"Gemini chat response generated an error: {e}")

        return JSONStandardizer.gemini(response.model_dump(), model=self.model)