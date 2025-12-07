# Data Model: Phase I Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-04
**Status**: Complete

## Overview

Phase I uses in-memory storage with a simple entity model. No database, no persistence between sessions.

## Entities

### Task

The core entity representing a todo item.

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    """Represents a todo item that a user wants to track."""

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = self.title.strip()
        if self.description:
            self.description = self.description.strip()
```

**Fields**:

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | int | Yes | Unique identifier | Auto-assigned, sequential starting from 1, never reused |
| title | str | Yes | Task title | Non-empty after stripping whitespace |
| description | str \| None | No | Task description | Optional, can be empty string or None |
| completed | bool | Yes | Completion status | Default: False |

**Validation Rules** (from FR-002, FR-003):
- `id`: System-assigned, positive integer, unique within session
- `title`: Required, must have at least 1 non-whitespace character
- `description`: Optional, None or string
- `completed`: Boolean, default False

### TaskStore

In-memory storage for tasks. NOT an entity per se, but the storage abstraction.

```python
from typing import Dict, List, Optional

class TaskStore:
    """In-memory storage for tasks with CRUD operations."""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Create and store a new task. Returns the created task."""
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID. Returns None if not found."""
        return self._tasks.get(task_id)

    def get_all(self) -> List[Task]:
        """Get all tasks, ordered by ID."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(self, task_id: int, title: Optional[str] = None,
               description: Optional[str] = None) -> Optional[Task]:
        """Update task fields. Returns updated task or None if not found."""
        task = self._tasks.get(task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status. Returns task or None if not found."""
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

    def is_empty(self) -> bool:
        """Check if store has no tasks."""
        return len(self._tasks) == 0
```

## State Transitions

### Task Completion State

```
[Incomplete] <--toggle--> [Complete]
```

- New tasks start as `completed=False`
- `toggle_complete()` flips the state
- Per FR-005: "System MUST allow marking tasks as complete or incomplete"
- Per US2 Scenario 4: "mark a complete task again" → "toggles back to incomplete"

### Task Lifecycle

```
[Created] --> [Active] --> [Deleted]
                 |
                 +--> [Completed] --> [Deleted]
```

- Created: Task added to store
- Active: Task exists, not completed
- Completed: Task exists, completed=True
- Deleted: Task removed from store (permanent)

## Relationships

No relationships in Phase I - single entity model.

```
┌─────────────────────┐
│     TaskStore       │
│  (In-Memory Dict)   │
├─────────────────────┤
│  _tasks: Dict[int,  │──────────────┐
│           Task]     │              │
│  _next_id: int      │              │
└─────────────────────┘              │
                                     │
         ┌───────────────────────────┘
         │ contains 0..* instances
         ▼
┌─────────────────────┐
│        Task         │
├─────────────────────┤
│  id: int            │
│  title: str         │
│  description: str?  │
│  completed: bool    │
└─────────────────────┘
```

## Storage Characteristics

| Characteristic | Value | Requirement |
|---------------|-------|-------------|
| Persistence | Session only | FR-010 |
| Access Pattern | By ID (O(1)) | Performance |
| Ordering | By ID (insertion order) | Display consistency |
| Capacity | Unlimited (memory bound) | SC-005: 100+ tasks |
| Concurrency | None (single user) | Assumption #1 |

## Mapping to Requirements

| Requirement | Data Model Support |
|-------------|-------------------|
| FR-002 | Task.title (required), Task.description (optional) |
| FR-003 | TaskStore._next_id generates sequential IDs |
| FR-004 | Task fields: id, title, description, completed |
| FR-005 | TaskStore.toggle_complete() |
| FR-006 | TaskStore.update() with optional title/description |
| FR-007 | TaskStore.delete() |
| FR-008 | TaskStore.get() returns None for invalid IDs |
| FR-010 | In-memory Dict, no persistence |
| FR-013 | TaskStore.count(), count_completed() |
