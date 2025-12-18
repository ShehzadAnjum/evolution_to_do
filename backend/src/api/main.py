"""FastAPI application entry point."""

import logging
from datetime import datetime, UTC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import select

from .routes import health, tasks, chat, events, categories, voice, devices
from .database import init_db
from .config import get_settings
from ..services.mqtt_service import start_mqtt_service, stop_mqtt_service, RELAY_NAMES
from ..models.task import TaskDB

# Configure logging to show INFO level (for debug logs in chat_service)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def mark_task_complete_by_command_id(command_id: str):
    """Mark a task as complete when ESP32 executes the schedule.

    Called by MQTT service when ESP32 sends EXECUTED message.
    """
    from sqlmodel import Session
    from .database import engine

    print(f"🔍 Looking for task with mqtt_command_id: {command_id}")

    # Use synchronous session (get_session is sync, not async)
    with Session(engine) as session:
        stmt = select(TaskDB).where(TaskDB.mqtt_command_id == command_id)
        result = session.execute(stmt)
        task = result.scalars().first()

        if task:
            print(f"📋 Found task: {task.title} (id={task.id})")
            task.is_complete = True
            task.updated_at = datetime.now(UTC)
            session.add(task)
            session.commit()
            print(f"✅ Task '{task.title}' marked complete (executed by ESP32)")
        else:
            print(f"⚠️  No task found for command_id: {command_id}")
            # Debug: List all device schedule tasks
            debug_stmt = select(TaskDB).where(TaskDB.task_type == "device_schedule")
            debug_result = session.execute(debug_stmt)
            all_schedules = debug_result.scalars().all()
            print(f"   Available device schedules ({len(all_schedules)}):")
            for t in all_schedules[:5]:  # Show first 5
                print(f"   - {t.title}: mqtt_cmd_id={t.mqtt_command_id}")


async def get_pending_schedules_for_sync():
    """Get all pending device schedules for ESP32 sync.

    Called by MQTT service when ESP32 sends SYNC_REQ.
    Returns list of unsynced device_schedule tasks.
    """
    from sqlmodel import Session
    from .database import engine

    pending = []
    now = datetime.now(UTC)

    # Use synchronous session (get_session is sync, not async)
    with Session(engine) as session:
        # Query all unsynced device schedules
        stmt = select(TaskDB).where(
            TaskDB.task_type == "device_schedule",
            TaskDB.schedule_synced == False,
            TaskDB.is_complete == False,
        )
        result = session.execute(stmt)
        tasks = result.scalars().all()

        for task in tasks:
            # Calculate scheduled time from due_date + due_time
            if task.due_date and task.due_time:
                scheduled_dt = datetime.combine(task.due_date, task.due_time)
                # Skip if already in the past
                if scheduled_dt.replace(tzinfo=UTC) <= now:
                    continue
                scheduled_unix = int(scheduled_dt.timestamp())
            else:
                continue

            relay_name = RELAY_NAMES.get(task.relay_number or 1, f"Relay {task.relay_number}")
            pending.append({
                "command_id": task.mqtt_command_id or str(task.id),
                "relay_number": task.relay_number or 1,
                "action": task.device_action or "toggle",
                "scheduled_time": scheduled_unix,
                "device_name": relay_name,
                "task_id": str(task.id),
            })

    return pending


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup: Initialize database tables
    import os
    port = os.environ.get("PORT", "NOT_SET")
    print(f"🚀 Starting FastAPI application...")
    print(f"🔍 DEBUG: PORT environment variable = {port}")
    print(f"🔍 DEBUG: All PORT-related env vars: {[k for k in os.environ.keys() if 'PORT' in k]}")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Warning: Database initialization failed: {e}")
        print("   Tables may need to be created manually")
        import traceback
        traceback.print_exc()

    # Start MQTT service for IoT device communication
    try:
        mqtt_service = await start_mqtt_service()
        if mqtt_service.is_connected:
            # Register sync callback for ESP32 reconnection
            mqtt_service.set_sync_callback(get_pending_schedules_for_sync)
            # Register task complete callback for ESP32 execution
            mqtt_service.set_task_complete_callback(mark_task_complete_by_command_id)
            print("✅ MQTT service started (IoT device control enabled)")
        else:
            print("⚠️  MQTT service not connected (IoT device control offline)")
    except Exception as e:
        print(f"⚠️  MQTT service failed to start: {e}")
        print("   IoT device control will be unavailable")

    yield

    # Shutdown: Cleanup
    print("🛑 Shutting down FastAPI application...")
    try:
        await stop_mqtt_service()
        print("✅ MQTT service stopped")
    except Exception as e:
        print(f"⚠️  Error stopping MQTT service: {e}")


# Create FastAPI app
app = FastAPI(
    title="Todo App API",
    description="Phase II - Full-Stack Web Application API",
    version="0.2.0",
    lifespan=lifespan,
)

# Configure CORS
settings = get_settings()
origins = settings.cors_origins.split(",") if "," in settings.cors_origins else [settings.cors_origins]
# Add common development ports and known frontend deployments
origins.extend([
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://evolution-to-do.vercel.app",
    "https://evolution-todo-v1.vercel.app",  # iteration-1 deployment
    "http://172.171.119.133.nip.io:3000",    # AKS deployment via nip.io
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(categories.router)
app.include_router(chat.router)
app.include_router(events.router)
app.include_router(voice.router)
app.include_router(devices.router)  # v4.0.0: IoT device control


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo App API",
        "version": "0.2.0",
        "docs": "/docs"
    }
