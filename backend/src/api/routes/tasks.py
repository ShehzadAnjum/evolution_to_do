"""Task CRUD endpoints."""

import logging
from datetime import datetime, UTC
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select

from ..deps import get_session, get_current_user_id
from ...models.task import TaskDB, TaskCreate, TaskRead, TaskUpdate
from ...services.event_service import get_event_service

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=dict)
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """List all tasks for the authenticated user.

    Returns tasks with summary statistics.
    """
    # Query tasks for this user, ordered by creation date (newest first)
    statement = select(TaskDB).where(TaskDB.user_id == user_id).order_by(TaskDB.created_at.desc())
    tasks = session.exec(statement).all()

    # Calculate statistics
    total = len(tasks)
    completed = sum(1 for task in tasks if task.is_complete)

    return {
        "tasks": [TaskRead.model_validate(task) for task in tasks],
        "total": total,
        "completed": completed,
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

    # Create task with v2.0.0 fields
    task = TaskDB(
        title=task_data.title.strip(),
        description=task_data.description or "",
        is_complete=False,
        user_id=user_id,
        # v2.0.0: New optional fields with defaults
        priority=task_data.priority or "medium",
        category=task_data.category or "general",
        due_date=task_data.due_date,
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
