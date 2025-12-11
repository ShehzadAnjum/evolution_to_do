"""Business logic service for task operations."""

from typing import List, Optional
from datetime import date

from .models import Task


class TaskService:
    """Service layer for task business logic.

    Handles all task operations: CRUD, search, filter, sort.
    Separates business logic from storage and UI concerns.
    """

    def __init__(self, storage):
        """Initialize service with a storage backend.

        Args:
            storage: Storage implementation (e.g., JsonStorage)
        """
        self.storage = storage

    def load_tasks(self) -> List[Task]:
        """Load all tasks from storage."""
        return self.storage.load()

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save all tasks to storage."""
        self.storage.save(tasks)

    def add_task(self, tasks: List[Task], task: Task) -> List[Task]:
        """Add a new task to the list.

        Args:
            tasks: Current task list
            task: New task to add

        Returns:
            Updated task list
        """
        tasks.append(task)
        return tasks

    def find_by_id(self, tasks: List[Task], task_id: str) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            tasks: Task list to search
            task_id: Full or partial (short) task ID

        Returns:
            Task if found, None otherwise
        """
        for t in tasks:
            # Match full ID or short ID (first 8 chars)
            if t.id == task_id or t.id.startswith(task_id):
                return t
        return None

    def find_by_index(self, tasks: List[Task], index: int) -> Optional[Task]:
        """Find a task by its display index (1-based).

        Args:
            tasks: Task list to search
            index: 1-based index

        Returns:
            Task if found, None otherwise
        """
        if 1 <= index <= len(tasks):
            return tasks[index - 1]
        return None

    def update_task(
        self,
        task: Task,
        title: Optional[str] = None,
        notes: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[date] = None,
        category: Optional[str] = None,
    ) -> Task:
        """Update task fields (preserves unchanged fields).

        Args:
            task: Task to update
            title: New title (if provided)
            notes: New notes (if provided)
            priority: New priority (if provided)
            due_date: New due date (if provided)
            category: New category (if provided)

        Returns:
            Updated task
        """
        if title is not None and title.strip():
            task.title = title.strip()[:200]
        if notes is not None:
            task.notes = notes.strip()[:1000]
        if priority is not None and priority in {"low", "medium", "high"}:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date
        if category is not None and category in {"general", "work", "personal", "study", "shopping"}:
            task.category = category
        return task

    def delete_task(self, tasks: List[Task], task_id: str) -> List[Task]:
        """Delete a task by ID.

        Args:
            tasks: Current task list
            task_id: ID of task to delete

        Returns:
            Updated task list without the deleted task
        """
        return [t for t in tasks if t.id != task_id and not t.id.startswith(task_id)]

    def toggle_complete(self, task: Task) -> Task:
        """Toggle task completion status.

        Args:
            task: Task to toggle

        Returns:
            Updated task
        """
        task.completed = not task.completed
        return task

    def search(
        self,
        tasks: List[Task],
        text: str = "",
        priority: Optional[str] = None,
        category: Optional[str] = None,
        completed: Optional[bool] = None,
        overdue_only: bool = False,
    ) -> List[Task]:
        """Search and filter tasks.

        Args:
            tasks: Task list to search
            text: Search text (matches title and notes)
            priority: Filter by priority
            category: Filter by category
            completed: Filter by completion status
            overdue_only: Only return overdue tasks

        Returns:
            Filtered list of tasks
        """
        text_lower = text.lower()
        result = []

        for t in tasks:
            # Text search in title and notes
            if text and text_lower not in t.title.lower() and text_lower not in t.notes.lower():
                continue

            # Priority filter
            if priority and t.priority != priority:
                continue

            # Category filter
            if category and t.category != category:
                continue

            # Completion filter
            if completed is not None and t.completed != completed:
                continue

            # Overdue filter
            if overdue_only and not t.is_overdue:
                continue

            result.append(t)

        return result

    def sort_tasks(
        self,
        tasks: List[Task],
        by: str = "priority",
        reverse: bool = False,
    ) -> List[Task]:
        """Sort tasks by specified field.

        Args:
            tasks: Task list to sort
            by: Sort field - "priority", "due_date", "category", "title"
            reverse: Reverse sort order

        Returns:
            Sorted list of tasks
        """
        priority_order = {"high": 0, "medium": 1, "low": 2}

        if by == "priority":
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 1), reverse=reverse)
        elif by == "due_date":
            # Tasks without due date go to the end
            return sorted(
                tasks,
                key=lambda t: (t.due_date is None, t.due_date or date.max),
                reverse=reverse
            )
        elif by == "category":
            return sorted(tasks, key=lambda t: t.category, reverse=reverse)
        elif by == "title":
            return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
        else:
            return tasks

    def get_stats(self, tasks: List[Task]) -> dict:
        """Get task statistics.

        Args:
            tasks: Task list to analyze

        Returns:
            Dictionary with stats: total, completed, pending, overdue
        """
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        pending = total - completed
        overdue = sum(1 for t in tasks if t.is_overdue)

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
        }
