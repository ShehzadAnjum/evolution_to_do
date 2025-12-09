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
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # From JWT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]
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
    
    db_task.updated_at = datetime.utcnow()
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

## Migration Pattern

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

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: II, III, IV, V
**Last Updated**: 2025-12-10
