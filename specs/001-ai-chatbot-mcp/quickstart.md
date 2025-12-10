# Quickstart Guide: Phase III AI Chatbot with MCP Tools

**Feature**: `001-ai-chatbot-mcp`
**Date**: 2025-12-10
**Status**: Planning Complete

## Overview

This guide helps developers get started with implementing the Phase III AI Chatbot feature. It assumes Phase II is complete with working authentication, task CRUD, and database.

---

## Prerequisites

### Required (from Phase II)

- ✅ FastAPI backend running on Railway
- ✅ Next.js frontend running on Vercel
- ✅ Neon PostgreSQL with user and task tables
- ✅ Better Auth JWT authentication working
- ✅ Task CRUD API endpoints functional

### New Dependencies to Install

**Backend**:
```bash
cd backend
uv add mcp openai
```

**Frontend**:
```bash
cd frontend
npm install ai
```

### Environment Variables

Add to backend `.env`:
```bash
OPENAI_API_KEY=sk-...your-key-here...
```

Add to Railway:
```bash
railway variables set OPENAI_API_KEY=sk-...your-key-here...
```

---

## Implementation Order

### Phase 1: Database Setup (~30 min)

1. **Create Models**:
   ```bash
   # Create model files
   touch backend/src/models/conversation.py
   touch backend/src/models/message.py
   ```

2. **Run Migration**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add conversation and message tables"
   alembic upgrade head
   ```

3. **Verify Tables**:
   ```sql
   -- In Neon console
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public';
   -- Should show: user, session, task, conversation, message
   ```

### Phase 2: MCP Server (~1 hour)

1. **Create MCP Module Structure**:
   ```bash
   mkdir -p backend/src/mcp/tools
   touch backend/src/mcp/__init__.py
   touch backend/src/mcp/server.py
   touch backend/src/mcp/tools/__init__.py
   ```

2. **Implement Tools** (one at a time):
   - `add_task.py` - Start here, simplest
   - `list_tasks.py` - Query tasks
   - `get_task.py` - Single task lookup
   - `complete_task.py` - Toggle completion
   - `update_task.py` - Modify task
   - `delete_task.py` - Remove task
   - `search_tasks.py` - Keyword search

3. **Test Each Tool**:
   ```python
   # backend/tests/test_mcp_tools.py
   async def test_add_task_tool():
       result = await mcp_server.call_tool("add_task", {
           "title": "Test task"
       })
       assert result["success"] is True
   ```

### Phase 3: Chat Service (~1 hour)

1. **Create Chat Service**:
   ```bash
   touch backend/src/services/chat_service.py
   ```

2. **Implement Core Flow**:
   ```python
   async def process_message(user_id: str, message: str, conversation_id: Optional[UUID] = None):
       # 1. Get or create conversation
       # 2. Save user message
       # 3. Call OpenAI with tools
       # 4. Execute any tool calls
       # 5. Save assistant response
       # 6. Return response
   ```

3. **Create Chat Endpoint**:
   ```bash
   touch backend/src/api/chat.py
   ```

### Phase 4: Frontend UI (~1 hour)

1. **Create Chat Components**:
   ```bash
   mkdir -p frontend/components/chat
   touch frontend/components/chat/ChatInterface.tsx
   touch frontend/components/chat/MessageList.tsx
   touch frontend/components/chat/MessageInput.tsx
   ```

2. **Create Chat Page**:
   ```bash
   mkdir -p frontend/app/chat
   touch frontend/app/chat/page.tsx
   ```

3. **Add API Route** (proxy to backend):
   ```bash
   mkdir -p frontend/app/api/chat
   touch frontend/app/api/chat/route.ts
   ```

### Phase 5: Integration & Testing (~1 hour)

1. **End-to-End Test**:
   - Login to app
   - Navigate to /chat
   - Send "Add a task to buy milk"
   - Verify task appears in task list
   - Send "Mark buy milk as complete"
   - Verify task is completed

2. **Run Test Suite**:
   ```bash
   cd backend && pytest tests/test_chat*.py -v
   cd frontend && npm test
   ```

---

## Key Files Reference

### Backend Files

| File | Purpose |
|------|---------|
| `src/models/conversation.py` | Conversation SQLModel |
| `src/models/message.py` | Message SQLModel |
| `src/mcp/server.py` | MCP server setup |
| `src/mcp/tools/*.py` | Individual tool implementations |
| `src/services/chat_service.py` | Chat orchestration |
| `src/api/chat.py` | Chat endpoint |

### Frontend Files

| File | Purpose |
|------|---------|
| `app/chat/page.tsx` | Chat page route |
| `components/chat/ChatInterface.tsx` | Main chat UI |
| `components/chat/MessageList.tsx` | Display messages |
| `components/chat/MessageInput.tsx` | User input |
| `app/api/chat/route.ts` | API proxy route |

---

## Common Issues & Solutions

### Issue: "Tool not found" error

**Cause**: Tool not registered in MCP server
**Solution**: Ensure tool is added to `@server.list_tools()` decorator

### Issue: "OPENAI_API_KEY not set"

**Cause**: Missing environment variable
**Solution**: Add to `.env` and Railway variables

### Issue: "Unauthorized" on chat endpoint

**Cause**: JWT not passed correctly
**Solution**: Ensure `Authorization: Bearer <token>` header is set

### Issue: "Conversation not found"

**Cause**: User trying to access another user's conversation
**Solution**: Check `user_id` filter in conversation queries

### Issue: "AI not calling tools"

**Cause**: System prompt not instructing tool use
**Solution**: Update system prompt to explicitly mention available tools

---

## Testing Checklist

- [ ] Can create task via "Add task X"
- [ ] Can list tasks via "Show my tasks"
- [ ] Can complete task via "Mark X as done"
- [ ] Can delete task via "Delete X"
- [ ] Can update task via "Rename X to Y"
- [ ] Can search tasks via "Find tasks about X"
- [ ] Error handling works (nonexistent task, etc.)
- [ ] Conversation persists across page reloads
- [ ] User isolation works (can't see other users' tasks)

---

## Documentation Resources

Before implementing, read:

1. **MCP Python SDK** (30 min):
   - https://github.com/modelcontextprotocol/python-sdk
   - Focus on: Server setup, Tool decorator, Type definitions

2. **OpenAI Function Calling** (20 min):
   - https://platform.openai.com/docs/guides/function-calling
   - Focus on: Tool definition, Handling tool_calls, Response format

3. **Vercel AI SDK** (20 min):
   - https://sdk.vercel.ai/docs
   - Focus on: useChat hook, Streaming, API routes

---

## Next Steps

After completing this quickstart:

1. Run `/sp.tasks` to generate detailed implementation tasks
2. Start with Phase 1 (Database Setup)
3. Test each phase before moving to next
4. Update SESSION_HANDOFF.md after each work session
5. Run phase gate check when all tests pass

---

**Total Estimated Time**: ~5 hours for full implementation

**Dependencies**:
- OpenAI API key (get from platform.openai.com)
- Working Phase II application
- All Phase II tests passing
