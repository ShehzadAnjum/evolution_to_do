# ADR 009: Browser Notifications Architecture

**Status**: Accepted
**Date**: 2025-12-13
**Decision Makers**: Development Team
**Phase**: Phase V Part A (Advanced Features)

## Context

The task management app needs reminder notifications when tasks are due. Users expect to be notified at the scheduled due time with both visual and audio alerts.

### Requirements
1. Notify user at task due time
2. Play alert sound
3. Visual bell animation
4. 15-minute early warning
5. Work without backend involvement

### Constraints
1. Must work in browser (no native app)
2. No paid notification services
3. Minimal backend changes

## Decision

We will use **Browser-Native Notifications with setTimeout Scheduling**:

```
User grants permission → Task loads → setTimeout schedules notification
                                    → At due time: Browser Notification + Web Audio bell sound
```

### Architecture Components

1. **Notification API** (Browser Native)
   - `Notification.requestPermission()` for user consent
   - `new Notification(title, options)` for display
   - `requireInteraction: true` for persistent alerts

2. **setTimeout Scheduling**
   - Calculate `msUntilDue = dueDateTime - Date.now()`
   - Schedule notification at exact time
   - Schedule 15-min early warning

3. **Web Audio API for Sound**
   - Generate bell sound with oscillators
   - Harmonics: 800Hz + 1200Hz + 1600Hz
   - Continuous ringing until dismissed

4. **CSS Animation for Visual**
   - Bell icon vibrates when ringing
   - Yellow highlight on button during alarm

### Key Design Decisions

1. **Shared AudioContext**: Browsers limit AudioContext instances (~6). Reuse single instance.

2. **Continuous Alarm**: Sound/animation loops for 10 seconds or until user clicks to stop.

3. **Client-Side Only**: No backend notification service - keeps it simple and free.

4. **Tab Must Be Open**: Critical limitation - setTimeout only fires when tab is active.

## Consequences

### Positive
- Zero cost (no paid services)
- No backend changes for notifications
- Instant setup (browser native)
- Works offline (once scheduled)

### Negative
- **Tab must stay open** - notifications won't fire if tab closed
- Limited to browser capabilities
- No mobile push notifications
- Sound requires user interaction first (autoplay policy)

### Neutral
- Requires user permission grant
- Different behavior across browsers

## Alternatives Considered

### 1. Service Workers + Push API
**Pros**: Works when tab closed, true background notifications
**Cons**: Requires backend push service, more complex setup, needs VAPID keys
**Decision**: Deferred to future - overkill for current scope

### 2. Web Workers for Scheduling
**Pros**: Runs in background thread
**Cons**: Still requires tab open, doesn't solve core limitation
**Decision**: No benefit over setTimeout

### 3. Third-Party Services (OneSignal, Firebase)
**Pros**: Full push notification support, mobile support
**Cons**: External dependency, potential costs, privacy concerns
**Decision**: Against project's self-contained philosophy

## Implementation

### Files Created/Modified
- `frontend/lib/notifications.ts` - Core notification service
- `frontend/app/globals.css` - Bell animation CSS
- `frontend/app/(dashboard)/tasks/page.tsx` - UI integration

### Key Code Patterns

```typescript
// Shared AudioContext (CRITICAL - browsers limit instances)
let sharedAudioContext: AudioContext | null = null;
function getAudioContext() {
  if (!sharedAudioContext) {
    sharedAudioContext = new AudioContext();
  }
  if (sharedAudioContext.state === 'suspended') {
    sharedAudioContext.resume();
  }
  return sharedAudioContext;
}

// Schedule notification
const msUntilDue = dueDateTime.getTime() - Date.now();
if (msUntilDue > 0) {
  setTimeout(() => showNotification(task), msUntilDue);
}
```

## Future Considerations

For true background notifications (Phase V Part C or later):
1. Implement Service Worker with Push API
2. Add backend notification scheduling service
3. Store VAPID keys for web push
4. Consider mobile app for native notifications

## References

- MDN: Notification API
- MDN: Web Audio API
- SESSION_HANDOFF.md: Reusable Knowledge section
- `.claude/skills/browser-notifications.md`
