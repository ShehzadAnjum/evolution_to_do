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
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { getAuthToken } from "@/lib/auth-token";
import type { Task, TaskCreate, TaskUpdate, Category, CategoryCreate } from "@/lib/types";
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

  // Custom categories (persisted in database)
  const [customCategories, setCustomCategories] = useState<Category[]>([]);
  const [loadingCategories, setLoadingCategories] = useState(true);

  // Load custom categories from API on mount
  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoadingCategories(true);
      const token = await getAuthToken();
      if (!token) return;
      const categories = await api.getCategories(token);
      setCustomCategories(categories);
    } catch (err) {
      console.error("Failed to load categories:", err);
    } finally {
      setLoadingCategories(false);
    }
  };

  const handleAddCategory = async (data: CategoryCreate) => {
    const token = await getAuthToken();
    if (!token) {
      setError("Please log in to add categories.");
      return;
    }
    const newCategory = await api.createCategory(token, data);
    setCustomCategories((prev) => [...prev, newCategory]);
  };

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
    <div className="h-full w-full overflow-hidden flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar - Fixed on mobile, relative on desktop */}
      <aside
        className={`
          fixed lg:relative lg:inset-auto inset-y-0 left-0 z-40 h-full shrink-0
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
          customCategories={customCategories}
          onAddCategory={handleAddCategory}
          isLoadingCategories={loadingCategories}
        />
      </aside>

      {/* Main Content Area - flex column with fixed header */}
      <div className="flex-1 flex flex-col h-full min-w-0 overflow-hidden">
        {/* Header - FIXED at top, never scrolls */}
        <header className="flex-none h-14 z-30 bg-card border-b border-border px-4 lg:px-6 flex items-center justify-between">
          {/* Left: Menu button (mobile) + Title */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 hover:bg-secondary rounded-lg"
            >
              ☰
            </button>
            <h1 className="text-lg font-semibold text-foreground whitespace-nowrap">
              {activeView === "all" ? "All Tasks" :
               activeView === "today" ? "Today" :
               activeView === "upcoming" ? "Upcoming" : "Completed"}
              {activeCategory !== "all" && ` • ${activeCategory}`}
              {activePriority !== "all" && ` • ${activePriority} priority`}
            </h1>
          </div>

          {/* Right: Add Task, Search, Chat, Theme, Logout */}
          <div className="flex items-center gap-2">
            {/* Add Task Button */}
            <button
              onClick={() => {
                setEditingTask(null);
                setTaskDialogOpen(true);
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-primary hover:bg-primary/90 text-primary-foreground rounded-md transition-colors font-medium text-sm"
              title="Add New Task"
            >
              <span className="text-base leading-none">+</span>
              <span className="hidden sm:inline">Add Task</span>
            </button>

            {/* Search */}
            <div className="hidden md:block relative">
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-48 lg:w-56 h-8 px-3 pr-8 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
              <span className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">
                🔍
              </span>
            </div>

            {/* Chat Toggle */}
            <button
              onClick={() => setChatOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-600 hover:to-indigo-700 text-white rounded-lg transition-all shadow-md hover:shadow-lg"
              title="Open AI Assistant"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span className="hidden sm:inline text-sm font-medium">AI Chat</span>
            </button>
          </div>
        </header>

        {/* Scrollable Content Area */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <div className="max-w-3xl mx-auto space-y-4">
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
            <div className="md:hidden">
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-10 px-4 rounded-lg border border-input bg-card text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>

            {/* Category Filter Pills */}
            <div className="flex flex-wrap gap-2">
              {(["all", "work", "personal", "study", "shopping", "general"] as const).map((cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    activeCategory === cat
                      ? "bg-primary text-primary-foreground"
                      : "bg-card hover:bg-secondary text-muted-foreground border border-border"
                  }`}
                >
                  {cat === "all" ? "All" : cat.charAt(0).toUpperCase() + cat.slice(1)}
                </button>
              ))}
              {/* Custom Category Pills */}
              {customCategories.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setActiveCategory(cat.name.toLowerCase())}
                  className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors flex items-center gap-1 ${
                    activeCategory === cat.name.toLowerCase()
                      ? "bg-primary text-primary-foreground"
                      : "bg-card hover:bg-secondary text-muted-foreground border border-border"
                  }`}
                >
                  <span>{cat.icon}</span>
                  <span>{cat.name}</span>
                </button>
              ))}
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
        </main>
      </div>

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
