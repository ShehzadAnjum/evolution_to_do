"""FastAPI dependencies for authentication and database."""

from typing import Generator
from fastapi import Depends, HTTPException, status, Header
from sqlmodel import Session
from jose import JWTError, jwt
from .database import get_session as get_db_session
from .config import get_settings


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    yield from get_db_session()


async def get_current_user_id(
    authorization: str = Header(..., description="Bearer token"),
) -> str:
    """Extract and validate user ID from JWT token.

    For Phase II, this validates the JWT from Better Auth.

    Args:
        authorization: Bearer token from Authorization header.

    Returns:
        User ID from the token.

    Raises:
        HTTPException: If token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization.startswith("Bearer "):
        raise credentials_exception

    token = authorization.split(" ")[1]
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
        )
        # Try multiple claim names for user ID (for compatibility)
        user_id: str = payload.get("sub") or payload.get("userId") or payload.get("user_id")
        if user_id is None:
            print(f"⚠️  JWT payload missing user ID. Payload keys: {list(payload.keys())}")
            raise credentials_exception
        return user_id
    except JWTError as e:
        print(f"⚠️  JWT validation failed: {type(e).__name__}: {str(e)}")
        print(f"⚠️  Using secret: {settings.better_auth_secret[:20]}... (first 20 chars)")
        raise credentials_exception
    except ValueError as e:
        print(f"⚠️  JWT decode error: {str(e)}")
        raise credentials_exception
