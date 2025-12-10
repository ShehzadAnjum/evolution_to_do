# Research: Phase III AI Chatbot with MCP Tools

**Feature**: `001-ai-chatbot-mcp`
**Date**: 2025-12-10
**Status**: Complete

## Overview

This document captures technology decisions and research findings for implementing the Phase III AI Chatbot feature.

---

## Decision 1: MCP Implementation Approach

### Decision

Use the **Official MCP Python SDK** (`mcp`) to implement MCP tools as function handlers that call existing TaskService methods.

### Rationale

1. **Official SDK**: The official MCP Python SDK is maintained by Anthropic and provides the standard implementation
2. **Integration Pattern**: MCP tools act as a thin layer that translates AI tool calls into TaskService method calls
3. **No Business Logic Duplication**: Tools delegate to existing backend services, maintaining single source of truth

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| Custom MCP implementation | Reinventing the wheel, more maintenance burden |
| Direct OpenAI function calling without MCP | Doesn't align with hackathon requirements, loses MCP benefits |
| GraphQL with tool annotations | Over-engineered for this use case |

### Implementation Notes

```python
# Example tool implementation pattern
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("todo-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_task",
            description="Add a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"}
                },
                "required": ["title"]
            }
        ),
        # ... other tools
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add_task":
        # Delegate to existing TaskService
        task = await task_service.create_task(
            user_id=current_user_id,
            title=arguments["title"],
            description=arguments.get("description", "")
        )
        return [TextContent(type="text", text=f"Created task: {task.title}")]
```

---

## Decision 2: AI Agent Framework

### Decision

Use **OpenAI Python SDK** with function calling (tools) for the AI agent, NOT the OpenAI Agents SDK.

### Rationale

1. **Simplicity**: OpenAI's standard chat completions API with tools is simpler than the full Agents SDK
2. **Control**: We control the tool execution loop, making it easier to integrate with MCP
3. **Hackathon Scope**: Full Agents SDK is overkill for single-turn tool calls
4. **Flexibility**: Can easily switch to Claude API if needed (similar tool calling pattern)

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| OpenAI Agents SDK | More complex, designed for multi-step autonomous agents |
| LangChain | Heavy dependency, abstracts too much for learning purposes |
| Claude API | Similar capability, but OpenAI was specified in hackathon brief |
| Custom agent loop | Reinventing the wheel |

### Implementation Notes

```python
from openai import OpenAI

client = OpenAI()

# Define tools from MCP tool list
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    }
    # ... other tools
]

# Chat completion with tool use
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        # Execute via MCP server
        result = await mcp_server.call_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
        # Continue conversation with result
```

---

## Decision 3: Frontend Chat UI

### Decision

Use **Vercel AI SDK** (`ai` package) for the chat interface, with custom React components styled using Tailwind CSS and shadcn/ui.

### Rationale

1. **Next.js Native**: Vercel AI SDK integrates seamlessly with Next.js App Router
2. **Streaming Support**: Built-in streaming for better UX
3. **Type Safety**: Full TypeScript support
4. **Minimal Dependencies**: Lighter than ChatKit, easier to customize
5. **Existing Stack**: Works with our existing Tailwind + shadcn/ui setup

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| ChatKit (OpenAI) | Heavier, more opinionated, harder to customize |
| Custom from scratch | More time, reinventing common patterns |
| Stream.io Chat SDK | Overkill, designed for multi-user chat |

### Implementation Notes

```typescript
// Frontend: app/chat/page.tsx
'use client';

import { useChat } from 'ai/react';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((m) => (
          <div key={m.id} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            {m.content}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type a message..."
          className="w-full p-2 border rounded"
        />
      </form>
    </div>
  );
}
```

---

## Decision 4: Conversation Persistence

### Decision

Store conversations and messages in **Neon PostgreSQL** using SQLModel, with a simple conversation → messages relationship.

### Rationale

1. **Existing Infrastructure**: Neon PostgreSQL already set up from Phase II
2. **SQLModel**: Consistent with existing Task model patterns
3. **Simple Schema**: Conversation has many messages, each message has role + content
4. **Stateless Backend**: Server restarts don't lose conversation state

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| In-memory storage | Lost on restart, doesn't scale |
| Redis | Another dependency, overkill for this use case |
| Separate chat database | Unnecessary complexity |
| File-based storage | Not suitable for production |

### Implementation Notes

```python
# Models
class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str  # "user", "assistant", "tool"
    content: str
    tool_calls: Optional[str] = None  # JSON string if role is "assistant"
    tool_call_id: Optional[str] = None  # If role is "tool"
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Decision 5: Authentication Flow

### Decision

Reuse **existing Better Auth JWT** authentication - chat endpoint validates JWT same as task endpoints.

### Rationale

1. **Already Working**: JWT validation middleware exists from Phase II
2. **User Isolation**: user_id extracted from JWT ensures users only access their own data
3. **Consistent**: Same auth pattern as task API endpoints
4. **No New Dependencies**: No additional auth complexity

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| Separate chat auth | Unnecessary complexity, inconsistent |
| API key auth | Different pattern, harder to manage |
| No auth (public chat) | Security risk, no user isolation |

### Implementation Notes

```python
# Chat endpoint with existing auth
@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)  # Existing dependency
):
    # user_id from JWT
    user_id = current_user.id

    # Load/create conversation for this user
    conversation = await get_or_create_conversation(user_id)

    # Process chat...
```

---

## Decision 6: Error Handling Strategy

### Decision

Wrap tool execution errors and return user-friendly messages via AI response, log detailed errors server-side.

### Rationale

1. **User Experience**: Users see helpful messages, not stack traces
2. **Debugging**: Full errors logged for developers
3. **Graceful Degradation**: AI can acknowledge failures and suggest alternatives

### Implementation Notes

```python
async def execute_tool_safely(tool_name: str, arguments: dict) -> str:
    try:
        result = await mcp_server.call_tool(tool_name, arguments)
        return result
    except TaskNotFoundError as e:
        logger.warning(f"Task not found: {e}")
        return f"I couldn't find that task. Can you check the task name?"
    except PermissionError as e:
        logger.warning(f"Permission denied: {e}")
        return "You don't have permission to access that task."
    except Exception as e:
        logger.error(f"Tool execution failed: {e}", exc_info=True)
        return "Something went wrong. Please try again."
```

---

## Summary of Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| MCP Server | Official MCP Python SDK | latest |
| AI Agent | OpenAI Python SDK | ^1.0 |
| Chat UI | Vercel AI SDK | ^3.0 |
| Database | Neon PostgreSQL + SQLModel | existing |
| Auth | Better Auth JWT | existing |
| Frontend | Next.js + React | 14+ |
| Styling | Tailwind CSS + shadcn/ui | existing |

---

## Required Documentation Reading (30-min rule)

Before implementation, complete these readings:

- [ ] MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk (30 min)
- [ ] OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling (20 min)
- [ ] Vercel AI SDK: https://sdk.vercel.ai/docs (20 min)

**Total**: ~70 minutes of documentation reading before implementation.

---

## Second Iteration Enhancements (Post-Phase V)

> **Note**: This section documents advanced features deferred to the second iteration.
> After completing all 5 phases (first iteration), we will revisit each phase with production-grade enhancements.

### Phase III Advanced Features (Second Iteration)

| Component | First Iteration (Current) | Second Iteration (Future) |
|-----------|---------------------------|---------------------------|
| **AI Agent** | OpenAI Python SDK with simple function calling | OpenAI Agents SDK with multi-step planning, reasoning chains |
| **MCP Tools** | 7 basic CRUD tools | Tool chaining, context-aware tools, batch operations |
| **Chat UI** | Basic Vercel AI SDK | ChatKit with rich components, typing indicators, file uploads |
| **Conversation** | Simple message history | Smart context management, conversation summarization |
| **Features** | Core task management | Smart suggestions, natural language scheduling, batch task creation |
| **Error Handling** | Basic error messages | Graceful recovery, retry logic, fallback strategies |

### Why Defer Advanced Features?

1. **Hackathon Focus**: First iteration meets hackathon requirements and earns points
2. **Foundation First**: Simple implementation provides stable base for enhancements
3. **Learning Curve**: Understand basics before adding complexity
4. **Time Constraints**: Ship working features, iterate later

### Technologies Reserved for Second Iteration

- **OpenAI Agents SDK**: For autonomous multi-step task planning
- **LangChain/LangGraph**: For complex agent workflows (if needed)
- **Vector Embeddings**: For semantic task search
- **Streaming with Tool Results**: Real-time tool execution feedback
- **Conversation Memory**: Long-term context across sessions

### Trigger for Second Iteration

Begin second iteration after:
- [ ] Phase V complete and deployed
- [ ] All hackathon requirements met
- [ ] Points submitted
- [ ] Stable production baseline established

---

## References

- [MCP Python SDK Repository](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) *(Second Iteration)*
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
