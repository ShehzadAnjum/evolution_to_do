"""Pytest fixtures for API integration tests.

Provides test client, mock authentication, and database setup.

Note: Uses SQLite file-based database for testing to handle FastAPI's
async-to-sync bridge which uses thread pools.
"""

import os
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from typing import Generator

# Set test environment BEFORE any imports
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-testing-only-32chars"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from jose import jwt


# Create test engine with StaticPool for connection reuse
test_engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Now import app modules - they will use the env vars we set
from src.api.main import app
from src.api.database import get_session
from src.models.task import TaskDB
from src.models.user import User


def get_test_session() -> Generator[Session, None, None]:
    """Override database session for testing."""
    with Session(test_engine) as session:
        yield session


def create_test_user(user_id: str) -> None:
    """Create a test user in the database."""
    with Session(test_engine) as session:
        # Check if user exists
        existing = session.get(User, user_id)
        if not existing:
            user = User(id=user_id)
            session.add(user)
            session.commit()


@pytest.fixture(scope="function", autouse=True)
def test_db():
    """Create fresh database tables for each test.

    This fixture is autouse=True so it runs for every test.
    """
    # Create all tables using the test engine
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    # Drop all tables after test
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def client(test_db) -> Generator[TestClient, None, None]:
    """Create test client with database override."""
    # Override the get_session dependency
    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as test_client:
        yield test_client

    # Clear overrides after test
    app.dependency_overrides.clear()


def create_test_token(user_id: str, expired: bool = False) -> str:
    """Create a valid JWT token for testing.

    Args:
        user_id: The user ID to include in the token.
        expired: If True, create an expired token.

    Returns:
        JWT token string.
    """
    secret = os.environ["BETTER_AUTH_SECRET"]

    now = datetime.now(timezone.utc)
    if expired:
        exp = now - timedelta(hours=1)
    else:
        exp = now + timedelta(hours=24)

    payload = {
        "sub": user_id,
        "exp": exp,
        "iat": now,
    }

    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def user_id() -> str:
    """Generate a unique user ID for testing."""
    return str(uuid4())


@pytest.fixture
def other_user_id() -> str:
    """Generate a different user ID for ownership tests."""
    return str(uuid4())


@pytest.fixture
def auth_headers(test_db, user_id: str) -> dict:
    """Create authorization headers with valid token and create test user."""
    # Create test user in database
    create_test_user(user_id)
    token = create_test_token(user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_auth_headers(test_db, other_user_id: str) -> dict:
    """Create authorization headers for a different user."""
    # Create test user in database
    create_test_user(other_user_id)
    token = create_test_token(other_user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def expired_auth_headers(user_id: str) -> dict:
    """Create authorization headers with expired token."""
    token = create_test_token(user_id, expired=True)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_task_data() -> dict:
    """Sample valid task creation data."""
    return {
        "title": "Test Task",
        "description": "Test description",
    }


@pytest.fixture
def sample_task(client: TestClient, auth_headers: dict, sample_task_data: dict) -> dict:
    """Create a sample task and return it."""
    response = client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
    assert response.status_code == 201, f"Failed to create sample task: {response.text}"
    return response.json()


@pytest.fixture
def multiple_tasks(client: TestClient, auth_headers: dict) -> list[dict]:
    """Create multiple tasks for testing list/summary functionality."""
    tasks = []
    for i in range(5):
        data = {"title": f"Task {i+1}", "description": f"Description {i+1}"}
        response = client.post("/api/tasks/", json=data, headers=auth_headers)
        assert response.status_code == 201, f"Failed to create task {i+1}: {response.text}"
        tasks.append(response.json())

    # Mark some as complete
    response0 = client.patch(f"/api/tasks/{tasks[0]['id']}/complete", headers=auth_headers)
    assert response0.status_code == 200, f"Failed to complete task 0: {response0.text}"

    response2 = client.patch(f"/api/tasks/{tasks[2]['id']}/complete", headers=auth_headers)
    assert response2.status_code == 200, f"Failed to complete task 2: {response2.text}"

    return tasks
