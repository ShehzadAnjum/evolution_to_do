"""Task manager for in-memory task operations."""

from typing import List, Optional
from .task import Task


class TaskManager:
    """Manages a collection of tasks in memory.

    Provides CRUD operations for tasks.
    Note: Tasks are NOT persisted - cleared when app exits.
    """

    def __init__(self):
        """Initialize with empty task list."""
        self.tasks: List[Task] = []

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            The created Task object
        """
        task = Task(title, description)
        self.tasks.append(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The task ID to find

        Returns:
            Task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks
        """
        return self.tasks

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """Update a task.

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if updated, False if task not found
        """
        task = self.get_task(task_id)
        if task:
            task.update(title, description)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if task not found
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle task completion status.

        Args:
            task_id: ID of task to toggle

        Returns:
            True if toggled, False if task not found
        """
        task = self.get_task(task_id)
        if task:
            task.toggle_complete()
            return True
        return False

    def get_stats(self) -> dict:
        """Get task statistics.

        Returns:
            Dictionary with total, completed, pending counts
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
        }
