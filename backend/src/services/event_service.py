"""Event publishing service using Dapr pub/sub.

This service handles publishing task events to Kafka via Dapr sidecar.
Supports both HTTP API and Python SDK approaches.
"""

import logging
import os
from typing import Optional
from uuid import UUID

import httpx

from ..models.event import (
    EventType,
    TaskEvent,
    TaskEventData,
    ReminderEvent,
    ReminderEventData,
    RecurringTriggerEvent,
    RecurringEventData,
)

logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = "taskevents"


class EventService:
    """Service for publishing events via Dapr pub/sub."""
    
    def __init__(self, dapr_port: Optional[str] = None):
        """Initialize event service.
        
        Args:
            dapr_port: Dapr sidecar HTTP port (default: 3500 or DAPR_HTTP_PORT env)
        """
        self.dapr_port = dapr_port or DAPR_HTTP_PORT
        self.base_url = f"http://localhost:{self.dapr_port}"
        self._enabled = os.getenv("DAPR_ENABLED", "false").lower() == "true"
    
    @property
    def is_enabled(self) -> bool:
        """Check if event publishing is enabled."""
        return self._enabled
    
    async def _publish_event(self, topic: str, data: dict) -> bool:
        """Publish an event to a topic via Dapr HTTP API.
        
        Args:
            topic: Topic name to publish to
            data: Event data to publish
            
        Returns:
            True if publish succeeded, False otherwise
        """
        if not self._enabled:
            logger.debug(f"Event publishing disabled, skipping: {topic}")
            return False
        
        url = f"{self.base_url}/v1.0/publish/{DAPR_PUBSUB_NAME}/{topic}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=5.0,
                )
                
                if response.status_code == 204:
                    logger.info(f"Published event to {topic}: {data.get('event_id')}")
                    return True
                else:
                    logger.warning(
                        f"Failed to publish to {topic}: {response.status_code} - {response.text}"
                    )
                    return False
                    
        except httpx.ConnectError:
            logger.warning(f"Dapr sidecar not available at {self.base_url}")
            return False
        except Exception as e:
            logger.error(f"Error publishing event to {topic}: {e}")
            return False
    
    async def publish_task_created(
        self,
        task_id: UUID,
        user_id: str,
        title: str,
        description: str = "",
    ) -> bool:
        """Publish task created event.
        
        Args:
            task_id: UUID of the created task
            user_id: ID of the task owner
            title: Task title
            description: Task description
            
        Returns:
            True if publish succeeded
        """
        event = TaskEvent(
            event_type=EventType.TASK_CREATED,
            user_id=user_id,
            task_id=task_id,
            data=TaskEventData(title=title, description=description),
        )
        
        return await self._publish_event(
            EventType.TASK_CREATED.value,
            event.model_dump(mode="json"),
        )
    
    async def publish_task_updated(
        self,
        task_id: UUID,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_complete: Optional[bool] = None,
        previous_state: Optional[dict] = None,
    ) -> bool:
        """Publish task updated event.
        
        Args:
            task_id: UUID of the updated task
            user_id: ID of the task owner
            title: Updated title (if changed)
            description: Updated description (if changed)
            is_complete: Updated completion status (if changed)
            previous_state: Previous task state for comparison
            
        Returns:
            True if publish succeeded
        """
        event = TaskEvent(
            event_type=EventType.TASK_UPDATED,
            user_id=user_id,
            task_id=task_id,
            data=TaskEventData(
                title=title,
                description=description,
                is_complete=is_complete,
                previous_state=previous_state,
            ),
        )
        
        return await self._publish_event(
            EventType.TASK_UPDATED.value,
            event.model_dump(mode="json"),
        )
    
    async def publish_task_completed(
        self,
        task_id: UUID,
        user_id: str,
        title: str,
        is_complete: bool,
    ) -> bool:
        """Publish task completed/uncompleted event.
        
        Args:
            task_id: UUID of the task
            user_id: ID of the task owner
            title: Task title
            is_complete: New completion status
            
        Returns:
            True if publish succeeded
        """
        event = TaskEvent(
            event_type=EventType.TASK_COMPLETED,
            user_id=user_id,
            task_id=task_id,
            data=TaskEventData(title=title, is_complete=is_complete),
        )
        
        return await self._publish_event(
            EventType.TASK_COMPLETED.value,
            event.model_dump(mode="json"),
        )
    
    async def publish_task_deleted(
        self,
        task_id: UUID,
        user_id: str,
        title: str,
    ) -> bool:
        """Publish task deleted event.
        
        Args:
            task_id: UUID of the deleted task
            user_id: ID of the task owner
            title: Task title (for logging/notification)
            
        Returns:
            True if publish succeeded
        """
        event = TaskEvent(
            event_type=EventType.TASK_DELETED,
            user_id=user_id,
            task_id=task_id,
            data=TaskEventData(title=title),
        )
        
        return await self._publish_event(
            EventType.TASK_DELETED.value,
            event.model_dump(mode="json"),
        )


# Singleton instance
_event_service: Optional[EventService] = None


def get_event_service() -> EventService:
    """Get or create the event service singleton."""
    global _event_service
    if _event_service is None:
        _event_service = EventService()
    return _event_service
