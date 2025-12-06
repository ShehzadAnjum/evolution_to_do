"""Task model for the todo application.

This module defines the Task dataclass representing a todo item.
"""

from dataclasses import dataclass
from typing import Optional

# Validation constants (from spec clarifications)
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000


@dataclass
class Task:
    """Represents a todo item that a user wants to track.

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
