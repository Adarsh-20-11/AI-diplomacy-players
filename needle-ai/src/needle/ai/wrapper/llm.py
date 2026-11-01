from typing import Any

from needle.llmapi import gemini, openai


class LLM:
    def __init__(self, provider: str, model: str, sync: str):
        self.provider = provider
        self.sync = sync
        self.model = model

    def generate(self, prompt:str, user_input:str) -> dict[str, Any]:
        if self.provider == 'openai':
            client = openai.OpenAIHelper(self.model,self.sync)
            response = client.invoke(prompt, user_input)
        elif self.provider == 'gemini':
            client2 = gemini.GeminiHelper(self.model,self.sync)
            response = client2.invoke(prompt, user_input)
        else:
            raise SyntaxError("Invalid provider name. " \
            "Either the provider does not exist or we do not support it. " \
            "Check the list of supported providers in our docs.")
        return response