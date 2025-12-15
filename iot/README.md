# Evolution Todo - IoT Controller

ESP32-S3 based IoT controller for home automation integrated with Evolution Todo.

## Hardware

| Component | Model | Interface |
|-----------|-------|-----------|
| Microcontroller | ESP32-S3-WROOM-1 (N16R8) | - |
| Display | 16x2 LCD with I2C backpack | I2C (0x27) |
| Relays | 4-channel relay module | GPIO (Active LOW) |

## Wiring

### I2C LCD (16x2)

| LCD Pin | ESP32-S3 Pin |
|---------|--------------|
| VCC | 5V |
| GND | GND |
| SDA | GPIO 8 |
| SCL | GPIO 9 |

### 4-Channel Relay Module

| Relay | ESP32-S3 Pin | Device |
|-------|--------------|--------|
| IN1 | GPIO 4 | Living Room Light |
| IN2 | GPIO 5 | Fan |
| IN3 | GPIO 6 | Aquarium Light |
| IN4 | GPIO 7 | Available |
| VCC | 5V | - |
| GND | GND | - |

**Note**: This relay module is **Active LOW** - the relay turns ON when the input pin is LOW.

## Setup Instructions

### 1. HiveMQ Cloud Setup

1. Go to [HiveMQ Cloud Console](https://console.hivemq.cloud/)
2. Sign up for free account
3. Create a new cluster (free tier)
4. Go to "Access Management" and create credentials:
   - Username: `evolution-todo`
   - Password: (generate a secure password)
5. Note your cluster URL (e.g., `abc123.s1.eu.hivemq.cloud`)

### 2. Arduino IDE Setup

1. Install Arduino IDE 2.x
2. Add ESP32 board support:
   - Go to File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Boards Manager
   - Search "ESP32" and install "esp32 by Espressif Systems"

3. Install required libraries (Tools → Manage Libraries):
   - `PubSubClient` by Nick O'Leary
   - `ArduinoJson` by Benoit Blanchon
   - `LiquidCrystal I2C` by Frank de Brabander

4. Select board:
   - Tools → Board → esp32 → ESP32S3 Dev Module
   - Tools → USB CDC On Boot → Enabled
   - Tools → Port → (select your ESP32 port)

### 3. Configure Credentials

1. Navigate to `iot/esp32/`
2. Copy `config_template.h` to `config.h`:
   ```bash
   cp config_template.h config.h
   ```
3. Edit `config.h` with your credentials:
   ```cpp
   #define WIFI_SSID     "YourWiFiName"
   #define WIFI_PASSWORD "YourWiFiPassword"

   #define MQTT_BROKER   "your-cluster.hivemq.cloud"
   #define MQTT_USERNAME "evolution-todo"
   #define MQTT_PASSWORD "your-mqtt-password"
   ```

### 4. Upload Sketch

1. Open `evolution_iot.ino` in Arduino IDE
2. Connect ESP32 via USB
3. Click Upload (→ button)
4. Open Serial Monitor (115200 baud) to see debug output

## Testing

### Test via MQTT Explorer

1. Download [MQTT Explorer](http://mqtt-explorer.com/)
2. Connect to your HiveMQ cluster:
   - Host: `your-cluster.hivemq.cloud`
   - Port: `8883`
   - Username/Password: your credentials
   - Enable SSL/TLS

3. Subscribe to topics:
   - `evolution-todo/devices/esp32-home/status`
   - `evolution-todo/devices/esp32-home/ack`

4. Publish test commands to `evolution-todo/devices/esp32-home/commands`:

**Turn on Relay 1 immediately:**
```json
{
  "type": "IMMEDIATE",
  "command_id": "test-001",
  "relay_number": 1,
  "action": "on"
}
```

**Turn off Relay 1:**
```json
{
  "type": "IMMEDIATE",
  "command_id": "test-002",
  "relay_number": 1,
  "action": "off"
}
```

**Toggle Relay 2:**
```json
{
  "type": "IMMEDIATE",
  "command_id": "test-003",
  "relay_number": 2,
  "action": "toggle"
}
```

**Schedule Relay 3 ON (replace timestamp with future Unix time):**
```json
{
  "type": "SCHEDULE",
  "command_id": "schedule-001",
  "relay_number": 3,
  "action": "on",
  "scheduled_time": 1734200000,
  "device_name": "Aquarium"
}
```

**Request status:**
```json
{
  "type": "STATUS_REQ",
  "command_id": "status-001"
}
```

## MQTT Topics

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `evolution-todo/devices/esp32-home/commands` | Backend → ESP32 | Send commands |
| `evolution-todo/devices/esp32-home/status` | ESP32 → Backend | Report status |
| `evolution-todo/devices/esp32-home/ack` | ESP32 → Backend | Acknowledge commands |

## Message Types

### Commands (Backend → ESP32)

| Type | Description |
|------|-------------|
| `IMMEDIATE` | Execute action now |
| `SCHEDULE` | Add scheduled action |
| `CANCEL` | Cancel scheduled action |
| `STATUS_REQ` | Request current status |
| `SYNC_REQ` | Request all schedules |

### Responses (ESP32 → Backend)

| Type | Description |
|------|-------------|
| `STATUS` | Current relay states |
| `ACK` | Command acknowledgment |
| `EXECUTED` | Scheduled command executed |
| `HEARTBEAT` | Periodic alive signal |

## Troubleshooting

### LCD not displaying

1. Check I2C address - try `0x3F` instead of `0x27`
2. Run I2C scanner sketch to find address
3. Verify wiring (SDA/SCL not swapped)
4. Check 5V power to LCD

### WiFi not connecting

1. Check SSID and password (case-sensitive)
2. Ensure 2.4GHz network (ESP32 doesn't support 5GHz)
3. Check router isn't blocking new devices

### MQTT not connecting

1. Verify HiveMQ credentials
2. Check cluster URL (no `https://` prefix)
3. Port should be 8883 (TLS)
4. Check Serial Monitor for error codes

### Relays not switching

1. Check wiring to correct GPIO pins
2. Verify 5V power to relay module
3. Remember: Active LOW (LOW = ON, HIGH = OFF)
4. Test with simple digitalWrite sketch first

## LCD Display

The LCD shows:
```
Line 1: HH:MM:SS    OK    (time and connection status)
Line 2: 1:OFF 2:OFF 3:ON   (relay states)
```

Connection indicators:
- `OK` = MQTT connected
- `WF` = WiFi only (MQTT disconnected)
- `--` = Offline

## Next Steps

After testing standalone:
1. Integrate with Evolution Todo backend
2. Add device management UI
3. Connect AI chat for voice commands

---

**Part of**: Evolution Todo Project
**Version**: 1.0.0
**Date**: 2025-12-14
