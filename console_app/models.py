"""Task model with rich metadata support."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
import uuid


@dataclass
class Task:
    """Represents a todo task with metadata.

    Attributes:
        id: Unique identifier (UUID)
        title: Task title (required, max 200 chars)
        notes: Additional notes/description (optional, max 1000 chars)
        priority: Task priority - "low", "medium", "high"
        due_date: Optional due date
        category: Task category - "general", "work", "personal", "study", "shopping"
        completed: Whether task is completed
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    notes: str = ""
    priority: str = "medium"  # "low", "medium", "high"
    due_date: Optional[date] = None
    category: str = "general"  # "general", "work", "personal", "study", "shopping"
    completed: bool = False

    def __post_init__(self):
        """Validate and truncate fields after initialization."""
        # Truncate title to 200 chars
        if len(self.title) > 200:
            self.title = self.title[:200]

        # Truncate notes to 1000 chars
        if len(self.notes) > 1000:
            self.notes = self.notes[:1000]

        # Validate priority
        valid_priorities = {"low", "medium", "high"}
        if self.priority not in valid_priorities:
            self.priority = "medium"

        # Validate category
        valid_categories = {"general", "work", "personal", "study", "shopping"}
        if self.category not in valid_categories:
            self.category = "general"

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "category": self.category,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create task from dictionary (JSON deserialization)."""
        d = data.copy()
        if d.get("due_date"):
            d["due_date"] = date.fromisoformat(d["due_date"])
        return cls(**d)

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue (past due date and not completed)."""
        if self.completed or not self.due_date:
            return False
        return self.due_date < date.today()

    @property
    def short_id(self) -> str:
        """Return first 8 characters of ID for display."""
        return self.id[:8]
