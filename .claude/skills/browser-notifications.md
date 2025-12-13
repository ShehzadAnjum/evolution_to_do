# Skill: Browser Notifications

**Version**: 1.0.0
**Created**: 2025-12-13
**Category**: Frontend / UX

## Overview

Patterns for implementing browser notifications with sound and visual alerts in web applications.

## When to Use

- Task reminders at scheduled times
- Alert notifications requiring user attention
- Timer/countdown completion alerts
- Any scenario needing audio-visual user alerts

## Core Patterns

### 1. Notification Permission Flow

```typescript
// Check support
export function isNotificationSupported(): boolean {
  return typeof window !== 'undefined' && 'Notification' in window;
}

// Get current permission
export function getNotificationPermission(): NotificationPermission | 'unsupported' {
  if (!isNotificationSupported()) return 'unsupported';
  return Notification.permission;
}

// Request permission (requires user gesture - button click)
export async function requestNotificationPermission(): Promise<NotificationPermission> {
  if (!isNotificationSupported()) return 'denied';
  return await Notification.requestPermission();
}
```

### 2. Show Notification

```typescript
export function showNotification(title: string, options?: NotificationOptions): Notification | null {
  if (!isNotificationSupported()) return null;
  if (Notification.permission !== 'granted') return null;

  return new Notification(title, {
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    requireInteraction: true,  // Stays until dismissed
    ...options,
  });
}
```

### 3. Schedule Notification with setTimeout

```typescript
interface SchedulableTask {
  id: string;
  title: string;
  due_date: string | null;  // YYYY-MM-DD
  due_time: string | null;  // HH:MM
  is_complete: boolean;
}

const scheduledNotifications = new Map<string, NodeJS.Timeout>();

export function scheduleTaskNotification(task: SchedulableTask): void {
  // Clear existing
  clearTaskNotification(task.id);

  // Skip if complete or no due date/time
  if (task.is_complete || !task.due_date || !task.due_time) return;

  // Parse date and time
  const [year, month, day] = task.due_date.split('-').map(Number);
  const [hours, minutes] = task.due_time.split(':').map(Number);
  const dueDateTime = new Date(year, month - 1, day, hours, minutes);

  const msUntilDue = dueDateTime.getTime() - Date.now();
  if (msUntilDue <= 0) return;  // Already past

  // Schedule notification
  const timeout = setTimeout(() => {
    showNotification(`Task Due: ${task.title}`, {
      body: `Your task is due now`,
      tag: task.id,
    });
    scheduledNotifications.delete(task.id);
  }, msUntilDue);

  scheduledNotifications.set(task.id, timeout);
}

export function clearTaskNotification(taskId: string): void {
  const timeout = scheduledNotifications.get(taskId);
  if (timeout) {
    clearTimeout(timeout);
    scheduledNotifications.delete(taskId);
  }
}
```

### 4. Web Audio API Bell Sound (Shared Context!)

```typescript
// CRITICAL: Reuse single AudioContext - browsers limit instances!
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

function playBellChime(): void {
  const ctx = getAudioContext();
  if (!ctx) return;

  const playTone = (freq: number, start: number, duration: number, volume: number) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.frequency.value = freq;
    osc.type = 'sine';

    // Bell envelope: quick attack, slow decay
    gain.gain.setValueAtTime(0, ctx.currentTime + start);
    gain.gain.linearRampToValueAtTime(volume, ctx.currentTime + start + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + start + duration);

    osc.start(ctx.currentTime + start);
    osc.stop(ctx.currentTime + start + duration);
  };

  // Bell harmonics: fundamental + overtones
  playTone(800, 0, 0.5, 0.3);      // Fundamental
  playTone(1200, 0, 0.4, 0.15);    // 2nd harmonic
  playTone(1600, 0, 0.3, 0.1);     // 3rd harmonic
  playTone(800, 0.3, 0.5, 0.25);   // Second ring
  playTone(1200, 0.3, 0.4, 0.12);
  playTone(1600, 0.3, 0.3, 0.08);
}
```

### 5. Continuous Alarm with Auto-Stop

```typescript
let isRinging = false;
let ringInterval: NodeJS.Timeout | null = null;
let ringTimeout: NodeJS.Timeout | null = null;

export function startBellRing(): void {
  if (isRinging) return;
  isRinging = true;

  // Play first chime immediately
  playBellChime();

  // Repeat every 1.5 seconds
  ringInterval = setInterval(() => {
    if (isRinging) playBellChime();
  }, 1500);

  // Auto-stop after 10 seconds
  ringTimeout = setTimeout(() => stopBellRing(), 10000);
}

export function stopBellRing(): void {
  if (!isRinging) return;
  isRinging = false;

  if (ringInterval) {
    clearInterval(ringInterval);
    ringInterval = null;
  }
  if (ringTimeout) {
    clearTimeout(ringTimeout);
    ringTimeout = null;
  }
}

export function toggleBellRing(): void {
  isRinging ? stopBellRing() : startBellRing();
}
```

### 6. CSS Bell Vibration Animation

```css
@keyframes bellRing {
  0%, 100% { transform: rotate(0deg); }
  5% { transform: rotate(20deg); }
  10% { transform: rotate(-18deg); }
  15% { transform: rotate(16deg); }
  20% { transform: rotate(-14deg); }
  25% { transform: rotate(12deg); }
  30% { transform: rotate(-10deg); }
  35% { transform: rotate(8deg); }
  40% { transform: rotate(-6deg); }
  45% { transform: rotate(4deg); }
  50% { transform: rotate(0deg); }
}

.animate-bell-ring {
  animation: bellRing 0.8s ease-in-out infinite;
  transform-origin: top center;
}
```

### 7. React Integration

```tsx
const [bellRinging, setBellRinging] = useState(false);
const [permission, setPermission] = useState<NotificationPermission>('default');

// Connect callbacks
useEffect(() => {
  setOnBellRing(
    () => setBellRinging(true),   // onStart
    () => setBellRinging(false)   // onStop
  );
  return () => setOnBellRing(null, null);
}, []);

// Bell button
<button
  onClick={() => {
    if (permission !== 'granted') {
      requestNotificationPermission().then(setPermission);
    } else {
      toggleBellRing();
    }
  }}
  className={bellRinging ? 'bg-yellow-100' : 'bg-green-100'}
>
  <span className={bellRinging ? 'animate-bell-ring' : ''}>
    🔔
  </span>
</button>
```

## Gotchas & Limitations

| Issue | Solution |
|-------|----------|
| Tab must be open | setTimeout only fires when tab active - no workaround without Service Workers |
| AudioContext limit (~6) | MUST reuse single shared instance |
| AudioContext suspended | Call `resume()` before each play |
| Autoplay blocked | Requires user gesture first (click) |
| Permission denied | Show fallback UI, can't prompt again |

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Notification API | ✅ | ✅ | ✅ | ✅ |
| Web Audio API | ✅ | ✅ | ✅ (webkit) | ✅ |
| requireInteraction | ✅ | ❌ | ❌ | ✅ |

## Future Enhancement: Service Workers

For true background notifications (tab can be closed):

```typescript
// Register service worker
navigator.serviceWorker.register('/sw.js');

// In service worker (sw.js)
self.addEventListener('push', (event) => {
  const data = event.data.json();
  self.registration.showNotification(data.title, data.options);
});
```

Requires backend push service with VAPID keys.

## Related

- ADR-009: Browser Notifications Architecture
- PHR-005: Web Audio API Browser Limitations
- MDN: Notification API
- MDN: Web Audio API
