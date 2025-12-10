---
id: "0002"
title: "Phase III AI Chatbot Implementation Plan"
stage: plan
date: 2025-12-10
surface: claude-code
model: claude-opus-4-5-20251101
feature: 001-ai-chatbot-mcp
branch: 001-ai-chatbot-mcp
user: anjum
command: /sp.plan
labels: [phase-iii, ai-chatbot, mcp, implementation-plan]
links:
  spec: specs/001-ai-chatbot-mcp/spec.md
  plan: specs/001-ai-chatbot-mcp/plan.md
  research: specs/001-ai-chatbot-mcp/research.md
  data-model: specs/001-ai-chatbot-mcp/data-model.md
  ticket:
  adr:
  pr:
files:
  - path: specs/001-ai-chatbot-mcp/plan.md
    action: created
  - path: specs/001-ai-chatbot-mcp/research.md
    action: created
  - path: specs/001-ai-chatbot-mcp/data-model.md
    action: created
  - path: specs/001-ai-chatbot-mcp/contracts/mcp-tools.yaml
    action: created
  - path: specs/001-ai-chatbot-mcp/contracts/chat-api.yaml
    action: created
  - path: specs/001-ai-chatbot-mcp/quickstart.md
    action: created
tests:
  - N/A (planning phase - no tests yet)
---

## Prompt

/sp.plan

## Response snapshot

Created comprehensive Phase III AI Chatbot implementation plan with:

**plan.md**:
- Technical context with language/version, dependencies, storage, testing
- Constitution check (all gates PASS)
- Project structure for backend MCP module and frontend chat components
- Component architecture diagram (Frontend → Backend → MCP Server → Database)
- Implementation phases (Phase 0-2)
- Risk assessment with mitigations
- Dependencies (external and internal)
- Complexity tracking

**research.md** (6 Technology Decisions):
1. MCP Implementation: Official MCP Python SDK
2. AI Agent: OpenAI Python SDK with function calling (not Agents SDK)
3. Frontend Chat UI: Vercel AI SDK (not ChatKit)
4. Conversation Persistence: Neon PostgreSQL + SQLModel
5. Authentication: Reuse Better Auth JWT
6. Error Handling: User-friendly messages + server-side logging

**data-model.md**:
- Conversation entity: id, user_id, title, created_at, updated_at
- Message entity: id, conversation_id, role, content, tool_calls, tool_call_id, created_at
- Entity relationship diagram
- Validation rules and state transitions
- Alembic migration SQL
- Query patterns

**contracts/mcp-tools.yaml**:
- 7 MCP tool schemas: add_task, list_tasks, get_task, update_task, delete_task, complete_task, search_tasks
- Input schemas with validation (minLength, maxLength, enum)
- Output schemas with task properties
- Consistent error schema

**contracts/chat-api.yaml**:
- OpenAPI 3.1.0 specification
- POST /api/chat - send message to AI
- GET /api/chat/conversations - list conversations
- GET /api/chat/conversations/{id} - get conversation with messages
- DELETE /api/chat/conversations/{id} - delete conversation
- Bearer JWT authentication
- Request/response schemas with examples

**quickstart.md**:
- Prerequisites checklist
- Implementation order (5 phases, ~5 hours total)
- Key files reference
- Common issues & solutions
- Testing checklist
- Documentation reading list

## Outcome

- ✅ Impact: Complete planning documentation for Phase III AI Chatbot feature
- 🧪 Tests: N/A - planning phase (tests will be defined in implementation)
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, mcp-tools.yaml, chat-api.yaml, quickstart.md)
- 🔁 Next prompts: /sp.tasks to generate implementation task list
- 🧠 Reflection: All constitution gates passed; technology decisions well-documented with rationale and alternatives; data model extends Phase II without breaking changes

## Evaluation notes (flywheel)

- Failure modes observed: None - plan created successfully following spec workflow
- Graders run and results (PASS/FAIL): Manual review PASS - all artifacts align with spec requirements
- Prompt variant (if applicable): Standard /sp.plan after /sp.specify
- Next experiment (smallest change to try): Run /sp.tasks to generate implementation task list
