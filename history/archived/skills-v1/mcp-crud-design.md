# Skill: MCP CRUD Tool Design

## Overview

This skill captures patterns for designing Model Context Protocol (MCP) tools for todo item CRUD operations with AI agents.

## Core Concepts

### MCP Tool Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Agent      │────▶│   MCP Server    │────▶│   FastAPI       │
│   (OpenAI)      │     │   (Python SDK)  │     │   Backend       │
│                 │     │                 │     │                 │
│ - Intent parse  │     │ - Tool registry │     │ - CRUD ops      │
│ - Tool calls    │     │ - Auth forward  │     │ - User context  │
│ - Response      │     │ - Validation    │     │ - Database      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Tool Categories

| Category | Tools | Phase |
|----------|-------|-------|
| Create | `add_task` | III |
| Read | `list_tasks`, `get_task` | III |
| Update | `update_task`, `complete_task` | III |
| Delete | `delete_task` | III |
| Batch | `complete_all`, `delete_completed` | V |

## MCP Tool Definitions

### Tool: add_task

```python
from mcp.server import Server, Tool
from mcp.types import TextContent
from pydantic import BaseModel, Field

class AddTaskInput(BaseModel):
    title: str = Field(description="The task title/description")

class TaskOutput(BaseModel):
    id: str
    title: str
    completed: bool
    message: str

@server.tool("add_task")
async def add_task(input: AddTaskInput, context: dict) -> TaskOutput:
    """Add a new task to the todo list.
    
    Use this when the user wants to:
    - Create a new task
    - Add something to their list
    - Remember to do something
    """
    user_id = context.get("user_id")
    
    task = await api_client.create_task(user_id, input.title)
    
    return TaskOutput(
        id=str(task.id),
        title=task.title,
        completed=task.completed,
        message=f"Added task: {task.title}",
    )
```

### Tool: list_tasks

```python
class ListTasksInput(BaseModel):
    filter: str = Field(
        default="all",
        description="Filter: 'all', 'pending', or 'completed'"
    )

class TaskListOutput(BaseModel):
    tasks: list[dict]
    count: int
    message: str

@server.tool("list_tasks")
async def list_tasks(input: ListTasksInput, context: dict) -> TaskListOutput:
    """List tasks from the todo list.
    
    Use this when the user wants to:
    - See their tasks
    - Check what's on their list
    - View pending or completed items
    """
    user_id = context.get("user_id")
    
    tasks = await api_client.get_tasks(user_id, filter=input.filter)
    
    return TaskListOutput(
        tasks=[t.model_dump() for t in tasks],
        count=len(tasks),
        message=f"Found {len(tasks)} tasks",
    )
```

### Tool: complete_task

```python
class CompleteTaskInput(BaseModel):
    task_id: str = Field(description="The ID of the task to complete")
    # OR for natural language
    task_title: str = Field(description="The title/name of the task")

@server.tool("complete_task")
async def complete_task(input: CompleteTaskInput, context: dict) -> TaskOutput:
    """Mark a task as completed.
    
    Use this when the user wants to:
    - Mark something as done
    - Complete a task
    - Check off an item
    """
    user_id = context.get("user_id")
    
    # Find task by title or ID
    if input.task_title:
        task = await api_client.find_task_by_title(
            user_id, input.task_title
        )
    else:
        task = await api_client.get_task(user_id, input.task_id)
    
    if not task:
        return TaskOutput(
            id="",
            title="",
            completed=False,
            message=f"Task not found: {input.task_title or input.task_id}",
        )
    
    updated = await api_client.update_task(
        user_id, task.id, completed=True
    )
    
    return TaskOutput(
        id=str(updated.id),
        title=updated.title,
        completed=True,
        message=f"Completed: {updated.title}",
    )
```

### Tool: delete_task

```python
class DeleteTaskInput(BaseModel):
    task_id: str = Field(description="The ID of the task to delete")
    task_title: str = Field(description="The title of the task to delete")

@server.tool("delete_task")
async def delete_task(input: DeleteTaskInput, context: dict) -> dict:
    """Delete a task from the todo list.
    
    Use this when the user wants to:
    - Remove a task
    - Delete something from their list
    - Get rid of an item
    """
    user_id = context.get("user_id")
    
    success = await api_client.delete_task(user_id, input.task_id)
    
    return {
        "success": success,
        "message": "Task deleted" if success else "Task not found",
    }
```

## MCP Server Setup

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

# Create server
server = Server("evolution-todo-mcp")

# Register tools
server.add_tool(add_task)
server.add_tool(list_tasks)
server.add_tool(complete_task)
server.add_tool(delete_task)

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

## Intent Mapping

| User Intent | Tool | Confidence |
|-------------|------|------------|
| "add buy milk" | add_task | High |
| "show my tasks" | list_tasks | High |
| "what do I need to do" | list_tasks | Medium |
| "mark buy milk done" | complete_task | High |
| "I finished..." | complete_task | Medium |
| "remove buy milk" | delete_task | High |
| "clear completed" | delete_completed | High |

## Error Handling

```python
from mcp.types import ErrorData

@server.tool("add_task")
async def add_task(input: AddTaskInput, context: dict):
    try:
        # ... implementation
    except AuthenticationError:
        return ErrorData(
            code="AUTH_ERROR",
            message="Please log in to manage tasks",
        )
    except ValidationError as e:
        return ErrorData(
            code="VALIDATION_ERROR",
            message=str(e),
        )
    except Exception as e:
        return ErrorData(
            code="INTERNAL_ERROR",
            message="Something went wrong",
        )
```

## Anti-Patterns

### ❌ Missing User Context

```python
# DANGEROUS: No user isolation
async def list_tasks():
    return await api_client.get_all_tasks()
```

### ✅ Always Pass User Context

```python
async def list_tasks(context: dict):
    user_id = context.get("user_id")
    return await api_client.get_tasks(user_id)
```

### ❌ Vague Tool Descriptions

```python
@server.tool("task")
async def task(input: dict):
    """Do something with tasks."""
```

### ✅ Clear Tool Descriptions

```python
@server.tool("add_task")
async def add_task(input: AddTaskInput):
    """Add a new task to the todo list.
    
    Use this when the user wants to:
    - Create a new task
    - Add something to their list
    """
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: III, IV, V
**Last Updated**: 2025-12-10
