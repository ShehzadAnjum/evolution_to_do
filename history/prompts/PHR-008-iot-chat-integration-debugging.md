# PHR-008: IoT Chat Integration and Multi-Device Control

**Date**: 2025-12-19
**Phase**: V (IoT Enhancement)
**Duration**: ~4 hours (across session)
**Severity**: Medium (feature enhancement)

---

## Context

Integrating ESP32 IoT device control with the AI chat interface revealed several issues around device scheduling, multi-device control, and UI/UX improvements.

## Issues and Fixes

### Issue 1: ESP32 Shows Online When Offline

**Symptom**: MQTT status shows "ESP32: Online" even when device is powered off.

**Root Cause**: Backend set `online = True` on receiving heartbeat but never checked for timeout.

**Fix**: Added computed `is_online` property with 45-second heartbeat timeout:
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

**File**: `backend/src/services/mqtt_service.py`

### Issue 2: LLM Chooses Wrong Tool for Scheduling

**Symptom**: User says "turn on light at 3am" but LLM calls `control_device` (immediate) instead of `schedule_device`.

**Root Cause**: Tool descriptions weren't explicit enough about when to use each tool.

**Fix**: Added critical decision rule to system prompt:
```
CRITICAL DECISION RULE:
- ANY time reference → ALWAYS use schedule_device
- NO time reference → use control_device
```

**File**: `backend/src/services/chat_service.py`

### Issue 3: Multi-Device Control Only Turns Off One Device

**Symptom**: User says "I'm going out" but only Light turns off, not all devices.

**Root Cause**: LLM only called `control_device` once, not understanding it needs to call 4 times.

**Fix**: Added explicit multi-device patterns with instruction to call tool 4 times:
```
MULTI-DEVICE CONTROL → Call control_device 4 times (relay 1,2,3,4)

ALL OFF triggers: "going out", "ghar se bahar", "dooston ke saath"...
ALL ON triggers: "I'm home", "ghar aa gaya", "party time"...

For multi-device: You MUST call control_device 4 SEPARATE times
```

**File**: `backend/src/services/chat_service.py`

### Issue 4: OpenAI API Error 400 - Orphaned Tool Messages

**Symptom**: "Invalid parameter: messages with role 'tool' must be a response to a preceeding message with 'tool_calls'"

**Root Cause**: Database had historical tool messages without matching assistant `tool_calls` (orphaned).

**Fix**: Filter orphaned tool messages during retrieval:
```python
valid_tool_call_ids: set[str] = set()
for msg in db_messages:
    if msg.role == "assistant" and msg.tool_calls:
        # Track valid tool call IDs
        for tc in json.loads(msg.tool_calls):
            valid_tool_call_ids.add(tc["id"])
    elif msg.role == "tool":
        if msg.tool_call_id not in valid_tool_call_ids:
            logger.warning(f"Skipping orphaned tool message: {msg.tool_call_id}")
            continue  # Skip orphaned messages
```

**File**: `backend/src/services/chat_service.py`

### Issue 5: Time Calculation "3AM Today" Wrong at 1:48 AM

**Symptom**: At 01:48 AM, user says "3AM today" but LLM says "time has passed".

**Root Cause**: Using `datetime.utcnow()` in backend, so UTC time (previous day) was being compared.

**Fix**: Changed to `datetime.now()` for local time comparisons and added current time to system prompt:
```python
now = datetime.now()
current_time = now.strftime("%H:%M")
return f"TODAY: {today}, CURRENT TIME: {current_time}"
```

**Files**: `backend/src/services/chat_service.py`, `backend/src/mcp/tools/tool_executor.py`

### Issue 6: Chat Timestamps Display Wrong Time

**Symptom**: Message timestamps in chat UI showing incorrect time.

**Root Cause**: Using deprecated `datetime.utcnow()` which creates naive datetime.

**Fix**: Changed to `datetime.now(UTC)` for timezone-aware timestamps:
```python
from datetime import datetime, UTC
created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
```

**Files**: `backend/src/models/message.py`, `backend/src/models/conversation.py`

## UI/UX Improvements Made

### Optimistic Message Display
User message appears immediately before API call (rollback on error).

### Auto-Scroll
New messages scroll into view using React refs:
```typescript
const messagesEndRef = useRef<HTMLDivElement>(null);
useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages.length]);
```

### Empty Conversation Cleanup
Auto-delete conversations with 0 messages on load.

### TTS Emoji Stripping
Remove emojis and box-drawing characters before speech synthesis.

### MQTT Status Indicator
- Bright text when online, dull when offline
- Rotating spinner during refresh (minimum 500ms visibility)

## Key Learnings

### 1. Heartbeat Timeout Pattern
Always check elapsed time, not just "last received" flag:
```python
elapsed = (datetime.now() - last_heartbeat).total_seconds()
is_online = elapsed < TIMEOUT
```

### 2. LLM Tool Selection
Explicit decision rules in system prompt work better than vague descriptions:
```
❌ "Use schedule_device for scheduling"
✅ "IF ANY time reference → use schedule_device"
```

### 3. Multi-Tool Calls
When LLM needs to call same tool multiple times, be very explicit:
```
❌ "Control all devices"
✅ "You MUST call control_device 4 SEPARATE times"
```

### 4. Datetime in Python 3.12+
```python
# ❌ Deprecated
datetime.utcnow()

# ✅ Correct
datetime.now(UTC)
```

### 5. Filter, Don't Crash
When encountering invalid database state, filter and log rather than crashing:
```python
if invalid:
    logger.warning(f"Skipping invalid record: {id}")
    continue
```

## Files Changed

| File | Changes |
|------|---------|
| `backend/src/services/chat_service.py` | Multi-device patterns, time fixes, orphan filtering |
| `backend/src/services/mqtt_service.py` | `is_online` computed property |
| `backend/src/api/routes/devices.py` | Use computed `is_online` |
| `backend/src/mcp/server.py` | Clearer tool descriptions |
| `backend/src/mcp/tools/tool_executor.py` | Local time for comparisons |
| `backend/src/models/message.py` | Timezone-aware datetime |
| `backend/src/models/conversation.py` | Timezone-aware datetime |
| `frontend/components/mqtt-status.tsx` | Spinner, bright/dull styling |
| `frontend/components/chat/chatkit-panel.tsx` | Optimistic UI, auto-scroll |
| `frontend/lib/voice/api.ts` | Emoji stripping for TTS |

## Related Resources

- ADR-011: IoT Multi-Device Intent Detection
- Skill: `.claude/skills/iot-mqtt-integration/SKILL.md`
- Skill: `.claude/skills/esp32-wifi-troubleshooting.md`

---

**Tags**: #iot #mqtt #esp32 #chat #openai #datetime #debugging
