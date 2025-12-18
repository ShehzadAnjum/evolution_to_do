"""Conversation model for Phase III AI Chatbot.

This module defines the Conversation model for storing chat sessions.
"""

import uuid
from datetime import datetime, UTC
from typing import Optional

from sqlmodel import Field, SQLModel


class ConversationBase(SQLModel):
    """Base conversation fields shared by all conversation schemas."""

    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    """Database model for conversations (SQLModel table)."""

    __tablename__ = "conversation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True, description="Owner user ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ConversationCreate(SQLModel):
    """Schema for creating a conversation (request body)."""

    title: Optional[str] = Field(default=None, max_length=255)


class ConversationRead(ConversationBase):
    """Schema for reading a conversation (response body)."""

    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
