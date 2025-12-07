"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import type { Task } from "@/lib/types";

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
}

export function TaskItem({
  task,
  onToggleComplete,
  onDelete,
  onEdit,
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

  return (
    <div className="flex items-center gap-3 p-4 border rounded-lg bg-white shadow-sm">
      {/* Checkbox */}
      <input
        type="checkbox"
        checked={task.is_complete}
        onChange={handleToggle}
        disabled={isLoading}
        className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
      />

      {/* Task content */}
      <div className="flex-1 min-w-0">
        <h3
          className={`font-medium ${
            task.is_complete ? "line-through text-gray-400" : "text-gray-900"
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p
            className={`text-sm mt-1 ${
              task.is_complete ? "text-gray-300" : "text-gray-500"
            }`}
          >
            {task.description}
          </p>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(task)}
          disabled={isLoading}
        >
          Edit
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={handleDelete}
          disabled={isLoading}
        >
          Delete
        </Button>
      </div>
    </div>
  );
}
