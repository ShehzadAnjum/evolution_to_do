"""Tests for TaskService."""

import pytest
from datetime import date

from console_app_v2.models import Task
from console_app_v2.services import TaskService


class DummyStorage:
    """Mock storage for testing."""

    def __init__(self, initial_tasks=None):
        self.tasks = initial_tasks or []
        self.saved = None

    def load(self):
        return self.tasks

    def save(self, tasks):
        self.saved = tasks


@pytest.fixture
def service():
    """Create TaskService with dummy storage."""
    return TaskService(DummyStorage())


@pytest.fixture
def service_with_tasks():
    """Create TaskService with pre-loaded tasks."""
    tasks = [
        Task(id="task-1", title="Buy milk", priority="low", category="shopping"),
        Task(id="task-2", title="Study math", priority="high", category="study"),
        Task(id="task-3", title="Call mom", priority="medium", category="personal", completed=True),
    ]
    storage = DummyStorage(tasks)
    return TaskService(storage), tasks


class TestTaskCRUD:
    """Tests for basic CRUD operations."""

    def test_add_task(self, service):
        """Can add a task to the list."""
        tasks = []
        task = Task(title="New task")
        tasks = service.add_task(tasks, task)

        assert len(tasks) == 1
        assert tasks[0].title == "New task"

    def test_find_by_id_full(self, service_with_tasks):
        """Can find task by full ID."""
        service, tasks = service_with_tasks
        found = service.find_by_id(tasks, "task-2")

        assert found is not None
        assert found.title == "Study math"

    def test_find_by_id_partial(self, service_with_tasks):
        """Can find task by partial ID prefix."""
        service, tasks = service_with_tasks
        found = service.find_by_id(tasks, "task-1")

        assert found is not None
        assert found.title == "Buy milk"

    def test_find_by_id_not_found(self, service_with_tasks):
        """Returns None when ID not found."""
        service, tasks = service_with_tasks
        found = service.find_by_id(tasks, "nonexistent")

        assert found is None

    def test_find_by_index(self, service_with_tasks):
        """Can find task by 1-based index."""
        service, tasks = service_with_tasks

        assert service.find_by_index(tasks, 1).title == "Buy milk"
        assert service.find_by_index(tasks, 2).title == "Study math"
        assert service.find_by_index(tasks, 3).title == "Call mom"

    def test_find_by_index_invalid(self, service_with_tasks):
        """Returns None for invalid index."""
        service, tasks = service_with_tasks

        assert service.find_by_index(tasks, 0) is None
        assert service.find_by_index(tasks, 4) is None
        assert service.find_by_index(tasks, -1) is None

    def test_delete_task(self, service_with_tasks):
        """Can delete a task by ID."""
        service, tasks = service_with_tasks
        tasks = service.delete_task(tasks, "task-2")

        assert len(tasks) == 2
        assert service.find_by_id(tasks, "task-2") is None

    def test_toggle_complete(self, service):
        """Can toggle task completion."""
        task = Task(title="Test", completed=False)
        service.toggle_complete(task)
        assert task.completed is True

        service.toggle_complete(task)
        assert task.completed is False


class TestTaskUpdate:
    """Tests for task update operations."""

    def test_update_title(self, service):
        """Can update task title."""
        task = Task(title="Old title")
        service.update_task(task, title="New title")
        assert task.title == "New title"

    def test_update_preserves_unchanged(self, service):
        """Update preserves fields not being changed."""
        task = Task(title="Original", notes="Notes", priority="high")
        service.update_task(task, title="Updated")

        assert task.title == "Updated"
        assert task.notes == "Notes"
        assert task.priority == "high"

    def test_update_empty_title_preserved(self, service):
        """Empty title string preserves original."""
        task = Task(title="Original")
        service.update_task(task, title="")
        assert task.title == "Original"

    def test_update_all_fields(self, service):
        """Can update all fields at once."""
        task = Task(title="Test")
        due = date(2025, 12, 31)

        service.update_task(
            task,
            title="Updated",
            notes="New notes",
            priority="high",
            due_date=due,
            category="work",
        )

        assert task.title == "Updated"
        assert task.notes == "New notes"
        assert task.priority == "high"
        assert task.due_date == due
        assert task.category == "work"


class TestTaskSearch:
    """Tests for search and filter."""

    def test_search_by_text_title(self, service_with_tasks):
        """Can search tasks by title text."""
        service, tasks = service_with_tasks
        results = service.search(tasks, text="milk")

        assert len(results) == 1
        assert results[0].title == "Buy milk"

    def test_search_by_text_case_insensitive(self, service_with_tasks):
        """Text search is case insensitive."""
        service, tasks = service_with_tasks
        results = service.search(tasks, text="MATH")

        assert len(results) == 1
        assert results[0].title == "Study math"

    def test_filter_by_priority(self, service_with_tasks):
        """Can filter by priority."""
        service, tasks = service_with_tasks
        results = service.search(tasks, priority="high")

        assert len(results) == 1
        assert results[0].title == "Study math"

    def test_filter_by_category(self, service_with_tasks):
        """Can filter by category."""
        service, tasks = service_with_tasks
        results = service.search(tasks, category="shopping")

        assert len(results) == 1
        assert results[0].title == "Buy milk"

    def test_filter_by_completed(self, service_with_tasks):
        """Can filter by completion status."""
        service, tasks = service_with_tasks

        completed = service.search(tasks, completed=True)
        assert len(completed) == 1
        assert completed[0].title == "Call mom"

        pending = service.search(tasks, completed=False)
        assert len(pending) == 2

    def test_filter_combined(self, service_with_tasks):
        """Can combine multiple filters."""
        service, tasks = service_with_tasks
        results = service.search(tasks, priority="low", category="shopping")

        assert len(results) == 1
        assert results[0].title == "Buy milk"


class TestTaskSort:
    """Tests for task sorting."""

    def test_sort_by_priority(self, service_with_tasks):
        """Can sort by priority (high first)."""
        service, tasks = service_with_tasks
        sorted_tasks = service.sort_tasks(tasks, by="priority")

        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"

    def test_sort_by_priority_reverse(self, service_with_tasks):
        """Can sort by priority reversed (low first)."""
        service, tasks = service_with_tasks
        sorted_tasks = service.sort_tasks(tasks, by="priority", reverse=True)

        assert sorted_tasks[0].priority == "low"

    def test_sort_by_category(self, service_with_tasks):
        """Can sort by category alphabetically."""
        service, tasks = service_with_tasks
        sorted_tasks = service.sort_tasks(tasks, by="category")

        categories = [t.category for t in sorted_tasks]
        assert categories == sorted(categories)

    def test_sort_by_title(self, service_with_tasks):
        """Can sort by title alphabetically."""
        service, tasks = service_with_tasks
        sorted_tasks = service.sort_tasks(tasks, by="title")

        assert sorted_tasks[0].title == "Buy milk"
        assert sorted_tasks[1].title == "Call mom"
        assert sorted_tasks[2].title == "Study math"


class TestTaskStats:
    """Tests for task statistics."""

    def test_stats_empty(self, service):
        """Stats for empty list."""
        stats = service.get_stats([])

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["pending"] == 0
        assert stats["overdue"] == 0
        assert stats["completion_rate"] == 0

    def test_stats_with_tasks(self, service_with_tasks):
        """Stats calculated correctly."""
        service, tasks = service_with_tasks
        stats = service.get_stats(tasks)

        assert stats["total"] == 3
        assert stats["completed"] == 1
        assert stats["pending"] == 2
        assert stats["completion_rate"] == pytest.approx(33.33, rel=0.1)

    def test_stats_overdue(self, service):
        """Overdue count is calculated."""
        tasks = [
            Task(title="Past due", due_date=date(2020, 1, 1)),
            Task(title="Future", due_date=date(2099, 1, 1)),
            Task(title="No due"),
        ]
        stats = service.get_stats(tasks)

        assert stats["overdue"] == 1
