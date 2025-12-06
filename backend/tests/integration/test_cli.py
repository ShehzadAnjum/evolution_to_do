"""Integration tests for CLI workflow.

Tests the full workflow through the handlers layer.
"""

import pytest

from src.cli.handlers import add_task, delete_task, mark_complete, update_task, view_tasks
from src.services.task_store import TaskStore


class TestFullWorkflow:
    """Integration tests for complete user workflows."""

    def test_add_view_workflow(self, monkeypatch, capsys) -> None:
        """Test adding a task and viewing it."""
        store = TaskStore()

        # Mock input for add_task
        inputs = iter(["Buy groceries", "Milk, eggs, bread", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        add_task(store)
        captured = capsys.readouterr()

        assert "Task added successfully" in captured.out
        assert store.count() == 1

        # Mock input for view_tasks
        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        view_tasks(store)
        captured = capsys.readouterr()

        assert "Buy groceries" in captured.out
        assert "Milk, eggs, bread" in captured.out

    def test_add_mark_complete_workflow(self, monkeypatch, capsys) -> None:
        """Test adding a task and marking it complete."""
        store = TaskStore()

        # Add a task
        inputs = iter(["Test task", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)

        # Mark it complete
        inputs = iter(["1", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mark_complete(store)

        captured = capsys.readouterr()
        assert "marked as complete" in captured.out

        task = store.get(1)
        assert task is not None
        assert task.completed is True

    def test_add_update_workflow(self, monkeypatch, capsys) -> None:
        """Test adding a task and updating it."""
        store = TaskStore()

        # Add a task
        inputs = iter(["Original title", "Original desc", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)

        # Update it
        inputs = iter(["1", "Updated title", "Updated desc", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        update_task(store)

        captured = capsys.readouterr()
        assert "updated successfully" in captured.out

        task = store.get(1)
        assert task is not None
        assert task.title == "Updated title"
        assert task.description == "Updated desc"

    def test_add_delete_workflow(self, monkeypatch, capsys) -> None:
        """Test adding a task and deleting it."""
        store = TaskStore()

        # Add a task
        inputs = iter(["Task to delete", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)

        assert store.count() == 1

        # Delete it with confirmation
        inputs = iter(["1", "y", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        delete_task(store)

        captured = capsys.readouterr()
        assert "deleted successfully" in captured.out
        assert store.count() == 0

    def test_delete_cancelled(self, monkeypatch, capsys) -> None:
        """Test cancelling a delete operation."""
        store = TaskStore()

        # Add a task
        inputs = iter(["Task to keep", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)

        # Try to delete but cancel
        inputs = iter(["1", "n", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        delete_task(store)

        captured = capsys.readouterr()
        assert "cancelled" in captured.out
        assert store.count() == 1  # Task still exists

    def test_full_crud_workflow(self, monkeypatch, capsys) -> None:
        """Test complete CRUD cycle: Create, Read, Update, Delete."""
        store = TaskStore()

        # Create
        inputs = iter(["Task 1", "Description 1", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)
        assert store.count() == 1

        # Create another
        inputs = iter(["Task 2", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)
        assert store.count() == 2

        # Read
        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        view_tasks(store)
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Total: 2" in captured.out

        # Update first task
        inputs = iter(["1", "Updated Task 1", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        update_task(store)
        assert store.get(1).title == "Updated Task 1"

        # Mark second task complete
        inputs = iter(["2", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mark_complete(store)
        assert store.get(2).completed is True

        # View again to see status
        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        view_tasks(store)
        captured = capsys.readouterr()
        assert "Completed: 1" in captured.out
        assert "Remaining: 1" in captured.out

        # Delete first task
        inputs = iter(["1", "y", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        delete_task(store)
        assert store.count() == 1
        assert store.get(1) is None
        assert store.get(2) is not None


class TestEmptyStateHandling:
    """Tests for empty store edge cases."""

    def test_view_empty_tasks(self, monkeypatch, capsys) -> None:
        """Viewing empty task list shows helpful message."""
        store = TaskStore()

        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        view_tasks(store)

        captured = capsys.readouterr()
        assert "No tasks yet" in captured.out


class TestErrorHandling:
    """Tests for error handling in handlers."""

    def test_mark_complete_invalid_id(self, monkeypatch, capsys) -> None:
        """Marking non-existent task shows error and reprompts."""
        store = TaskStore()
        store.add("Test task")

        # First try invalid, then valid
        inputs = iter(["999", "1", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        mark_complete(store)

        captured = capsys.readouterr()
        assert "not found" in captured.out
        assert "marked as complete" in captured.out

    def test_update_invalid_id(self, monkeypatch, capsys) -> None:
        """Updating non-existent task shows error and reprompts."""
        store = TaskStore()
        store.add("Test task")

        # First try invalid, then valid
        inputs = iter(["999", "1", "", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        update_task(store)

        captured = capsys.readouterr()
        assert "not found" in captured.out
        assert "updated successfully" in captured.out

    def test_delete_invalid_id(self, monkeypatch, capsys) -> None:
        """Deleting non-existent task shows error and reprompts."""
        store = TaskStore()
        store.add("Test task")

        # First try invalid, then valid with confirmation
        inputs = iter(["999", "1", "y", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        delete_task(store)

        captured = capsys.readouterr()
        assert "not found" in captured.out
        assert "deleted successfully" in captured.out

    def test_add_empty_title_reprompts(self, monkeypatch, capsys) -> None:
        """Adding task with empty title reprompts."""
        store = TaskStore()

        # First empty, then valid
        inputs = iter(["", "Valid title", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        add_task(store)

        captured = capsys.readouterr()
        assert "cannot be empty" in captured.out
        assert "added successfully" in captured.out
        assert store.count() == 1
