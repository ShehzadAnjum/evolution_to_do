"""Tool executor for Phase III AI Chatbot.

This module provides the ToolExecutor class that executes MCP tools
by delegating to the task database operations.
"""

import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlmodel import Session, select

from src.models.task import TaskDB, TaskCreate

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Executes MCP tools by interfacing with the task database."""

    def __init__(self, db: Session, user_id: str):
        """Initialize the tool executor.

        Args:
            db: Database session
            user_id: ID of the authenticated user
        """
        self.db = db
        self.user_id = user_id

    async def execute_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool by name with given arguments.

        Args:
            name: Tool name (e.g., "add_task", "list_tasks")
            arguments: Tool arguments

        Returns:
            Tool execution result as a dict
        """
        tool_handlers = {
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "get_task": self._get_task,
            "update_task": self._update_task,
            "delete_task": self._delete_task,
            "complete_task": self._complete_task,
            "search_tasks": self._search_tasks,
            "clear_completed_tasks": self._clear_completed_tasks,
        }

        handler = tool_handlers.get(name)
        if not handler:
            return {
                "success": False,
                "error": f"Unknown tool: {name}",
            }

        try:
            return await handler(arguments)
        except Exception as e:
            logger.error(f"Tool execution error for {name}: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def _add_task(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Create a new task.

        Args:
            arguments: {title: str, description?: str, priority?: str, category?: str, due_date?: str}

        Returns:
            Created task details
        """
        title = arguments.get("title", "").strip()
        description = arguments.get("description", "").strip()
        priority = arguments.get("priority", "medium").lower()
        category = arguments.get("category", "general").lower()
        due_date_str = arguments.get("due_date")

        if not title:
            return {"success": False, "error": "Title is required"}

        if len(title) > 200:
            return {"success": False, "error": "Title must be 200 characters or less"}

        # Validate priority
        if priority not in ["high", "medium", "low"]:
            priority = "medium"

        # Validate category (default categories)
        valid_categories = ["work", "personal", "study", "shopping", "general"]
        if category not in valid_categories:
            # Allow custom categories, just use as-is
            pass

        # Parse due_date or default to today
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                # If invalid format, default to today
                due_date = datetime.utcnow().date()
        else:
            # Default to today
            due_date = datetime.utcnow().date()

        task = TaskDB(
            title=title,
            description=description,
            is_complete=False,
            user_id=self.user_id,
            priority=priority,
            category=category,
            due_date=due_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                "priority": task.priority,
                "category": task.category,
                "due_date": str(task.due_date) if task.due_date else None,
                "created_at": task.created_at.isoformat(),
            },
            "message": f"Task '{title}' created successfully",
        }

    async def _list_tasks(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """List all tasks for the user.

        Args:
            arguments: {status?: "all" | "complete" | "incomplete"}

        Returns:
            List of tasks with statistics
        """
        status_filter = arguments.get("status", "all")

        statement = (
            select(TaskDB)
            .where(TaskDB.user_id == self.user_id)
            .order_by(TaskDB.created_at.desc())
        )

        tasks = self.db.exec(statement).all()

        # Apply status filter
        if status_filter == "complete":
            tasks = [t for t in tasks if t.is_complete]
        elif status_filter == "incomplete":
            tasks = [t for t in tasks if not t.is_complete]

        total = len(tasks)

        return {
            "success": True,
            "tasks": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "description": t.description,
                    "is_complete": t.is_complete,
                    "created_at": t.created_at.isoformat(),
                }
                for t in tasks
            ],
            "total": total,
            "message": f"Found {total} task(s)",
        }

    async def _get_task(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Get a specific task by ID or title.

        Args:
            arguments: {task_id?: str, title?: str}

        Returns:
            Task details
        """
        task_id = arguments.get("task_id")
        title = arguments.get("title", "").strip()

        task = None

        if task_id:
            try:
                uuid_id = UUID(task_id)
                statement = select(TaskDB).where(
                    TaskDB.id == uuid_id,
                    TaskDB.user_id == self.user_id,
                )
                task = self.db.exec(statement).first()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        elif title:
            # Search by title (case-insensitive partial match)
            statement = select(TaskDB).where(TaskDB.user_id == self.user_id)
            all_tasks = self.db.exec(statement).all()
            for t in all_tasks:
                if title.lower() in t.title.lower():
                    task = t
                    break

        if not task:
            return {"success": False, "error": "Task not found"}

        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
        }

    async def _update_task(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Update a task's title or description.

        Args:
            arguments: {task_id?: str, title?: str, new_title?: str, new_description?: str}

        Returns:
            Updated task details
        """
        task_id = arguments.get("task_id")
        title = arguments.get("title", "").strip()
        new_title = arguments.get("new_title")
        new_description = arguments.get("new_description")

        # Find the task
        task = None
        if task_id:
            try:
                uuid_id = UUID(task_id)
                statement = select(TaskDB).where(
                    TaskDB.id == uuid_id,
                    TaskDB.user_id == self.user_id,
                )
                task = self.db.exec(statement).first()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        elif title:
            statement = select(TaskDB).where(TaskDB.user_id == self.user_id)
            all_tasks = self.db.exec(statement).all()
            for t in all_tasks:
                if title.lower() in t.title.lower():
                    task = t
                    break

        if not task:
            return {"success": False, "error": "Task not found"}

        # Update fields
        if new_title is not None:
            new_title = new_title.strip()
            if not new_title:
                return {"success": False, "error": "Title cannot be empty"}
            if len(new_title) > 200:
                return {"success": False, "error": "Title must be 200 characters or less"}
            task.title = new_title

        if new_description is not None:
            task.description = new_description.strip()

        task.updated_at = datetime.utcnow()
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Task '{task.title}' updated successfully",
        }

    async def _delete_task(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Delete a task.

        Args:
            arguments: {task_id?: str, title?: str}

        Returns:
            Deletion confirmation
        """
        task_id = arguments.get("task_id")
        title = arguments.get("title", "").strip()

        task = None
        if task_id:
            try:
                uuid_id = UUID(task_id)
                statement = select(TaskDB).where(
                    TaskDB.id == uuid_id,
                    TaskDB.user_id == self.user_id,
                )
                task = self.db.exec(statement).first()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        elif title:
            statement = select(TaskDB).where(TaskDB.user_id == self.user_id)
            all_tasks = self.db.exec(statement).all()
            for t in all_tasks:
                if title.lower() in t.title.lower():
                    task = t
                    break

        if not task:
            return {"success": False, "error": "Task not found"}

        task_title = task.title
        self.db.delete(task)
        self.db.commit()

        return {
            "success": True,
            "message": f"Task '{task_title}' deleted successfully",
        }

    async def _complete_task(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Mark a task as complete or toggle its status.

        Args:
            arguments: {task_id?: str, title?: str, is_complete?: bool}

        Returns:
            Updated task details
        """
        task_id = arguments.get("task_id")
        title = arguments.get("title", "").strip()
        is_complete = arguments.get("is_complete")

        task = None
        if task_id:
            try:
                uuid_id = UUID(task_id)
                statement = select(TaskDB).where(
                    TaskDB.id == uuid_id,
                    TaskDB.user_id == self.user_id,
                )
                task = self.db.exec(statement).first()
            except ValueError:
                return {"success": False, "error": "Invalid task ID format"}
        elif title:
            statement = select(TaskDB).where(TaskDB.user_id == self.user_id)
            all_tasks = self.db.exec(statement).all()
            for t in all_tasks:
                if title.lower() in t.title.lower():
                    task = t
                    break

        if not task:
            return {"success": False, "error": "Task not found"}

        # Set completion status (toggle if not specified)
        if is_complete is not None:
            task.is_complete = is_complete
        else:
            task.is_complete = not task.is_complete

        task.updated_at = datetime.utcnow()
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        status = "complete" if task.is_complete else "incomplete"
        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "is_complete": task.is_complete,
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Task '{task.title}' marked as {status}",
        }

    async def _search_tasks(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Search tasks by keyword.

        Args:
            arguments: {query: str}

        Returns:
            Matching tasks
        """
        query = arguments.get("query", "").strip().lower()

        if not query:
            return {"success": False, "error": "Search query is required"}

        statement = select(TaskDB).where(TaskDB.user_id == self.user_id)
        all_tasks = self.db.exec(statement).all()

        # Filter tasks by keyword match in title or description
        matching_tasks = [
            t
            for t in all_tasks
            if query in t.title.lower() or query in (t.description or "").lower()
        ]

        return {
            "success": True,
            "tasks": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "description": t.description,
                    "is_complete": t.is_complete,
                    "created_at": t.created_at.isoformat(),
                }
                for t in matching_tasks
            ],
            "total": len(matching_tasks),
            "message": f"Found {len(matching_tasks)} task(s) matching '{query}'",
        }

    async def _clear_completed_tasks(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Delete all completed tasks.

        Args:
            arguments: {} (no arguments needed)

        Returns:
            Deletion confirmation with count
        """
        statement = select(TaskDB).where(
            TaskDB.user_id == self.user_id,
            TaskDB.is_complete == True,
        )
        completed_tasks = self.db.exec(statement).all()

        if not completed_tasks:
            return {
                "success": True,
                "deleted_count": 0,
                "message": "No completed tasks to clear",
            }

        count = len(completed_tasks)
        for task in completed_tasks:
            self.db.delete(task)
        self.db.commit()

        return {
            "success": True,
            "deleted_count": count,
            "message": f"Cleared {count} completed task(s)",
        }
