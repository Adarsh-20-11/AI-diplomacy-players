import llmapi

class LLM():
    def __init__(self, provider, model, sync):
        self.provider = provider
        self.sync = sync
        self.model = model

    def run(self):
        if self.provider == 'openai':
            client = llmapi.openai.OpenAIHelper(self.model,self.sync)
        elif self.provider == 'gemini':
            client = llmapi.gemini.GeminiHelper(self.model,self.sync)
        else:
            raise SyntaxError("Invalid provider name. Either the provider does not exist or we do not support it. Check the list of supported providers in our docs.")
        