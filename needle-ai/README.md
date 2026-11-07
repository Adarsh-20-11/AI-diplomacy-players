# needle

A Python library for building AI agents from prebuilt patterns (ReAct, Reflection, ...) that
you can eject into editable graphs.

> **Status: pre-alpha.** Not on PyPI, and the API will change. Right now this package holds the
> canonical message model and the early provider clients; the first working agent is still
> being built.

## What's here

| Module | What it is |
|---|---|
| `needle.core.message` | The canonical message model: typed content blocks (text, tool call, tool result, reasoning) and `Message`, validated with Pydantic |
| `needle.llmapi` | Early OpenAI and Gemini clients. They predate the current design and will be replaced by provider adapters |
| `needle.ai` | Early wrapper and ReAct placeholder, also due to be replaced |

```python
from needle.core.message import Message, TextBlock

msg = Message(role="user", content=[TextBlock(text="What's the weather in Pune?")])
msg.model_dump_json()  # the same format, whichever provider the message goes to
```

## Development

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```
uv sync
uv run ruff check
uv run ruff format
uv run mypy src
uv run pytest
```

mypy runs in strict mode, and CI runs all checks on Python 3.12 and 3.13.

## More

The design, the ADRs and the project's background are in the
[repository README](../README.md).
