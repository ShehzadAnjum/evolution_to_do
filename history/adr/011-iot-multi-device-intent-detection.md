# ADR-011: IoT Multi-Device Intent Detection Pattern

## Status
**Accepted** - 2025-12-19

## Context
The Evolution Todo application includes IoT device control via MQTT. Users can control individual relays (Light, Fan, Aquarium, Relay4) through chat commands. However, users often want to control ALL devices at once based on context:

- Going out → Turn everything OFF
- Coming home → Turn everything ON
- Going to sleep → Turn everything OFF
- Party time → Turn everything ON

Initial implementation only turned off single devices because the LLM would only call `control_device` once.

## Decision
**Implement intent-based multi-device control through system prompt patterns**

### Approach
Instead of creating a new `control_all_devices` tool, instruct the LLM to call `control_device` 4 times (once per relay) when detecting multi-device intent patterns.

### System Prompt Addition
```
MULTI-DEVICE CONTROL → Call control_device 4 times (relay 1,2,3,4)

ALL OFF triggers - turn off ALL 4 relays (1,2,3,4):
- "going out", "leaving", "ghar se bahar", "dooston ke saath"
- "goodnight", "so raha hoon", "energy saving"
- Urdu: "باہر جا رہا", "گھر سے باہر", "سو رہا ہوں"

ALL ON triggers - turn on ALL 4 relays (1,2,3,4):
- "I'm home", "ghar aa gaya", "party time", "make it lively"
- Urdu: "گھر آ گیا", "واپس آ گیا"

For multi-device: You MUST call control_device 4 SEPARATE times
```

### Why Not a New Tool?
1. **Simplicity**: No new tool implementation needed
2. **Flexibility**: Patterns can be added without code changes
3. **LLM Capability**: OpenAI supports parallel function calls
4. **Consistency**: Same tool, same MQTT handling

### Language Coverage
| Language | ALL OFF Examples | ALL ON Examples |
|----------|------------------|-----------------|
| English | "going out", "goodnight" | "I'm home", "party time" |
| Roman Urdu | "ghar se bahar", "so raha hoon" | "ghar aa gaya" |
| Urdu Script | "باہر جا رہا ہوں" | "گھر آ گیا ہوں" |

## Consequences

### Positive
- No new code needed (just system prompt update)
- Bilingual support (English, Roman Urdu, Urdu Script)
- Extensible patterns without deployment
- Works with existing MCP tool infrastructure

### Negative
- Relies on LLM correctly interpreting instructions
- May need prompt tuning if LLM calls tool once instead of four times
- Pattern list can grow large over time

### Validation
User says: "dooston ke saath ja raha hoon" (going out with friends)
Expected: LLM calls control_device 4 times with action="off" for relays 1,2,3,4
Result: All devices turn off

## References
- `.claude/skills/iot-mqtt-integration/SKILL.md` - Full IoT integration patterns
- `backend/src/services/chat_service.py` - System prompt with patterns
- `backend/src/mcp/server.py` - control_device tool definition
