"""Health check endpoint."""

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Check if API is running.

    Returns:
        Health status with timestamp.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
