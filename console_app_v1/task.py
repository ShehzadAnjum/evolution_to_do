"""Task model for the todo application."""


class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier (sequential integer)
        title: Task title (required)
        description: Task description (optional)
        completed: Whether task is done
    """

    _id_counter = 0

    def __init__(self, title: str, description: str = ""):
        """Create a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)
        """
        Task._id_counter += 1
        self.id = Task._id_counter
        self.title = title[:200] if len(title) > 200 else title
        self.description = description[:1000] if len(description) > 1000 else description
        self.completed = False

    def toggle_complete(self):
        """Toggle the completion status."""
        self.completed = not self.completed

    def update(self, title: str = None, description: str = None):
        """Update task fields.

        Args:
            title: New title (if provided)
            description: New description (if provided)
        """
        if title and title.strip():
            self.title = title.strip()[:200]
        if description is not None:
            self.description = description.strip()[:1000]

    def __str__(self):
        """String representation for display."""
        status = "[X]" if self.completed else "[ ]"
        desc = f" - {self.description}" if self.description else ""
        return f"{self.id}. {status} {self.title}{desc}"

    @classmethod
    def reset_counter(cls):
        """Reset ID counter (for testing)."""
        cls._id_counter = 0
