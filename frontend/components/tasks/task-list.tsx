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
      <div className="text-center py-16 px-4">
        <div className="text-6xl mb-4">📝</div>
        <h3 className="text-xl font-semibold text-foreground mb-2">No tasks found</h3>
        <p className="text-muted-foreground max-w-sm mx-auto">
          Add your first task above or adjust your filters to see more tasks.
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
