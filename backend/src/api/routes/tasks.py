"""Task CRUD endpoints."""

from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..deps import get_session, get_current_user_id
from ...models.task import TaskDB, TaskCreate, TaskRead, TaskUpdate


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

    # Create task
    task = TaskDB(
        title=task_data.title.strip(),
        description=task_data.description or "",
        is_complete=False,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
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

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
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

    session.delete(task)
    session.commit()

    return None


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    task_id: UUID,
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
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskRead.model_validate(task)
