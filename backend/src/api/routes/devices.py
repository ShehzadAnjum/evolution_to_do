"""Device management API endpoints.

This module provides endpoints for IoT device control and status.
Communicates with ESP32 devices via MQTT through HiveMQ Cloud.

v4.0.0: Initial implementation for device scheduling feature.
v4.0.1: Added schedule sync for offline ESP recovery.
"""

import logging
from datetime import datetime, UTC
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from ..deps import get_current_user_id, get_session
from ..database import get_session as get_db_session
from ...models.task import TaskDB
from ...services.mqtt_service import get_mqtt_service, RELAY_NAMES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/devices", tags=["devices"])


# =============================================================================
# Request/Response Models
# =============================================================================


class DeviceCommandRequest(BaseModel):
    """Request body for immediate device command."""
    relay_number: int = Field(ge=1, le=4, description="Relay number (1-4)")
    action: str = Field(description="Action: on, off, toggle")


class DeviceScheduleRequest(BaseModel):
    """Request body for scheduling a device action."""
    relay_number: int = Field(ge=1, le=4, description="Relay number (1-4)")
    action: str = Field(description="Action: on, off, toggle")
    scheduled_time: datetime = Field(description="When to execute (ISO format)")
    device_name: Optional[str] = Field(default=None, description="Display name for device")


class DeviceCommandResponse(BaseModel):
    """Response for device command."""
    success: bool
    command_id: Optional[str] = None
    relay_name: Optional[str] = None
    action: Optional[str] = None
    message: str
    error: Optional[str] = None


class RelayStatus(BaseModel):
    """Status of a single relay."""
    number: int
    name: str
    state: str


class DeviceStatusResponse(BaseModel):
    """Response for device status."""
    online: bool
    relays: list[RelayStatus]
    last_heartbeat: Optional[str] = None
    wifi_rssi: Optional[int] = None
    last_updated: Optional[str] = None
    mqtt_connected: bool


# =============================================================================
# Endpoints
# =============================================================================


@router.get("/status", response_model=DeviceStatusResponse)
async def get_device_status(
    user_id: str = Depends(get_current_user_id),
):
    """Get current device status.

    Returns cached device status including relay states,
    online/offline status, and connection info.

    Also sends a status request to the device for fresh data.
    """
    mqtt = get_mqtt_service()

    # Request fresh status (async - will update cache when received)
    status_data = await mqtt.request_status()

    return DeviceStatusResponse(
        online=status_data["online"],
        relays=[RelayStatus(**r) for r in status_data["relays"]],
        last_heartbeat=status_data.get("last_heartbeat"),
        wifi_rssi=status_data.get("wifi_rssi"),
        last_updated=status_data.get("last_updated"),
        mqtt_connected=mqtt.is_connected,
    )


@router.post("/command", response_model=DeviceCommandResponse)
async def send_device_command(
    command: DeviceCommandRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Send immediate command to device.

    Turns a relay on, off, or toggles it immediately.
    """
    mqtt = get_mqtt_service()

    if not mqtt.is_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MQTT service not available. Device control is offline.",
        )

    # Validate action
    if command.action not in ["on", "off", "toggle"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be 'on', 'off', or 'toggle'",
        )

    result = await mqtt.publish_immediate(
        relay_number=command.relay_number,
        action=command.action,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to send command"),
        )

    return DeviceCommandResponse(
        success=True,
        command_id=result.get("command_id"),
        relay_name=result.get("relay_name"),
        action=result.get("action"),
        message=result.get("message", "Command sent"),
    )


@router.post("/schedule", response_model=DeviceCommandResponse)
async def schedule_device_action(
    schedule: DeviceScheduleRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Schedule a device action for later.

    Sends a schedule command to the ESP32, which stores it locally
    and executes at the specified time (even if offline).
    """
    mqtt = get_mqtt_service()

    if not mqtt.is_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MQTT service not available. Scheduling is offline.",
        )

    # Validate action
    if schedule.action not in ["on", "off", "toggle"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be 'on', 'off', or 'toggle'",
        )

    # Validate scheduled time is in the future
    if schedule.scheduled_time <= datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheduled time must be in the future",
        )

    # Convert to Unix timestamp
    scheduled_unix = int(schedule.scheduled_time.timestamp())

    relay_name = schedule.device_name or RELAY_NAMES.get(
        schedule.relay_number, f"Relay {schedule.relay_number}"
    )

    result = await mqtt.publish_schedule(
        relay_number=schedule.relay_number,
        action=schedule.action,
        scheduled_time=scheduled_unix,
        device_name=relay_name,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to send schedule"),
        )

    return DeviceCommandResponse(
        success=True,
        command_id=result.get("command_id"),
        relay_name=relay_name,
        action=result.get("action"),
        message=f"Scheduled {relay_name} to {schedule.action} at {schedule.scheduled_time.isoformat()}",
    )


@router.get("/relays", response_model=list[RelayStatus])
async def list_relays(
    user_id: str = Depends(get_current_user_id),
):
    """List available relays with their current states.

    Returns the 4 relays with their names and current on/off states.
    """
    mqtt = get_mqtt_service()
    status_data = mqtt.device_status.to_dict()

    return [RelayStatus(**r) for r in status_data["relays"]]


@router.get("/health")
async def device_health():
    """Check device connectivity health.

    Returns MQTT connection status and device online status.
    Does not require authentication (for monitoring).
    """
    mqtt = get_mqtt_service()
    device_status = mqtt.device_status

    return {
        "mqtt_connected": mqtt.is_connected,
        "device_online": device_status.is_online,  # Use computed property with timeout
        "last_heartbeat": device_status.last_heartbeat.isoformat() if device_status.last_heartbeat else None,
        "wifi_rssi": device_status.wifi_rssi,
    }


@router.post("/reconnect")
async def reconnect_mqtt(
    user_id: str = Depends(get_current_user_id),
):
    """Reconnect to MQTT broker.

    Attempts to reconnect to the MQTT broker if disconnected.
    Returns the new connection status.
    """
    from ...services.mqtt_service import start_mqtt_service, stop_mqtt_service

    mqtt = get_mqtt_service()

    # If already connected, just return status
    if mqtt.is_connected:
        return {
            "success": True,
            "mqtt_connected": True,
            "message": "MQTT already connected",
        }

    # Try to reconnect
    logger.info("Attempting MQTT reconnection...")
    try:
        # Stop existing service
        await stop_mqtt_service()
        # Start fresh
        await start_mqtt_service()

        mqtt = get_mqtt_service()
        connected = mqtt.is_connected

        return {
            "success": connected,
            "mqtt_connected": connected,
            "message": "MQTT reconnected successfully" if connected else "Failed to reconnect to MQTT",
        }
    except Exception as e:
        logger.error(f"MQTT reconnection failed: {e}")
        return {
            "success": False,
            "mqtt_connected": False,
            "message": f"Reconnection failed: {str(e)}",
        }


class PendingSchedule(BaseModel):
    """Pending schedule waiting to be synced to device."""
    command_id: str
    relay_number: int
    action: str
    scheduled_time: int  # Unix timestamp
    device_name: str
    task_id: str


@router.get("/pending-schedules", response_model=list[PendingSchedule])
async def get_pending_schedules(
    user_id: str = Depends(get_current_user_id),
):
    """Get device schedules that haven't been synced to ESP32.

    Returns all device_schedule tasks where schedule_synced=False.
    Used by ESP32 on reconnect to retrieve missed schedules.
    """
    async for session in get_db_session():
        # Query all unsynced device schedules for this user that are in the future
        now = datetime.now(UTC)
        stmt = select(TaskDB).where(
            TaskDB.user_id == user_id,
            TaskDB.task_type == "device_schedule",
            TaskDB.schedule_synced == False,
            TaskDB.is_complete == False,
        )
        result = await session.execute(stmt)
        tasks = result.scalars().all()

        pending = []
        for task in tasks:
            # Calculate scheduled time from due_date + due_time
            if task.due_date and task.due_time:
                scheduled_dt = datetime.combine(task.due_date, task.due_time)
                # Skip if already in the past
                if scheduled_dt.replace(tzinfo=UTC) <= now:
                    continue
                scheduled_unix = int(scheduled_dt.timestamp())
            else:
                continue  # Skip tasks without proper schedule info

            relay_name = RELAY_NAMES.get(task.relay_number or 1, f"Relay {task.relay_number}")
            pending.append(PendingSchedule(
                command_id=task.mqtt_command_id or str(task.id),
                relay_number=task.relay_number or 1,
                action=task.device_action or "toggle",
                scheduled_time=scheduled_unix,
                device_name=relay_name,
                task_id=str(task.id),
            ))

        return pending


@router.post("/mark-synced/{task_id}")
async def mark_schedule_synced(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Mark a device schedule as synced to ESP32.

    Called when ESP32 acknowledges receiving a schedule.
    """
    async for session in get_db_session():
        stmt = select(TaskDB).where(
            TaskDB.id == task_id,
            TaskDB.user_id == user_id,
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        task.schedule_synced = True
        session.add(task)
        await session.commit()

        return {"success": True, "message": f"Task {task_id} marked as synced"}
