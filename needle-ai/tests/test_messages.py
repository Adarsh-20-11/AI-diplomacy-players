import pytest
from pydantic import ValidationError

from needle.core.message import (
    Block,
    Message,
    ReasoningBlock,
    TextBlock,
    ToolCallBlock,
    ToolResultBlock,
)


def test_round_trip() -> None:
    b1 = TextBlock(text="This is a text block")
    b2 = ToolCallBlock(name="Sample Tool Call", arguments={"arg1": 20}, provider_id="01")
    b3 = ToolResultBlock(tool_call_id=b2.id, content="Sample Tool Result")
    b4 = ReasoningBlock(
        provider="OpenAI", model="GPT-5", data={"reasoning": "Wow, this is so difficult"}
    )
    blocks: list[Block] = [b1, b2, b3, b4]
    original = Message(role="assistant", content=blocks)
    j = original.model_dump_json()
    restored = Message.model_validate_json(j)
    assert restored == original
    assert isinstance(restored.content[0], TextBlock)
    assert isinstance(restored.content[1], ToolCallBlock)
    assert isinstance(restored.content[2], ToolResultBlock)
    assert isinstance(restored.content[3], ReasoningBlock)


def test_bad_role() -> None:
    with pytest.raises(ValidationError):
        Message(role="system", content=[])  # type: ignore[arg-type]


def test_bad_tag() -> None:
    with pytest.raises(ValidationError):
        Message.model_validate({"role": "user", "content": [{"type": "video", "url": "x.mp4"}]})
