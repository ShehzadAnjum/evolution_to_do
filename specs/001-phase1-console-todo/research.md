# Research: Phase I Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-05
**Status**: Complete

## Overview

Research for Phase I focuses on Python best practices, UV package manager setup, and CLI design patterns. Since we're using only standard library components, external dependency research is minimal.

## Research Tasks & Findings

### 1. Python 3.13+ Features

**Task**: Identify Python 3.13+ features relevant for this project

**Decision**: Use Python 3.13+ with dataclasses and type hints
**Rationale**: Python 3.13 offers improved error messages, better typing support, and performance improvements. Key features we'll use:
- `@dataclass` for Task model (clean, auto-generated methods)
- Type hints for code clarity and IDE support
- f-strings for output formatting
- `__post_init__` for validation in dataclasses

**Alternatives Considered**:
- Python 3.11/3.12: Would work but user specified 3.13+
- External libraries (attrs, pydantic): Overkill for Phase I, adds dependencies
- Named tuples: Less flexible than dataclasses

**Best Practices Applied**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
```

### 2. UV Package Manager

**Task**: Best practices for UV project setup

**Decision**: Use UV for dependency management and virtual environments
**Rationale**: UV is fast, modern, and specified in the hackathon requirements.

**Key Commands**:
```bash
# Initialize project
uv init backend
cd backend

# Add dev dependencies only (no runtime deps for Phase I)
uv add --dev pytest pytest-cov

# Run the application
uv run python -m src.main

# Run tests
uv run pytest tests/ -v --cov=src
```

**Alternatives Considered**:
- pip + venv: Traditional but slower, less ergonomic
- Poetry: More complex than needed for Phase I
- Pipenv: Less modern than UV

**Project Structure**:
```toml
# pyproject.toml
[project]
name = "todo-console"
version = "0.1.0"
description = "Phase I Console Todo Application"
requires-python = ">=3.13"

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]
```

### 3. CLI Design Patterns

**Task**: Menu-driven interface best practices

**Decision**: Numbered menu with clear prompts and validation loops
**Rationale**: Most discoverable and user-friendly for a console application

**Alternatives Considered**:
- Command-line arguments (argparse): Less discoverable, harder for first-time users
- REPL-style commands: More typing required, steeper learning curve
- Interactive TUI (rich, textual): Overkill for Phase I, adds dependencies

**Design Pattern Selected**:
```
╔════════════════════════════════════╗
║       Todo Application v1.0        ║
╠════════════════════════════════════╣
║  1. Add Task                       ║
║  2. View Tasks                     ║
║  3. Mark Complete/Incomplete       ║
║  4. Update Task                    ║
║  5. Delete Task                    ║
║  6. Exit                           ║
╚════════════════════════════════════╝

Enter choice (1-6): _
```

**Best Practices**:
1. Clear menu title with version
2. Numbered options for easy selection
3. Box drawing characters for visual structure
4. Input validation with retry on error
5. Confirmation for destructive operations (delete)
6. Consistent output formatting (✓ for success, ✗ for error)
7. "Press Enter to continue" for operation feedback
8. Summary statistics when viewing tasks

### 4. In-Memory Storage Pattern

**Task**: Best approach for session-based task storage

**Decision**: Dictionary with integer keys for O(1) lookup
**Rationale**: Simple, fast, and sufficient for Phase I requirements

**Implementation Pattern**:
```python
class TaskStore:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: Optional[str] = None) -> Task:
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def get_all(self) -> List[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.id)
```

**Alternatives Considered**:
- List with linear search: Slower for lookups
- SQLite in-memory: Overkill, adds complexity
- External storage: Out of Phase I scope

### 5. Error Handling Strategy

**Task**: User-friendly error handling approach

**Decision**: Validation at boundaries with clear re-prompting
**Rationale**: Users should be able to self-correct without external help

**Pattern**:
```python
def get_valid_task_id(store: TaskStore, prompt: str) -> int:
    while True:
        try:
            task_id = int(input(prompt))
            if store.get(task_id) is None:
                print(f"✗ Error: Task with ID {task_id} not found.")
                continue
            return task_id
        except ValueError:
            print("✗ Error: Invalid input. Please enter a number.")
```

**Error Message Format**:
- Start with ✗ symbol for visibility
- Clear description of what went wrong
- Implicit guidance on how to fix (re-prompt)

## Reusability Analysis (Principle IX)

| Component | Current Use | Future Reuse | Extraction Priority |
|-----------|-------------|--------------|---------------------|
| Task dataclass | Phase I model | Phase II-V (extend) | High |
| TaskStore | In-memory CRUD | Base for DB store | High |
| Menu pattern | CLI navigation | Other CLI tools | Medium |
| Validators | Input validation | All phases | High |
| Formatters | Console output | CLI tools | Medium |

## Resolved Technical Context

All items from Technical Context are resolved:

| Item | Resolution |
|------|------------|
| Language/Version | Python 3.13+ |
| Package Manager | UV |
| Dependencies | Standard library only (+ pytest for dev) |
| Storage | In-memory Dict[int, Task] |
| Testing | pytest with coverage |
| Platform | Cross-platform console |

## Conclusion

Phase I research is complete. No NEEDS CLARIFICATION items remain. The technical approach is:

1. **Python 3.13+** with type hints and dataclasses
2. **UV** for package management
3. **Standard library** only (no external runtime dependencies)
4. **Menu-driven CLI** for discoverability
5. **pytest** for testing (development dependency only)
6. **Dictionary-based storage** for O(1) task lookups

Ready for Phase 1: Design & Contracts
