"""JSON file storage for tasks."""

import json
from pathlib import Path
from typing import List

from .models import Task


class JsonStorage:
    """Handles reading and writing tasks to a JSON file.

    Provides simple local persistence without requiring a database.
    Tasks are stored as a JSON array in the specified file.
    """

    def __init__(self, path: str = "tasks.json"):
        """Initialize storage with file path.

        Args:
            path: Path to the JSON file (default: tasks.json in current directory)
        """
        self.path = Path(path)

    def load(self) -> List[Task]:
        """Load all tasks from the JSON file.

        Returns:
            List of Task objects. Empty list if file doesn't exist.
        """
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError) as e:
            # If file is corrupted, return empty list and log warning
            print(f"Warning: Could not parse {self.path}: {e}")
            return []

    def save(self, tasks: List[Task]) -> None:
        """Save all tasks to the JSON file.

        Args:
            tasks: List of Task objects to save
        """
        data = [t.to_dict() for t in tasks]
        self.path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def clear(self) -> None:
        """Delete all tasks by removing the file."""
        if self.path.exists():
            self.path.unlink()

    def exists(self) -> bool:
        """Check if the storage file exists."""
        return self.path.exists()

    @property
    def file_path(self) -> str:
        """Return the absolute path to the storage file."""
        return str(self.path.absolute())
