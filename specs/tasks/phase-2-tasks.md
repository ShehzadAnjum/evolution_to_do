# Tasks: Phase II - Full-Stack Web Application

**Input**: Design documents from `/specs/phase-2/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/api-endpoints.md ✅

**Tests**: Included (pytest for backend, Jest for frontend)

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- Backend paths relative to `backend/`
- Frontend paths relative to `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, database connection, basic structure

- [ ] T001 Create Neon PostgreSQL project and get connection string
- [ ] T002 [P] Update backend/pyproject.toml with Phase II dependencies (fastapi, sqlmodel, uvicorn, asyncpg, python-jose)
- [ ] T003 [P] Initialize frontend Next.js 16 project in frontend/ directory
- [ ] T004 [P] Create backend/.env.example with required environment variables
- [ ] T005 [P] Create frontend/.env.example with required environment variables
- [ ] T006 Create backend/src/api/ directory structure per plan.md
- [ ] T007 Create backend/src/api/database.py with Neon connection (NullPool)
- [ ] T008 Run `uv sync` and verify backend dependencies install

**Checkpoint**: Database connection works, both projects initialized

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core components that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundational

- [ ] T009 Upgrade backend/src/models/task.py from dataclass to SQLModel (per data-model.md)
- [ ] T010 Create TaskBase, Task, TaskCreate, TaskUpdate, TaskRead schemas in backend/src/models/task.py
- [ ] T011 Create backend/src/api/main.py FastAPI application with CORS middleware
- [ ] T012 Create backend/src/api/deps.py with get_session dependency
- [ ] T013 Create backend/src/api/routes/health.py with GET /health endpoint
- [ ] T014 Wire health route to main app, verify http://localhost:8000/health works

### Frontend Foundational

- [ ] T015 [P] Configure frontend/tailwind.config.ts
- [ ] T016 [P] Create frontend/src/app/layout.tsx root layout
- [ ] T017 [P] Create frontend/src/app/globals.css with Tailwind imports
- [ ] T018 [P] Create frontend/src/types/index.ts with Task, User types (per data-model.md)
- [ ] T019 [P] Create frontend/src/lib/utils.ts with helper functions
- [ ] T020 Create frontend/src/lib/api.ts with base API client (fetch wrapper)

**Checkpoint**: Backend serves /health, frontend renders root layout

---

## Phase 3: User Story 1 & 2 - Authentication (Priority: P1)

**Goal**: Users can register, login, and logout

**Independent Test**: Register new user, login, see dashboard, logout

### Backend Auth (US1 + US2)

- [ ] T021 [US1] Install and configure Better Auth in backend
- [ ] T022 [US1] Create backend/src/api/routes/auth.py with Better Auth endpoints
- [ ] T023 [US1] Run Better Auth migration: create users table in Neon
- [ ] T024 [US1] Create backend/src/api/deps.py get_current_user dependency (JWT validation)
- [ ] T025 [P] [US1] Unit test for JWT validation in backend/tests/unit/test_auth.py

### Frontend Auth (US1 + US2)

- [ ] T026 [P] [US1] Create frontend/src/lib/auth.ts Better Auth client
- [ ] T027 [US1] Create frontend/src/components/auth/signup-form.tsx
- [ ] T028 [US1] Create frontend/src/app/(auth)/layout.tsx (no nav layout)
- [ ] T029 [US1] Create frontend/src/app/(auth)/signup/page.tsx
- [ ] T030 [US2] Create frontend/src/components/auth/login-form.tsx
- [ ] T031 [US2] Create frontend/src/app/(auth)/login/page.tsx
- [ ] T032 [US2] Create frontend/src/components/auth/user-menu.tsx (logout button)
- [ ] T033 [US2] Create frontend/src/app/(dashboard)/layout.tsx (protected, with nav)

### Integration Tests (US1 + US2)

- [ ] T034 [P] [US1] Integration test: register new user in backend/tests/integration/test_auth.py
- [ ] T035 [P] [US2] Integration test: login/logout flow

**Checkpoint**: User can signup, login, see protected dashboard, logout

---

## Phase 4: User Story 3 - View Task List (Priority: P2)

**Goal**: Logged-in user sees their tasks in web UI

**Independent Test**: Login, view empty state, add tasks via API, refresh to see list

### Backend (US3)

- [ ] T036 [US3] Create backend/src/api/routes/tasks.py with router
- [ ] T037 [US3] Implement GET /api/tasks endpoint (list user's tasks)
- [ ] T038 [P] [US3] Unit test for task listing in backend/tests/unit/test_tasks_api.py

### Frontend (US3)

- [ ] T039 [US3] Create frontend/src/components/tasks/task-item.tsx
- [ ] T040 [US3] Create frontend/src/components/tasks/task-list.tsx
- [ ] T041 [US3] Create frontend/src/components/tasks/task-summary.tsx (total/completed)
- [ ] T042 [US3] Create frontend/src/app/(dashboard)/tasks/page.tsx
- [ ] T043 [US3] Implement empty state ("No tasks yet") in task-list.tsx

**Checkpoint**: User can view their task list (empty or populated)

---

## Phase 5: User Story 4 - Add New Task (Priority: P2)

**Goal**: Logged-in user can create tasks

**Independent Test**: Login, add task, see it appear in list, refresh to verify persistence

### Backend (US4)

- [ ] T044 [US4] Implement POST /api/tasks endpoint (create task)
- [ ] T045 [US4] Add validation for title (required, max 200 chars)
- [ ] T046 [P] [US4] Unit test for task creation in backend/tests/unit/test_tasks_api.py

### Frontend (US4)

- [ ] T047 [US4] Create frontend/src/components/tasks/task-form.tsx
- [ ] T048 [US4] Wire task-form to POST /api/tasks
- [ ] T049 [US4] Show success feedback on task creation
- [ ] T050 [US4] Handle validation errors (empty title, too long)

**Checkpoint**: User can add tasks, they persist across refresh

---

## Phase 6: User Story 5 - Update Task (Priority: P2)

**Goal**: Logged-in user can edit their tasks

**Independent Test**: Create task, edit title/description, verify changes persist

### Backend (US5)

- [ ] T051 [US5] Implement GET /api/tasks/{id} endpoint
- [ ] T052 [US5] Implement PUT /api/tasks/{id} endpoint
- [ ] T053 [US5] Add ownership check (403 if not owner)
- [ ] T054 [P] [US5] Unit test for task update in backend/tests/unit/test_tasks_api.py

### Frontend (US5)

- [ ] T055 [US5] Add edit button to task-item.tsx
- [ ] T056 [US5] Create edit dialog/modal for task editing
- [ ] T057 [US5] Wire edit form to PUT /api/tasks/{id}
- [ ] T058 [US5] Show success feedback on update

**Checkpoint**: User can edit tasks, changes persist

---

## Phase 7: User Story 6 - Delete Task (Priority: P2)

**Goal**: Logged-in user can delete their tasks

**Independent Test**: Create task, delete it, verify it's gone

### Backend (US6)

- [ ] T059 [US6] Implement DELETE /api/tasks/{id} endpoint
- [ ] T060 [US6] Add ownership check (403 if not owner)
- [ ] T061 [P] [US6] Unit test for task deletion in backend/tests/unit/test_tasks_api.py

### Frontend (US6)

- [ ] T062 [US6] Add delete button to task-item.tsx
- [ ] T063 [US6] Add confirmation dialog before delete
- [ ] T064 [US6] Wire delete to DELETE /api/tasks/{id}
- [ ] T065 [US6] Remove task from UI on successful delete

**Checkpoint**: User can delete tasks with confirmation

---

## Phase 8: User Story 7 - Mark Complete (Priority: P2)

**Goal**: Logged-in user can toggle task completion

**Independent Test**: Create task, mark complete, verify status change

### Backend (US7)

- [ ] T066 [US7] Implement PATCH /api/tasks/{id}/complete endpoint
- [ ] T067 [P] [US7] Unit test for completion toggle in backend/tests/unit/test_tasks_api.py

### Frontend (US7)

- [ ] T068 [US7] Add checkbox to task-item.tsx
- [ ] T069 [US7] Wire checkbox to PATCH /api/tasks/{id}/complete
- [ ] T070 [US7] Show visual distinction for completed tasks (strikethrough)

**Checkpoint**: User can toggle task completion status

---

## Phase 9: Multi-User Isolation Testing

**Purpose**: Verify User A cannot see/modify User B's tasks

- [ ] T071 Integration test: create two users, verify task isolation
- [ ] T072 Integration test: User A cannot GET User B's task (404)
- [ ] T073 Integration test: User A cannot PUT User B's task (403)
- [ ] T074 Integration test: User A cannot DELETE User B's task (403)

**Checkpoint**: Multi-user isolation verified

---

## Phase 10: Polish & Deployment

**Purpose**: Final quality, deployment, documentation

### Backend Polish

- [ ] T075 [P] Add comprehensive error handling to all endpoints
- [ ] T076 [P] Run all backend tests, ensure 100% pass rate
- [ ] T077 Create backend startup script for production

### Frontend Polish

- [ ] T078 [P] Add loading states to all async operations
- [ ] T079 [P] Add error handling for API failures
- [ ] T080 [P] Ensure responsive design (mobile-friendly)
- [ ] T081 Run frontend build, verify no errors

### Deployment

- [ ] T082 Deploy backend to Railway/Render
- [ ] T083 Update backend CORS_ORIGINS with Vercel URL
- [ ] T084 Deploy frontend to Vercel
- [ ] T085 Update frontend env vars with production backend URL
- [ ] T086 Test production: full signup/login/CRUD workflow

### Documentation

- [ ] T087 [P] Update backend/README.md with Phase II instructions
- [ ] T088 [P] Update frontend/README.md with setup instructions
- [ ] T089 Update quickstart.md with production URLs
- [ ] T090 Record demo video (< 90 seconds) showing all features

**Checkpoint**: Both apps deployed, demo video recorded, ready for submission

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Auth (3) → View (4) → Add (5) → Update (6) → Delete (7) → Complete (8) → Isolation (9) → Polish (10)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US1 (Register) | Foundational | - |
| US2 (Login) | US1 | - |
| US3 (View) | US2 | - |
| US4 (Add) | US3 | US5, US6, US7 |
| US5 (Update) | US3 | US4, US6, US7 |
| US6 (Delete) | US3 | US4, US5, US7 |
| US7 (Complete) | US3 | US4, US5, US6 |

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002, T003, T004, T005 can run in parallel

**Phase 2 (Foundational)**:
- T015-T019 frontend tasks can run in parallel
- Backend and frontend foundational can run in parallel after T008

**User Story Phases**:
- Backend and frontend for same story can partially parallelize
- US4-US7 can parallelize after US3 complete

---

## Summary

| Phase | Tasks | Story Coverage |
|-------|-------|----------------|
| Setup | T001-T008 (8) | Infrastructure |
| Foundational | T009-T020 (12) | Shared components |
| US1+US2 (P1) | T021-T035 (15) | Auth (Register, Login) |
| US3 (P2) | T036-T043 (8) | View Tasks |
| US4 (P2) | T044-T050 (7) | Add Task |
| US5 (P2) | T051-T058 (8) | Update Task |
| US6 (P2) | T059-T065 (7) | Delete Task |
| US7 (P2) | T066-T070 (5) | Mark Complete |
| Isolation | T071-T074 (4) | Multi-user testing |
| Polish | T075-T090 (16) | Quality & Deployment |
| **Total** | **90 tasks** | **7 user stories** |

---

## Notes

- All backend paths relative to `backend/` directory
- All frontend paths relative to `frontend/` directory
- Each task should result in a commit
- Stop at checkpoints to validate before continuing
- Run tests frequently during implementation
- Update CLAUDE.md after major changes

---

**Tasks Version**: 1.0.0
**Created**: 2025-12-06
**Status**: Ready for implementation
