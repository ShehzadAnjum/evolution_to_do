# Skill: Kafka + Dapr Event Patterns

## Overview

This skill captures patterns for implementing event-driven architecture with Kafka/Redpanda and Dapr in Phase V.

## Core Concepts

### Event-Driven Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Producer      │────▶│   Kafka/Redpanda│────▶│   Consumer      │
│   (Backend)     │     │   (Message Bus) │     │   (Workers)     │
│                 │     │                 │     │                 │
│ - Task created  │     │ - Topics        │     │ - Notifications │
│ - Task updated  │     │ - Partitions    │     │ - Reminders     │
│ - Reminder due  │     │ - Retention     │     │ - Analytics     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Dapr Sidecar Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                        Pod                                   │
├────────────────────────┬────────────────────────────────────┤
│   Application          │   Dapr Sidecar                     │
│   (FastAPI)            │   (daprd)                          │
│                        │                                     │
│   localhost:8000 ◄────►│ localhost:3500                     │
│                        │ - Pub/Sub                          │
│                        │ - State management                 │
│                        │ - Service invocation               │
└────────────────────────┴────────────────────────────────────┘
```

## Event Schema

### Task Events

```python
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum

class EventType(str, Enum):
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    REMINDER_DUE = "reminder.due"
    RECURRING_TRIGGER = "recurring.trigger"

class TaskEvent(BaseModel):
    event_id: UUID
    event_type: EventType
    timestamp: datetime
    user_id: str
    task_id: UUID
    data: dict
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }
```

### Topic Naming Convention

```
evolution-todo.<domain>.<action>

Examples:
- evolution-todo.tasks.created
- evolution-todo.tasks.updated
- evolution-todo.reminders.due
- evolution-todo.recurring.trigger
```

## Dapr Components

### Pub/Sub Component (Kafka)

**File**: `infra/dapr/components/pubsub.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskevents
  namespace: evolution-todo
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "evolution-todo-group"
    - name: authType
      value: "none"
    - name: maxMessageBytes
      value: "1048576"  # 1MB
```

### Pub/Sub Component (Redpanda - Alternative)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskevents
spec:
  type: pubsub.kafka  # Redpanda is Kafka-compatible
  version: v1
  metadata:
    - name: brokers
      value: "redpanda:9092"
    - name: consumerGroup
      value: "evolution-todo-group"
```

## Publishing Events

### Using Dapr SDK

```python
from dapr.clients import DaprClient
import json

async def publish_task_event(event: TaskEvent):
    """Publish task event via Dapr."""
    with DaprClient() as client:
        client.publish_event(
            pubsub_name="taskevents",
            topic_name=event.event_type.value,
            data=event.model_dump_json(),
            data_content_type="application/json",
        )

# Usage
async def create_task(task: TaskCreate, user_id: str):
    db_task = await save_task(task, user_id)
    
    # Publish event
    await publish_task_event(TaskEvent(
        event_id=uuid4(),
        event_type=EventType.TASK_CREATED,
        timestamp=datetime.utcnow(),
        user_id=user_id,
        task_id=db_task.id,
        data={"title": db_task.title},
    ))
    
    return db_task
```

### Using HTTP (Alternative)

```python
import httpx

DAPR_HTTP_PORT = 3500

async def publish_event_http(topic: str, data: dict):
    """Publish event via Dapr HTTP API."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/taskevents/{topic}",
            json=data,
        )
```

## Subscribing to Events

### Subscription Configuration

**File**: `infra/dapr/subscriptions/tasks.yaml`
```yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-events-subscription
spec:
  pubsubname: taskevents
  topic: task.created
  routes:
    default: /events/task-created
---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: reminder-subscription
spec:
  pubsubname: taskevents
  topic: reminder.due
  routes:
    default: /events/reminder-due
```

### Event Handler Endpoints

```python
from fastapi import APIRouter
from dapr.ext.fastapi import DaprApp

router = APIRouter()
dapr_app = DaprApp()

@dapr_app.subscribe(pubsub="taskevents", topic="task.created")
@router.post("/events/task-created")
async def handle_task_created(event: dict):
    """Handle task created event."""
    task_id = event.get("task_id")
    user_id = event.get("user_id")
    
    # Send notification, update analytics, etc.
    await send_notification(user_id, f"Task created: {task_id}")
    
    return {"status": "ok"}

@dapr_app.subscribe(pubsub="taskevents", topic="reminder.due")
@router.post("/events/reminder-due")
async def handle_reminder_due(event: dict):
    """Handle reminder due event."""
    task_id = event.get("task_id")
    user_id = event.get("user_id")
    
    # Send reminder notification
    await send_reminder_notification(user_id, task_id)
    
    return {"status": "ok"}
```

## Recurring Tasks Pattern

### Cron Binding

**File**: `infra/dapr/components/cron.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: recurring-scheduler
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "0 * * * *"  # Every hour
    - name: direction
      value: "input"
```

### Cron Handler

```python
@router.post("/bindings/recurring-scheduler")
async def check_recurring_tasks():
    """Check and create recurring task instances."""
    recurring_tasks = await get_due_recurring_tasks()
    
    for task in recurring_tasks:
        # Create new instance
        new_task = await create_task_instance(task)
        
        # Publish event
        await publish_task_event(TaskEvent(
            event_id=uuid4(),
            event_type=EventType.RECURRING_TRIGGER,
            timestamp=datetime.utcnow(),
            user_id=task.user_id,
            task_id=new_task.id,
            data={"recurring_id": str(task.id)},
        ))
    
    return {"processed": len(recurring_tasks)}
```

## Testing Events

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_dapr_client():
    with patch("dapr.clients.DaprClient") as mock:
        client = AsyncMock()
        mock.return_value.__enter__.return_value = client
        yield client

async def test_task_created_publishes_event(mock_dapr_client):
    """Test that creating a task publishes an event."""
    task = await create_task(TaskCreate(title="Test"), "user-123")
    
    mock_dapr_client.publish_event.assert_called_once()
    call_args = mock_dapr_client.publish_event.call_args
    assert call_args.kwargs["topic_name"] == "task.created"
```

## Anti-Patterns

### ❌ Synchronous Event Publishing

```python
# Blocks the request
def create_task(task):
    db_task = save_task(task)
    publish_event(task)  # What if Kafka is down?
    return db_task
```

### ✅ Async with Error Handling

```python
async def create_task(task):
    db_task = await save_task(task)
    try:
        await publish_event(task)
    except Exception as e:
        logger.error(f"Failed to publish event: {e}")
        # Task still created - event will be retried/reconciled
    return db_task
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: V
**Last Updated**: 2025-12-10
