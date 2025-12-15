---
name: browser-notifications
description: Browser notifications with Web Audio API sounds. Use when implementing task reminders, due date alerts, or notification sounds in web applications.
---

# Browser Notifications

## Request Permission

```typescript
const permission = await Notification.requestPermission();
if (permission === "granted") {
  // Can show notifications
}
```

## Schedule Notification

```typescript
const msUntilDue = dueDateTime.getTime() - Date.now();
if (msUntilDue > 0) {
  setTimeout(() => {
    new Notification("Task Due!", {
      body: task.title,
      icon: "/icon.png",
      requireInteraction: true,
    });
    playBellSound();
  }, msUntilDue);
}
```

## Bell Sound (Web Audio API)

```typescript
// Reuse single AudioContext (browsers limit instances!)
let audioContext: AudioContext | null = null;

function playBellSound() {
  if (!audioContext) {
    audioContext = new AudioContext();
  }
  if (audioContext.state === "suspended") {
    audioContext.resume();
  }

  const osc = audioContext.createOscillator();
  const gain = audioContext.createGain();
  osc.connect(gain);
  gain.connect(audioContext.destination);
  osc.frequency.value = 800;
  osc.type = "sine";
  gain.gain.setValueAtTime(0.3, audioContext.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
  osc.start();
  osc.stop(audioContext.currentTime + 0.5);
}
```

## Limitations

- `setTimeout` only works while tab is open
- For true background notifications, need Service Workers + Push API
- AudioContext requires user gesture to start
