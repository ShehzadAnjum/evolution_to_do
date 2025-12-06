"""Unit tests for Task dataclass validation."""

import pytest

from src.models.task import MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH, Task


class TestTaskCreation:
    """Tests for Task creation and validation."""

    def test_create_task_with_title_only(self) -> None:
        """Task can be created with just a title."""
        task = Task(id=1, title="Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.completed is False

    def test_create_task_with_title_and_description(self) -> None:
        """Task can be created with title and description."""
        task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread")
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_create_completed_task(self) -> None:
        """Task can be created with completed status."""
        task = Task(id=1, title="Done task", completed=True)
        assert task.completed is True

    def test_empty_title_raises_error(self) -> None:
        """Empty title should raise ValueError."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Task(id=1, title="")

    def test_whitespace_only_title_raises_error(self) -> None:
        """Whitespace-only title should raise ValueError."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            Task(id=1, title="   ")

    def test_title_is_stripped(self) -> None:
        """Title should be stripped of leading/trailing whitespace."""
        task = Task(id=1, title="  Buy groceries  ")
        assert task.title == "Buy groceries"

    def test_description_is_stripped(self) -> None:
        """Description should be stripped of leading/trailing whitespace."""
        task = Task(id=1, title="Test", description="  Some description  ")
        assert task.description == "Some description"

    def test_unicode_title_supported(self) -> None:
        """Unicode characters in title should be supported."""
        task = Task(id=1, title="Buy groceries 🛒")
        assert task.title == "Buy groceries 🛒"

    def test_unicode_description_supported(self) -> None:
        """Unicode characters in description should be supported."""
        task = Task(id=1, title="Test", description="Description with emojis 🎉✨")
        assert task.description == "Description with emojis 🎉✨"

    def test_long_title_truncated(self) -> None:
        """Title exceeding max length should be truncated."""
        long_title = "A" * (MAX_TITLE_LENGTH + 50)
        task = Task(id=1, title=long_title)
        assert len(task.title) == MAX_TITLE_LENGTH

    def test_long_description_truncated(self) -> None:
        """Description exceeding max length should be truncated."""
        long_desc = "B" * (MAX_DESCRIPTION_LENGTH + 50)
        task = Task(id=1, title="Test", description=long_desc)
        assert len(task.description) == MAX_DESCRIPTION_LENGTH


class TestTaskDefaults:
    """Tests for Task default values."""

    def test_default_description_is_none(self) -> None:
        """Default description should be None."""
        task = Task(id=1, title="Test")
        assert task.description is None

    def test_default_completed_is_false(self) -> None:
        """Default completed status should be False."""
        task = Task(id=1, title="Test")
        assert task.completed is False
