# Implementation Plan: Phase III AI Chatbot with MCP Tools

**Branch**: `001-ai-chatbot-mcp` | **Date**: 2025-12-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot-mcp/spec.md`

## Summary

Implement an AI-powered chatbot that enables users to manage tasks through natural language conversation. The chatbot uses the Model Context Protocol (MCP) to expose 7 task operations as tools that an AI agent can invoke. Built on the existing Phase II infrastructure (FastAPI, Next.js, Better Auth, Neon PostgreSQL), adding an MCP server, OpenAI Agents SDK integration, and ChatKit UI.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Node 20+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, MCP Python SDK, OpenAI Python SDK
- Frontend: Next.js 14+, ChatKit (or Vercel AI SDK), React
**Storage**: Neon PostgreSQL (existing) + new conversation/message tables
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web (Vercel frontend, Railway backend)
**Project Type**: Web application (monorepo with backend/ and frontend/)
**Performance Goals**: <10s task creation via chat, <2s UI load, 90% intent accuracy
**Constraints**: Stateless backend (all state in DB), JWT-authenticated requests
**Scale/Scope**: Single user conversations, ~100 messages per conversation max

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phase Boundaries | ✅ PASS | Phase III is current phase, AI chatbot is Phase III scope |
| II. Finish One Thing | ✅ PASS | Phase II signed off, no WIP |
| III. Documentation First | ⚠️ PENDING | Must read MCP SDK, OpenAI Agents SDK docs before implementing |
| IV. Context Preservation | ✅ PASS | SESSION_HANDOFF.md up to date |
| V. Repository Cleanliness | ✅ PASS | Repo sanitized in previous session |
| VI. Spec-Driven Development | ✅ PASS | Using /sp.specify, /sp.plan workflow |
| VII. Value-Driven Features | ✅ PASS | Chat interface delivers immediate user value |
| VIII. Quality Over Speed | ✅ PASS | Focus on core 7 tools before extras |

**Gate Status**: ✅ PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-mcp/
├── spec.md              # Feature specification (created via /sp.specify)
├── plan.md              # This file (created via /sp.plan)
├── research.md          # Phase 0 output - technology decisions
├── data-model.md        # Phase 1 output - entity definitions
├── quickstart.md        # Phase 1 output - getting started guide
├── contracts/           # Phase 1 output - API contracts
│   ├── mcp-tools.yaml   # MCP tool definitions
│   └── chat-api.yaml    # Chat endpoint OpenAPI
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py              # FastAPI entry point (existing)
│   ├── models/
│   │   ├── task.py          # Task model (existing)
│   │   ├── conversation.py  # NEW: Conversation model
│   │   └── message.py       # NEW: Message model
│   ├── services/
│   │   ├── task_service.py  # Task CRUD logic (existing)
│   │   └── chat_service.py  # NEW: Chat orchestration
│   ├── api/
│   │   ├── tasks.py         # Task endpoints (existing)
│   │   └── chat.py          # NEW: Chat endpoint
│   └── mcp/
│       ├── __init__.py      # NEW: MCP module
│       ├── server.py        # NEW: MCP server setup
│       └── tools/           # NEW: MCP tool implementations
│           ├── __init__.py
│           ├── add_task.py
│           ├── list_tasks.py
│           ├── get_task.py
│           ├── update_task.py
│           ├── delete_task.py
│           ├── complete_task.py
│           └── search_tasks.py
└── tests/
    ├── test_mcp_tools.py    # NEW: MCP tool tests
    └── test_chat_api.py     # NEW: Chat endpoint tests

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx         # NEW: Chat page
│   └── api/
│       └── chat/
│           └── route.ts     # NEW: Chat API route (proxy to backend)
├── components/
│   └── chat/
│       ├── ChatInterface.tsx    # NEW: Main chat component
│       ├── MessageList.tsx      # NEW: Message display
│       ├── MessageInput.tsx     # NEW: Input component
│       └── ToolResultCard.tsx   # NEW: Tool result display
└── lib/
    └── chat/
        ├── api.ts           # NEW: Chat API client
        └── types.ts         # NEW: Chat types
```

**Structure Decision**: Web application structure with backend/ and frontend/ separation (existing Phase II structure). New MCP module added to backend/src/mcp/.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (Next.js)                         │
├─────────────────────────────────────────────────────────────────────┤
│  /chat (page.tsx)                                                    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ ChatInterface                                                │    │
│  │ ┌───────────────────────────────────────────────────────┐   │    │
│  │ │ MessageList                                            │   │    │
│  │ │ - User messages                                        │   │    │
│  │ │ - AI responses                                         │   │    │
│  │ │ - Tool result cards                                    │   │    │
│  │ └───────────────────────────────────────────────────────┘   │    │
│  │ ┌───────────────────────────────────────────────────────┐   │    │
│  │ │ MessageInput                                           │   │    │
│  │ │ - Text input                                           │   │    │
│  │ │ - Send button                                          │   │    │
│  │ └───────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ POST /api/chat
                                    │ Authorization: Bearer <jwt>
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI)                          │
├─────────────────────────────────────────────────────────────────────┤
│  /api/chat (chat.py)                                                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ ChatService                                                  │    │
│  │ 1. Validate JWT, extract user_id                            │    │
│  │ 2. Load/create conversation                                 │    │
│  │ 3. Add user message to DB                                   │    │
│  │ 4. Call AI Agent with MCP tools                             │    │
│  │ 5. Execute tool calls                                       │    │
│  │ 6. Store AI response in DB                                  │    │
│  │ 7. Return response                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          │                                           │
│                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ AI Agent (OpenAI Agents SDK)                                │    │
│  │ - System prompt with task assistant behavior                │    │
│  │ - Access to 7 MCP tools                                     │    │
│  │ - Handles tool calls and responses                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                          │                                           │
│                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ MCP Server (mcp/server.py)                                  │    │
│  │ ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐      │    │
│  │ │add_task │ │list_tasks│ │get_task  │ │update_task  │      │    │
│  │ └─────────┘ └──────────┘ └──────────┘ └─────────────┘      │    │
│  │ ┌───────────┐ ┌──────────────┐ ┌────────────┐              │    │
│  │ │delete_task│ │complete_task │ │search_tasks│              │    │
│  │ └───────────┘ └──────────────┘ └────────────┘              │    │
│  │                                                              │    │
│  │ Each tool calls TaskService (existing API logic)            │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DATABASE (Neon PostgreSQL)                       │
├─────────────────────────────────────────────────────────────────────┤
│  Existing:                    │  New:                                │
│  - user (from Better Auth)    │  - conversation                      │
│  - session                    │  - message                           │
│  - task                       │                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 0: Research (Completed in research.md)

- MCP Python SDK usage patterns
- OpenAI Agents SDK vs Claude API decision
- ChatKit vs Vercel AI SDK decision
- Conversation persistence strategy

### Phase 1: Foundation

1. **Database Models** (data-model.md)
   - Conversation model
   - Message model
   - Migrations

2. **MCP Server Setup**
   - Initialize MCP server
   - Define tool schemas
   - Implement tool handlers (calling existing TaskService)

3. **API Contracts** (contracts/)
   - MCP tool definitions
   - Chat endpoint OpenAPI spec

### Phase 2: Implementation (tasks.md)

1. Backend MCP tools (7 tools)
2. Chat service and endpoint
3. AI agent integration
4. Frontend chat UI
5. Integration testing
6. Deployment

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| MCP SDK learning curve | Medium | Read docs first (30 min rule), use official examples |
| OpenAI API rate limits | Low | Implement retry with backoff |
| JWT auth in chat flow | Medium | Reuse existing Better Auth middleware |
| Conversation state management | Medium | Keep stateless, all state in DB |
| UI complexity | Low | Use ChatKit/Vercel AI SDK components |

## Dependencies

### External Dependencies (to be installed)

**Backend**:
- `mcp` - Official MCP Python SDK
- `openai` - OpenAI Python SDK (likely already installed)

**Frontend**:
- `ai` - Vercel AI SDK (or ChatKit)
- UI components (may use existing shadcn/ui)

### Internal Dependencies (existing)

- Phase II task CRUD API (working)
- Better Auth JWT authentication (working)
- Neon PostgreSQL connection (working)
- FastAPI middleware (working)

## Complexity Tracking

> No constitution violations - complexity justified.

| Decision | Justification |
|----------|---------------|
| Separate MCP module | Clean separation of concerns, follows existing structure |
| 7 MCP tools (not fewer) | Matches spec requirements, each maps to a user action |
| New chat endpoint (not extending existing) | Different responsibility, cleaner API |

## Next Steps

1. Generate `research.md` - Technology decisions
2. Generate `data-model.md` - Entity definitions
3. Generate `contracts/` - API specifications
4. Generate `quickstart.md` - Getting started guide
5. Run `/sp.tasks` to generate implementation tasks
