# Skill: Neon PostgreSQL + SQLModel

## Overview

This skill captures patterns for using Neon serverless PostgreSQL with SQLModel ORM in FastAPI.

## Core Concepts

### Neon Connection

**Connection String Format**:
```
postgresql://user:password@ep-xxx-yyy-zzz.region.aws.neon.tech/dbname?sslmode=require
```

**Environment Variable**:
```bash
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/evolution_todo?sslmode=require
```

### SQLModel Setup

**Database Configuration** (`backend/src/db/database.py`):
```python
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

# Use NullPool for serverless - no connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Critical for serverless
    echo=False,
)

def get_session():
    with Session(engine) as session:
        yield session
```

### Model Definition

**Task Model** (`backend/src/models/task.py`):
```python
from sqlmodel import SQLModel, Field
from datetime import datetime, date, UTC
from uuid import UUID, uuid4
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    is_complete: bool = Field(default=False)
    # v2.0.0: Optional fields with defaults
    priority: str = Field(default="medium")  # high, medium, low
    category: str = Field(default="general", max_length=50)
    due_date: Optional[date] = Field(default=None)

class TaskDB(TaskBase, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # From JWT
    # Use lambda for datetime.now(UTC) - see PHR-003
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    priority: str = Field(default="medium")
    category: str = Field(default="general", max_length=50)
    due_date: Optional[date] = Field(default=None)

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[date] = None

class TaskRead(TaskBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
```

## CRUD Patterns

### Create

```python
def create_task(session: Session, task: TaskCreate, user_id: str) -> Task:
    db_task = Task(
        **task.model_dump(),
        user_id=user_id,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Read (with User Isolation)

```python
def get_tasks(session: Session, user_id: str) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

def get_task(session: Session, task_id: UUID, user_id: str) -> Task | None:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: User isolation
    )
    return session.exec(statement).first()
```

### Update

```python
def update_task(
    session: Session, 
    task_id: UUID, 
    user_id: str, 
    task_update: TaskUpdate
) -> Task | None:
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.now(UTC)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Delete

```python
def delete_task(session: Session, task_id: UUID, user_id: str) -> bool:
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return False
    
    session.delete(db_task)
    session.commit()
    return True
```

## Neon-Specific Patterns

### Connection Pooling

```python
# ❌ DON'T: Use connection pooling with Neon serverless
engine = create_engine(DATABASE_URL, pool_size=5)

# ✅ DO: Use NullPool for serverless
engine = create_engine(DATABASE_URL, poolclass=NullPool)
```

### SSL Requirement

```python
# ❌ DON'T: Skip SSL
DATABASE_URL = "postgresql://user:pass@host/db"

# ✅ DO: Always use sslmode=require
DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"
```

### Cold Start Optimization

```python
# Consider connection warmup for frequently used routes
@app.on_event("startup")
async def warmup_db():
    with Session(engine) as session:
        session.exec(text("SELECT 1"))
```

## Migration Patterns

### Auto-Create Tables (Development)

```python
# backend/src/db/init_db.py
from sqlmodel import SQLModel
from .database import engine

def init_db():
    SQLModel.metadata.create_all(engine)

# Call in main.py startup
@app.on_event("startup")
def on_startup():
    init_db()
```

### Manual Migration Script (Production - Adding Columns)

When adding new columns to existing tables with data, use idempotent migration scripts:

```python
# backend/scripts/migrate_v2.py
"""Add new columns to existing table (idempotent - safe to run multiple times)."""

from sqlalchemy import text
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

def run_migration():
    engine = create_engine(os.getenv("DATABASE_URL"))

    with Session(engine) as session:
        # Check existing columns first
        result = session.exec(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'tasks'
        """))
        existing_columns = [row[0] for row in result]

        # Add columns only if they don't exist
        if "priority" not in existing_columns:
            session.exec(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'
            """))
            session.commit()

        # Create indexes (IF NOT EXISTS is safe)
        session.exec(text("""
            CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)
        """))
        session.commit()

if __name__ == "__main__":
    run_migration()
```

### Migration Best Practices

1. **Always use defaults** for new columns so existing rows remain valid
2. **Use `IF NOT EXISTS`** for idempotent migrations
3. **Check column existence** before ALTER TABLE
4. **Create indexes** for columns used in filtering
5. **Run migrations** before deploying new code that uses new columns

## Anti-Patterns

### ❌ Missing User Isolation

```python
# DANGEROUS: No user_id filter
def get_all_tasks(session: Session):
    return session.exec(select(Task)).all()
```

### ✅ Always Filter by User

```python
# SAFE: Always include user_id
def get_user_tasks(session: Session, user_id: str):
    return session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout | Check sslmode=require |
| Pool exhaustion | Use NullPool for serverless |
| Cold start latency | Add connection warmup |
| Migration fails | Check DATABASE_URL format |

## Datetime Best Practices (Python 3.12+)

```python
# ❌ DON'T: Use deprecated utcnow()
created_at: datetime = Field(default_factory=datetime.utcnow)

# ✅ DO: Use timezone-aware datetime with UTC
from datetime import datetime, UTC
created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

# ❌ DON'T: Use utcnow() in updates
task.updated_at = datetime.utcnow()

# ✅ DO: Use datetime.now(UTC)
task.updated_at = datetime.now(UTC)
```

See PHR-003 for detailed rationale.

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: II, III, IV, V
**Last Updated**: 2025-12-12
