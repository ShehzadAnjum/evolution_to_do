"use client";

import { TaskItem } from "./task-item";
import type { Task } from "@/lib/types";

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
}

export function TaskList({
  tasks,
  onToggleComplete,
  onDelete,
  onEdit,
}: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <p className="text-gray-500 text-lg">No tasks yet</p>
        <p className="text-gray-400 text-sm mt-1">
          Add your first task above to get started
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
}
