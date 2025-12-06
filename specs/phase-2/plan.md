# Implementation Plan: Phase II - Full-Stack Web Application

**Branch**: `phase-2-web-app` | **Date**: 2025-12-06 | **Spec**: `specs/phase-2/spec.md`
**Input**: Feature specification from `/specs/phase-2/spec.md`

---

## Summary

Transform the Phase I console todo application into a multi-user web application with:
- **Frontend**: Next.js 16+ (App Router) deployed on Vercel
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: Better Auth with JWT tokens

This delivers all 5 Phase I operations (Add, View, Update, Delete, Complete) in a web interface with multi-user isolation.

---

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript 5.x, Node.js 20+

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, uvicorn, python-jose, asyncpg
- Frontend: Next.js 16+, React 19, Better Auth, Tailwind CSS

**Storage**: Neon PostgreSQL (serverless, connection pooling via `@neondatabase/serverless`)

**Testing**:
- Backend: pytest, pytest-asyncio
- Frontend: Jest, React Testing Library

**Target Platform**:
- Frontend: Vercel (Edge/Serverless)
- Backend: Any Python hosting (Railway, Render, Fly.io)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- API response time < 500ms
- Time to Interactive < 3s

**Constraints**:
- No secrets in source code
- JWT token expiry: 24 hours
- Max title: 200 chars, max description: 2000 chars

**Scale/Scope**:
- Support 100+ concurrent users
- 1000+ tasks per user

---

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Phase Boundaries** | ✅ PASS | Only Phase II technologies used |
| **II. Complete One Thing** | ✅ PASS | Phase I capstone validated |
| **III. Documentation First** | ⏳ PENDING | Must read docs before implementation |
| **IV. Context Preservation** | ✅ PASS | SESSION_HANDOFF will be updated |
| **V. Repository Cleanliness** | ✅ PASS | .gitignore configured |
| **VI. Spec-Driven Development** | ✅ PASS | Implementing from spec.md |
| **VII. Value-Driven Features** | ✅ PASS | All features in spec |
| **VIII. Quality Over Speed** | ✅ PASS | Tests included in plan |

### Technology Compliance

| Technology | Status | Phase II Allowed |
|------------|--------|------------------|
| Next.js 16+ | ✅ | Yes |
| FastAPI | ✅ | Yes |
| SQLModel | ✅ | Yes |
| Neon PostgreSQL | ✅ | Yes |
| Better Auth | ✅ | Yes |
| Docker | ❌ NOT USED | No (Phase IV) |
| OpenAI/MCP | ❌ NOT USED | No (Phase III) |

---

## Project Structure

### Documentation (this feature)

```
specs/phase-2/
├── spec.md              # Feature requirements ✅
├── plan.md              # This file
├── research.md          # Phase 0 research output
├── data-model.md        # Database schema
├── quickstart.md        # Setup instructions
├── contracts/
│   └── api-endpoints.md # REST API contract
└── tasks.md             # Generated via /sp.tasks
```

### Source Code (repository root)

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # CLI entry (Phase I - keep)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py             # SQLModel Task (upgrade from dataclass)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_store.py       # Database CRUD (upgrade from in-memory)
│   │
│   ├── api/                    # NEW: FastAPI app
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI application
│   │   ├── deps.py             # Dependency injection
│   │   ├── database.py         # Neon connection
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── tasks.py        # Task CRUD endpoints
│   │       └── health.py       # Health check
│   │
│   ├── cli/                    # Keep Phase I CLI
│   │   └── ...
│   │
│   └── lib/
│       ├── __init__.py
│       └── validators.py       # Reuse from Phase I
│
├── tests/
│   ├── unit/
│   │   ├── test_task.py        # Update for SQLModel
│   │   └── test_task_store.py  # Update for async DB
│   ├── integration/
│   │   ├── test_cli.py         # Keep Phase I tests
│   │   └── test_api.py         # NEW: API integration tests
│   └── conftest.py             # Fixtures
│
├── pyproject.toml              # Update dependencies
└── CLAUDE.md

frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home (redirect)
│   │   ├── globals.css
│   │   │
│   │   ├── (auth)/             # Auth pages (no nav)
│   │   │   ├── layout.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   │
│   │   └── (dashboard)/        # Protected pages
│   │       ├── layout.tsx
│   │       └── tasks/
│   │           └── page.tsx
│   │
│   ├── components/
│   │   ├── ui/                 # Base components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── card.tsx
│   │   │
│   │   ├── tasks/              # Task components
│   │   │   ├── task-list.tsx
│   │   │   ├── task-item.tsx
│   │   │   ├── task-form.tsx
│   │   │   └── task-summary.tsx
│   │   │
│   │   └── auth/               # Auth components
│   │       ├── login-form.tsx
│   │       ├── signup-form.tsx
│   │       └── user-menu.tsx
│   │
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Better Auth client
│   │   └── utils.ts
│   │
│   └── types/
│       └── index.ts            # Shared types
│
├── public/
├── package.json
├── tsconfig.json
├── next.config.ts
├── tailwind.config.ts
└── CLAUDE.md
```

**Structure Decision**: Web application with separate frontend and backend directories. Backend extends Phase I structure; frontend is new Next.js project.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│                      (Next.js on Vercel)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Login   │  │  Signup  │  │  Tasks   │  │  Logout  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       └─────────────┴──────┬──────┴─────────────┘               │
│                            │                                     │
│                    Better Auth Client                            │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ HTTPS + JWT
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
│                    (FastAPI on Railway/Render)                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Application                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │ /api/tasks  │  │ /auth/*     │  │ /health     │       │   │
│  │  └──────┬──────┘  └──────┬──────┘  └─────────────┘       │   │
│  │         │                │                                │   │
│  │         │         Better Auth Server                      │   │
│  │         │                │                                │   │
│  │    ┌────┴────────────────┴────┐                          │   │
│  │    │      JWT Validation      │                          │   │
│  │    └────────────┬─────────────┘                          │   │
│  │                 │                                         │   │
│  │    ┌────────────┴─────────────┐                          │   │
│  │    │    TaskStore Service     │                          │   │
│  │    └────────────┬─────────────┘                          │   │
│  └─────────────────┼─────────────────────────────────────────┘   │
│                    │                                             │
└────────────────────┼─────────────────────────────────────────────┘
                     │ SQL
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE                                      │
│                 (Neon PostgreSQL)                                │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │      users       │  │      tasks       │                     │
│  │  (Better Auth)   │  │   (SQLModel)     │                     │
│  └────────┬─────────┘  └────────┬─────────┘                     │
│           │                     │                                │
│           └─────────FK──────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

### Registration
```
1. User fills signup form (email, password)
2. Frontend calls Better Auth signup endpoint
3. Better Auth creates user in Neon database
4. Better Auth returns JWT token
5. Frontend stores token, redirects to /tasks
```

### Login
```
1. User fills login form (email, password)
2. Frontend calls Better Auth signin endpoint
3. Better Auth validates credentials
4. Better Auth returns JWT token
5. Frontend stores token, redirects to /tasks
```

### API Request
```
1. Frontend reads JWT from storage
2. Frontend sends request with Authorization: Bearer <token>
3. Backend validates JWT signature
4. Backend extracts user_id from token
5. Backend filters tasks by user_id
6. Backend returns user's tasks only
```

---

## API Endpoints Contract

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/tasks` | JWT | Create task |
| GET | `/api/tasks` | JWT | List user's tasks |
| GET | `/api/tasks/{id}` | JWT | Get single task |
| PUT | `/api/tasks/{id}` | JWT | Update task |
| DELETE | `/api/tasks/{id}` | JWT | Delete task |
| PATCH | `/api/tasks/{id}/complete` | JWT | Toggle completion |
| GET | `/health` | None | Health check |
| POST | `/auth/signup` | None | Register user |
| POST | `/auth/signin` | None | Login user |
| POST | `/auth/signout` | JWT | Logout user |

---

## Database Schema

### users (managed by Better Auth)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### tasks (SQLModel)
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

---

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-32-char-secret
BETTER_AUTH_URL=https://your-backend.com
CORS_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.com
NEXT_PUBLIC_AUTH_URL=https://your-backend.com
```

---

## Deployment Strategy

### Backend (Railway/Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy from `backend/` directory
4. Get public URL for API

### Frontend (Vercel)
1. Connect GitHub repository
2. Set environment variables with backend URL
3. Deploy from `frontend/` directory
4. Get Vercel URL

### Database (Neon)
1. Create Neon project
2. Get connection string
3. Run Better Auth migrations: `npx @better-auth/cli migrate`
4. Create tasks table via SQLModel

---

## Phase I Compatibility

### What Stays
- `backend/src/models/task.py` - Upgrade to SQLModel
- `backend/src/services/task_store.py` - Add async DB methods
- `backend/src/lib/validators.py` - Reuse validation logic
- `backend/src/cli/*` - Keep CLI for local testing
- `backend/tests/unit/*` - Update for new models

### What Changes
- Task model: dataclass → SQLModel
- TaskStore: in-memory dict → Neon PostgreSQL
- Add user_id to all task operations

### What's New
- `backend/src/api/` - FastAPI application
- `frontend/` - Entire Next.js application
- JWT authentication flow
- Multi-user task isolation

---

## Complexity Tracking

No constitution violations. All technologies are Phase II approved.

---

## Documentation Requirements (30-Minute Rule)

Before implementation, create checklists in `docs/tools/`:

| Tool | Checklist | Est. Time |
|------|-----------|-----------|
| Better Auth | `better-auth-checklist.md` | 30 min |
| Neon | `neon-checklist.md` | 15 min |
| FastAPI + SQLModel | `fastapi-sqlmodel-checklist.md` | 30 min |
| Next.js 16 | `nextjs-checklist.md` | 45 min |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth learning curve | Medium | Read docs first, use CLI for migrations |
| Neon connection issues | Medium | Use connection pooling, test locally |
| JWT token handling | Medium | Use Better Auth's built-in handling |
| CORS configuration | Low | Configure in FastAPI middleware |

---

## Success Metrics

- [ ] Backend API responds to health check
- [ ] User can register and login
- [ ] JWT tokens are issued and validated
- [ ] Tasks are isolated by user
- [ ] All 5 CRUD operations work
- [ ] Frontend deployed on Vercel
- [ ] Demo video recorded

---

**Plan Version**: 1.0.0
**Created**: 2025-12-06
**Status**: Ready for /sp.tasks
