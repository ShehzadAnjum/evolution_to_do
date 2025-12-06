"""Task model for the todo application.

This module defines Task models for both Phase I (dataclass) and Phase II (SQLModel).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

# Validation constants (from spec clarifications)
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000


# =============================================================================
# Phase I: Dataclass model (for CLI, backward compatibility)
# =============================================================================


@dataclass
class Task:
    """Phase I Task model - simple dataclass for CLI application.

    Attributes:
        id: Unique identifier assigned by system (sequential, starting from 1)
        title: User-provided task title (required, non-empty, max 200 chars)
        description: Optional task description (max 1000 chars)
        completed: Completion status (default: False)
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = self.title.strip()[:MAX_TITLE_LENGTH]
        if self.description:
            self.description = self.description.strip()[:MAX_DESCRIPTION_LENGTH]


# =============================================================================
# Phase II: SQLModel models (for web application)
# =============================================================================


class TaskBase(SQLModel):
    """Base task fields shared by all task schemas."""

    title: str = Field(min_length=1, max_length=MAX_TITLE_LENGTH)
    description: str = Field(default="", max_length=MAX_DESCRIPTION_LENGTH)
    is_complete: bool = Field(default=False)


class TaskDB(TaskBase, table=True):
    """Database model for tasks (SQLModel table)."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # Note: Foreign key constraint exists at database level
    # We don't define it here to avoid SQLModel metadata resolution issues
    # The user table is managed by Better Auth (uses TEXT for user.id)
    user_id: str = Field(index=True, description="Owner user ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for creating a task (request body)."""

    title: str = Field(min_length=1, max_length=MAX_TITLE_LENGTH)
    description: str = Field(default="", max_length=MAX_DESCRIPTION_LENGTH)


class TaskUpdate(SQLModel):
    """Schema for updating a task (partial update)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=MAX_TITLE_LENGTH)
    description: Optional[str] = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    is_complete: Optional[bool] = None


class TaskRead(TaskBase):
    """Schema for reading a task (response body)."""

    id: UUID
    user_id: str  # Better Auth uses TEXT for user.id
    created_at: datetime
    updated_at: datetime
