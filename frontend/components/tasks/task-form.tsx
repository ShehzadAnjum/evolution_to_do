"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { Task, TaskCreate, Priority, Category, RecurrencePattern } from "@/lib/types";

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
  const [dueDate, setDueDate] = useState(initialData?.due_date || "");
  const [dueTime, setDueTime] = useState(initialData?.due_time || "");
  const [recurrence, setRecurrence] = useState<RecurrencePattern>(initialData?.recurrence_pattern || "none");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
    }
  }, [initialData]);

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
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        category,
        due_date: dueDate || undefined,
        due_time: dueTime || undefined,
        recurrence_pattern: recurrence,
      });
      if (!isEdit) {
        // Reset form after successful create
        setTitle("");
        setDescription("");
        setPriority("medium");
        setCategory("general");
        setDueDate("");
        setDueTime("");
        setRecurrence("none");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Title */}
      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          maxLength={200}
          disabled={isLoading}
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
