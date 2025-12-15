---
name: kafka-dapr-patterns
description: Event-driven architecture with Kafka/Redpanda and Dapr. Use when implementing pub/sub messaging, event handlers, or state management with Dapr sidecars.
---

# Kafka & Dapr Patterns

## Dapr Pub/Sub Component

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskevents
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: "broker:9092"
    - name: consumerGroup
      value: "evolution-todo-group"
```

## Publish Event

```python
import httpx

async def publish_event(topic: str, data: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:3500/v1.0/publish/taskevents/{topic}",
            json=data
        )
```

## Subscribe to Events

```python
@app.post("/dapr/subscribe")
async def subscribe():
    return [
        {"pubsubname": "taskevents", "topic": "task.created", "route": "/events/task-created"},
    ]

@app.post("/events/task-created")
async def handle_task_created(event: dict):
    data = event.get("data", {})
    # Process event
    return {"status": "ok"}
```

## Dapr Annotations (K8s)

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "backend"
  dapr.io/app-port: "8000"
```

## State Store

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  metadata:
    - name: connectionString
      secretKeyRef:
        name: db-secret
        key: url
```
