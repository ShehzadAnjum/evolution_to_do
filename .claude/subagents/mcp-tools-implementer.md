# MCP Tools Implementer Subagent

**Type**: Implementer
**Used For**: Creating MCP tools for AI agent
**Version**: 1.0.0

## Purpose

Implement MCP tools for todo CRUD operations using Official MCP SDK.

## When to Use

Phase III - implementing AI chatbot MCP tools

## Process

1. Read tool spec from specs/api/mcp-tools.md
2. Define tool with MCP decorator
3. Create Pydantic input/output schemas
4. Implement by calling existing API logic (DON'T duplicate)
5. Return structured data (not prose)
6. Handle errors gracefully
7. Write tool tests

## Example

```python
from mcp import Tool
from pydantic import BaseModel

class AddTaskInput(BaseModel):
    user_id: str
    title: str
    description: str | None = None

@Tool
async def add_task(input: AddTaskInput):
    """Add a new task to user's list."""
    # Call existing API function
    task = await create_task_api(
        input.user_id,
        input.title,
        input.description
    )
    return {"id": task.id, "title": task.title}
```

## Best Practices

- One operation per tool
- Structured input/output (Pydantic)
- Call existing logic (no duplication)
- Clear docstrings
- Error handling

---

**Related**: AI MCP Agent
