"""Models package for the todo application.

Exports all models for easy importing.
"""

from src.models.conversation import (
    Conversation,
    ConversationBase,
    ConversationCreate,
    ConversationRead,
)
from src.models.message import (
    Message,
    MessageBase,
    MessageCreate,
    MessageRead,
    MessageRole,
)
from src.models.task import (
    MAX_DESCRIPTION_LENGTH,
    MAX_TITLE_LENGTH,
    Task,
    TaskBase,
    TaskCreate,
    TaskDB,
    TaskRead,
    TaskUpdate,
)

__all__ = [
    # Task models (Phase I & II)
    "Task",
    "TaskBase",
    "TaskDB",
    "TaskCreate",
    "TaskUpdate",
    "TaskRead",
    "MAX_TITLE_LENGTH",
    "MAX_DESCRIPTION_LENGTH",
    # Conversation models (Phase III)
    "Conversation",
    "ConversationBase",
    "ConversationCreate",
    "ConversationRead",
    # Message models (Phase III)
    "Message",
    "MessageBase",
    "MessageCreate",
    "MessageRead",
    "MessageRole",
]
