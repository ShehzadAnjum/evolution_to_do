"""Tests for Task model."""

import pytest
from datetime import date

from console_app.models import Task


class TestTaskCreation:
    """Tests for Task creation and initialization."""

    def test_create_minimal_task(self):
        """Task can be created with just a title."""
        task = Task(title="Buy milk")
        assert task.title == "Buy milk"
        assert task.notes == ""
        assert task.priority == "medium"
        assert task.category == "general"
        assert task.completed is False
        assert task.id is not None

    def test_create_full_task(self):
        """Task can be created with all fields."""
        due = date(2025, 12, 31)
        task = Task(
            title="Important meeting",
            notes="Prepare slides",
            priority="high",
            due_date=due,
            category="work",
        )
        assert task.title == "Important meeting"
        assert task.notes == "Prepare slides"
        assert task.priority == "high"
        assert task.due_date == due
        assert task.category == "work"

    def test_title_truncation(self):
        """Long titles are truncated to 200 characters."""
        long_title = "x" * 300
        task = Task(title=long_title)
        assert len(task.title) == 200

    def test_notes_truncation(self):
        """Long notes are truncated to 1000 characters."""
        long_notes = "y" * 1500
        task = Task(title="Test", notes=long_notes)
        assert len(task.notes) == 1000

    def test_invalid_priority_defaults_to_medium(self):
        """Invalid priority defaults to medium."""
        task = Task(title="Test", priority="invalid")
        assert task.priority == "medium"

    def test_invalid_category_defaults_to_general(self):
        """Invalid category defaults to general."""
        task = Task(title="Test", category="invalid")
        assert task.category == "general"

    def test_unique_ids(self):
        """Each task gets a unique ID."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        assert task1.id != task2.id


class TestTaskSerialization:
    """Tests for Task serialization (to_dict, from_dict)."""

    def test_to_dict(self):
        """Task can be converted to dictionary."""
        task = Task(
            title="Test task",
            notes="Some notes",
            priority="high",
            category="work",
        )
        d = task.to_dict()

        assert d["title"] == "Test task"
        assert d["notes"] == "Some notes"
        assert d["priority"] == "high"
        assert d["category"] == "work"
        assert d["completed"] is False
        assert d["due_date"] is None
        assert "id" in d

    def test_to_dict_with_due_date(self):
        """Due date is serialized as ISO string."""
        task = Task(title="Test", due_date=date(2025, 12, 25))
        d = task.to_dict()
        assert d["due_date"] == "2025-12-25"

    def test_from_dict(self):
        """Task can be created from dictionary."""
        d = {
            "id": "abc123",
            "title": "Test task",
            "notes": "Some notes",
            "priority": "low",
            "due_date": "2025-12-25",
            "category": "personal",
            "completed": True,
        }
        task = Task.from_dict(d)

        assert task.id == "abc123"
        assert task.title == "Test task"
        assert task.notes == "Some notes"
        assert task.priority == "low"
        assert task.due_date == date(2025, 12, 25)
        assert task.category == "personal"
        assert task.completed is True

    def test_roundtrip(self):
        """Task survives to_dict -> from_dict roundtrip."""
        original = Task(
            title="Roundtrip test",
            notes="Testing serialization",
            priority="high",
            due_date=date(2025, 6, 15),
            category="study",
        )
        d = original.to_dict()
        restored = Task.from_dict(d)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.notes == original.notes
        assert restored.priority == original.priority
        assert restored.due_date == original.due_date
        assert restored.category == original.category
        assert restored.completed == original.completed


class TestTaskProperties:
    """Tests for Task computed properties."""

    def test_is_overdue_false_when_no_due_date(self):
        """Task without due date is not overdue."""
        task = Task(title="Test")
        assert task.is_overdue is False

    def test_is_overdue_false_when_completed(self):
        """Completed task is not overdue."""
        task = Task(title="Test", due_date=date(2020, 1, 1), completed=True)
        assert task.is_overdue is False

    def test_is_overdue_true_when_past_due(self):
        """Task past due date is overdue."""
        task = Task(title="Test", due_date=date(2020, 1, 1))
        assert task.is_overdue is True

    def test_is_overdue_false_when_future(self):
        """Task with future due date is not overdue."""
        task = Task(title="Test", due_date=date(2099, 12, 31))
        assert task.is_overdue is False

    def test_short_id(self):
        """Short ID is first 8 characters."""
        task = Task(title="Test")
        assert len(task.short_id) == 8
        assert task.id.startswith(task.short_id)
