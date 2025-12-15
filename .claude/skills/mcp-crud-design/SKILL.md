---
name: mcp-crud-design
description: Design and implement MCP (Model Context Protocol) tools for CRUD operations. Use when building AI agent tools, implementing task management via MCP, or creating function-calling interfaces for LLMs.
---

# MCP CRUD Design

## Tool Structure

```python
from mcp.types import Tool, TextContent

TOOLS = [
    Tool(
        name="add_task",
        description="Create a new task with title and optional description",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task details"},
            },
            "required": ["title"],
        },
    ),
    Tool(
        name="list_tasks",
        description="List tasks, optionally filtered by status",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["all", "pending", "complete"]},
            },
        },
    ),
    # ... complete_task, delete_task, update_task
]
```

## Tool Executor Pattern

```python
class ToolExecutor:
    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    async def execute(self, tool_name: str, args: dict) -> dict:
        handlers = {
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "complete_task": self._complete_task,
            "delete_task": self._delete_task,
            "update_task": self._update_task,
        }
        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
        return await handler(**args)
```

## OpenAI Integration

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    tools=[{"type": "function", "function": tool.model_dump()} for tool in TOOLS],
    tool_choice="auto",
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        result = await executor.execute(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
```

## Best Practices

- Return structured results (JSON) for easy parsing
- Include success/error status in responses
- Validate user ownership before operations
- Keep tool descriptions concise but complete
