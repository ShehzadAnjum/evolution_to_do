---
name: neon-sqlmodel
description: SQLModel with Neon PostgreSQL patterns. Use when working with database models, migrations, or Neon serverless PostgreSQL connections in FastAPI applications.
---

# Neon SQLModel

## Connection Setup

```python
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql://user:pass@host/db?sslmode=require
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
```

## Model Definition

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="")
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## CRUD Operations

```python
# Create
task = Task(user_id=user_id, title="New task")
session.add(task)
session.commit()
session.refresh(task)

# Read
tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()

# Update
task.title = "Updated"
session.add(task)
session.commit()

# Delete
session.delete(task)
session.commit()
```

## Manual Migrations (Without Alembic)

```python
def run_migrations():
    migrations = [
        ("tasks", "due_date", "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date DATE"),
        ("tasks", "priority", "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'"),
    ]
    with Session(engine) as session:
        for table, column, sql in migrations:
            session.exec(text(sql))
            session.commit()
```

## Neon-Specific Notes

- Always use `?sslmode=require` in connection string
- Connection pooling handled by Neon
- Serverless may have cold start on first query
