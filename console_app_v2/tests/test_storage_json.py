"""Tests for JSON storage."""

import pytest
from pathlib import Path
from datetime import date

from console_app_v2.models import Task
from console_app_v2.storage_json import JsonStorage


class TestJsonStorage:
    """Tests for JsonStorage."""

    def test_save_and_load(self, tmp_path: Path):
        """Can save and load tasks."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        tasks = [
            Task(title="Task 1"),
            Task(title="Task 2", priority="high"),
        ]
        storage.save(tasks)

        loaded = storage.load()
        assert len(loaded) == 2
        assert loaded[0].title == "Task 1"
        assert loaded[1].title == "Task 2"
        assert loaded[1].priority == "high"

    def test_load_empty_file(self, tmp_path: Path):
        """Returns empty list when file doesn't exist."""
        file_path = tmp_path / "nonexistent.json"
        storage = JsonStorage(str(file_path))

        loaded = storage.load()
        assert loaded == []

    def test_roundtrip_with_all_fields(self, tmp_path: Path):
        """All task fields survive save/load roundtrip."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        original = Task(
            title="Complete task",
            notes="With all fields",
            priority="high",
            due_date=date(2025, 12, 25),
            category="work",
            completed=True,
        )
        storage.save([original])

        loaded = storage.load()
        task = loaded[0]

        assert task.id == original.id
        assert task.title == original.title
        assert task.notes == original.notes
        assert task.priority == original.priority
        assert task.due_date == original.due_date
        assert task.category == original.category
        assert task.completed == original.completed

    def test_unicode_support(self, tmp_path: Path):
        """Unicode characters are preserved."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        task = Task(title="Buy 牛奶 🥛", notes="Emoji test 😊")
        storage.save([task])

        loaded = storage.load()
        assert loaded[0].title == "Buy 牛奶 🥛"
        assert loaded[0].notes == "Emoji test 😊"

    def test_clear(self, tmp_path: Path):
        """Can clear all tasks."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        storage.save([Task(title="Test")])
        assert storage.exists()

        storage.clear()
        assert not storage.exists()

    def test_exists(self, tmp_path: Path):
        """Can check if storage file exists."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        assert not storage.exists()

        storage.save([])
        assert storage.exists()

    def test_file_path_property(self, tmp_path: Path):
        """Can get absolute file path."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        assert storage.file_path == str(file_path.absolute())

    def test_corrupted_file_returns_empty(self, tmp_path: Path):
        """Returns empty list if JSON is corrupted."""
        file_path = tmp_path / "tasks.json"
        file_path.write_text("{ invalid json }", encoding="utf-8")

        storage = JsonStorage(str(file_path))
        loaded = storage.load()

        assert loaded == []

    def test_multiple_save_overwrites(self, tmp_path: Path):
        """Subsequent saves overwrite previous data."""
        file_path = tmp_path / "tasks.json"
        storage = JsonStorage(str(file_path))

        storage.save([Task(title="First")])
        storage.save([Task(title="Second"), Task(title="Third")])

        loaded = storage.load()
        assert len(loaded) == 2
        assert loaded[0].title == "Second"
