"""Task model for the todo application.

This module defines Task models for both Phase I (dataclass) and Phase II (SQLModel).

Version History:
- v1.0.0: Basic task (title, description, is_complete)
- v2.0.0: Added priority, category, due_date for 2nd iteration
- v3.0.0: Added due_time for time picker support
- v3.1.0: Added recurrence_pattern for recurring tasks
- v4.0.0: Added device scheduling fields (task_type, device_id, relay_number, device_action, weekday)
"""

from dataclasses import dataclass
from datetime import datetime, date, UTC
from typing import Optional, Literal
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field, SQLModel

# Validation constants (from spec clarifications)
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
MAX_CATEGORY_LENGTH = 50


# =============================================================================
# Enums for constrained fields
# =============================================================================


class Priority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DefaultCategory(str, Enum):
    """Default task categories."""
    GENERAL = "general"
    WORK = "work"
    PERSONAL = "personal"
    STUDY = "study"
    SHOPPING = "shopping"
    IOT = "iot"  # v4.0.0: For device schedules


class TaskType(str, Enum):
    """Task types - v4.0.0."""
    REGULAR = "regular"
    DEVICE_SCHEDULE = "device_schedule"


class DeviceAction(str, Enum):
    """Device actions for IoT schedules - v4.0.0."""
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"


class Weekday(str, Enum):
    """Weekdays for weekly recurring schedules - v4.0.0."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


# =============================================================================
# Phase I: Dataclass model (for CLI, backward compatibility)
# =============================================================================


@dataclass
class Task:
    """Phase I Task model - simple dataclass for CLI application.

    Attributes:
        id: Unique identifier assigned by system (sequential, starting from 1)
        title: User-provided task title (required, non-empty, max 200 chars)
        description: Optional task description (max 1000 chars)
        completed: Completion status (default: False)
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = self.title.strip()[:MAX_TITLE_LENGTH]
        if self.description:
            self.description = self.description.strip()[:MAX_DESCRIPTION_LENGTH]


# =============================================================================
# Phase II: SQLModel models (for web application)
# =============================================================================


class RecurrencePattern(str, Enum):
    """Recurring task patterns."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class TaskBase(SQLModel):
    """Base task fields shared by all task schemas.

    v2.0.0: Added priority, category, due_date (all optional with defaults)
    v3.0.0: Added due_time for time picker support
    v3.1.0: Added recurrence_pattern for recurring tasks
    v4.0.0: Added device scheduling fields (task_type, device_id, relay_number, device_action, weekday)
    """

    title: str = Field(min_length=1, max_length=MAX_TITLE_LENGTH)
    description: str = Field(default="", max_length=MAX_DESCRIPTION_LENGTH)
    is_complete: bool = Field(default=False)

    # v2.0.0: New optional fields with sensible defaults
    priority: str = Field(
        default="medium",
        description="Task priority: high, medium, low"
    )
    category: str = Field(
        default="general",
        max_length=MAX_CATEGORY_LENGTH,
        description="Task category (default or custom)"
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date for the task"
    )
    # v3.0.0: Time picker support
    due_time: Optional[str] = Field(
        default=None,
        max_length=5,
        description="Optional due time in HH:MM format (e.g., '14:30')"
    )
    # v3.1.0: Recurring tasks
    recurrence_pattern: str = Field(
        default="none",
        description="Recurrence: none, daily, weekly, biweekly, monthly"
    )

    # v4.0.0: Device scheduling fields
    task_type: str = Field(
        default="regular",
        description="Task type: regular or device_schedule"
    )
    device_id: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Target device ID (e.g., 'esp32-home')"
    )
    relay_number: Optional[int] = Field(
        default=None,
        ge=1,
        le=4,
        description="Relay number (1-4) for device control"
    )
    device_action: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Device action: on, off, toggle"
    )
    weekday: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Weekday for weekly recurrence (monday, tuesday, etc.)"
    )
    mqtt_command_id: Optional[str] = Field(
        default=None,
        max_length=40,
        description="MQTT command ID for tracking"
    )
    schedule_synced: bool = Field(
        default=False,
        description="Has the device received this schedule?"
    )


class TaskDB(TaskBase, table=True):
    """Database model for tasks (SQLModel table).

    v2.0.0: Added priority, category, due_date columns (nullable/defaults for backward compat)
    """

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # Note: Foreign key constraint exists at database level
    # We don't define it here to avoid SQLModel metadata resolution issues
    # The user table is managed by Better Auth (uses TEXT for user.id)
    user_id: str = Field(index=True, description="Owner user ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # v2.0.0: Indexes for filtering
    # Note: SQLModel will add these columns, but for existing DBs we need migration


class TaskCreate(SQLModel):
    """Schema for creating a task (request body).

    v2.0.0: Added optional priority, category, due_date
    v3.0.0: Added due_time for time picker support
    v3.1.0: Added recurrence_pattern for recurring tasks
    v4.0.0: Added device scheduling fields
    """

    title: str = Field(min_length=1, max_length=MAX_TITLE_LENGTH)
    description: str = Field(default="", max_length=MAX_DESCRIPTION_LENGTH)

    # v2.0.0: New optional fields
    priority: str = Field(default="medium", description="high, medium, low")
    category: str = Field(default="general", max_length=MAX_CATEGORY_LENGTH)
    due_date: Optional[date] = Field(default=None)
    # v3.0.0: Time picker
    due_time: Optional[str] = Field(default=None, max_length=5, description="HH:MM format")
    # v3.1.0: Recurring tasks
    recurrence_pattern: str = Field(default="none", description="none, daily, weekly, biweekly, monthly")

    # v4.0.0: Device scheduling fields
    task_type: str = Field(default="regular", description="regular or device_schedule")
    device_id: Optional[str] = Field(default=None, max_length=50)
    relay_number: Optional[int] = Field(default=None, ge=1, le=4)
    device_action: Optional[str] = Field(default=None, max_length=10, description="on, off, toggle")
    weekday: Optional[str] = Field(default=None, max_length=10, description="monday, tuesday, etc.")


class TaskUpdate(SQLModel):
    """Schema for updating a task (partial update).

    v2.0.0: Added optional priority, category, due_date
    v3.0.0: Added due_time for time picker support
    v3.1.0: Added recurrence_pattern for recurring tasks
    v4.0.0: Added device scheduling fields
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=MAX_TITLE_LENGTH)
    description: Optional[str] = Field(default=None, max_length=MAX_DESCRIPTION_LENGTH)
    is_complete: Optional[bool] = None

    # v2.0.0: New optional fields
    priority: Optional[str] = Field(default=None, description="high, medium, low")
    category: Optional[str] = Field(default=None, max_length=MAX_CATEGORY_LENGTH)
    due_date: Optional[date] = Field(default=None)
    # v3.0.0: Time picker
    due_time: Optional[str] = Field(default=None, max_length=5, description="HH:MM format")
    # v3.1.0: Recurring tasks
    recurrence_pattern: Optional[str] = Field(default=None, description="none, daily, weekly, biweekly, monthly")

    # v4.0.0: Device scheduling fields
    task_type: Optional[str] = Field(default=None, description="regular or device_schedule")
    device_id: Optional[str] = Field(default=None, max_length=50)
    relay_number: Optional[int] = Field(default=None, ge=1, le=4)
    device_action: Optional[str] = Field(default=None, max_length=10, description="on, off, toggle")
    weekday: Optional[str] = Field(default=None, max_length=10)
    mqtt_command_id: Optional[str] = Field(default=None, max_length=40)
    schedule_synced: Optional[bool] = Field(default=None)


class TaskRead(TaskBase):
    """Schema for reading a task (response body).

    v2.0.0: Includes priority, category, due_date
    """

    id: UUID
    user_id: str  # Better Auth uses TEXT for user.id
    created_at: datetime
    updated_at: datetime
