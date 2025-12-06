"""User model for SQLModel metadata (for foreign key resolution).

Note: The actual user table is managed by Better Auth.
This model exists only to help SQLModel resolve foreign key constraints.
"""

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """User model for SQLModel metadata.

    This is a placeholder model to help SQLModel resolve foreign keys.
    The actual user table is created and managed by Better Auth.
    """
    __tablename__ = "user"

    id: str = Field(primary_key=True, description="User ID from Better Auth")
