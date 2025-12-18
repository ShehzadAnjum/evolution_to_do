"""Message model for Phase III AI Chatbot.

This module defines the Message model for storing chat messages.
"""

import uuid
from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class MessageRole(str, Enum):
    """Valid message roles."""

    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class MessageBase(SQLModel):
    """Base message fields shared by all message schemas."""

    role: str = Field(description="Message role: user, assistant, or tool")
    content: str = Field(description="Message content")
    tool_calls: Optional[str] = Field(
        default=None, description="JSON string of tool calls (for assistant messages)"
    )
    tool_call_id: Optional[str] = Field(
        default=None, description="Tool call ID this message responds to (for tool messages)"
    )


class Message(MessageBase, table=True):
    """Database model for messages (SQLModel table)."""

    __tablename__ = "message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(index=True, description="Parent conversation ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MessageCreate(SQLModel):
    """Schema for creating a message (internal use)."""

    role: str
    content: str
    tool_calls: Optional[str] = None
    tool_call_id: Optional[str] = None


class MessageRead(MessageBase):
    """Schema for reading a message (response body)."""

    id: uuid.UUID
    conversation_id: uuid.UUID
    created_at: datetime
