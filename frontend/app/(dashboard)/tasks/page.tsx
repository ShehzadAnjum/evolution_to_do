"use client";

import { useEffect, useState, useMemo } from "react";
import {
  TaskForm,
  TaskList,
  Sidebar,
  FilterView,
  CategoryFilter,
  PriorityFilter,
} from "@/components/tasks";
import { ChatPanel } from "@/components/chat";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { SignOutButton } from "@/app/dashboard/SignOutButton";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
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

  // Filter states
  const [activeView, setActiveView] = useState<FilterView>("all");
  const [activeCategory, setActiveCategory] = useState<CategoryFilter>("all");
  const [activePriority, setActivePriority] = useState<PriorityFilter>("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Mobile sidebar toggle
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Chat panel toggle
  const [chatOpen, setChatOpen] = useState(false);

  // Task dialog toggle
  const [taskDialogOpen, setTaskDialogOpen] = useState(false);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = await getAuthToken();
      if (!token) {
        setError("Please log in to view your tasks.");
        console.error("No JWT token received from /api/auth/token");
        return;
      }

      console.log("Got JWT token, fetching tasks...");
      const response = await api.getTasks(token);
      setTasks(response.tasks);
      setTotal(response.total);
      setCompleted(response.completed);
      console.log("Tasks loaded successfully:", response);
    } catch (err: any) {
      console.error("Error loading tasks:", err);

      if (err.statusCode === 401 || err.statusCode === 422) {
        setError(
          "Authentication required. Please log in to view your tasks. " +
          "(Tip: Check that BETTER_AUTH_SECRET matches between frontend and backend)"
        );
      } else if (err.statusCode === 0 || err.message?.includes("Failed to fetch")) {
        setError(
          "Cannot connect to backend server. " +
          "Is the backend running on port 8000? " +
          `Check: ${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/health`
        );
      } else {
        const errorMessage = err.message || "Failed to load tasks";
        setError(`Error: ${errorMessage}`);
      }
    } finally {
      setLoading(false);
    }
  };

  // Filter tasks based on active filters
  const filteredTasks = useMemo(() => {
    let result = [...tasks];
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const todayStr = today.toISOString().split('T')[0];

    // View filter
    switch (activeView) {
      case "today":
        result = result.filter(t => t.due_date === todayStr && !t.is_complete);
        break;
      case "upcoming":
        result = result.filter(t => {
          if (!t.due_date || t.is_complete) return false;
          return new Date(t.due_date) >= today;
        });
        break;
      case "completed":
        result = result.filter(t => t.is_complete);
        break;
      // "all" - no filter
    }

    // Category filter
    if (activeCategory !== "all") {
      result = result.filter(t => t.category === activeCategory);
    }

    // Priority filter
    if (activePriority !== "all") {
      result = result.filter(t => t.priority === activePriority);
    }

    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        t =>
          t.title.toLowerCase().includes(query) ||
          t.description?.toLowerCase().includes(query)
      );
    }

    return result;
  }, [tasks, activeView, activeCategory, activePriority, searchQuery]);

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
      await loadTasks();
      setTaskDialogOpen(false);
      setSuccessMessage(`Task "${newTask.title}" created successfully!`);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      throw err;
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
      await loadTasks();
      setEditingTask(null);
      setTaskDialogOpen(false);
      setSuccessMessage(`Task "${updatedTask.title}" updated successfully!`);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      throw err;
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
      await loadTasks();
    } catch (err: any) {
      setError(err.message || "Failed to update task status");
      console.error("Error toggling task completion:", err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">⏳</div>
          <p className="text-muted-foreground">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden bg-secondary/30 dark:bg-background flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar - Fixed with independent scroll */}
      <aside
        className={`
          fixed lg:relative inset-y-0 left-0 z-50 h-screen
          transform transition-transform duration-300
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
        `}
      >
        <Sidebar
          tasks={tasks}
          activeView={activeView}
          activeCategory={activeCategory}
          activePriority={activePriority}
          onViewChange={(v) => { setActiveView(v); setSidebarOpen(false); }}
          onCategoryChange={(c) => { setActiveCategory(c); setSidebarOpen(false); }}
          onPriorityChange={(p) => { setActivePriority(p); setSidebarOpen(false); }}
        />
      </aside>

      {/* Main Content - Takes remaining width, has its own scroll */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Header - Sticky */}
        <header className="shrink-0 z-30 bg-card border-b border-border px-4 lg:px-8 h-16 flex items-center justify-between">
          {/* Left: Menu button (mobile) + Title */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 hover:bg-secondary rounded-lg"
            >
              ☰
            </button>
            <h1 className="text-xl font-semibold text-foreground">
              {activeView === "all" ? "All Tasks" :
               activeView === "today" ? "Today" :
               activeView === "upcoming" ? "Upcoming" : "Completed"}
              {activeCategory !== "all" && ` • ${activeCategory}`}
              {activePriority !== "all" && ` • ${activePriority} priority`}
            </h1>
          </div>

          {/* Right: Search, Chat, Theme, User */}
          <div className="flex items-center gap-3">
            {/* Search */}
            <div className="hidden sm:block relative">
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-48 lg:w-64 h-9 px-3 pr-8 rounded-lg border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                🔍
              </span>
            </div>

            {/* Chat Toggle */}
            <button
              onClick={() => setChatOpen(true)}
              className="p-2 hover:bg-secondary rounded-lg transition-colors"
              title="Open AI Assistant"
            >
              <span className="text-lg">🤖</span>
            </button>

            <ThemeToggle />
            <SignOutButton />
          </div>
        </header>

        {/* Content Area - Scrollable */}
        <div className="flex-1 overflow-y-auto p-4 lg:p-8">
          <div className="max-w-3xl mx-auto space-y-6">
            {/* Success Message */}
            {successMessage && (
              <div className="p-3 bg-success/10 border border-success/30 rounded-lg text-success font-medium">
                ✅ {successMessage}
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="p-3 bg-destructive/10 border border-destructive/30 rounded-lg text-destructive font-medium">
                ⚠️ {error}
                <button
                  onClick={loadTasks}
                  className="ml-4 text-sm font-semibold underline hover:no-underline"
                >
                  Retry
                </button>
              </div>
            )}

            {/* Mobile Search */}
            <div className="sm:hidden">
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-10 px-4 rounded-lg border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            {/* Task Count */}
            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>
                Showing {filteredTasks.length} of {tasks.length} tasks
              </span>
              {(activeView !== "all" || activeCategory !== "all" || activePriority !== "all" || searchQuery) && (
                <button
                  onClick={() => {
                    setActiveView("all");
                    setActiveCategory("all");
                    setActivePriority("all");
                    setSearchQuery("");
                  }}
                  className="text-primary hover:underline"
                >
                  Clear filters
                </button>
              )}
            </div>

            {/* Task List */}
            <TaskList
              tasks={filteredTasks}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTask}
              onEdit={(task) => {
                setEditingTask(task);
                setTaskDialogOpen(true);
              }}
            />
          </div>
        </div>
      </main>

      {/* Floating Add Task Button */}
      <button
        onClick={() => {
          setEditingTask(null);
          setTaskDialogOpen(true);
        }}
        className="fixed bottom-6 right-6 z-30 w-14 h-14 bg-primary hover:bg-primary/90 text-primary-foreground rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center group"
        title="Add New Task"
      >
        <span className="text-2xl font-light transition-transform group-hover:rotate-90 duration-200">+</span>
        <span className="absolute right-full mr-3 px-3 py-1.5 bg-popover text-popover-foreground text-sm rounded-lg shadow-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
          Add New Task
        </span>
      </button>

      {/* Add/Edit Task Dialog */}
      <Dialog
        open={taskDialogOpen}
        onOpenChange={(open) => {
          setTaskDialogOpen(open);
          if (!open) setEditingTask(null);
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingTask ? "Edit Task" : "Add New Task"}
            </DialogTitle>
          </DialogHeader>
          <TaskForm
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            initialData={editingTask || undefined}
            isEdit={!!editingTask}
            onCancel={() => {
              setTaskDialogOpen(false);
              setEditingTask(null);
            }}
          />
        </DialogContent>
      </Dialog>

      {/* Chat Panel */}
      <ChatPanel isOpen={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
