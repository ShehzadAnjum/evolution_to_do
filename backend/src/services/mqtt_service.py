"""MQTT service for IoT device communication.

This module provides MQTT client functionality for communicating with
ESP32 IoT devices via HiveMQ Cloud broker.

v4.0.0: Initial implementation for device scheduling feature.
"""

import json
import logging
import asyncio
from datetime import datetime, UTC
from typing import Optional, Callable, Any
from uuid import uuid4

logger = logging.getLogger(__name__)


def sanitize_for_lcd(text: str, max_length: int = 16) -> str:
    """Sanitize text for LCD display (ASCII only, limited length).

    LCDs typically only support ASCII characters. This removes emojis,
    special characters, and truncates to fit the display.
    """
    # Keep only printable ASCII characters (32-126)
    ascii_text = ''.join(c if 32 <= ord(c) <= 126 else '' for c in text)
    # Remove extra spaces
    ascii_text = ' '.join(ascii_text.split())
    # Truncate to max length
    return ascii_text[:max_length]


def get_mqtt_config():
    """Get MQTT configuration from settings."""
    from ..api.config import get_settings
    settings = get_settings()
    return {
        "broker": settings.mqtt_broker,
        "port": settings.mqtt_port,
        "username": settings.mqtt_username,
        "password": settings.mqtt_password,
        "enabled": settings.mqtt_enabled,
    }

# Default device configuration (single device for now)
DEFAULT_DEVICE_ID = "esp32-home"
TOPIC_BASE = "evolution-todo/devices"

# Relay names for human-readable messages
RELAY_NAMES = {
    1: "Light",
    2: "Fan",
    3: "Aquarium",
    4: "Relay 4",
}


class DeviceStatus:
    """Cached device status."""

    # Device is considered offline if no heartbeat for this many seconds
    HEARTBEAT_TIMEOUT = 45  # seconds (ESP32 sends heartbeat every 30s)

    def __init__(self):
        self.online = False
        self.relay_states = ["off", "off", "off", "off"]
        self.last_heartbeat: Optional[datetime] = None
        self.wifi_rssi: Optional[int] = None
        self.last_updated: Optional[datetime] = None

    @property
    def is_online(self) -> bool:
        """Check if device is online based on heartbeat timeout."""
        if not self.last_heartbeat:
            return False
        elapsed = (datetime.now(UTC) - self.last_heartbeat).total_seconds()
        return elapsed < self.HEARTBEAT_TIMEOUT

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "online": self.is_online,  # Use computed property
            "relays": [
                {"number": i + 1, "name": RELAY_NAMES.get(i + 1, f"Relay {i + 1}"), "state": state}
                for i, state in enumerate(self.relay_states)
            ],
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "wifi_rssi": self.wifi_rssi,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }


class MQTTService:
    """MQTT service for device communication.

    Handles publishing commands to ESP32 devices and receiving status updates.
    Uses aiomqtt for async MQTT operations with HiveMQ Cloud (TLS).
    """

    # Rate limit: only send STATUS_REQ every N seconds
    STATUS_REQUEST_COOLDOWN = 30  # seconds

    def __init__(self):
        self._client = None
        self._connected = False
        self._device_status = DeviceStatus()
        self._message_handlers: dict[str, Callable] = {}
        self._listen_task: Optional[asyncio.Task] = None
        self._last_status_request: Optional[datetime] = None
        # Callback for sync requests - returns list of pending schedules
        self._sync_callback: Optional[Callable[[], Any]] = None
        # Callback for marking task complete when executed
        self._task_complete_callback: Optional[Callable[[str], Any]] = None

    def set_task_complete_callback(self, callback: Callable[[str], Any]):
        """Set callback for marking tasks complete when executed.

        The callback receives the mqtt_command_id and should mark the task as complete.
        """
        self._task_complete_callback = callback

    def set_sync_callback(self, callback: Callable[[], Any]):
        """Set callback for handling sync requests.

        The callback should return a list of pending schedules in the format:
        [{"command_id": str, "relay_number": int, "action": str,
          "scheduled_time": int, "device_name": str, "task_id": str}, ...]
        """
        self._sync_callback = callback

    @property
    def is_connected(self) -> bool:
        """Check if MQTT is connected."""
        return self._connected

    @property
    def device_status(self) -> DeviceStatus:
        """Get cached device status."""
        return self._device_status

    async def connect(self) -> bool:
        """Connect to MQTT broker.

        Returns:
            True if connection successful, False otherwise.
        """
        config = get_mqtt_config()

        if not config["enabled"]:
            logger.info("MQTT disabled via MQTT_ENABLED=false")
            return False

        if not config["broker"]:
            logger.warning("MQTT_BROKER not configured, MQTT disabled")
            return False

        try:
            import aiomqtt

            self._client = aiomqtt.Client(
                hostname=config["broker"],
                port=config["port"],
                username=config["username"],
                password=config["password"],
                tls_params=aiomqtt.TLSParameters(),  # Enable TLS
            )
            await self._client.__aenter__()
            self._connected = True
            logger.info(f"Connected to MQTT broker: {config['broker']}:{config['port']}")

            # Subscribe to device status and ack topics
            await self._subscribe_device(DEFAULT_DEVICE_ID)

            return True

        except ImportError:
            logger.error("aiomqtt not installed. Run: pip install aiomqtt")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to MQTT: {e}")
            self._connected = False
            return False

    async def disconnect(self):
        """Disconnect from MQTT broker."""
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass

        if self._client:
            try:
                await self._client.__aexit__(None, None, None)
            except Exception as e:
                logger.error(f"Error disconnecting MQTT: {e}")
            self._connected = False
            logger.info("Disconnected from MQTT broker")

    async def _subscribe_device(self, device_id: str):
        """Subscribe to a device's status and ack topics."""
        if not self._connected or not self._client:
            return

        status_topic = f"{TOPIC_BASE}/{device_id}/status"
        ack_topic = f"{TOPIC_BASE}/{device_id}/ack"

        await self._client.subscribe(status_topic)
        await self._client.subscribe(ack_topic)
        logger.info(f"Subscribed to {status_topic} and {ack_topic}")

    async def start_listening(self):
        """Start background task to listen for messages."""
        if not self._connected:
            return

        self._listen_task = asyncio.create_task(self._listen_messages())
        logger.info("Started MQTT message listener")

    async def _listen_messages(self):
        """Listen for incoming MQTT messages (run as background task)."""
        try:
            # aiomqtt 2.x: messages is a property that returns an async iterator
            async for message in self._client.messages:
                try:
                    # Use errors='replace' to handle any non-UTF8 bytes gracefully
                    payload_str = message.payload.decode('utf-8', errors='replace')
                    payload = json.loads(payload_str)
                    await self._handle_message(str(message.topic), payload)
                except json.JSONDecodeError as e:
                    # Log first 100 chars of payload for debugging
                    preview = message.payload[:100] if message.payload else b''
                    logger.warning(f"Invalid JSON in MQTT message: {e} - preview: {preview}")
                except Exception as e:
                    logger.error(f"Error handling MQTT message: {e}")
        except asyncio.CancelledError:
            logger.info("MQTT listener cancelled")
        except Exception as e:
            logger.error(f"MQTT listener error: {e}")
            self._connected = False

    async def _handle_message(self, topic: str, payload: dict):
        """Handle incoming MQTT message."""
        msg_type = payload.get("type")
        # Extract device_id from topic: evolution-todo/devices/{device_id}/status
        parts = topic.split("/")
        device_id = parts[-2] if len(parts) >= 2 else "unknown"

        logger.info(f"Received {msg_type} from {device_id}")

        if msg_type == "STATUS":
            await self._handle_status(device_id, payload)
        elif msg_type == "HEARTBEAT":
            await self._handle_heartbeat(device_id, payload)
        elif msg_type == "ACK":
            await self._handle_ack(device_id, payload)
        elif msg_type == "EXECUTED":
            await self._handle_executed(device_id, payload)
        elif msg_type == "SYNC_REQ":
            await self._handle_sync_request(device_id, payload)

    async def _handle_status(self, device_id: str, payload: dict):
        """Handle device status update."""
        relays = payload.get("relays", [])
        if relays:
            for relay in relays:
                idx = relay.get("number", 0) - 1
                if 0 <= idx < 4:
                    self._device_status.relay_states[idx] = relay.get("state", "off")

        self._device_status.online = True
        self._device_status.wifi_rssi = payload.get("wifi_rssi")
        self._device_status.last_updated = datetime.now(UTC)
        logger.info(f"Device {device_id} status updated: {self._device_status.relay_states}")

    async def _handle_heartbeat(self, device_id: str, payload: dict):
        """Handle device heartbeat."""
        self._device_status.online = True
        self._device_status.last_heartbeat = datetime.now(UTC)
        self._device_status.wifi_rssi = payload.get("wifi_rssi")
        logger.debug(f"Heartbeat from {device_id}: RSSI={payload.get('wifi_rssi')}")

    async def _handle_ack(self, device_id: str, payload: dict):
        """Handle command acknowledgment."""
        command_id = payload.get("command_id")
        success = payload.get("success")
        message = payload.get("message", "")
        logger.info(f"ACK for {command_id}: success={success}, message={message}")

    async def _handle_executed(self, device_id: str, payload: dict):
        """Handle scheduled command execution."""
        command_id = payload.get("command_id")
        relay_number = payload.get("relay_number")
        state = payload.get("state")
        logger.info(f"Executed schedule {command_id}: relay {relay_number} -> {state}")

        # Update cached state
        if relay_number and 1 <= relay_number <= 4:
            self._device_status.relay_states[relay_number - 1] = state or "off"

        # Mark task as complete in database
        if command_id and self._task_complete_callback:
            try:
                await self._task_complete_callback(command_id)
                logger.info(f"Task marked complete for command {command_id}")
            except Exception as e:
                logger.error(f"Failed to mark task complete: {e}")

    async def _handle_sync_request(self, device_id: str, payload: dict):
        """Handle sync request from device.

        When ESP32 reconnects, it sends SYNC_REQ to get any pending schedules
        that were created while it was offline.
        """
        logger.info(f"Sync request from {device_id}")

        if not self._sync_callback:
            logger.warning("No sync callback set - cannot provide pending schedules")
            return

        try:
            # Get pending schedules via callback
            pending = await self._sync_callback()
            logger.info(f"Found {len(pending)} pending schedules to sync")

            # Send each pending schedule
            for schedule in pending:
                result = await self.publish_schedule(
                    relay_number=schedule["relay_number"],
                    action=schedule["action"],
                    scheduled_time=schedule["scheduled_time"],
                    device_name=schedule.get("device_name"),
                    device_id=device_id,
                )
                if result["success"]:
                    logger.info(f"Synced schedule {schedule['command_id']} to {device_id}")
                else:
                    logger.error(f"Failed to sync schedule {schedule['command_id']}: {result.get('error')}")

            # Send sync complete acknowledgment
            topic = f"{TOPIC_BASE}/{device_id}/commands"
            ack_payload = {
                "type": "SYNC_COMPLETE",
                "count": len(pending),
            }
            await self._client.publish(topic, json.dumps(ack_payload))
            logger.info(f"Sync complete - sent {len(pending)} schedules to {device_id}")

        except Exception as e:
            logger.error(f"Error handling sync request: {e}")

    async def publish_immediate(
        self,
        relay_number: int,
        action: str,
        device_id: str = DEFAULT_DEVICE_ID,
    ) -> dict[str, Any]:
        """Send immediate command to device.

        Args:
            relay_number: Relay number (1-4)
            action: Action to perform (on, off, toggle)
            device_id: Target device ID

        Returns:
            Result dict with success, command_id, message
        """
        if not self._connected:
            return {
                "success": False,
                "error": "MQTT not connected",
            }

        if relay_number < 1 or relay_number > 4:
            return {
                "success": False,
                "error": "Relay number must be 1-4",
            }

        if action not in ["on", "off", "toggle"]:
            return {
                "success": False,
                "error": "Action must be on, off, or toggle",
            }

        command_id = str(uuid4())
        topic = f"{TOPIC_BASE}/{device_id}/commands"

        payload = {
            "type": "IMMEDIATE",
            "command_id": command_id,
            "relay_number": relay_number,
            "action": action,
        }

        try:
            await self._client.publish(topic, json.dumps(payload))
            relay_name = RELAY_NAMES.get(relay_number, f"Relay {relay_number}")
            logger.info(f"Published IMMEDIATE command {command_id}: {relay_name} -> {action}")

            return {
                "success": True,
                "command_id": command_id,
                "relay_name": relay_name,
                "action": action,
                "message": f"Sent {action} command to {relay_name}",
            }
        except Exception as e:
            logger.error(f"Failed to publish MQTT command: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def publish_schedule(
        self,
        relay_number: int,
        action: str,
        scheduled_time: int,
        device_name: Optional[str] = None,
        device_id: str = DEFAULT_DEVICE_ID,
    ) -> dict[str, Any]:
        """Send schedule command to device.

        Args:
            relay_number: Relay number (1-4)
            action: Action to perform (on, off, toggle)
            scheduled_time: Unix timestamp for execution
            device_name: Friendly name for display on LCD
            device_id: Target device ID

        Returns:
            Result dict with success, command_id, message
        """
        if not self._connected:
            return {
                "success": False,
                "error": "MQTT not connected",
            }

        if relay_number < 1 or relay_number > 4:
            return {
                "success": False,
                "error": "Relay number must be 1-4",
            }

        command_id = str(uuid4())
        topic = f"{TOPIC_BASE}/{device_id}/commands"
        relay_name = device_name or RELAY_NAMES.get(relay_number, f"Relay {relay_number}")

        # Sanitize device name for LCD display (ASCII only, max 16 chars)
        lcd_device_name = sanitize_for_lcd(relay_name, 16)

        payload = {
            "type": "SCHEDULE",
            "command_id": command_id,
            "relay_number": relay_number,
            "action": action,
            "scheduled_time": scheduled_time,
            "device_name": lcd_device_name,
        }

        try:
            await self._client.publish(topic, json.dumps(payload))
            logger.info(f"Published SCHEDULE command {command_id}: {relay_name} -> {action} at {scheduled_time}")

            return {
                "success": True,
                "command_id": command_id,
                "relay_name": relay_name,
                "action": action,
                "scheduled_time": scheduled_time,
                "message": f"Scheduled {relay_name} to {action} at timestamp {scheduled_time}",
            }
        except Exception as e:
            logger.error(f"Failed to publish MQTT schedule: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def cancel_schedule(
        self,
        command_id: str,
        device_id: str = DEFAULT_DEVICE_ID,
    ) -> dict[str, Any]:
        """Cancel a scheduled command.

        Args:
            command_id: Command ID to cancel
            device_id: Target device ID

        Returns:
            Result dict with success, message
        """
        if not self._connected:
            return {
                "success": False,
                "error": "MQTT not connected",
            }

        topic = f"{TOPIC_BASE}/{device_id}/commands"

        payload = {
            "type": "CANCEL",
            "command_id": command_id,
        }

        try:
            await self._client.publish(topic, json.dumps(payload))
            logger.info(f"Published CANCEL for command {command_id}")

            return {
                "success": True,
                "command_id": command_id,
                "message": f"Cancellation request sent for {command_id}",
            }
        except Exception as e:
            logger.error(f"Failed to publish MQTT cancel: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def request_status(
        self,
        device_id: str = DEFAULT_DEVICE_ID,
        force: bool = False,
    ) -> dict[str, Any]:
        """Request current status from device.

        Args:
            device_id: Target device ID
            force: If True, bypass rate limiting

        Returns:
            Cached device status (status request is sent but response is async)
        """
        now = datetime.now(UTC)

        # Rate limiting: only send STATUS_REQ if cooldown has passed
        should_request = force or (
            self._last_status_request is None or
            (now - self._last_status_request).total_seconds() >= self.STATUS_REQUEST_COOLDOWN
        )

        if self._connected and self._client and should_request:
            topic = f"{TOPIC_BASE}/{device_id}/commands"
            payload = {
                "type": "STATUS_REQ",
                "command_id": str(uuid4()),
            }
            try:
                await self._client.publish(topic, json.dumps(payload))
                self._last_status_request = now
                logger.info(f"Requested status from {device_id}")
            except Exception as e:
                logger.error(f"Failed to request status: {e}")
        elif not should_request:
            logger.debug(f"Status request rate-limited (cooldown: {self.STATUS_REQUEST_COOLDOWN}s)")

        # Return cached status
        return self._device_status.to_dict()


# Singleton instance
_mqtt_service: Optional[MQTTService] = None


def get_mqtt_service() -> MQTTService:
    """Get the MQTT service singleton.

    Returns:
        MQTTService instance (may not be connected)
    """
    global _mqtt_service
    if _mqtt_service is None:
        _mqtt_service = MQTTService()
    return _mqtt_service


async def start_mqtt_service() -> MQTTService:
    """Start the MQTT service (call from FastAPI lifespan).

    Returns:
        Started MQTTService instance
    """
    service = get_mqtt_service()
    if await service.connect():
        await service.start_listening()
    return service


async def stop_mqtt_service():
    """Stop the MQTT service (call from FastAPI lifespan)."""
    global _mqtt_service
    if _mqtt_service:
        await _mqtt_service.disconnect()
        _mqtt_service = None
