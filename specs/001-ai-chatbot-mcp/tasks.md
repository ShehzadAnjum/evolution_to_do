# Tasks: Phase III AI Chatbot with MCP Tools

**Input**: Design documents from `/specs/001-ai-chatbot-mcp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec - tests are optional for this feature.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/`
- Web app monorepo structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic structure

- [ ] T001 Install backend dependencies: `uv add mcp openai` in backend/
- [ ] T002 Install frontend dependencies: `npm install ai` in frontend/
- [ ] T003 [P] Create MCP module structure: backend/src/mcp/__init__.py, backend/src/mcp/server.py, backend/src/mcp/tools/__init__.py
- [ ] T004 [P] Create chat module structure: backend/src/api/chat.py, backend/src/services/chat_service.py
- [ ] T005 [P] Create frontend chat structure: frontend/app/chat/page.tsx, frontend/components/chat/, frontend/lib/chat/
- [ ] T006 Add OPENAI_API_KEY to backend .env and Railway environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create Conversation model in backend/src/models/conversation.py per data-model.md
- [ ] T008 Create Message model in backend/src/models/message.py per data-model.md
- [ ] T009 Create and run Alembic migration for conversation and message tables
- [ ] T010 [P] Create MCP server setup in backend/src/mcp/server.py with tool registration
- [ ] T011 [P] Create OpenAI client wrapper in backend/src/services/openai_client.py
- [ ] T012 Create ChatService base class in backend/src/services/chat_service.py with conversation management
- [ ] T013 Create chat types in frontend/lib/chat/types.ts (ChatRequest, ChatResponse, Message)
- [ ] T014 [P] Create chat API client in frontend/lib/chat/api.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Create Task via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by typing natural language in chat (e.g., "Add a task to buy groceries")

**Independent Test**: Type "Add a task called 'Buy groceries'" and verify task appears in task list

### Implementation for User Story 1

- [ ] T015 [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py
- [ ] T016 [US1] Register add_task tool in backend/src/mcp/server.py
- [ ] T017 [US1] Add tool execution logic for add_task in backend/src/services/chat_service.py
- [ ] T018 [US1] Create POST /api/chat endpoint in backend/src/api/chat.py with JWT auth
- [ ] T019 [US1] Create system prompt for task assistant in backend/src/mcp/prompts.py
- [ ] T020 [US1] Implement ChatInterface component in frontend/components/chat/ChatInterface.tsx using Vercel AI SDK
- [ ] T021 [US1] Implement MessageInput component in frontend/components/chat/MessageInput.tsx
- [ ] T022 [US1] Implement MessageList component in frontend/components/chat/MessageList.tsx
- [ ] T023 [US1] Create chat page in frontend/app/chat/page.tsx with auth protection
- [ ] T024 [US1] Create frontend API route in frontend/app/api/chat/route.ts to proxy to backend

**Checkpoint**: User Story 1 complete - users can create tasks via chat

---

## Phase 4: User Story 2 - List Tasks via Chat (Priority: P1)

**Goal**: Users can view their tasks by asking the chatbot (e.g., "Show me my tasks")

**Independent Test**: Type "Show my tasks" and verify AI lists all user tasks

### Implementation for User Story 2

- [ ] T025 [US2] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py
- [ ] T026 [US2] Register list_tasks tool in backend/src/mcp/server.py
- [ ] T027 [US2] Add tool execution logic for list_tasks in backend/src/services/chat_service.py
- [ ] T028 [US2] Update system prompt to handle list requests in backend/src/mcp/prompts.py
- [ ] T029 [US2] Create ToolResultCard component in frontend/components/chat/ToolResultCard.tsx for displaying task lists

**Checkpoint**: User Stories 1 AND 2 complete - users can create and view tasks via chat

---

## Phase 5: User Story 3 - Complete Task via Chat (Priority: P2)

**Goal**: Users can mark tasks as complete by telling the chatbot (e.g., "Mark 'Buy groceries' as done")

**Independent Test**: Type "Complete the 'Buy groceries' task" and verify task status changes

### Implementation for User Story 3

- [ ] T030 [US3] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py
- [ ] T031 [US3] Register complete_task tool in backend/src/mcp/server.py
- [ ] T032 [US3] Add tool execution logic for complete_task in backend/src/services/chat_service.py
- [ ] T033 [US3] Update system prompt to handle completion requests in backend/src/mcp/prompts.py

**Checkpoint**: User Story 3 complete - users can complete tasks via chat

---

## Phase 6: User Story 4 - Delete Task via Chat (Priority: P2)

**Goal**: Users can delete tasks by telling the chatbot (e.g., "Delete the 'Call dentist' task")

**Independent Test**: Type "Delete 'Call dentist'" and verify task is removed

### Implementation for User Story 4

- [ ] T034 [US4] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py
- [ ] T035 [US4] Register delete_task tool in backend/src/mcp/server.py
- [ ] T036 [US4] Add tool execution logic for delete_task in backend/src/services/chat_service.py
- [ ] T037 [US4] Update system prompt to handle delete requests in backend/src/mcp/prompts.py

**Checkpoint**: User Story 4 complete - users can delete tasks via chat

---

## Phase 7: User Story 5 - Update Task via Chat (Priority: P2)

**Goal**: Users can update task details by telling the chatbot (e.g., "Rename 'Buy groceries' to 'Buy organic groceries'")

**Independent Test**: Type "Rename 'Buy groceries' to 'Buy organic groceries'" and verify change

### Implementation for User Story 5

- [ ] T038 [US5] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py
- [ ] T039 [US5] Register update_task tool in backend/src/mcp/server.py
- [ ] T040 [US5] Add tool execution logic for update_task in backend/src/services/chat_service.py
- [ ] T041 [US5] Update system prompt to handle update requests in backend/src/mcp/prompts.py

**Checkpoint**: User Story 5 complete - users can update tasks via chat

---

## Phase 8: User Story 6 - Search Tasks via Chat (Priority: P3)

**Goal**: Users can search for tasks by keyword (e.g., "Find tasks about groceries")

**Independent Test**: Type "Find tasks about groceries" and verify matching tasks appear

### Implementation for User Story 6

- [ ] T042 [US6] Implement search_tasks MCP tool in backend/src/mcp/tools/search_tasks.py
- [ ] T043 [US6] Register search_tasks tool in backend/src/mcp/server.py
- [ ] T044 [US6] Add tool execution logic for search_tasks in backend/src/services/chat_service.py
- [ ] T045 [US6] Update system prompt to handle search requests in backend/src/mcp/prompts.py

**Checkpoint**: User Story 6 complete - users can search tasks via chat

---

## Phase 9: User Story 7 - Get Task Details via Chat (Priority: P3)

**Goal**: Users can get full details of a specific task (e.g., "Show details for 'Project report'")

**Independent Test**: Type "Tell me about the 'Buy groceries' task" and verify full details appear

### Implementation for User Story 7

- [ ] T046 [US7] Implement get_task MCP tool in backend/src/mcp/tools/get_task.py
- [ ] T047 [US7] Register get_task tool in backend/src/mcp/server.py
- [ ] T048 [US7] Add tool execution logic for get_task in backend/src/services/chat_service.py
- [ ] T049 [US7] Update system prompt to handle detail requests in backend/src/mcp/prompts.py

**Checkpoint**: User Story 7 complete - users can get task details via chat

---

## Phase 10: User Story 8 - Conversation History (Priority: P3)

**Goal**: Chat history persists across page reloads and sessions

**Independent Test**: Have a conversation, refresh the page, verify previous messages appear

### Implementation for User Story 8

- [ ] T050 [US8] Implement conversation persistence in backend/src/services/chat_service.py (save/load messages)
- [ ] T051 [US8] Add GET /api/chat/conversations endpoint in backend/src/api/chat.py
- [ ] T052 [US8] Add GET /api/chat/conversations/{id} endpoint in backend/src/api/chat.py
- [ ] T053 [US8] Update frontend to load conversation history on page load in frontend/app/chat/page.tsx
- [ ] T054 [US8] Add conversation selector UI in frontend/components/chat/ConversationList.tsx (optional)

**Checkpoint**: User Story 8 complete - conversation history persists

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Add error handling for all MCP tools in backend/src/mcp/tools/
- [ ] T056 [P] Add loading states and error messages in frontend/components/chat/
- [ ] T057 Add logging for chat interactions in backend/src/services/chat_service.py
- [ ] T058 [P] Add input validation for chat messages in backend/src/api/chat.py
- [ ] T059 Run quickstart.md validation - verify all scenarios work end-to-end
- [ ] T060 Update SESSION_HANDOFF.md with Phase III completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - US1 & US2 (P1): Can run in parallel after Foundation
  - US3, US4, US5 (P2): Can run in parallel after Foundation
  - US6, US7, US8 (P3): Can run in parallel after Foundation
- **Polish (Phase 11)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories - MVP
- **User Story 2 (P1)**: No dependencies on other stories
- **User Story 3 (P2)**: No dependencies on other stories
- **User Story 4 (P2)**: No dependencies on other stories
- **User Story 5 (P2)**: No dependencies on other stories
- **User Story 6 (P3)**: No dependencies on other stories
- **User Story 7 (P3)**: No dependencies on other stories
- **User Story 8 (P3)**: Depends on chat endpoint from US1 being functional

### Within Each User Story

- MCP tool before registration
- Registration before ChatService integration
- Backend complete before frontend integration
- Core implementation before system prompt updates

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- MCP tools (T015, T025, T030, T034, T038, T042, T046) can be developed in parallel
- Frontend components (T020, T021, T022, T029) can be developed in parallel
- All user stories can be worked on in parallel after Foundation

---

## Parallel Example: Foundation Phase

```bash
# Launch in parallel:
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"

# Then sequentially:
Task: "Create and run Alembic migration for conversation and message tables"

# Then in parallel:
Task: "Create MCP server setup in backend/src/mcp/server.py"
Task: "Create OpenAI client wrapper in backend/src/services/openai_client.py"
Task: "Create chat types in frontend/lib/chat/types.ts"
Task: "Create chat API client in frontend/lib/chat/api.ts"
```

---

## Parallel Example: All MCP Tools

```bash
# After Foundation, launch all MCP tools in parallel:
Task: "Implement add_task MCP tool in backend/src/mcp/tools/add_task.py"
Task: "Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py"
Task: "Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py"
Task: "Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py"
Task: "Implement update_task MCP tool in backend/src/mcp/tools/update_task.py"
Task: "Implement search_tasks MCP tool in backend/src/mcp/tools/search_tasks.py"
Task: "Implement get_task MCP tool in backend/src/mcp/tools/get_task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - Create Task via Chat
4. **STOP and VALIDATE**: Test creating tasks via chat independently
5. Deploy/demo if ready - this is the MVP!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Create) + US2 (List) → Test independently → Deploy (MVP with read/write!)
3. Add US3 (Complete) + US4 (Delete) + US5 (Update) → Full CRUD via chat
4. Add US6 (Search) + US7 (Details) → Enhanced functionality
5. Add US8 (History) → Polished experience
6. Polish phase → Production ready

### Suggested Execution Order (Single Developer)

1. T001-T006 (Setup) - ~30 min
2. T007-T014 (Foundation) - ~2 hours
3. T015-T024 (US1 - Create Task) - ~2 hours → **MVP Checkpoint**
4. T025-T029 (US2 - List Tasks) - ~1 hour
5. T030-T037 (US3-4 - Complete/Delete) - ~1 hour
6. T038-T041 (US5 - Update) - ~30 min
7. T042-T049 (US6-7 - Search/Details) - ~1 hour
8. T050-T054 (US8 - History) - ~1 hour
9. T055-T060 (Polish) - ~1 hour

**Total Estimated: ~10 hours**

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Setup | 6 | Dependencies and project structure |
| Foundational | 8 | Models, migrations, core services |
| US1 (P1) | 10 | Create task via chat - MVP |
| US2 (P1) | 5 | List tasks via chat |
| US3 (P2) | 4 | Complete task via chat |
| US4 (P2) | 4 | Delete task via chat |
| US5 (P2) | 4 | Update task via chat |
| US6 (P3) | 4 | Search tasks via chat |
| US7 (P3) | 4 | Get task details via chat |
| US8 (P3) | 5 | Conversation history |
| Polish | 6 | Error handling, logging, validation |
| **Total** | **60** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = Phase 1 + 2 + 3 (Setup + Foundation + US1)
