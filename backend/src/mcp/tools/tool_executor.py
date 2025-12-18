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
            # v4.0.0: IoT device control tools
            "control_device": self._control_device,
            "schedule_device": self._schedule_device,
            "device_status": self._device_status,
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
            arguments: {title: str, description?: str, priority?: str, category?: str,
                       due_date?: str, recurrence_pattern?: str}

        Returns:
            Created task details
        """
        title = arguments.get("title", "").strip()
        description = arguments.get("description", "").strip()
        priority = arguments.get("priority", "medium").lower()
        category = arguments.get("category", "general").lower()
        due_date_str = arguments.get("due_date")
        recurrence = arguments.get("recurrence_pattern", "none").lower()

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

        # Validate recurrence pattern
        valid_recurrence = ["none", "daily", "weekly", "biweekly", "monthly"]
        if recurrence not in valid_recurrence:
            recurrence = "none"

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
            recurrence_pattern=recurrence,
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
                "recurrence_pattern": task.recurrence_pattern,
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
                    "priority": t.priority,
                    "category": t.category,
                    "due_date": str(t.due_date) if t.due_date else None,
                    "recurrence_pattern": t.recurrence_pattern,
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
                "priority": task.priority,
                "category": task.category,
                "due_date": str(task.due_date) if task.due_date else None,
                "recurrence_pattern": task.recurrence_pattern,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
        }

    async def _update_task(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Update a task's title, description, due date, priority, category, or recurrence.

        Args:
            arguments: {task_id?: str, title?: str, new_title?: str, new_description?: str,
                       new_due_date?: str, new_priority?: str, new_category?: str,
                       new_recurrence_pattern?: str}

        Returns:
            Updated task details
        """
        task_id = arguments.get("task_id")
        title = arguments.get("title", "").strip()
        new_title = arguments.get("new_title")
        new_description = arguments.get("new_description")
        new_due_date = arguments.get("new_due_date")
        new_priority = arguments.get("new_priority")
        new_category = arguments.get("new_category")
        new_recurrence = arguments.get("new_recurrence_pattern")

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

        # Track what changed for message
        changes = []
        old_due_date = str(task.due_date) if task.due_date else None

        # Update fields
        if new_title is not None:
            new_title = new_title.strip()
            if not new_title:
                return {"success": False, "error": "Title cannot be empty"}
            if len(new_title) > 200:
                return {"success": False, "error": "Title must be 200 characters or less"}
            task.title = new_title
            changes.append("title")

        if new_description is not None:
            task.description = new_description.strip()
            changes.append("description")

        if new_due_date is not None:
            try:
                task.due_date = datetime.strptime(new_due_date, "%Y-%m-%d").date()
                changes.append(f"due date ({old_due_date} → {new_due_date})")
            except ValueError:
                return {"success": False, "error": "Invalid date format. Use YYYY-MM-DD"}

        if new_priority is not None:
            if new_priority.lower() in ["high", "medium", "low"]:
                task.priority = new_priority.lower()
                changes.append("priority")
            else:
                return {"success": False, "error": "Priority must be high, medium, or low"}

        if new_category is not None:
            task.category = new_category.lower().strip()
            changes.append("category")

        if new_recurrence is not None:
            valid_recurrence = ["none", "daily", "weekly", "biweekly", "monthly"]
            if new_recurrence.lower() in valid_recurrence:
                task.recurrence_pattern = new_recurrence.lower()
                changes.append("recurrence")
            else:
                return {"success": False, "error": "Recurrence must be none, daily, weekly, biweekly, or monthly"}

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
                "priority": task.priority,
                "category": task.category,
                "due_date": str(task.due_date) if task.due_date else None,
                "recurrence_pattern": task.recurrence_pattern,
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Task '{task.title}' updated: {', '.join(changes)}" if changes else f"Task '{task.title}' unchanged",
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

    # =========================================================================
    # v4.0.0: IoT Device Control Tools
    # =========================================================================

    async def _control_device(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Control an IoT device immediately.

        Args:
            arguments: {relay_number: int, action: str, device_name?: str}

        Returns:
            Command result
        """
        from ...services.mqtt_service import get_mqtt_service, RELAY_NAMES

        relay_number = arguments.get("relay_number", 1)
        action = arguments.get("action", "toggle").lower()
        device_name = arguments.get("device_name", "").lower()

        # Map device names to relay numbers
        name_to_relay = {
            "light": 1, "batii": 1, "rooshni": 1, "bulb": 1,
            "fan": 2, "pankha": 2,
            "aquarium": 3, "fish": 3, "machli": 3, "fish tank": 3,
            "relay4": 4, "relay 4": 4,
        }

        # If device_name provided, try to map it
        if device_name and device_name in name_to_relay:
            relay_number = name_to_relay[device_name]

        # Validate
        if relay_number < 1 or relay_number > 4:
            return {"success": False, "error": "Relay number must be 1-4"}
        if action not in ["on", "off", "toggle"]:
            return {"success": False, "error": "Action must be on, off, or toggle"}

        mqtt = get_mqtt_service()
        if not mqtt.is_connected:
            return {
                "success": False,
                "error": "MQTT not connected. Device control is offline.",
            }

        result = await mqtt.publish_immediate(
            relay_number=relay_number,
            action=action,
        )

        if result["success"]:
            relay_name = RELAY_NAMES.get(relay_number, f"Relay {relay_number}")
            return {
                "success": True,
                "command_id": result.get("command_id"),
                "relay": relay_name,
                "action": action,
                "message": f"Sent {action} command to {relay_name}",
            }
        else:
            return result

    async def _schedule_device(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Schedule a device action for a future time.

        Args:
            arguments: {
                relay_number: int,
                action: str,
                due_date: str (YYYY-MM-DD),
                due_time: str (HH:MM),
                recurrence_pattern?: str,
                weekday?: str
            }

        Returns:
            Schedule confirmation with task_id
        """
        from ...services.mqtt_service import get_mqtt_service, RELAY_NAMES

        relay_number = arguments.get("relay_number", 1)
        action = arguments.get("action", "toggle").lower()
        due_date_str = arguments.get("due_date")
        due_time_str = arguments.get("due_time", "00:00")
        recurrence = arguments.get("recurrence_pattern", "none").lower()
        weekday = arguments.get("weekday")
        device_name = arguments.get("device_name", "").lower()

        # Map device names to relay numbers
        name_to_relay = {
            "light": 1, "batii": 1, "rooshni": 1, "bulb": 1,
            "fan": 2, "pankha": 2,
            "aquarium": 3, "fish": 3, "machli": 3, "fish tank": 3,
            "relay4": 4, "relay 4": 4,
        }

        if device_name and device_name in name_to_relay:
            relay_number = name_to_relay[device_name]

        # Validate
        if relay_number < 1 or relay_number > 4:
            return {"success": False, "error": "Relay number must be 1-4"}
        if action not in ["on", "off", "toggle"]:
            return {"success": False, "error": "Action must be on, off, or toggle"}

        # Parse due_date
        if not due_date_str:
            # Default to today (use local time, not UTC)
            due_date = datetime.now().date()
        else:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                return {"success": False, "error": "Invalid date format. Use YYYY-MM-DD"}

        # Parse due_time
        try:
            time_parts = due_time_str.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        except (ValueError, IndexError):
            return {"success": False, "error": "Invalid time format. Use HH:MM"}

        # Combine date and time
        scheduled_datetime = datetime(
            due_date.year, due_date.month, due_date.day,
            hour, minute, 0
        )

        # Check if in the past (for non-recurring) - use local time for comparison
        if recurrence == "none" and scheduled_datetime <= datetime.now():
            return {"success": False, "error": "Scheduled time must be in the future"}

        relay_name = RELAY_NAMES.get(relay_number, f"Relay {relay_number}")

        # Create a task of type device_schedule
        task = TaskDB(
            title=f"{action.upper()} {relay_name}",
            description=f"Device schedule: {action} {relay_name}",
            user_id=self.user_id,
            task_type="device_schedule",
            device_id="esp32-home",
            relay_number=relay_number,
            device_action=action,
            due_date=due_date,
            due_time=due_time_str,
            recurrence_pattern=recurrence,
            weekday=weekday.lower() if weekday else None,
            category="iot",
            schedule_synced=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        # Try to send to ESP32 via MQTT
        mqtt = get_mqtt_service()
        if mqtt.is_connected:
            scheduled_unix = int(scheduled_datetime.timestamp())
            result = await mqtt.publish_schedule(
                relay_number=relay_number,
                action=action,
                scheduled_time=scheduled_unix,
                device_name=relay_name,
            )
            if result["success"]:
                task.mqtt_command_id = result.get("command_id")
                task.schedule_synced = True
                self.db.add(task)
                self.db.commit()

        # Format time for message
        time_str = scheduled_datetime.strftime("%I:%M %p")
        date_str = scheduled_datetime.strftime("%b %d")

        recurrence_msg = ""
        if recurrence == "daily":
            recurrence_msg = " (daily)"
        elif recurrence == "weekly" and weekday:
            recurrence_msg = f" (every {weekday.capitalize()})"

        return {
            "success": True,
            "task_id": str(task.id),
            "relay": relay_name,
            "action": action,
            "scheduled_time": scheduled_datetime.isoformat(),
            "synced": task.schedule_synced,
            "message": f"Scheduled {relay_name} to {action} at {time_str} on {date_str}{recurrence_msg}",
        }

    async def _device_status(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Get current device status.

        Args:
            arguments: {} (no arguments needed)

        Returns:
            Device status including relay states
        """
        from ...services.mqtt_service import get_mqtt_service

        mqtt = get_mqtt_service()

        # Request fresh status (async)
        status_data = await mqtt.request_status()

        # Build friendly message
        relays = status_data.get("relays", [])
        relay_states = []
        for r in relays:
            relay_states.append(f"{r['name']}: {r['state'].upper()}")

        online_status = "ONLINE" if status_data.get("online") else "OFFLINE"
        wifi_rssi = status_data.get("wifi_rssi")
        signal_str = f" (WiFi: {wifi_rssi}dBm)" if wifi_rssi else ""

        return {
            "success": True,
            "device": {
                "device_id": "esp32-home",
                "name": "Home Controller",
                "status": online_status.lower(),
                "relays": relays,
                "wifi_rssi": wifi_rssi,
                "last_heartbeat": status_data.get("last_heartbeat"),
            },
            "mqtt_connected": mqtt.is_connected,
            "message": f"Device: {online_status}{signal_str}. {', '.join(relay_states)}",
        }
