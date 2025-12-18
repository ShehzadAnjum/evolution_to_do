# IoT MQTT Integration Skill

## Overview

This skill documents patterns for integrating IoT devices (ESP32) with a web application using MQTT and AI chat interface.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│   Backend    │────▶│  HiveMQ     │────▶│   ESP32     │
│  (Chat UI)  │     │  (FastAPI)   │     │   Cloud     │     │  (Relays)   │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                   │                                        │
       │                   │                                        │
       ▼                   ▼                                        ▼
   User Intent      OpenAI + MCP Tools                      Physical Devices
                    (control_device,                        (Light, Fan, etc.)
                     schedule_device)
```

## Key Components

### 1. MQTT Service (Backend)

```python
# backend/src/services/mqtt_service.py
import ssl
import aiomqtt
from datetime import datetime, UTC

class DeviceStatus:
    HEARTBEAT_TIMEOUT = 45  # seconds (ESP32 sends every 30s)

    def __init__(self):
        self.online = False
        self.last_heartbeat: datetime | None = None
        self.wifi_rssi: int | None = None
        self.relays: dict[int, bool] = {1: False, 2: False, 3: False, 4: False}

    @property
    def is_online(self) -> bool:
        """Check if device is online based on heartbeat timeout."""
        if not self.last_heartbeat:
            return False
        elapsed = (datetime.now(UTC) - self.last_heartbeat).total_seconds()
        return elapsed < self.HEARTBEAT_TIMEOUT

class MQTTService:
    def __init__(self, broker: str, port: int, username: str, password: str):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client: aiomqtt.Client | None = None
        self.device_status = DeviceStatus()

    async def connect(self):
        """Connect with TLS to HiveMQ Cloud."""
        tls_context = ssl.create_default_context()
        self.client = aiomqtt.Client(
            hostname=self.broker,
            port=self.port,
            username=self.username,
            password=self.password,
            tls_context=tls_context,
        )
        await self.client.__aenter__()

    async def publish_command(self, relay: int, action: str):
        """Publish immediate device command."""
        topic = "evo-todo/esp32-home/command"
        payload = json.dumps({
            "type": "IMMEDIATE",
            "relay": relay,
            "action": action.upper(),  # "ON", "OFF", "TOGGLE"
        })
        await self.client.publish(topic, payload.encode())

    async def publish_schedule(self, relay: int, action: str, timestamp: str, name: str):
        """Publish scheduled device command."""
        topic = "evo-todo/esp32-home/command"
        payload = json.dumps({
            "type": "SCHEDULE",
            "relay": relay,
            "action": action.upper(),
            "timestamp": timestamp,  # ISO format
            "name": name,
        })
        await self.client.publish(topic, payload.encode())
```

### 2. MCP Tools for Device Control

```python
# backend/src/mcp/server.py - Tool definitions
DEVICE_TOOLS = [
    {
        "name": "control_device",
        "description": "Control IoT device IMMEDIATELY. ONLY use when NO time mentioned.",
        "parameters": {
            "type": "object",
            "properties": {
                "relay_number": {
                    "type": "integer",
                    "description": "1=Light, 2=Fan, 3=Aquarium, 4=Relay4"
                },
                "action": {
                    "type": "string",
                    "enum": ["on", "off", "toggle"]
                }
            },
            "required": ["relay_number", "action"]
        }
    },
    {
        "name": "schedule_device",
        "description": "Schedule device for FUTURE time. Use when ANY time mentioned.",
        "parameters": {
            "type": "object",
            "properties": {
                "relay_number": {"type": "integer"},
                "action": {"type": "string", "enum": ["on", "off"]},
                "due_date": {"type": "string", "description": "YYYY-MM-DD"},
                "due_time": {"type": "string", "description": "HH:MM 24-hour"},
                "recurrence_pattern": {"type": "string", "enum": ["none", "daily", "weekly"]},
                "weekday": {"type": "string", "description": "For weekly: monday, tuesday, etc."}
            },
            "required": ["relay_number", "action", "due_date", "due_time"]
        }
    },
    {
        "name": "device_status",
        "description": "Get current device status including relay states.",
        "parameters": {"type": "object", "properties": {}}
    }
]
```

### 3. Multi-Device Intent Detection

The AI assistant detects user intent for controlling multiple devices at once:

#### ALL OFF Triggers (turn off relays 1,2,3,4)
- English: "energy saving", "going out", "leaving home", "goodnight", "sleep mode"
- Roman Urdu: "ghar se bahar", "bahar ja raha", "dooston ke saath", "so raha hoon"
- Urdu Script: "باہر جا رہا", "گھر سے باہر", "سو رہا ہوں"

#### ALL ON Triggers (turn on relays 1,2,3,4)
- English: "I'm home", "back home", "party time", "make it lively", "welcome mode"
- Roman Urdu: "ghar aa gaya", "wapas aa gaya", "sab chalu karo"
- Urdu Script: "گھر آ گیا", "واپس آ گیا"

#### System Prompt Pattern
```
MULTI-DEVICE CONTROL → Call control_device 4 times (relay 1,2,3,4)

When user is LEAVING HOME or GOING TO SLEEP → ALL OFF
When user is COMING HOME or WAKING UP → ALL ON

For multi-device: You MUST call control_device 4 SEPARATE times:
1. control_device(relay_number=1, action="off/on")
2. control_device(relay_number=2, action="off/on")
3. control_device(relay_number=3, action="off/on")
4. control_device(relay_number=4, action="off/on")
```

### 4. Immediate vs Scheduled Decision Rule

```
CRITICAL DECISION RULE:

IF message contains ANY time reference:
   - "at 3am", "at 6pm", "7 baje", "shaam ko"
   - "tomorrow", "kal", "daily", "har rouz"
   - "every friday", "har jumma"
   → ALWAYS use schedule_device

IF message has NO time reference:
   - "turn on light", "fan off karo"
   → Use control_device for immediate action
```

### 5. Device Heartbeat Detection

```python
class DeviceStatus:
    HEARTBEAT_TIMEOUT = 45  # ESP32 sends every 30s, allow 15s grace

    @property
    def is_online(self) -> bool:
        if not self.last_heartbeat:
            return False
        elapsed = (datetime.now(UTC) - self.last_heartbeat).total_seconds()
        return elapsed < self.HEARTBEAT_TIMEOUT
```

## Frontend Integration

### MQTT Status Indicator
```typescript
// Show spinner during refresh (minimum 500ms for visibility)
const [refreshing, setRefreshing] = useState(false);

const fetchHealth = async (showRefreshing = false) => {
  if (showRefreshing) setRefreshing(true);

  const [res] = await Promise.all([
    fetch(`/api/devices/health`),
    showRefreshing ? new Promise(r => setTimeout(r, 500)) : Promise.resolve(),
  ]);
  // ...
  setRefreshing(false);
};

// Bright when online, dull when offline
<span className={deviceOnline ? "text-foreground font-medium" : "text-muted-foreground"}>
  ESP32: {deviceOnline ? "Online" : "Offline"}
</span>
```

### Task Refresh on Device Tools
```typescript
// Refresh tasks when device tools are called
const taskTools = [
  "add_task", "update_task", "delete_task",
  "schedule_device", "control_device"  // Include device tools!
];

if (assistantMessage.tool_calls?.some(tc => taskTools.includes(tc.function.name))) {
  await refreshTasks();
}
```

## ESP32 Side

### MQTT Topics
- `evo-todo/esp32-home/command` - Receives commands from backend
- `evo-todo/esp32-home/status` - Publishes heartbeat and status
- `evo-todo/esp32-home/ack` - Acknowledges commands

### Command Payload Format
```json
// Immediate command
{
  "type": "IMMEDIATE",
  "relay": 1,
  "action": "ON"
}

// Scheduled command
{
  "type": "SCHEDULE",
  "relay": 2,
  "action": "OFF",
  "timestamp": "2025-12-19T18:00:00",
  "name": "Turn off fan at 6pm"
}
```

### Heartbeat Payload
```json
{
  "online": true,
  "wifi_rssi": -45,
  "relays": [true, false, false, false],
  "timestamp": "2025-12-19T02:30:00"
}
```

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Device shows online when offline | No heartbeat timeout check | Use computed `is_online` property with 45s timeout |
| Scheduled command runs immediately | LLM chose wrong tool | Add clear decision rule in system prompt |
| Multi-device only controls one | LLM calls tool once | Explicitly instruct: call 4 times for 4 relays |
| Device schedules not in task list | Frontend not refreshing | Add device tools to taskTools refresh list |

## Environment Variables

```bash
# Backend
MQTT_BROKER=xxx.hivemq.cloud
MQTT_PORT=8883
MQTT_USERNAME=esp32user
MQTT_PASSWORD=your-password
```

## References

- [HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/)
- [aiomqtt Python library](https://sbtinstruments.github.io/aiomqtt/)
- [ESP32 MQTT Example](https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/)
