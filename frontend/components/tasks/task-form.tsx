"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { Task, TaskCreate } from "@/lib/types";

interface TaskFormProps {
  onSubmit: (data: TaskCreate) => Promise<void>;
  initialData?: Task;
  onCancel?: () => void;
  isEdit?: boolean;
}

export function TaskForm({
  onSubmit,
  initialData,
  onCancel,
  isEdit = false,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      });
      if (!isEdit) {
        setTitle("");
        setDescription("");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
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
        />
      </div>

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
        />
      </div>

      {error && (
        <p className="text-sm text-red-600">{error}</p>
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
