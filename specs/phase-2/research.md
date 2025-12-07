# Research: Phase II Web Application

**Feature**: Phase II - Full-Stack Web Application
**Date**: 2025-12-06
**Status**: Complete

---

## Technology Research Summary

### 1. Better Auth

**Purpose**: Authentication library with JWT support

**Key Findings**:
- Works with Next.js App Router natively
- Handles user table schema automatically
- JWT tokens for API authentication
- CLI for database migrations: `npx @better-auth/cli migrate`

**Integration Pattern**:
```typescript
// Frontend: src/lib/auth.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL,
});

// Backend: src/api/deps.py
from better_auth import BetterAuth

auth = BetterAuth(
    secret=os.getenv("BETTER_AUTH_SECRET"),
    database_url=os.getenv("DATABASE_URL"),
)
```

**Critical Notes**:
- Must run migrations before first use
- JWT secret must be 32+ characters
- Token stored in httpOnly cookie by default

---

### 2. Neon PostgreSQL

**Purpose**: Serverless PostgreSQL database

**Key Findings**:
- Connection string format: `postgresql://user:pass@host/db?sslmode=require`
- Supports connection pooling via `?pooling=true`
- Compatible with SQLModel/SQLAlchemy
- Free tier: 0.5GB storage, 3GB compute

**Connection Pattern**:
```python
# Backend: src/api/database.py
from sqlmodel import create_engine, Session
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("DATABASE_URL")

# Use NullPool for serverless
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

def get_session():
    with Session(engine) as session:
        yield session
```

**Critical Notes**:
- Use `sslmode=require` for security
- NullPool recommended for serverless environments
- Connection string from Neon dashboard

---

### 3. SQLModel

**Purpose**: ORM combining SQLAlchemy + Pydantic

**Key Findings**:
- Type-safe models that work as both ORM and API schemas
- Built on SQLAlchemy 2.0
- Async support via `sqlalchemy.ext.asyncio`

**Model Pattern**:
```python
# Backend: src/models/task.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    is_complete: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
```

**Critical Notes**:
- Separate Base/Create/Read classes for API
- Use `table=True` only for database models
- Foreign keys require exact table name

---

### 4. FastAPI

**Purpose**: Python web framework for REST API

**Key Findings**:
- Automatic OpenAPI documentation
- Dependency injection for auth/database
- Pydantic integration (works with SQLModel)
- CORS middleware for frontend access

**Route Pattern**:
```python
# Backend: src/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..deps import get_current_user, get_session
from ...models.task import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.user_id == user.id)
    tasks = session.exec(statement).all()
    return tasks
```

**Critical Notes**:
- Use `Depends()` for dependency injection
- Always filter by `user_id` for multi-tenant
- Return 403 for ownership violations

---

### 5. Next.js 16 (App Router)

**Purpose**: React framework for frontend

**Key Findings**:
- App Router uses `src/app/` directory
- Server Components by default
- Client Components need "use client" directive
- Route groups with `(folder)` syntax

**Page Pattern**:
```typescript
// Frontend: src/app/(dashboard)/tasks/page.tsx
import { TaskList } from "@/components/tasks/task-list";

export default async function TasksPage() {
  // Server component - can fetch data directly
  return (
    <main className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">My Tasks</h1>
      <TaskList />
    </main>
  );
}
```

**Critical Notes**:
- Use route groups for shared layouts
- Protect routes in layout.tsx, not page.tsx
- Environment variables: `NEXT_PUBLIC_*` for client

---

## Integration Architecture

### Authentication Flow
```
1. Frontend → Better Auth → Neon (users table)
2. Better Auth → JWT token → Frontend storage
3. Frontend → API request + JWT → Backend
4. Backend → Validate JWT → Extract user_id
5. Backend → Query tasks WHERE user_id → Response
```

### Data Flow
```
Frontend                    Backend                     Database
   │                           │                            │
   │──POST /api/tasks──────────▶│                            │
   │                           │──INSERT task───────────────▶│
   │                           │◀──task row─────────────────│
   │◀──TaskRead JSON───────────│                            │
   │                           │                            │
```

---

## Deployment Research

### Backend Options

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| Railway | $5 credit/mo | Easy Python deploy |
| Render | 750 hrs/mo | Good for FastAPI |
| Fly.io | 3 VMs free | Low latency |

**Recommendation**: Railway or Render for simplicity

### Frontend (Vercel)

- Automatic deployment from GitHub
- Free for hobby projects
- Built-in Next.js optimization
- Environment variables in dashboard

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Better Auth complexity | Use official Next.js example |
| JWT token expiry | Set 24h expiry, refresh on activity |
| CORS errors | Configure allowed origins explicitly |
| Database connection limits | Use connection pooling |

---

## Documentation Links

- Better Auth: https://www.better-auth.com/docs
- Neon: https://neon.tech/docs
- SQLModel: https://sqlmodel.tiangolo.com/
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs

---

**Research Status**: Complete
**Next Step**: Create data-model.md
