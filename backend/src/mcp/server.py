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
                "description": "Create a new task for the current user. Infer category from task context if not specified. Detect priority from words like 'important', 'urgent', 'zaroori'. Detect recurrence from words like 'daily', 'every friday', 'har rouz', 'har jumma', 'monthly'.",
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
                            "description": "Task priority. Set to 'high' if user says important/urgent/zaroori/ahem/fori. Defaults to medium.",
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
                        "recurrence_pattern": {
                            "type": "string",
                            "description": "Recurrence pattern. Set based on user intent: 'daily' (har rouz, every day), 'weekly' (har jumma, every friday, har hafta), 'biweekly' (har doosra hafta), 'monthly' (har mahina). Defaults to 'none'.",
                            "enum": ["none", "daily", "weekly", "biweekly", "monthly"],
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
                "description": "Update an existing task's title, description, due date, priority, category, or recurrence pattern",
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
                        "new_due_date": {
                            "type": "string",
                            "description": "New due date in YYYY-MM-DD format",
                        },
                        "new_priority": {
                            "type": "string",
                            "description": "New priority: high, medium, or low",
                            "enum": ["high", "medium", "low"],
                        },
                        "new_category": {
                            "type": "string",
                            "description": "New category for the task",
                        },
                        "new_recurrence_pattern": {
                            "type": "string",
                            "description": "New recurrence pattern: none, daily, weekly, biweekly, or monthly",
                            "enum": ["none", "daily", "weekly", "biweekly", "monthly"],
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
        {
            "type": "function",
            "function": {
                "name": "clear_completed_tasks",
                "description": "Delete all completed tasks to clean up the task list",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        },
        # v4.0.0: IoT Device Control Tools
        {
            "type": "function",
            "function": {
                "name": "control_device",
                "description": "Control an IoT device IMMEDIATELY (right now). ONLY use when NO time is mentioned. Examples: 'turn on light', 'fan off karo'. Do NOT use if user mentions any time like 'at 3am', '6 baje', 'tomorrow', 'daily'. Maps: light/batii=Relay1, fan/pankha=Relay2, aquarium/machli=Relay3.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relay_number": {
                            "type": "integer",
                            "description": "Relay number (1-4). 1=Light, 2=Fan, 3=Aquarium, 4=Relay4",
                        },
                        "action": {
                            "type": "string",
                            "enum": ["on", "off", "toggle"],
                            "description": "Action to perform: on, off, or toggle",
                        },
                        "device_name": {
                            "type": "string",
                            "description": "Device name if provided (light, fan, aquarium, pankha, batii, etc.)",
                        },
                    },
                    "required": ["action"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "schedule_device",
                "description": "Schedule a device action for a FUTURE time. ALWAYS use when ANY time is mentioned: 'at 3am', 'at 6pm', '7 baje', 'tomorrow', 'daily', 'har rouz', 'every friday'. Examples: 'turn on light at 3am' → schedule for 03:00, 'fishes need light at 3am today' → schedule for 03:00 today. Supports one-time, daily, and weekly schedules.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relay_number": {
                            "type": "integer",
                            "description": "Relay number (1-4). 1=Light, 2=Fan, 3=Aquarium, 4=Relay4",
                        },
                        "action": {
                            "type": "string",
                            "enum": ["on", "off", "toggle"],
                            "description": "Action to perform",
                        },
                        "device_name": {
                            "type": "string",
                            "description": "Device name if provided (light, fan, aquarium, pankha, batii, etc.)",
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format. Defaults to today.",
                        },
                        "due_time": {
                            "type": "string",
                            "description": "Time in HH:MM 24-hour format (e.g., '18:00' for 6pm)",
                        },
                        "recurrence_pattern": {
                            "type": "string",
                            "enum": ["none", "daily", "weekly"],
                            "description": "Recurrence: none (one-time), daily (har rouz), weekly (har hafta/har jumma)",
                        },
                        "weekday": {
                            "type": "string",
                            "description": "For weekly recurrence: monday, tuesday, wednesday, thursday, friday, saturday, sunday. Maps: jumma=friday, hafta=week, somwar=monday, mangal=tuesday, budh=wednesday, jumerat=thursday, sanichar=saturday, itwar=sunday",
                        },
                    },
                    "required": ["action", "due_time"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "device_status",
                "description": "Get current status of the IoT device including relay states (on/off), online/offline status, and WiFi signal strength. Use for 'show device status', 'kya light on hai?', 'device ka status dikhao'.",
                "parameters": {
                    "type": "object",
                    "properties": {},
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
