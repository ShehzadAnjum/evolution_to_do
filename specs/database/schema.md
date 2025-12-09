# Data Model: Phase II Web Application

**Feature**: Phase II - Full-Stack Web Application
**Date**: 2025-12-06
**Database**: Neon PostgreSQL

---

## Entity Relationship Diagram

```
┌──────────────────────────────────────┐
│               users                   │
│          (Better Auth)                │
├──────────────────────────────────────┤
│ id          UUID         PK          │
│ email       VARCHAR(255) UNIQUE      │
│ name        VARCHAR(255) NULL        │
│ image       TEXT         NULL        │
│ created_at  TIMESTAMP    DEFAULT NOW │
│ updated_at  TIMESTAMP    DEFAULT NOW │
└────────────────┬─────────────────────┘
                 │
                 │ 1:N
                 │
                 ▼
┌──────────────────────────────────────┐
│               tasks                   │
│            (SQLModel)                 │
├──────────────────────────────────────┤
│ id          UUID         PK          │
│ user_id     UUID         FK → users  │
│ title       VARCHAR(200) NOT NULL    │
│ description TEXT         DEFAULT ''  │
│ is_complete BOOLEAN      DEFAULT F   │
│ created_at  TIMESTAMP    DEFAULT NOW │
│ updated_at  TIMESTAMP    DEFAULT NOW │
└──────────────────────────────────────┘
```

---

## Table Definitions

### users (Managed by Better Auth)

```sql
-- Created automatically by: npx @better-auth/cli migrate

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Better Auth also creates: sessions, accounts, verifications
```

### tasks (SQLModel)

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_tasks_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

---

## SQLModel Definitions

### Task Models

```python
# backend/src/models/task.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    """Base task fields shared by all task schemas."""
    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=2000)
    is_complete: bool = Field(default=False)

class Task(TaskBase, table=True):
    """Database model for tasks."""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    """Schema for creating a task (request body)."""
    pass

class TaskUpdate(SQLModel):
    """Schema for updating a task (partial update)."""
    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_complete: Optional[bool] = None

class TaskRead(TaskBase):
    """Schema for reading a task (response body)."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
```

---

## TypeScript Types (Frontend)

```typescript
// frontend/src/types/index.ts

export interface Task {
  id: string;           // UUID as string
  user_id: string;      // UUID as string
  title: string;
  description: string;
  is_complete: boolean;
  created_at: string;   // ISO 8601 datetime
  updated_at: string;   // ISO 8601 datetime
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_complete?: boolean;
}

export interface User {
  id: string;
  email: string;
  name?: string;
  image?: string;
}
```

---

## Validation Rules

### Task Title
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Allowed**: Unicode, emojis, special characters

### Task Description
- **Required**: No (defaults to empty string)
- **Max Length**: 2000 characters
- **Allowed**: Unicode, emojis, special characters, newlines

### User Email
- **Required**: Yes
- **Format**: Valid email address
- **Unique**: Yes (enforced by database)

---

## Data Access Patterns

### List User's Tasks
```python
# Most common query - filtered by user_id
statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
tasks = session.exec(statement).all()
```

### Get Single Task (with ownership check)
```python
# Always verify ownership
statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
task = session.exec(statement).first()
if not task:
    raise HTTPException(status_code=404)  # or 403 if exists but wrong user
```

### Create Task
```python
task = Task(
    title=data.title,
    description=data.description,
    user_id=user_id,
)
session.add(task)
session.commit()
session.refresh(task)
```

### Update Task
```python
# Update only provided fields
for key, value in data.dict(exclude_unset=True).items():
    setattr(task, key, value)
task.updated_at = datetime.utcnow()
session.commit()
```

### Delete Task
```python
session.delete(task)
session.commit()
```

---

## Migration Strategy

### Phase 1: Better Auth Tables
```bash
# Run from frontend directory (Better Auth CLI)
npx @better-auth/cli migrate
```

### Phase 2: Tasks Table
```python
# Run once to create tables
from sqlmodel import SQLModel
from .database import engine

SQLModel.metadata.create_all(engine)
```

### Rollback Plan
```sql
-- If needed, drop in reverse order
DROP TABLE IF EXISTS tasks;
-- Better Auth tables managed by their CLI
```

---

## Data Integrity

### Constraints
- `user_id` foreign key ensures tasks belong to valid users
- `ON DELETE CASCADE` removes tasks when user is deleted
- `NOT NULL` on `title` prevents empty task titles

### Indexes
- `idx_tasks_user_id` for fast user task lookups
- `idx_tasks_created_at` for sorted task lists

---

**Model Version**: 1.0.0
**Created**: 2025-12-06
