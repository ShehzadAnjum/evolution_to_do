"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TaskForm, TaskList, TaskSummary } from "@/components/tasks";
import { SignOutButton } from "@/app/dashboard/SignOutButton";
import { getAuthToken } from "@/lib/auth-token";
import type { Task, TaskCreate, TaskUpdate, TaskListResponse } from "@/lib/types";
import * as api from "@/lib/api";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get JWT token from Better Auth
      const token = await getAuthToken();
      if (!token) {
        setError("Please log in to view your tasks.");
        return;
      }

      const response = await api.getTasks(token);
      setTasks(response.tasks);
      setTotal(response.total);
      setCompleted(response.completed);
    } catch (err: any) {
      // Handle authentication errors gracefully
      if (err.statusCode === 401 || err.statusCode === 422) {
        setError("Authentication required. Please log in to view your tasks.");
      } else if (err.statusCode === 0) {
        setError("Cannot connect to server. Is the backend running on port 8000?");
      } else {
        const errorMessage = err.message || "Failed to load tasks";
        setError(errorMessage);
      }
      console.error("Error loading tasks:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData: TaskCreate) => {
    try {
      setError(null);
      setSuccessMessage(null);
      const token = await getAuthToken();
      if (!token) {
        setError("Please log in to create tasks.");
        return;
      }
      const newTask = await api.createTask(token, taskData);

      // Reload tasks to get updated stats
      await loadTasks();

      setSuccessMessage(`Task "${newTask.title}" created successfully!`);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleUpdateTask = async (taskData: TaskCreate) => {
    if (!editingTask) return;
    try {
      setError(null);
      setSuccessMessage(null);
      const token = await getAuthToken();
      if (!token) {
        setError("Please log in to edit tasks.");
        return;
      }
      const updatedTask = await api.updateTask(token, editingTask.id, taskData as TaskUpdate);

      // Reload tasks to get updated data
      await loadTasks();

      setEditingTask(null);
      setSuccessMessage(`Task "${updatedTask.title}" updated successfully!`);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      throw err; // Let TaskForm handle the error
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      setError(null);
      setSuccessMessage(null);
      const token = await getAuthToken();
      if (!token) {
        setError("Please log in to delete tasks.");
        return;
      }
      await api.deleteTask(token, taskId);

      // Reload tasks to get updated data
      await loadTasks();

      setSuccessMessage("Task deleted successfully!");
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to delete task");
      console.error("Error deleting task:", err);
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      setError(null);
      const token = await getAuthToken();
      if (!token) {
        setError("Please log in to update tasks.");
        return;
      }
      await api.toggleComplete(token, taskId);

      // Reload tasks to get updated data and stats
      await loadTasks();
    } catch (err: any) {
      setError(err.message || "Failed to update task status");
      console.error("Error toggling task completion:", err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading tasks...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              My Tasks
            </h1>
            <TaskSummary total={total} completed={completed} />
          </div>
          <SignOutButton />
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="mb-4 p-3 bg-green-100 border-2 border-green-400 rounded-lg text-green-900 font-medium">
            {successMessage}
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 border-2 border-red-400 rounded-lg text-red-900 font-medium">
            {error}
            <button
              onClick={loadTasks}
              className="ml-4 text-sm font-semibold underline hover:no-underline"
            >
              Retry
            </button>
          </div>
        )}

        {/* Add Task Form */}
        <Card className="mb-8 border-accent/20 shadow-lg shadow-accent/5">
          <CardHeader>
            <CardTitle>
              {editingTask ? "Edit Task" : "Add New Task"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <TaskForm
              onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
              initialData={editingTask || undefined}
              isEdit={!!editingTask}
              onCancel={editingTask ? () => setEditingTask(null) : undefined}
            />
          </CardContent>
        </Card>

        {/* Task List */}
        <TaskList
          tasks={tasks}
          onToggleComplete={handleToggleComplete}
          onDelete={handleDeleteTask}
          onEdit={setEditingTask}
        />
      </div>
    </div>
  );
}
