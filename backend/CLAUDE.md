# Backend Context: Evolution of Todo

**Stack**: Python 3.13+ | FastAPI | SQLModel | UV
**Last Updated**: 2025-12-06

---

## Quick Reference

```bash
# Development
cd backend
uv sync                      # Install dependencies
uv run python main.py        # Run CLI (Phase I)
uv run uvicorn src.api.main:app --reload  # Run API (Phase II+)

# Testing
uv run pytest                # Run all tests
uv run pytest -v             # Verbose output
uv run pytest --cov=src      # With coverage
uv run pytest tests/unit/    # Unit tests only
uv run pytest tests/integration/  # Integration tests only
```

---

## Directory Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point (Phase I)
│   │
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass/SQLModel
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── task_store.py    # CRUD operations
│   │
│   ├── cli/                 # CLI interface (Phase I)
│   │   ├── __init__.py
│   │   ├── menu.py          # Menu display
│   │   ├── handlers.py      # Operation handlers
│   │   └── formatters.py    # Output formatting
│   │
│   ├── lib/                 # Shared utilities
│   │   ├── __init__.py
│   │   └── validators.py    # Input validation
│   │
│   ├── api/                 # REST API (Phase II+)
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── routes/          # API endpoints
│   │   └── deps.py          # Dependencies
│   │
│   └── mcp_server/          # MCP tools (Phase III+)
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── unit/                # Unit tests
│   │   ├── test_task.py
│   │   └── test_task_store.py
│   └── integration/         # Integration tests
│       └── test_cli.py
│
├── pyproject.toml           # UV project config
├── main.py                  # Shortcut entry point
└── CLAUDE.md                # This file
```

---

## Code Patterns

### 1. Task Model (Phase I - Dataclass)

```python
# src/models/task.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

### 2. Task Model (Phase II - SQLModel)

```python
# src/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 3. Service Pattern

```python
# src/services/task_store.py
class TaskStore:
    """CRUD operations for tasks."""

    def add(self, title: str, description: str = "") -> Task:
        """Create a new task."""
        pass

    def get(self, task_id: int) -> Task | None:
        """Get task by ID."""
        pass

    def get_all(self) -> list[Task]:
        """Get all tasks."""
        pass

    def update(self, task_id: int, title: str | None = None,
               description: str | None = None) -> Task | None:
        """Update task fields."""
        pass

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        pass

    def toggle_complete(self, task_id: int) -> Task | None:
        """Toggle completion status."""
        pass
```

### 4. Input Validation

```python
# src/lib/validators.py
TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 1000

def validate_title(title: str) -> tuple[bool, str]:
    """Validate task title."""
    if not title or not title.strip():
        return False, "Title cannot be empty"
    if len(title) > TITLE_MAX_LENGTH:
        return False, f"Title exceeds {TITLE_MAX_LENGTH} characters"
    return True, ""
```

### 5. FastAPI Endpoint (Phase II)

```python
# src/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from ..deps import get_current_user, get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", status_code=201)
async def create_task(
    task: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the authenticated user."""
    pass

@router.get("/")
async def list_tasks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tasks for the authenticated user."""
    pass
```

---

## Testing Patterns

### Unit Test Structure

```python
# tests/unit/test_task.py
import pytest
from src.models.task import Task

class TestTaskCreation:
    def test_task_with_title_only(self):
        task = Task(id=1, title="Test")
        assert task.title == "Test"
        assert task.description == ""
        assert task.is_complete is False

    def test_task_with_description(self):
        task = Task(id=1, title="Test", description="Details")
        assert task.description == "Details"
```

### Integration Test Structure

```python
# tests/integration/test_cli.py
import pytest
from io import StringIO
from unittest.mock import patch

class TestCLIWorkflow:
    @pytest.fixture
    def store(self):
        from src.services.task_store import TaskStore
        return TaskStore()

    def test_add_and_view_workflow(self, store):
        # Add task
        task = store.add("Test Task", "Description")
        assert task.id == 1

        # View tasks
        tasks = store.get_all()
        assert len(tasks) == 1
```

---

## Environment Variables (Phase II+)

```bash
# .env (never commit)
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key
OPENAI_API_KEY=sk-...  # Phase III
```

---

## Dependencies

### Phase I (Minimal)
```toml
[project]
dependencies = []

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]
```

### Phase II (Web)
```toml
[project]
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlmodel>=0.0.14",
    "asyncpg>=0.29.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]
```

---

## Current State

### Phase I (Complete)
- ✅ Task dataclass with validation
- ✅ In-memory TaskStore with CRUD
- ✅ CLI menu and handlers
- ✅ 52 tests passing (74% coverage)

### Phase II (In Progress)
- ⏳ Convert Task to SQLModel
- ⏳ Add FastAPI routes
- ⏳ Neon PostgreSQL connection
- ⏳ Better Auth integration (JWT)

---

## Reusable Components

| Component | Location | Reuse Potential |
|-----------|----------|-----------------|
| Input validators | `src/lib/validators.py` | High - universal |
| Output formatters | `src/cli/formatters.py` | Medium - CLI only |
| Task model | `src/models/task.py` | High - extend for Phase II |
| TaskStore interface | `src/services/task_store.py` | High - swap storage |

---

**Parent Context**: See `/CLAUDE.md` for project-wide instructions.
