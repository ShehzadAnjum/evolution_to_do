"""Category model for custom task categories.

This module defines Category models for user-defined categories.
"""

from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


MAX_CATEGORY_NAME_LENGTH = 50
MAX_ICON_LENGTH = 10


class CategoryBase(SQLModel):
    """Base category fields shared by all category schemas."""

    name: str = Field(min_length=1, max_length=MAX_CATEGORY_NAME_LENGTH)
    icon: str = Field(default="📁", max_length=MAX_ICON_LENGTH)


class CategoryDB(CategoryBase, table=True):
    """Database model for categories (SQLModel table)."""

    __tablename__ = "categories"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, description="Owner user ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CategoryCreate(SQLModel):
    """Schema for creating a category (request body)."""

    name: str = Field(min_length=1, max_length=MAX_CATEGORY_NAME_LENGTH)
    icon: str = Field(default="📁", max_length=MAX_ICON_LENGTH)


class CategoryRead(CategoryBase):
    """Schema for reading a category (response body)."""

    id: UUID
    user_id: str
    created_at: datetime
