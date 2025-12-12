/**
 * Browser Notification Service for Task Reminders
 *
 * Provides:
 * - Permission request for notifications
 * - Task due time notifications
 * - Background notification scheduling
 * - Bell sound and visual vibration
 */

// Bell vibration callback (set by UI component)
let onBellRing: (() => void) | null = null;

export function setOnBellRing(callback: (() => void) | null): void {
  onBellRing = callback;
}

// Play bell sound using Web Audio API
export function playBellSound(): void {
  if (typeof window === 'undefined') return;

  try {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();

    // Create a bell-like sound with multiple harmonics
    const playTone = (frequency: number, startTime: number, duration: number, volume: number) => {
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      oscillator.frequency.value = frequency;
      oscillator.type = 'sine';

      // Bell-like envelope: quick attack, slow decay
      gainNode.gain.setValueAtTime(0, audioContext.currentTime + startTime);
      gainNode.gain.linearRampToValueAtTime(volume, audioContext.currentTime + startTime + 0.01);
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + startTime + duration);

      oscillator.start(audioContext.currentTime + startTime);
      oscillator.stop(audioContext.currentTime + startTime + duration);
    };

    // Bell sound: fundamental + harmonics (two rings)
    // First ring
    playTone(800, 0, 0.5, 0.3);      // Fundamental
    playTone(1200, 0, 0.4, 0.15);    // 2nd harmonic
    playTone(1600, 0, 0.3, 0.1);     // 3rd harmonic

    // Second ring (slightly delayed)
    playTone(800, 0.3, 0.5, 0.25);
    playTone(1200, 0.3, 0.4, 0.12);
    playTone(1600, 0.3, 0.3, 0.08);

    console.log('🔔 Bell sound played');
  } catch (err) {
    console.warn('Could not play bell sound:', err);
  }
}

// Trigger bell ring (sound + visual)
function triggerBellRing(): void {
  playBellSound();
  if (onBellRing) {
    onBellRing();
  }
}

// Check if notifications are supported
export function isNotificationSupported(): boolean {
  return typeof window !== 'undefined' && 'Notification' in window;
}

// Get current notification permission
export function getNotificationPermission(): NotificationPermission | 'unsupported' {
  if (!isNotificationSupported()) return 'unsupported';
  return Notification.permission;
}

// Request notification permission
export async function requestNotificationPermission(): Promise<NotificationPermission | 'unsupported'> {
  if (!isNotificationSupported()) return 'unsupported';

  const permission = await Notification.requestPermission();
  return permission;
}

// Show a notification with bell sound and visual
export function showNotification(
  title: string,
  options?: NotificationOptions
): Notification | null {
  if (!isNotificationSupported()) return null;
  if (Notification.permission !== 'granted') return null;

  // Trigger bell ring (sound + visual animation)
  triggerBellRing();

  return new Notification(title, {
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    ...options,
  });
}

// Show task reminder notification
export function showTaskReminder(
  taskTitle: string,
  dueTime?: string,
  taskId?: string
): Notification | null {
  const timeStr = dueTime ? ` at ${formatTime12Hour(dueTime)}` : '';

  console.log(`🔔 Showing notification for: ${taskTitle}`);

  return showNotification(
    `Task Reminder: ${taskTitle}`,
    {
      body: `Your task is due${timeStr}`,
      tag: taskId || 'task-reminder', // Prevents duplicate notifications
      requireInteraction: true, // Notification stays until dismissed
    }
  );
}

// Test notification - call this to verify notifications work
export function testNotification(): Notification | null {
  console.log('🔔 Testing notification...');
  return showNotification(
    'Test Notification',
    {
      body: 'If you see this, notifications are working!',
      tag: 'test-notification',
    }
  );
}

// Format time to 12-hour format
function formatTime12Hour(time: string): string {
  const [hours, minutes] = time.split(':').map(Number);
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const hour12 = hours % 12 || 12;
  return `${hour12}:${minutes.toString().padStart(2, '0')} ${ampm}`;
}

// Task interface for scheduling
interface SchedulableTask {
  id: string;
  title: string;
  due_date: string | null;
  due_time: string | null;
  is_complete: boolean;
}

// Scheduled notification timeouts
const scheduledNotifications = new Map<string, NodeJS.Timeout>();

// Schedule notification for a task
export function scheduleTaskNotification(task: SchedulableTask): void {
  // Clear any existing notification for this task
  clearTaskNotification(task.id);

  // Don't schedule if task is complete or has no due date/time
  if (task.is_complete || !task.due_date || !task.due_time) {
    console.log(`⏭️ Skipping notification for "${task.title}" - complete: ${task.is_complete}, date: ${task.due_date}, time: ${task.due_time}`);
    return;
  }

  // Parse due date and time
  const [year, month, day] = task.due_date.split('-').map(Number);
  const [hours, minutes] = task.due_time.split(':').map(Number);

  const dueDateTime = new Date(year, month - 1, day, hours, minutes);
  const now = new Date();

  // Calculate time until due
  const msUntilDue = dueDateTime.getTime() - now.getTime();

  // Don't schedule if already past
  if (msUntilDue <= 0) {
    console.log(`⏭️ Skipping notification for "${task.title}" - already past (${msUntilDue}ms ago)`);
    return;
  }

  const minutesUntilDue = Math.round(msUntilDue / 60000);
  console.log(`📅 Scheduled notification for "${task.title}" in ${minutesUntilDue} minutes (${dueDateTime.toLocaleString()})`);

  // Schedule notification at due time
  const timeout = setTimeout(() => {
    showTaskReminder(task.title, task.due_time || undefined, task.id);
    scheduledNotifications.delete(task.id);
  }, msUntilDue);

  scheduledNotifications.set(task.id, timeout);

  // Also schedule a 15-minute reminder if due is more than 15 minutes away
  const fifteenMinutes = 15 * 60 * 1000;
  if (msUntilDue > fifteenMinutes) {
    const earlyTimeout = setTimeout(() => {
      showNotification(
        `Upcoming Task: ${task.title}`,
        {
          body: `Due in 15 minutes at ${formatTime12Hour(task.due_time!)}`,
          tag: `${task.id}-15min`,
        }
      );
    }, msUntilDue - fifteenMinutes);

    scheduledNotifications.set(`${task.id}-15min`, earlyTimeout);
  }
}

// Clear scheduled notification for a task
export function clearTaskNotification(taskId: string): void {
  const timeout = scheduledNotifications.get(taskId);
  if (timeout) {
    clearTimeout(timeout);
    scheduledNotifications.delete(taskId);
  }

  // Also clear the 15-minute reminder
  const earlyTimeout = scheduledNotifications.get(`${taskId}-15min`);
  if (earlyTimeout) {
    clearTimeout(earlyTimeout);
    scheduledNotifications.delete(`${taskId}-15min`);
  }
}

// Schedule notifications for all tasks
export function scheduleAllTaskNotifications(tasks: SchedulableTask[]): void {
  // Clear all existing notifications
  scheduledNotifications.forEach((timeout) => clearTimeout(timeout));
  scheduledNotifications.clear();

  // Schedule new notifications for incomplete tasks with due date/time
  tasks.forEach((task) => {
    if (!task.is_complete && task.due_date && task.due_time) {
      scheduleTaskNotification(task);
    }
  });
}

// Check for tasks due soon (within the next hour) and show notification
export function checkTasksDueSoon(tasks: SchedulableTask[]): void {
  const now = new Date();
  const oneHourFromNow = new Date(now.getTime() + 60 * 60 * 1000);

  tasks.forEach((task) => {
    if (task.is_complete || !task.due_date || !task.due_time) return;

    const [year, month, day] = task.due_date.split('-').map(Number);
    const [hours, minutes] = task.due_time.split(':').map(Number);
    const dueDateTime = new Date(year, month - 1, day, hours, minutes);

    // If due within the next hour
    if (dueDateTime > now && dueDateTime <= oneHourFromNow) {
      const minutesUntilDue = Math.round((dueDateTime.getTime() - now.getTime()) / 60000);
      showNotification(
        `Task Due Soon: ${task.title}`,
        {
          body: `Due in ${minutesUntilDue} minutes`,
          tag: `${task.id}-soon`,
        }
      );
    }
  });
}
