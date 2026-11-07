from typing import Annotated, Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    text: str


class ToolCallBlock(BaseModel):
    type: Literal["tool_call"] = "tool_call"
    id: str = Field(default_factory=lambda: "tc-" + uuid4().hex)
    name: str
    arguments: dict[str, Any]
    provider_id: str | None = None


class ToolResultBlock(BaseModel):
    type: Literal["tool_result"] = "tool_result"
    id: str = Field(default_factory=lambda: "tr-" + uuid4().hex)
    tool_call_id: str
    content: str
    is_error: bool = False


class ReasoningBlock(BaseModel):
    type: Literal["reasoning"] = "reasoning"
    provider: str
    model: str
    data: dict[str, Any]


Block = Annotated[
    TextBlock | ToolCallBlock | ToolResultBlock | ReasoningBlock, Field(discriminator="type")
]


class Message(BaseModel):
    id: str = Field(default_factory=lambda: "mes-" + uuid4().hex)
    role: Literal["user", "assistant", "tool"]
    author: str | None = None
    content: list[Block]
