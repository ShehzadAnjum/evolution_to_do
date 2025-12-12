"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import type { Task, Priority, Category } from "@/lib/types";

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  customCategories?: Category[];
}

// Get priority badge class
function getPriorityClass(priority: Priority): string {
  switch (priority) {
    case "high":
      return "priority-badge priority-high";
    case "medium":
      return "priority-badge priority-medium";
    case "low":
      return "priority-badge priority-low";
    default:
      return "priority-badge priority-medium";
  }
}

// Get priority icon
function getPriorityIcon(priority: Priority): string {
  switch (priority) {
    case "high":
      return "🔴";
    case "medium":
      return "🟡";
    case "low":
      return "🟢";
    default:
      return "🟡";
  }
}

// Get category badge class
function getCategoryClass(category: string): string {
  const baseClass = "category-badge";
  switch (category) {
    case "work":
      return `${baseClass} category-work`;
    case "personal":
      return `${baseClass} category-personal`;
    case "study":
      return `${baseClass} category-study`;
    case "shopping":
      return `${baseClass} category-shopping`;
    default:
      return `${baseClass} category-general`;
  }
}

// Get category icon (checks custom categories first)
function getCategoryIcon(category: string, customCategories: Category[] = []): string {
  // Check custom categories first
  const customCat = customCategories.find(
    (c) => c.name.toLowerCase() === category.toLowerCase()
  );
  if (customCat) {
    return customCat.icon;
  }

  // Default categories
  switch (category) {
    case "work":
      return "💼";
    case "personal":
      return "🏠";
    case "study":
      return "📚";
    case "shopping":
      return "🛒";
    default:
      return "📋";
  }
}

// Format time for display (12-hour format)
function formatTime(time: string | null): string {
  if (!time) return "";
  const [hours, minutes] = time.split(":").map(Number);
  const ampm = hours >= 12 ? "PM" : "AM";
  const hour12 = hours % 12 || 12;
  return `${hour12}:${minutes.toString().padStart(2, "0")} ${ampm}`;
}

// Format due date and get status
function formatDueDate(dueDate: string | null, dueTime: string | null): { text: string; className: string } | null {
  if (!dueDate) return null;

  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const due = new Date(dueDate);
  due.setHours(0, 0, 0, 0);

  const diffDays = Math.ceil((due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
  const timeStr = dueTime ? ` @ ${formatTime(dueTime)}` : "";

  if (diffDays < 0) {
    return { text: `Overdue (${Math.abs(diffDays)}d)${timeStr}`, className: "due-overdue" };
  } else if (diffDays === 0) {
    return { text: `Today${timeStr}`, className: "due-today" };
  } else if (diffDays === 1) {
    return { text: `Tomorrow${timeStr}`, className: "due-today" };
  } else if (diffDays <= 7) {
    return { text: `${diffDays} days${timeStr}`, className: "due-upcoming" };
  } else {
    // Format as date
    return {
      text: due.toLocaleDateString("en-US", { month: "short", day: "numeric" }) + timeStr,
      className: "due-upcoming"
    };
  }
}

export function TaskItem({
  task,
  onToggleComplete,
  onDelete,
  onEdit,
  customCategories = [],
}: TaskItemProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleToggle = async () => {
    setIsLoading(true);
    try {
      await onToggleComplete(task.id);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    setIsLoading(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsLoading(false);
    }
  };

  const dueInfo = formatDueDate(task.due_date, task.due_time);

  return (
    <div
      className={`
        flex items-start gap-3 p-4 rounded-lg border transition-all
        ${task.is_complete
          ? "bg-muted/50 border-border opacity-60"
          : "bg-card border-border hover:border-primary/50 hover:shadow-sm"
        }
      `}
    >
      {/* Checkbox */}
      <div className="pt-0.5">
        <input
          type="checkbox"
          checked={task.is_complete}
          onChange={handleToggle}
          disabled={isLoading}
          className="task-checkbox"
          aria-label={task.is_complete ? "Mark as incomplete" : "Mark as complete"}
        />
      </div>

      {/* Task content */}
      <div className="flex-1 min-w-0">
        {/* Title row with priority */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm" title={`Priority: ${task.priority}`}>
            {getPriorityIcon(task.priority)}
          </span>
          <h3
            className={`font-medium ${
              task.is_complete ? "line-through text-muted-foreground" : "text-foreground"
            }`}
          >
            {task.title}
          </h3>
        </div>

        {/* Description */}
        {task.description && (
          <p
            className={`text-sm mt-1 ${
              task.is_complete ? "text-muted-foreground/60" : "text-muted-foreground"
            }`}
          >
            {task.description}
          </p>
        )}

        {/* Meta row: Category + Due date + Recurrence */}
        <div className="flex items-center gap-3 mt-2 flex-wrap">
          {/* Category badge */}
          <span className={getCategoryClass(task.category)}>
            {getCategoryIcon(task.category, customCategories)} {task.category}
          </span>

          {/* Due date */}
          {dueInfo && !task.is_complete && (
            <span className={`text-xs ${dueInfo.className}`}>
              📅 {dueInfo.text}
            </span>
          )}

          {/* Recurrence indicator */}
          {task.recurrence_pattern && task.recurrence_pattern !== "none" && (
            <span className="text-xs text-blue-600 dark:text-blue-400">
              🔄 {task.recurrence_pattern}
            </span>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-2 shrink-0">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onEdit(task)}
          disabled={isLoading}
          className="h-8 px-2 text-muted-foreground hover:text-foreground"
        >
          ✏️
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleDelete}
          disabled={isLoading}
          className="h-8 px-2 text-muted-foreground hover:text-destructive"
        >
          🗑️
        </Button>
      </div>
    </div>
  );
}
