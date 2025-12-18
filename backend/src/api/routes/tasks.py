"""Task CRUD endpoints."""

import logging
from datetime import datetime, UTC, timedelta, date, time
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select

from ..deps import get_session, get_current_user_id
from ...models.task import TaskDB, TaskCreate, TaskRead, TaskUpdate
from ...services.event_service import get_event_service
from ...services.mqtt_service import get_mqtt_service, RELAY_NAMES

logger = logging.getLogger(__name__)


def calculate_next_due_date(current_date: date, pattern: str) -> date:
    """Calculate the next due date based on recurrence pattern."""
    if pattern == "daily":
        return current_date + timedelta(days=1)
    elif pattern == "weekly":
        return current_date + timedelta(weeks=1)
    elif pattern == "biweekly":
        return current_date + timedelta(weeks=2)
    elif pattern == "monthly":
        # Add one month (handle month overflow)
        year = current_date.year
        month = current_date.month + 1
        if month > 12:
            month = 1
            year += 1
        # Handle day overflow (e.g., Jan 31 -> Feb 28)
        day = min(current_date.day, 28)  # Safe default
        return date(year, month, day)
    return current_date


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=dict)
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
    # Search & Filter parameters
    search: str | None = None,
    category: str | None = None,
    priority: str | None = None,
    status: str | None = None,  # "all", "complete", "incomplete"
    # Sort parameters
    sort_by: str = "created_at",  # "created_at", "due_date", "priority", "title"
    sort_order: str = "desc",  # "asc", "desc"
):
    """List all tasks for the authenticated user with search, filter, and sort.

    Query Parameters:
    - search: Search text in title and description
    - category: Filter by category (e.g., "work", "personal")
    - priority: Filter by priority ("high", "medium", "low")
    - status: Filter by completion ("all", "complete", "incomplete")
    - sort_by: Sort field ("created_at", "due_date", "priority", "title")
    - sort_order: Sort direction ("asc", "desc")

    Returns tasks with summary statistics.
    """
    # Base query for user's tasks
    statement = select(TaskDB).where(TaskDB.user_id == user_id)

    # Apply search filter (case-insensitive search in title and description)
    if search:
        search_term = f"%{search.lower()}%"
        statement = statement.where(
            (TaskDB.title.ilike(search_term)) | (TaskDB.description.ilike(search_term))
        )

    # Apply category filter
    if category:
        statement = statement.where(TaskDB.category == category.lower())

    # Apply priority filter
    if priority:
        statement = statement.where(TaskDB.priority == priority.lower())

    # Apply status filter
    if status == "complete":
        statement = statement.where(TaskDB.is_complete == True)
    elif status == "incomplete":
        statement = statement.where(TaskDB.is_complete == False)
    # "all" or None = no filter

    # Apply sorting
    sort_column = {
        "created_at": TaskDB.created_at,
        "due_date": TaskDB.due_date,
        "priority": TaskDB.priority,
        "title": TaskDB.title,
        "updated_at": TaskDB.updated_at,
    }.get(sort_by, TaskDB.created_at)

    if sort_order == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    tasks = session.exec(statement).all()

    # Calculate statistics (from all user's tasks, not filtered)
    all_tasks_statement = select(TaskDB).where(TaskDB.user_id == user_id)
    all_tasks = session.exec(all_tasks_statement).all()
    total = len(all_tasks)
    completed = sum(1 for task in all_tasks if task.is_complete)

    return {
        "tasks": [TaskRead.model_validate(task) for task in tasks],
        "total": total,
        "completed": completed,
        "filtered_count": len(tasks),  # Count of filtered results
    }


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Create a new task for the authenticated user.

    Validates:
    - Title is required and 1-200 characters
    - Description is optional, max 2000 characters
    """
    # Validation is handled by Pydantic in TaskCreate model
    # Additional validation if needed
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty",
        )

    if len(task_data.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be 200 characters or less",
        )

    # Generate MQTT command ID for device schedules
    mqtt_command_id = str(uuid4()) if task_data.task_type == "device_schedule" else None

    # Create task with v2.0.0, v3.0.0, v3.1.0, v4.0.0 fields
    task = TaskDB(
        title=task_data.title.strip(),
        description=task_data.description or "",
        is_complete=False,
        user_id=user_id,
        # v2.0.0: New optional fields with defaults
        priority=task_data.priority or "medium",
        category=task_data.category or "general",
        due_date=task_data.due_date,
        # v3.0.0: Time picker support
        due_time=task_data.due_time,
        # v3.1.0: Recurring tasks
        recurrence_pattern=task_data.recurrence_pattern or "none",
        weekday=task_data.weekday,
        # v4.0.0: Device scheduling fields
        task_type=task_data.task_type or "regular",
        device_id=task_data.device_id,
        relay_number=task_data.relay_number,
        device_action=task_data.device_action,
        mqtt_command_id=mqtt_command_id,
        schedule_synced=False,  # Will be set to True after MQTT publish
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    session.add(task)
    try:
        session.commit()
        session.refresh(task)
    except Exception as e:
        session.rollback()
        # If it's a foreign key error, it means the user doesn't exist
        if "foreign key" in str(e).lower() or "user" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user ID: {user_id}",
            )
        raise

    # v4.0.0: Send MQTT schedule command for device schedules
    if task_data.task_type == "device_schedule" and task_data.relay_number and task_data.device_action:
        mqtt = get_mqtt_service()
        logger.info(f"Device schedule task created: relay={task_data.relay_number}, action={task_data.device_action}, mqtt_connected={mqtt.is_connected}, due_date={task_data.due_date}, due_time={task_data.due_time}")
        if mqtt.is_connected and task_data.due_date and task_data.due_time:
            # Parse due_time string (HH:MM) to time object
            try:
                hour, minute = map(int, task_data.due_time.split(":"))
                due_time_obj = time(hour, minute)
            except (ValueError, AttributeError):
                logger.warning(f"Invalid due_time format: {task_data.due_time}")
                due_time_obj = None

            if due_time_obj:
                # Calculate scheduled time
                scheduled_dt = datetime.combine(task_data.due_date, due_time_obj)
                scheduled_unix = int(scheduled_dt.timestamp())

                relay_name = RELAY_NAMES.get(task_data.relay_number, f"Relay {task_data.relay_number}")

                # Send MQTT schedule command
                result = await mqtt.publish_schedule(
                    relay_number=task_data.relay_number,
                    action=task_data.device_action,
                    scheduled_time=scheduled_unix,
                    device_name=relay_name,
                )

                if result["success"]:
                    # Mark as synced
                    task.schedule_synced = True
                    task.mqtt_command_id = result.get("command_id", mqtt_command_id)
                    session.add(task)
                    session.commit()
                    session.refresh(task)
                    logger.info(f"Device schedule sent to ESP: {task.id} -> {relay_name} {task_data.device_action} at {scheduled_unix}")
                else:
                    logger.warning(f"Failed to send device schedule: {result.get('error')}")
        else:
            missing = []
            if not mqtt.is_connected:
                missing.append("MQTT not connected")
            if not task_data.due_date:
                missing.append("missing due_date")
            if not task_data.due_time:
                missing.append("missing due_time")
            logger.warning(f"Device schedule NOT sent: {', '.join(missing)}")

    # Publish task created event (non-blocking)
    event_service = get_event_service()
    background_tasks.add_task(
        event_service.publish_task_created,
        task_id=task.id,
        user_id=user_id,
        title=task.title,
        description=task.description,
    )

    return TaskRead.model_validate(task)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Get a single task by ID.

    Returns 404 if task doesn't exist or 403 if task belongs to another user.
    """
    statement = select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Check if task exists but belongs to another user
        any_task = session.exec(select(TaskDB).where(TaskDB.id == task_id)).first()
        if any_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this task",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskRead.model_validate(task)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Update an existing task.

    Returns 404 if task doesn't exist or 403 if task belongs to another user.
    """
    # Find task and verify ownership
    statement = select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Check if task exists but belongs to another user
        any_task = session.exec(select(TaskDB).where(TaskDB.id == task_id)).first()
        if any_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to modify this task",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Validate title if provided
    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty",
            )
        if len(task_data.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be 200 characters or less",
            )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(task, key, value)

    task.updated_at = datetime.now(UTC)
    session.add(task)
    session.commit()
    session.refresh(task)

    # v4.0.0: Send MQTT schedule update for device schedules
    if task.task_type == "device_schedule" and task.relay_number and task.device_action:
        mqtt = get_mqtt_service()
        if mqtt.is_connected and task.due_date and task.due_time:
            # Parse due_time string (HH:MM) to time object
            try:
                hour, minute = map(int, task.due_time.split(":"))
                due_time_obj = time(hour, minute)
            except (ValueError, AttributeError):
                logger.warning(f"Invalid due_time format: {task.due_time}")
                due_time_obj = None

            if due_time_obj:
                # Calculate scheduled time
                scheduled_dt = datetime.combine(task.due_date, due_time_obj)
                scheduled_unix = int(scheduled_dt.timestamp())

                relay_name = RELAY_NAMES.get(task.relay_number, f"Relay {task.relay_number}")

                # Cancel old schedule first (if exists), then add new one
                if task.mqtt_command_id:
                    await mqtt.cancel_schedule(task.mqtt_command_id)

                # Send updated MQTT schedule command
                result = await mqtt.publish_schedule(
                    relay_number=task.relay_number,
                    action=task.device_action,
                    scheduled_time=scheduled_unix,
                    device_name=relay_name,
                )

                if result["success"]:
                    task.schedule_synced = True
                    task.mqtt_command_id = result.get("command_id", task.mqtt_command_id)
                    session.add(task)
                    session.commit()
                    session.refresh(task)
                    logger.info(f"Device schedule updated: {task.id} -> {relay_name} {task.device_action} at {scheduled_unix}")
                else:
                    logger.warning(f"Failed to update device schedule: {result.get('error')}")

    # Publish task updated event (non-blocking)
    event_service = get_event_service()
    background_tasks.add_task(
        event_service.publish_task_updated,
        task_id=task.id,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        is_complete=task_data.is_complete,
    )

    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Delete a task.

    Returns 404 if task doesn't exist or 403 if task belongs to another user.
    Returns 204 No Content on success.
    """
    # Find task and verify ownership
    statement = select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Check if task exists but belongs to another user
        any_task = session.exec(select(TaskDB).where(TaskDB.id == task_id)).first()
        if any_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this task",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Store title for event before deleting
    task_title = task.title

    session.delete(task)
    session.commit()

    # Publish task deleted event (non-blocking)
    event_service = get_event_service()
    background_tasks.add_task(
        event_service.publish_task_deleted,
        task_id=task_id,
        user_id=user_id,
        title=task_title,
    )

    return None


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    task_id: UUID,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Toggle task completion status.

    Returns 404 if task doesn't exist or 403 if task belongs to another user.
    """
    # Find task and verify ownership
    statement = select(TaskDB).where(TaskDB.id == task_id, TaskDB.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        # Check if task exists but belongs to another user
        any_task = session.exec(select(TaskDB).where(TaskDB.id == task_id)).first()
        if any_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to modify this task",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Toggle completion status
    task.is_complete = not task.is_complete
    task.updated_at = datetime.now(UTC)

    # v3.1.0: Auto-reschedule recurring tasks when completed
    rescheduled = False
    if task.is_complete and task.recurrence_pattern and task.recurrence_pattern != "none":
        if task.due_date:
            # Calculate next due date
            next_due = calculate_next_due_date(task.due_date, task.recurrence_pattern)
            # Mark task as incomplete and update due date
            task.is_complete = False
            task.due_date = next_due
            rescheduled = True
            logger.info(f"Recurring task rescheduled: {task.title} -> {next_due}")

    session.add(task)
    session.commit()
    session.refresh(task)

    # Publish task completed event (non-blocking)
    event_service = get_event_service()
    background_tasks.add_task(
        event_service.publish_task_completed,
        task_id=task.id,
        user_id=user_id,
        title=task.title,
        is_complete=task.is_complete,
    )

    return TaskRead.model_validate(task)
