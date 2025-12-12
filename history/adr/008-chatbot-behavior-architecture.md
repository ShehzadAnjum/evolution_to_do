# ADR 008: Chatbot Behavior Architecture

**Status**: Accepted
**Date**: 2025-12-12
**Decision Makers**: Development Team
**Phase**: Phase III (AI Chatbot)

## Context

The task management chatbot needs a well-defined behavioral architecture to ensure:
1. Consistent language handling (English + Urdu/Roman Urdu)
2. Accurate intent detection across multiple layers
3. Intelligent task relationship inference
4. Reliable result verification
5. Proper response formatting

Previous iterations had scattered rules across multiple files, leading to inconsistent behavior and difficult maintenance.

## Decision

We will implement a **5-layer processing architecture** for the chatbot:

```
Layer 1: Language Detection
Layer 2: Task Context Loading (MANDATORY)
Layer 3: Intent Detection (3-tier: Explicit → Implicit → Contextual)
Layer 4: Action Execution with Verification
Layer 5: Response Generation
```

### Key Architectural Decisions

1. **Single Source of Truth**: All behavioral rules consolidated in `.claude/subagents/chat-agent-behavior-tuner.md`

2. **Mandatory Task Awareness**: Every response MUST be preceded by `list_tasks()` call

3. **Three-Tier Intent Detection**:
   - Explicit: Direct commands ("add task", "delete")
   - Implicit: Inferred from action words ("buy milk" → ADD)
   - Contextual: Inferred from situation ("feeling sick" → travel tasks affected)

4. **Language Matching Rules**:
   - English input → English response
   - Roman Urdu input → Urdu script response (NEVER Roman Urdu output)
   - Current message only (ignore conversation history for language)

5. **Task Relationship Groups**: TRAVEL, HEALTH, WORK, SHOPPING, EVENTS

6. **Verification Requirement**: Every tool result must be checked before reporting

## Consequences

### Positive
- Deterministic, predictable chatbot behavior
- Easier debugging (clear processing layers)
- Maintainable single source of truth
- Clear failure conditions defined
- Scalable pattern for future enhancements

### Negative
- More complex initial setup
- Requires strict adherence to spec
- May need tuning iterations

### Neutral
- Learning curve for understanding the architecture
- Regular updates to spec as edge cases discovered

## Alternatives Considered

1. **Simple system prompt**: Too fragile, rules scattered
2. **Hard-coded logic**: Less flexible, harder to tune
3. **ML-based intent**: Overkill for current scope, less deterministic

## Implementation

- **Specification**: `.claude/subagents/chat-agent-behavior-tuner.md` (v2.0.0)
- **Implementation**: `backend/src/services/chat_service.py` (system prompt)
- **Parent Agent**: `.claude/agents/ai-mcp.md`

## References

- Chat Agent Behavior Tuner Subagent v2.0.0
- AI MCP Agent v1.1.0
- Original CHATBOT_FINETUNING.md (now archived)
