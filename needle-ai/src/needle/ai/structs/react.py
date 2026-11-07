from needle.ai.wrapper.llm import LLM


def create_react_node() -> LLM:
    model = LLM("gemini", "flash 2.5", "sync")
    return model
