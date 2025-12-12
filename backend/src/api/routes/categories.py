"""Category CRUD endpoints."""

import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..deps import get_session, get_current_user_id
from ...models.category import CategoryDB, CategoryCreate, CategoryRead

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
async def list_categories(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """List all custom categories for the authenticated user.

    Returns categories ordered by creation date (oldest first).
    """
    statement = select(CategoryDB).where(CategoryDB.user_id == user_id).order_by(CategoryDB.created_at)
    categories = session.exec(statement).all()
    return [CategoryRead.model_validate(cat) for cat in categories]


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Create a new custom category for the authenticated user.

    Validates:
    - Name is required and 1-50 characters
    - Icon is optional, max 10 characters
    - Name must be unique for this user
    """
    if not category_data.name or not category_data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name is required and cannot be empty",
        )

    # Check for duplicate category name for this user
    existing = session.exec(
        select(CategoryDB).where(
            CategoryDB.user_id == user_id,
            CategoryDB.name == category_data.name.strip()
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category '{category_data.name}' already exists",
        )

    category = CategoryDB(
        name=category_data.name.strip(),
        icon=category_data.icon or "📁",
        user_id=user_id,
    )

    session.add(category)
    session.commit()
    session.refresh(category)

    return CategoryRead.model_validate(category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Delete a custom category.

    Returns 404 if category doesn't exist or 403 if category belongs to another user.
    Returns 204 No Content on success.
    """
    statement = select(CategoryDB).where(CategoryDB.id == category_id, CategoryDB.user_id == user_id)
    category = session.exec(statement).first()

    if not category:
        # Check if category exists but belongs to another user
        any_category = session.exec(select(CategoryDB).where(CategoryDB.id == category_id)).first()
        if any_category:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this category",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    session.delete(category)
    session.commit()

    return None
