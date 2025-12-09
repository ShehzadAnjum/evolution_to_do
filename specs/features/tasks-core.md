# Feature: Tasks Core (CRUD Operations)

**Phases**: I, II, III, IV, V (All phases)
**Status**: Implemented (Phase I & II)
**Version**: 02.002.000

---

## Overview

Core task management functionality - Create, Read, Update, Delete, and Complete operations for todo tasks. This is the foundational feature that spans all phases with increasing sophistication.

---

## Evolution Across Phases

### Phase I: Console CRUD
- In-memory storage (Python dict)
- Menu-driven CLI interface
- 5 basic operations
- Session-based (no persistence)

### Phase II: Web CRUD
- REST API endpoints (FastAPI)
- Database persistence (Neon PostgreSQL via SQLModel)
- Multi-user with authentication (Better Auth + JWT)
- Web UI (Next.js)
- User isolation (each user sees only their tasks)

### Phase III: AI CRUD
- MCP tools for AI agent
- Natural language interface
- All operations via chat

### Phase IV: Containerized CRUD
- Same functionality as Phase III
- Runs in Kubernetes

### Phase V: Event-Driven CRUD
- Domain events published to Kafka
- Dapr pub/sub integration
- Event sourcing patterns

---

## Core Operations

### 1. Create Task (Add)

**What**: Add a new task to the user's list

**Inputs**:
- Title (required, 1-200 chars)
- Description (optional, max 1000 chars)
- User ID (from auth context)

**Outputs**:
- New task object with generated ID
- Created timestamp
- Initial status (incomplete)

**Validation**:
- Title not empty
- Title length ≤ 200 chars
- Description length ≤ 1000 chars

### 2. Read Tasks (View/List)

**What**: Retrieve tasks for viewing

**Variants**:
- List all tasks
- Get single task by ID
- Filter by status (complete/incomplete)
- Search by keyword

**Outputs**:
- Array of task objects
- Each task includes: ID, title, description, status, timestamps

### 3. Update Task

**What**: Modify existing task details

**Inputs**:
- Task ID
- Updated title (optional)
- Updated description (optional)

**Validation**:
- Task exists
- Task belongs to current user
- New values meet constraints

### 4. Delete Task

**What**: Remove task from list

**Inputs**:
- Task ID

**Validation**:
- Task exists
- Task belongs to current user

**Side Effects**:
- Task permanently removed (Phase I-IV)
- Soft delete with event (Phase V)

### 5. Complete/Uncomplete Task

**What**: Toggle task completion status

**Inputs**:
- Task ID

**Validation**:
- Task exists
- Task belongs to current user

**Side Effects**:
- Updated timestamp recorded
- Completion event published (Phase V)

---

## Data Model

See `specs/database/schema.md` for full schema.

**Core Task Fields**:
```typescript
{
  id: string | number,
  user_id: string,
  title: string,
  description: string | null,
  is_complete: boolean,
  created_at: timestamp,
  updated_at: timestamp
}
```

---

## API Contracts

See `specs/api/rest-endpoints.md` for REST API (Phase II+)
See `specs/api/mcp-tools.md` for MCP tools (Phase III+)

---

## User Stories

### US-1: Add Task
As a user, I want to add new tasks so I can track what I need to do.

**Acceptance Criteria**:
- Can add task with just title
- Can add task with title and description
- Task appears in my task list immediately
- Task is not visible to other users

### US-2: View Tasks
As a user, I want to see my todo list so I know what needs to be done.

**Acceptance Criteria**:
- Can see all my tasks
- Tasks show title, description, completion status
- Empty state message if no tasks
- Cannot see other users' tasks

### US-3: Mark Complete
As a user, I want to mark tasks complete so I can track my progress.

**Acceptance Criteria**:
- Can toggle completion status
- Visual indication of completed tasks
- Completed tasks remain in list (not auto-deleted)

### US-4: Update Task
As a user, I want to edit tasks so I can fix mistakes or add details.

**Acceptance Criteria**:
- Can edit title
- Can edit description
- Changes save immediately
- Updated timestamp recorded

### US-5: Delete Task
As a user, I want to delete tasks I no longer need.

**Acceptance Criteria**:
- Can delete any of my tasks
- Confirmation prompt (Phase II+)
- Task removed permanently
- Cannot be undone

---

## Testing Requirements

### Unit Tests
- CRUD operation logic
- Validation rules
- Error handling

### Integration Tests
- Full request/response cycle (Phase II+)
- Database operations (Phase II+)
- User isolation

### UI Tests (Phase II+)
- Form validation
- Error states
- Loading states

---

## Current Implementation Status

- ✅ Phase I: Complete (console CRUD)
- ⏳ Phase II: In Progress (REST API partial, UI pending)
- ⏳ Phase III: Planned
- ⏳ Phase IV: Planned
- ⏳ Phase V: Planned

---

## References

- Phase I Spec: `specs/phases/phase-1.md`
- Phase II Spec: `specs/phases/phase-2.md`
- API Spec: `specs/api/rest-endpoints.md`
- Database Schema: `specs/database/schema.md`
