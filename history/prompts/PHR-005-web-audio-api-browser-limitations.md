# PHR-005: Web Audio API Browser Limitations

## Date
2025-12-13

## Context
Implementing continuous bell sound for task notifications using Web Audio API.

## Problem Statement
Bell sound played once but didn't repeat - interval was firing but no sound after first chime.

## Approaches Tried

### Attempt 1: New AudioContext Per Chime
**Action**: Create fresh `AudioContext` for each `playBellChime()` call
```typescript
async function playBellChime() {
  const ctx = new AudioContext();
  // ... play sound
  setTimeout(() => ctx.close(), 1000);
}
```
**Result**: First chime played, subsequent chimes silent
**Learning**: Browsers limit AudioContext instances (~6 in Chrome)

### Attempt 2: Async/Await with Resume
**Action**: Made function async, awaited `ctx.resume()`
```typescript
async function playBellChime() {
  const ctx = new AudioContext();
  if (ctx.state === 'suspended') {
    await ctx.resume();
  }
  // ... play sound
}
```
**Result**: Still only first chime played
**Learning**: Creating new contexts still hits the limit, resume doesn't help

### Attempt 3: Shared AudioContext (SUCCESS)
**Action**: Reuse single AudioContext instance across all chimes
```typescript
let sharedAudioContext: AudioContext | null = null;

function getAudioContext(): AudioContext | null {
  if (!sharedAudioContext) {
    sharedAudioContext = new AudioContext();
    console.log('Created shared AudioContext');
  }
  if (sharedAudioContext.state === 'suspended') {
    sharedAudioContext.resume();
  }
  return sharedAudioContext;
}

function playBellChime() {
  const ctx = getAudioContext();
  // ... play sound using shared context
}
```
**Result**: All chimes play correctly, continuous sound works

## Root Causes Identified

### 1. AudioContext Instance Limit
Browsers limit concurrent `AudioContext` instances (typically 6 in Chrome). Creating a new context for each sound quickly exhausts this limit, causing subsequent sounds to fail silently.

### 2. No Error Thrown
When the limit is reached, browsers don't throw an error - they just fail to create a working context or the context gets auto-closed. This makes debugging difficult.

### 3. Suspended State After Inactivity
Even a reused AudioContext can become `suspended` if idle. Always check and call `resume()` before playing.

## Solution Pattern

```typescript
// CORRECT: Shared AudioContext pattern
let sharedAudioContext: AudioContext | null = null;

function getAudioContext(): AudioContext | null {
  if (typeof window === 'undefined') return null;

  if (!sharedAudioContext) {
    sharedAudioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  }

  // Resume if suspended (browser autoplay policy)
  if (sharedAudioContext.state === 'suspended') {
    sharedAudioContext.resume();
  }

  return sharedAudioContext;
}

// Play sound using shared context
function playSound() {
  const ctx = getAudioContext();
  if (!ctx) return;

  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();
  oscillator.connect(gain);
  gain.connect(ctx.destination);
  // ... configure and play
}
```

## Key Learnings

1. **NEVER create AudioContext per sound** - Reuse a single shared instance
2. **Always check for `suspended` state** - Browser autoplay policy can suspend context
3. **Use `webkitAudioContext` fallback** - Safari compatibility
4. **Silent failures are common** - Add console logging for debugging
5. **Context lives for page lifetime** - Don't close it unless page unloads

## Error Signals (No Explicit Errors!)

| Symptom | Cause | Fix |
|---------|-------|-----|
| First sound plays, rest silent | AudioContext limit hit | Use shared context |
| No sound at all | Context suspended | Call `resume()` |
| Sound works then stops | Context auto-suspended | Check state before each play |
| Works in dev, fails in prod | Different browser limits | Always use shared pattern |

## Testing Checklist

```markdown
- [ ] First sound plays
- [ ] Second sound plays (same context)
- [ ] Sound after 10+ second pause (context may suspend)
- [ ] Sound in Chrome, Firefox, Safari
- [ ] Console shows context creation only once
```

## Related

- ADR-009: Browser Notifications Architecture
- `.claude/skills/browser-notifications.md`
- MDN: AudioContext
