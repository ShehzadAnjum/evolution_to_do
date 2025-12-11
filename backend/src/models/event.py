"""Event models for Dapr pub/sub with Kafka.

These events are published when task operations occur and are consumed
by event handlers for notifications, analytics, etc.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of events that can be published."""
    
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    REMINDER_DUE = "reminder.due"
    RECURRING_TRIGGER = "recurring.trigger"


class TaskEventData(BaseModel):
    """Data payload for task events."""
    
    title: Optional[str] = None
    description: Optional[str] = None
    is_complete: Optional[bool] = None
    previous_state: Optional[dict] = None


class TaskEvent(BaseModel):
    """Event model for task-related events.
    
    Published to Kafka via Dapr pub/sub when task operations occur.
    """
    
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    task_id: UUID
    data: TaskEventData = Field(default_factory=TaskEventData)
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }


class ReminderEventData(BaseModel):
    """Data payload for reminder events."""
    
    task_title: str
    due_at: datetime
    reminder_type: str = "push"  # push, email, etc.


class ReminderEvent(BaseModel):
    """Event model for reminder-related events."""
    
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType = EventType.REMINDER_DUE
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    task_id: UUID
    data: ReminderEventData
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }


class RecurringEventData(BaseModel):
    """Data payload for recurring task trigger events."""
    
    recurring_pattern: str  # daily, weekly, monthly
    original_task_id: UUID
    new_task_id: UUID


class RecurringTriggerEvent(BaseModel):
    """Event model for recurring task triggers."""
    
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType = EventType.RECURRING_TRIGGER
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    task_id: UUID
    data: RecurringEventData
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }
