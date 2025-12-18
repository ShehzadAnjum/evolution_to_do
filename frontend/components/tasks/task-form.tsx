"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { Task, TaskCreate, Priority, Category, RecurrencePattern, TaskType, DeviceAction, Weekday } from "@/lib/types";
import { RELAY_NAMES } from "@/lib/types";

interface TaskFormProps {
  onSubmit: (data: TaskCreate) => Promise<void>;
  initialData?: Task;
  onCancel?: () => void;
  isEdit?: boolean;
  customCategories?: Category[];
}

const PRIORITY_OPTIONS: { value: Priority; label: string; color: string }[] = [
  { value: "high", label: "High", color: "text-priority-high" },
  { value: "medium", label: "Medium", color: "text-priority-medium" },
  { value: "low", label: "Low", color: "text-priority-low" },
];

const CATEGORY_OPTIONS: { value: string; label: string; icon: string }[] = [
  { value: "general", label: "General", icon: "📋" },
  { value: "work", label: "Work", icon: "💼" },
  { value: "personal", label: "Personal", icon: "🏠" },
  { value: "study", label: "Study", icon: "📚" },
  { value: "shopping", label: "Shopping", icon: "🛒" },
];

const RECURRENCE_OPTIONS: { value: RecurrencePattern; label: string; icon: string }[] = [
  { value: "none", label: "No repeat", icon: "⏺️" },
  { value: "daily", label: "Daily", icon: "📅" },
  { value: "weekly", label: "Weekly", icon: "📆" },
  { value: "biweekly", label: "Bi-weekly", icon: "📆" },
  { value: "monthly", label: "Monthly", icon: "🗓️" },
];

// v4.0.0: Device scheduling options
const DEVICE_OPTIONS: { value: number; label: string; icon: string }[] = [
  { value: 1, label: RELAY_NAMES[1], icon: "💡" },
  { value: 2, label: RELAY_NAMES[2], icon: "🌀" },
  { value: 3, label: RELAY_NAMES[3], icon: "🐠" },
  { value: 4, label: RELAY_NAMES[4], icon: "🔌" },
];

const ACTION_OPTIONS: { value: DeviceAction; label: string; icon: string }[] = [
  { value: "on", label: "Turn ON", icon: "✅" },
  { value: "off", label: "Turn OFF", icon: "⛔" },
  { value: "toggle", label: "Toggle", icon: "🔄" },
];

const WEEKDAY_OPTIONS: { value: Weekday; label: string }[] = [
  { value: "monday", label: "Monday" },
  { value: "tuesday", label: "Tuesday" },
  { value: "wednesday", label: "Wednesday" },
  { value: "thursday", label: "Thursday" },
  { value: "friday", label: "Friday" },
  { value: "saturday", label: "Saturday" },
  { value: "sunday", label: "Sunday" },
];

// Helper to get today's date in YYYY-MM-DD format
function getTodayDate(): string {
  const today = new Date();
  return today.toISOString().split('T')[0];
}

// Helper to get current time + 1 minute in HH:MM format
function getTimePlusOneMinute(): string {
  const now = new Date();
  now.setMinutes(now.getMinutes() + 1);
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes}`;
}

export function TaskForm({
  onSubmit,
  initialData,
  onCancel,
  isEdit = false,
  customCategories = [],
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [priority, setPriority] = useState<Priority>(initialData?.priority || "medium");
  const [category, setCategory] = useState(initialData?.category || "general");
  // Default to today's date for new tasks
  const [dueDate, setDueDate] = useState(initialData?.due_date || (isEdit ? "" : getTodayDate()));
  const [dueTime, setDueTime] = useState(initialData?.due_time || "");
  const [recurrence, setRecurrence] = useState<RecurrencePattern>(initialData?.recurrence_pattern || "none");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // v4.0.0: Device scheduling state
  const [taskType, setTaskType] = useState<TaskType>(initialData?.task_type || "regular");
  const [relayNumber, setRelayNumber] = useState<number>(initialData?.relay_number || 1);
  const [deviceAction, setDeviceAction] = useState<DeviceAction>(initialData?.device_action || "on");
  const [weekday, setWeekday] = useState<Weekday>(initialData?.weekday as Weekday || "monday");

  // Update form when initialData changes (for edit mode)
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description || "");
      setPriority(initialData.priority || "medium");
      setCategory(initialData.category || "general");
      setDueDate(initialData.due_date || "");
      setDueTime(initialData.due_time || "");
      setRecurrence(initialData.recurrence_pattern || "none");
      // v4.0.0: Device scheduling fields
      setTaskType(initialData.task_type || "regular");
      setRelayNumber(initialData.relay_number || 1);
      setDeviceAction((initialData.device_action as DeviceAction) || "on");
      setWeekday((initialData.weekday as Weekday) || "monday");
    }
  }, [initialData]);

  // v4.0.0: Auto-generate title and set category for device schedules
  useEffect(() => {
    if (taskType === "device_schedule") {
      const deviceName = RELAY_NAMES[relayNumber] || `Relay ${relayNumber}`;
      const actionText = deviceAction.toUpperCase();
      const timeText = dueTime ? ` at ${dueTime}` : "";
      const recurrenceText = recurrence === "daily" ? " (Daily)" :
                             recurrence === "weekly" ? ` (Every ${weekday})` : "";
      setTitle(`${actionText} ${deviceName}${timeText}${recurrenceText}`);
      // Auto-set category to device_schedules
      setCategory("device_schedules");
    }
  }, [taskType, relayNumber, deviceAction, dueTime, recurrence, weekday]);

  // Auto-set due time to current+1 minute when switching to device schedule (new tasks only)
  useEffect(() => {
    if (taskType === "device_schedule" && !isEdit && !dueTime) {
      setDueTime(getTimePlusOneMinute());
    }
  }, [taskType, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    if (title.length > 200) {
      setError("Title must be 200 characters or less");
      return;
    }

    setIsLoading(true);
    try {
      const taskData: TaskCreate = {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        category,
        due_date: dueDate || undefined,
        due_time: dueTime || undefined,
        recurrence_pattern: recurrence,
        // v4.0.0: Device scheduling fields
        task_type: taskType,
      };

      // Only include device fields for device schedules
      if (taskType === "device_schedule") {
        taskData.device_id = "esp32-home";
        taskData.relay_number = relayNumber;
        taskData.device_action = deviceAction;
        if (recurrence === "weekly") {
          taskData.weekday = weekday;
        }
      }

      await onSubmit(taskData);

      if (!isEdit) {
        // Reset form after successful create
        setTitle("");
        setDescription("");
        setPriority("medium");
        setCategory("general");
        setDueDate("");
        setDueTime("");
        setRecurrence("none");
        // v4.0.0: Reset device fields
        setTaskType("regular");
        setRelayNumber(1);
        setDeviceAction("on");
        setWeekday("monday");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* v4.0.0: Task Type Toggle */}
      <div className="space-y-2">
        <Label>Task Type</Label>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setTaskType("regular")}
            disabled={isLoading}
            className={`flex-1 px-4 py-2 rounded-md border text-sm font-medium transition-colors ${
              taskType === "regular"
                ? "bg-primary text-primary-foreground border-primary"
                : "bg-background border-input hover:bg-accent"
            }`}
          >
            📋 Regular Task
          </button>
          <button
            type="button"
            onClick={() => setTaskType("device_schedule")}
            disabled={isLoading}
            className={`flex-1 px-4 py-2 rounded-md border text-sm font-medium transition-colors ${
              taskType === "device_schedule"
                ? "bg-primary text-primary-foreground border-primary"
                : "bg-background border-input hover:bg-accent"
            }`}
          >
            🏠 Device Schedule
          </button>
        </div>
      </div>

      {/* v4.0.0: Device Scheduling Fields (only shown for device_schedule) */}
      {taskType === "device_schedule" && (
        <div className="p-4 rounded-lg border border-dashed border-primary/50 bg-primary/5 space-y-4">
          <div className="text-sm font-medium text-primary flex items-center gap-2">
            🏠 IoT Device Control
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Device Selection */}
            <div className="space-y-2">
              <Label htmlFor="device">Device</Label>
              <select
                id="device"
                value={relayNumber}
                onChange={(e) => setRelayNumber(Number(e.target.value))}
                disabled={isLoading}
                className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              >
                {DEVICE_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.icon} {opt.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Action Selection */}
            <div className="space-y-2">
              <Label htmlFor="action">Action</Label>
              <select
                id="action"
                value={deviceAction}
                onChange={(e) => setDeviceAction(e.target.value as DeviceAction)}
                disabled={isLoading}
                className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              >
                {ACTION_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.icon} {opt.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Weekday (shown only for weekly recurrence) */}
          {recurrence === "weekly" && (
            <div className="space-y-2">
              <Label htmlFor="weekday">Repeat on</Label>
              <select
                id="weekday"
                value={weekday}
                onChange={(e) => setWeekday(e.target.value as Weekday)}
                disabled={isLoading}
                className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              >
                {WEEKDAY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
          )}

          <p className="text-xs text-muted-foreground">
            Set time and recurrence below. The schedule will be sent to your ESP32 device.
          </p>
        </div>
      )}

      {/* Title */}
      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder={taskType === "device_schedule" ? "Auto-generated from device settings" : "What needs to be done?"}
          maxLength={200}
          disabled={isLoading || taskType === "device_schedule"}
          required
          className="bg-background"
        />
      </div>

      {/* Description */}
      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Input
          id="description"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details (optional)"
          maxLength={2000}
          disabled={isLoading}
          className="bg-background"
        />
      </div>

      {/* Priority, Category Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Priority */}
        <div className="space-y-2">
          <Label htmlFor="priority">Priority</Label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as Priority)}
            disabled={isLoading}
            className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {PRIORITY_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.value === "high" ? "🔴" : opt.value === "medium" ? "🟡" : "🟢"} {opt.label}
              </option>
            ))}
          </select>
        </div>

        {/* Category */}
        <div className="space-y-2">
          <Label htmlFor="category">Category</Label>
          {taskType === "device_schedule" ? (
            <div className="w-full h-10 px-3 rounded-md border border-input bg-muted text-sm flex items-center text-muted-foreground">
              🏠 Device Schedules
            </div>
          ) : (
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              disabled={isLoading}
              className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            >
              {CATEGORY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.icon} {opt.label}
                </option>
              ))}
              {customCategories.length > 0 && (
                <option disabled>──────────</option>
              )}
              {customCategories.map((cat) => (
                <option key={cat.id} value={cat.name.toLowerCase()}>
                  {cat.icon} {cat.name}
                </option>
              ))}
            </select>
          )}
        </div>
      </div>

      {/* Due Date, Time & Recurrence Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Due Date */}
        <div className="space-y-2">
          <Label htmlFor="dueDate">Due Date</Label>
          <Input
            id="dueDate"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={isLoading}
            className="bg-background"
          />
        </div>

        {/* Due Time */}
        <div className="space-y-2">
          <Label htmlFor="dueTime">Due Time</Label>
          <Input
            id="dueTime"
            type="time"
            value={dueTime}
            onChange={(e) => setDueTime(e.target.value)}
            disabled={isLoading}
            className="bg-background"
          />
        </div>

        {/* Recurrence */}
        <div className="space-y-2">
          <Label htmlFor="recurrence">Repeat</Label>
          <select
            id="recurrence"
            value={recurrence}
            onChange={(e) => setRecurrence(e.target.value as RecurrencePattern)}
            disabled={isLoading}
            className="w-full h-10 px-3 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {RECURRENCE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.icon} {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <p className="text-sm text-destructive">{error}</p>
      )}

      <div className="flex gap-2">
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Saving..." : isEdit ? "Update Task" : "Add Task"}
        </Button>
        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}
