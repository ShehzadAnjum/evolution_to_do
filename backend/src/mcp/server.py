"""MCP Server setup for Phase III AI Chatbot.

This module sets up the MCP server with tool definitions for task management.
Tools delegate to the existing TaskService for actual operations.
"""

from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool

# MCP Server instance
server = Server("todo-mcp-server")


def get_tool_definitions() -> list[dict[str, Any]]:
    """Return OpenAI-compatible tool definitions for the AI agent.

    These are used by the ChatService to tell OpenAI what tools are available.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the current user. Infer category from task context if not specified.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task (required)",
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional detailed description of the task",
                        },
                        "priority": {
                            "type": "string",
                            "description": "Task priority: high, medium, or low. Defaults to medium if not specified.",
                            "enum": ["high", "medium", "low"],
                        },
                        "category": {
                            "type": "string",
                            "description": "Task category. Infer from context: work (job/office tasks), personal (home/family), study (learning/education), shopping (buying items), or general (default).",
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Due date in YYYY-MM-DD format. Defaults to today if not specified.",
                        },
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List all tasks for the current user, optionally filtered by completion status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by task status: all, complete, or incomplete",
                            "enum": ["all", "complete", "incomplete"],
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of tasks to return (1-100)",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_task",
                "description": "Get details of a specific task by ID or title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The UUID of the task",
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task (case-insensitive search)",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task's title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The UUID of the task to update",
                        },
                        "title": {
                            "type": "string",
                            "description": "Identify task by title (if task_id not provided)",
                        },
                        "new_title": {
                            "type": "string",
                            "description": "New title for the task",
                        },
                        "new_description": {
                            "type": "string",
                            "description": "New description for the task",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task permanently",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The UUID of the task to delete",
                        },
                        "title": {
                            "type": "string",
                            "description": "Identify task by title (if task_id not provided)",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete (or toggle completion status)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The UUID of the task to complete",
                        },
                        "title": {
                            "type": "string",
                            "description": "Identify task by title (if task_id not provided)",
                        },
                        "toggle": {
                            "type": "boolean",
                            "description": "If true, toggle the status; if false, set to complete",
                        },
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_tasks",
                "description": "Search tasks by keyword in title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (searches in title and description)",
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter results by status: all, complete, or incomplete",
                            "enum": ["all", "complete", "incomplete"],
                        },
                    },
                    "required": ["query"],
                },
            },
        },
    ]


# MCP Server tool handlers (for future MCP client connections)
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Create a new task for the current user",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for the current user",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "complete", "incomplete"]},
                    "limit": {"type": "integer"},
                },
            },
        ),
        Tool(
            name="get_task",
            description="Get details of a specific task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "title": {"type": "string"},
                },
            },
        ),
        Tool(
            name="update_task",
            description="Update an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "title": {"type": "string"},
                    "new_title": {"type": "string"},
                    "new_description": {"type": "string"},
                },
            },
        ),
        Tool(
            name="delete_task",
            description="Delete a task permanently",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "title": {"type": "string"},
                },
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "title": {"type": "string"},
                    "toggle": {"type": "boolean"},
                },
            },
        ),
        Tool(
            name="search_tasks",
            description="Search tasks by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "complete", "incomplete"]},
                },
                "required": ["query"],
            },
        ),
    ]
