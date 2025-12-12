"""Database connection and session management for Neon PostgreSQL."""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool

from .config import get_settings

# Import models so SQLModel knows about them for table creation
# IMPORTANT: Import User BEFORE Task so foreign key can be resolved
from ..models.user import User  # noqa: F401 - For FK resolution (must be first)
from ..models.task import TaskDB  # noqa: F401
from ..models.category import CategoryDB  # noqa: F401 - Custom categories
from ..models.conversation import Conversation  # noqa: F401 - Phase III
from ..models.message import Message  # noqa: F401 - Phase III


# Create engine with NullPool for serverless compatibility
def get_engine():
    """Create SQLModel engine with Neon PostgreSQL connection."""
    settings = get_settings()
    return create_engine(
        settings.database_url,
        poolclass=NullPool,  # Required for serverless PostgreSQL
        echo=False,  # Set to True for SQL query logging
    )


# Global engine instance
engine = get_engine()


def get_session():
    """Dependency for FastAPI to get database session."""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database tables (create all tables).

    Note: The 'user' table is created by Better Auth migrations.
    This function creates the 'tasks' table and other SQLModel tables.
    """
    try:
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        if "user" in str(e).lower() or "NoReferencedTableError" in str(type(e).__name__):
            print("⚠️  Warning: 'user' table not found.")
            print("   This is expected - Better Auth will create the 'user' table.")
            print("   Run Better Auth migrations first: npx @better-auth/cli migrate")
            print("   Then run this again to create the 'tasks' table.")
        else:
            print(f"❌ Error creating tables: {e}")
            raise


if __name__ == "__main__":
    # For running migrations manually
    init_db()
