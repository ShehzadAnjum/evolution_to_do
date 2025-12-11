"""Event handler endpoints for Dapr pub/sub subscriptions.

These endpoints receive events published to Kafka via Dapr sidecar.
Dapr automatically routes events based on subscription configuration.
"""

import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


class CloudEvent(BaseModel):
    """CloudEvent format used by Dapr pub/sub."""
    
    id: str
    source: str
    specversion: str = "1.0"
    type: str
    datacontenttype: str = "application/json"
    data: dict


@router.get("/dapr/subscribe")
async def dapr_subscribe():
    """Return Dapr subscription configuration.
    
    Dapr calls this endpoint to discover subscriptions.
    Alternative to declarative subscription YAML files.
    """
    return [
        {
            "pubsubname": "taskevents",
            "topic": "task.created",
            "route": "/events/task-created",
        },
        {
            "pubsubname": "taskevents",
            "topic": "task.updated",
            "route": "/events/task-updated",
        },
        {
            "pubsubname": "taskevents",
            "topic": "task.completed",
            "route": "/events/task-completed",
        },
        {
            "pubsubname": "taskevents",
            "topic": "task.deleted",
            "route": "/events/task-deleted",
        },
        {
            "pubsubname": "taskevents",
            "topic": "reminder.due",
            "route": "/events/reminder-due",
        },
        {
            "pubsubname": "taskevents",
            "topic": "recurring.trigger",
            "route": "/events/recurring-trigger",
        },
    ]


@router.post("/task-created")
async def handle_task_created(request: Request) -> dict:
    """Handle task created events.
    
    Called by Dapr when a task.created event is published.
    Can be used for:
    - Sending notifications
    - Updating analytics
    - Triggering integrations
    """
    body = await request.json()
    logger.info(f"Received task.created event: {body}")
    
    try:
        # Extract event data (CloudEvent format)
        data = body.get("data", body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        task_data = data.get("data", {})
        
        logger.info(
            f"Task created: {task_id} by user {user_id} - '{task_data.get('title')}'"
        )
        
        # TODO: Implement notification logic
        # await send_notification(user_id, f"Task created: {task_data.get('title')}")
        
    except Exception as e:
        logger.error(f"Error processing task.created event: {e}")
        # Don't fail - acknowledge receipt to prevent retry loop
    
    return {"status": "ok"}


@router.post("/task-updated")
async def handle_task_updated(request: Request) -> dict:
    """Handle task updated events."""
    body = await request.json()
    logger.info(f"Received task.updated event: {body}")
    
    try:
        data = body.get("data", body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        
        logger.info(f"Task updated: {task_id} by user {user_id}")
        
    except Exception as e:
        logger.error(f"Error processing task.updated event: {e}")
    
    return {"status": "ok"}


@router.post("/task-completed")
async def handle_task_completed(request: Request) -> dict:
    """Handle task completion toggle events.
    
    Useful for:
    - Gamification (streaks, achievements)
    - Progress tracking
    - Team notifications
    """
    body = await request.json()
    logger.info(f"Received task.completed event: {body}")
    
    try:
        data = body.get("data", body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        task_data = data.get("data", {})
        is_complete = task_data.get("is_complete", True)
        
        status = "completed" if is_complete else "reopened"
        logger.info(f"Task {status}: {task_id} by user {user_id}")
        
        # TODO: Update completion streak, send celebration notification
        
    except Exception as e:
        logger.error(f"Error processing task.completed event: {e}")
    
    return {"status": "ok"}


@router.post("/task-deleted")
async def handle_task_deleted(request: Request) -> dict:
    """Handle task deleted events."""
    body = await request.json()
    logger.info(f"Received task.deleted event: {body}")
    
    try:
        data = body.get("data", body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        
        logger.info(f"Task deleted: {task_id} by user {user_id}")
        
    except Exception as e:
        logger.error(f"Error processing task.deleted event: {e}")
    
    return {"status": "ok"}


@router.post("/reminder-due")
async def handle_reminder_due(request: Request) -> dict:
    """Handle reminder due events.
    
    Called when a task reminder is due. Should trigger:
    - Push notification
    - Email notification (if configured)
    - In-app notification
    """
    body = await request.json()
    logger.info(f"Received reminder.due event: {body}")
    
    try:
        data = body.get("data", body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        reminder_data = data.get("data", {})
        
        logger.info(
            f"Reminder due for task {task_id}, user {user_id}: {reminder_data.get('task_title')}"
        )
        
        # TODO: Send notification via push, email, etc.
        # await notification_service.send_reminder(user_id, task_id, reminder_data)
        
    except Exception as e:
        logger.error(f"Error processing reminder.due event: {e}")
    
    return {"status": "ok"}


@router.post("/recurring-trigger")
async def handle_recurring_trigger(request: Request) -> dict:
    """Handle recurring task trigger events.
    
    Called when a recurring task needs a new instance created.
    The cron binding triggers this to check for due recurring tasks.
    """
    body = await request.json()
    logger.info(f"Received recurring.trigger event: {body}")
    
    try:
        data = body.get("data", body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")
        recurring_data = data.get("data", {})
        
        logger.info(
            f"Recurring task triggered: {task_id} pattern={recurring_data.get('recurring_pattern')}"
        )
        
        # TODO: Create new task instance from template
        
    except Exception as e:
        logger.error(f"Error processing recurring.trigger event: {e}")
    
    return {"status": "ok"}
