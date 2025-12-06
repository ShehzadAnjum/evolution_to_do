"""Unit tests for TaskStore CRUD operations."""

import pytest

from src.services.task_store import TaskStore


class TestTaskStoreAdd:
    """Tests for TaskStore.add() method."""

    def test_add_task_returns_task(self) -> None:
        """Adding a task should return the created task."""
        store = TaskStore()
        task = store.add("Buy groceries")
        assert task.title == "Buy groceries"
        assert task.id == 1

    def test_add_task_with_description(self) -> None:
        """Adding a task with description should include it."""
        store = TaskStore()
        task = store.add("Buy groceries", "Milk, eggs, bread")
        assert task.description == "Milk, eggs, bread"

    def test_add_multiple_tasks_sequential_ids(self) -> None:
        """Tasks should get sequential IDs starting from 1."""
        store = TaskStore()
        task1 = store.add("First")
        task2 = store.add("Second")
        task3 = store.add("Third")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_default_not_completed(self) -> None:
        """New tasks should be incomplete by default."""
        store = TaskStore()
        task = store.add("Test task")
        assert task.completed is False


class TestTaskStoreGetAll:
    """Tests for TaskStore.get_all() method."""

    def test_get_all_empty_store(self) -> None:
        """get_all() on empty store should return empty list."""
        store = TaskStore()
        tasks = store.get_all()
        assert tasks == []

    def test_get_all_returns_all_tasks(self) -> None:
        """get_all() should return all added tasks."""
        store = TaskStore()
        store.add("First")
        store.add("Second")
        store.add("Third")
        tasks = store.get_all()
        assert len(tasks) == 3

    def test_get_all_ordered_by_id(self) -> None:
        """get_all() should return tasks in ID order."""
        store = TaskStore()
        store.add("First")
        store.add("Second")
        store.add("Third")
        tasks = store.get_all()
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3


class TestTaskStoreGet:
    """Tests for TaskStore.get() method."""

    def test_get_existing_task(self) -> None:
        """get() should return task with matching ID."""
        store = TaskStore()
        store.add("Test task")
        task = store.get(1)
        assert task is not None
        assert task.title == "Test task"

    def test_get_nonexistent_task(self) -> None:
        """get() should return None for non-existent ID."""
        store = TaskStore()
        task = store.get(999)
        assert task is None


class TestTaskStoreToggleComplete:
    """Tests for TaskStore.toggle_complete() method."""

    def test_toggle_incomplete_to_complete(self) -> None:
        """Toggling incomplete task should make it complete."""
        store = TaskStore()
        store.add("Test task")
        task = store.toggle_complete(1)
        assert task is not None
        assert task.completed is True

    def test_toggle_complete_to_incomplete(self) -> None:
        """Toggling complete task should make it incomplete."""
        store = TaskStore()
        store.add("Test task")
        store.toggle_complete(1)  # Now complete
        task = store.toggle_complete(1)  # Now incomplete
        assert task is not None
        assert task.completed is False

    def test_toggle_nonexistent_task(self) -> None:
        """Toggling non-existent task should return None."""
        store = TaskStore()
        result = store.toggle_complete(999)
        assert result is None


class TestTaskStoreUpdate:
    """Tests for TaskStore.update() method."""

    def test_update_title(self) -> None:
        """Updating title should change only the title."""
        store = TaskStore()
        store.add("Original", "Description")
        task = store.update(1, title="Updated")
        assert task is not None
        assert task.title == "Updated"
        assert task.description == "Description"

    def test_update_description(self) -> None:
        """Updating description should change only the description."""
        store = TaskStore()
        store.add("Title", "Original")
        task = store.update(1, description="Updated")
        assert task is not None
        assert task.title == "Title"
        assert task.description == "Updated"

    def test_update_both(self) -> None:
        """Updating both should change both."""
        store = TaskStore()
        store.add("Title", "Description")
        task = store.update(1, title="New Title", description="New Desc")
        assert task is not None
        assert task.title == "New Title"
        assert task.description == "New Desc"

    def test_update_preserves_unchanged(self) -> None:
        """Passing None preserves original values."""
        store = TaskStore()
        store.add("Title", "Description")
        task = store.update(1)  # Both None
        assert task is not None
        assert task.title == "Title"
        assert task.description == "Description"

    def test_update_empty_title_raises_error(self) -> None:
        """Updating with empty title should raise ValueError."""
        store = TaskStore()
        store.add("Title")
        with pytest.raises(ValueError, match="title cannot be empty"):
            store.update(1, title="   ")

    def test_update_nonexistent_task(self) -> None:
        """Updating non-existent task should return None."""
        store = TaskStore()
        result = store.update(999, title="New")
        assert result is None

    def test_update_description_to_empty_clears_it(self) -> None:
        """Updating description to empty string should clear it."""
        store = TaskStore()
        store.add("Title", "Description")
        task = store.update(1, description="")
        assert task is not None
        assert task.description is None


class TestTaskStoreDelete:
    """Tests for TaskStore.delete() method."""

    def test_delete_existing_task(self) -> None:
        """Deleting existing task should return True."""
        store = TaskStore()
        store.add("Test task")
        result = store.delete(1)
        assert result is True
        assert store.get(1) is None

    def test_delete_nonexistent_task(self) -> None:
        """Deleting non-existent task should return False."""
        store = TaskStore()
        result = store.delete(999)
        assert result is False


class TestTaskStoreCounts:
    """Tests for TaskStore count methods."""

    def test_count_empty(self) -> None:
        """count() on empty store should return 0."""
        store = TaskStore()
        assert store.count() == 0

    def test_count_with_tasks(self) -> None:
        """count() should return number of tasks."""
        store = TaskStore()
        store.add("One")
        store.add("Two")
        store.add("Three")
        assert store.count() == 3

    def test_count_completed_none(self) -> None:
        """count_completed() with no completed tasks should return 0."""
        store = TaskStore()
        store.add("One")
        store.add("Two")
        assert store.count_completed() == 0

    def test_count_completed_some(self) -> None:
        """count_completed() should count only completed tasks."""
        store = TaskStore()
        store.add("One")
        store.add("Two")
        store.toggle_complete(1)
        assert store.count_completed() == 1

    def test_count_remaining(self) -> None:
        """count_remaining() should return incomplete count."""
        store = TaskStore()
        store.add("One")
        store.add("Two")
        store.add("Three")
        store.toggle_complete(1)
        assert store.count_remaining() == 2

    def test_is_empty_true(self) -> None:
        """is_empty() should return True for empty store."""
        store = TaskStore()
        assert store.is_empty() is True

    def test_is_empty_false(self) -> None:
        """is_empty() should return False with tasks."""
        store = TaskStore()
        store.add("Test")
        assert store.is_empty() is False
