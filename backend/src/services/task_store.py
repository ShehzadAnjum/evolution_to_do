"""In-memory task storage with CRUD operations.

This module provides the TaskStore class for managing tasks in memory.
"""

from typing import Optional

from src.models.task import Task


class TaskStore:
    """In-memory storage for tasks with CRUD operations.

    Provides O(1) lookups by ID and maintains insertion order via sequential IDs.
    All data is lost when the application exits (session-only storage).
    """

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Create and store a new task.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            The created task with assigned ID
        """
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Get all tasks, ordered by ID (insertion order).

        Returns:
            List of all tasks sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Task]:
        """Update task fields.

        Only updates fields that are explicitly provided (not None).
        Empty string for description clears it.

        Args:
            task_id: The ID of the task to update
            title: New title (None to keep current)
            description: New description (None to keep current, "" to clear)

        Returns:
            The updated task if found, None otherwise

        Raises:
            ValueError: If title is provided but empty
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.completed = not task.completed
        return task

    def count(self) -> int:
        """Return total number of tasks."""
        return len(self._tasks)

    def count_completed(self) -> int:
        """Return number of completed tasks."""
        return sum(1 for t in self._tasks.values() if t.completed)

    def count_remaining(self) -> int:
        """Return number of incomplete tasks."""
        return self.count() - self.count_completed()

    def is_empty(self) -> bool:
        """Check if store has no tasks."""
        return len(self._tasks) == 0
