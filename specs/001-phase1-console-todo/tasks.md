# Tasks: Phase I Console Todo Application

**Input**: Design documents from `/specs/001-phase1-console-todo/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/cli-interface.md ✅

**Tests**: Included (pytest for unit and integration testing per plan.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- All paths relative to `backend/` directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Python/UV configuration

- [ ] T001 Create backend directory structure per plan.md
- [ ] T002 Initialize UV project with `uv init` in backend/
- [ ] T003 Configure pyproject.toml with Python 3.13+ requirement
- [ ] T004 [P] Add pytest and pytest-cov as dev dependencies
- [ ] T005 [P] Create all `__init__.py` files for packages (src/, models/, services/, cli/, lib/, tests/)
- [ ] T006 [P] Create .gitignore with Python patterns (venv, __pycache__, .pytest_cache, etc.)

**Checkpoint**: UV project initialized, can run `uv sync` successfully

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core components that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Create Task dataclass with validation in backend/src/models/task.py (from data-model.md)
- [ ] T008 [P] Create TaskStore class with CRUD operations in backend/src/services/task_store.py (from data-model.md)
- [ ] T009 [P] Create input validators (title length 200, description 1000, Unicode support) in backend/src/lib/validators.py
- [ ] T010 [P] Create output formatters (success ✓, error ✗, box drawing) in backend/src/cli/formatters.py
- [ ] T011 Create menu display system with box drawing in backend/src/cli/menu.py (from cli-interface.md)
- [ ] T012 Create main entry point with menu loop and Ctrl+C handling in backend/src/main.py

**Checkpoint**: Foundation ready - can display menu and handle Ctrl+C gracefully

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks and see their complete task list

**Independent Test**: Add several tasks, view list - should see all tasks with IDs, titles, descriptions, status

### Tests for User Story 1

- [ ] T013 [P] [US1] Unit test for Task dataclass validation in backend/tests/unit/test_task.py
- [ ] T014 [P] [US1] Unit test for TaskStore.add() and TaskStore.get_all() in backend/tests/unit/test_task_store.py

### Implementation for User Story 1

- [ ] T015 [US1] Implement add_task handler (prompt title, optional description) in backend/src/cli/handlers.py
- [ ] T016 [US1] Implement view_tasks handler (list all with status indicators) in backend/src/cli/handlers.py
- [ ] T017 [US1] Implement empty state display ("No tasks yet") in view_tasks handler
- [ ] T018 [US1] Implement task summary (Total/Completed/Remaining) in view_tasks handler
- [ ] T019 [US1] Wire add_task and view_tasks to menu options 1 and 2 in backend/src/main.py

**Checkpoint**: Can add tasks and view them - MVP is functional

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can toggle task completion status to track progress

**Independent Test**: Add tasks, mark some complete, verify status changes visible in task list

### Tests for User Story 2

- [ ] T020 [P] [US2] Unit test for TaskStore.toggle_complete() in backend/tests/unit/test_task_store.py

### Implementation for User Story 2

- [ ] T021 [US2] Implement mark_complete handler (prompt ID, toggle status) in backend/src/cli/handlers.py
- [ ] T022 [US2] Add error handling for invalid task ID in mark_complete handler
- [ ] T023 [US2] Wire mark_complete to menu option 3 in backend/src/main.py

**Checkpoint**: Can mark tasks complete/incomplete - status tracking works

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Users can modify task title and/or description

**Independent Test**: Create tasks, update titles/descriptions, verify changes persist

### Tests for User Story 3

- [ ] T024 [P] [US3] Unit test for TaskStore.update() (partial updates, preserve unchanged) in backend/tests/unit/test_task_store.py

### Implementation for User Story 3

- [ ] T025 [US3] Implement update_task handler (show current, prompt new values) in backend/src/cli/handlers.py
- [ ] T026 [US3] Handle empty input preservation (keep current value) in update_task handler
- [ ] T027 [US3] Add error handling for invalid task ID in update_task handler
- [ ] T028 [US3] Wire update_task to menu option 4 in backend/src/main.py

**Checkpoint**: Can update tasks - editing functionality complete

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P3)

**Goal**: Users can remove unwanted tasks with confirmation

**Independent Test**: Create tasks, delete specific ones with confirmation, verify removal

### Tests for User Story 4

- [ ] T029 [P] [US4] Unit test for TaskStore.delete() in backend/tests/unit/test_task_store.py

### Implementation for User Story 4

- [ ] T030 [US4] Implement delete_task handler (prompt ID, show task, confirm) in backend/src/cli/handlers.py
- [ ] T031 [US4] Implement confirmation dialog (y/n with validation) in backend/src/cli/handlers.py
- [ ] T032 [US4] Add error handling for invalid task ID in delete_task handler
- [ ] T033 [US4] Wire delete_task to menu option 5 in backend/src/main.py

**Checkpoint**: All 5 operations complete - full feature set implemented

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements and verification

- [ ] T034 [P] Create integration test for full CLI workflow in backend/tests/integration/test_cli.py
- [ ] T035 [P] Create backend/README.md with setup and usage instructions
- [ ] T036 Implement exit handler (menu option 6) with goodbye message in backend/src/main.py
- [ ] T037 Run all tests and ensure 100% pass rate
- [ ] T038 Manual test: Complete full workflow (add → view → complete → update → delete) in < 60 seconds
- [ ] T039 Validate quickstart.md instructions work for fresh setup

**Checkpoint**: All tests pass, quickstart works, ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → User Stories (3-6) → Phase 7 (Polish)
                                          ↓
                              US1 → US2 → US3 → US4
                              (can be parallel if staffed)
```

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational completion
  - US1 must complete first (others depend on view to verify)
  - US2, US3, US4 can be parallel after US1
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US1 (Add/View) | Foundational only | None - must be first |
| US2 (Mark Complete) | US1 (need tasks to mark) | US3, US4 |
| US3 (Update) | US1 (need tasks to update) | US2, US4 |
| US4 (Delete) | US1 (need tasks to delete) | US2, US3 |

### Within Each User Story

1. Tests written first (TDD)
2. Implementation follows tests
3. Wire to menu last
4. Verify checkpoint before proceeding

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# Run in parallel:
T004: Add pytest dependencies
T005: Create __init__.py files
T006: Create .gitignore
```

**Phase 2 (Foundational)**:
```bash
# Run in parallel:
T007: Task dataclass
T008: TaskStore class
T009: Input validators
T010: Output formatters
```

**User Story Tests** (within each story):
```bash
# All test tasks marked [P] can run in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Complete Phase 1: Setup (T001-T006)
2. ✅ Complete Phase 2: Foundational (T007-T012)
3. ✅ Complete Phase 3: User Story 1 (T013-T019)
4. **STOP and VALIDATE**: Test add and view independently
5. Demo MVP if needed

### Incremental Delivery

```
Setup → Foundational → US1 (MVP!) → US2 → US3 → US4 → Polish
                         ↓           ↓     ↓     ↓
                       Demo?      Demo? Demo? Demo?
```

Each checkpoint is a potential demo/validation point.

### Recommended Execution Order

```
T001 → T002 → T003 → [T004, T005, T006] parallel
     ↓
[T007, T008, T009, T010] parallel → T011 → T012
     ↓
[T013, T014] parallel → T015 → T016 → T017 → T018 → T019 ✓ MVP
     ↓
T020 → T021 → T022 → T023 ✓ US2
     ↓
T024 → T025 → T026 → T027 → T028 ✓ US3
     ↓
T029 → T030 → T031 → T032 → T033 ✓ US4
     ↓
[T034, T035] parallel → T036 → T037 → T038 → T039 ✓ DONE
```

---

## Summary

| Phase | Tasks | Story Coverage |
|-------|-------|----------------|
| Setup | T001-T006 (6) | Infrastructure |
| Foundational | T007-T012 (6) | Shared components |
| US1 (P1) | T013-T019 (7) | Add + View |
| US2 (P2) | T020-T023 (4) | Mark Complete |
| US3 (P2) | T024-T028 (5) | Update |
| US4 (P3) | T029-T033 (5) | Delete |
| Polish | T034-T039 (6) | Quality |
| **Total** | **39 tasks** | **4 user stories** |

### Parallel Opportunities

- Setup: 3 tasks can run in parallel
- Foundational: 4 tasks can run in parallel
- Each user story: Tests can run in parallel
- After US1: US2, US3, US4 can be parallelized

### MVP Scope

**Minimum deployment**: Complete through T019 (US1)
- Users can add tasks
- Users can view tasks with status
- Delivers immediate value

---

## Notes

- All file paths relative to `backend/` directory
- Each task should result in a commit
- Stop at checkpoints to validate before continuing
- Tests use pytest (dev dependency only)
- Unicode and length limits per clarifications (title: 200, desc: 1000)
