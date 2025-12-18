"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import {
  TaskForm,
  TaskList,
  Sidebar,
  FilterView,
  CategoryFilter,
  PriorityFilter,
} from "@/components/tasks";
import { ChatKitPanel } from "@/components/chat";
import { MqttStatus } from "@/components/mqtt-status";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { getAuthToken } from "@/lib/auth-token";
import type { Task, TaskCreate, TaskUpdate, Category, CategoryCreate } from "@/lib/types";
import * as api from "@/lib/api";
import {
  isNotificationSupported,
  getNotificationPermission,
  requestNotificationPermission,
  scheduleAllTaskNotifications,
  setOnBellRing,
  toggleBellRing,
  stopBellRing,
  isBellRinging,
} from "@/lib/notifications";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false); // For CRUD operations
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Filter states
  const [activeView, setActiveView] = useState<FilterView>("all");
  const [activeCategory, setActiveCategory] = useState<CategoryFilter>("all");
  const [activePriority, setActivePriority] = useState<PriorityFilter>("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Sort state
  const [sortBy, setSortBy] = useState<"created_at" | "due_date" | "priority" | "title">("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Notification state
  const [notificationPermission, setNotificationPermission] = useState<NotificationPermission | 'unsupported'>('default');
  const [bellRinging, setBellRinging] = useState(false);

  // Mobile sidebar toggle
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Chat panel toggle
  const [chatOpen, setChatOpen] = useState(false);

  // Chat loading state (for main header indicator)
  const [chatLoading, setChatLoading] = useState(false);
  const [chatLoadComplete, setChatLoadComplete] = useState(false);

  // Handle chat loading state changes - memoized to prevent infinite loops
  const handleChatLoadingChange = useCallback((isLoading: boolean) => {
    setChatLoading(isLoading);
    if (!isLoading) {
      // Loading just finished - show success message briefly
      setChatLoadComplete(true);
      setTimeout(() => setChatLoadComplete(false), 2500);
    }
  }, []);

  // Task dialog toggle
  const [taskDialogOpen, setTaskDialogOpen] = useState(false);

  // Custom categories (persisted in database)
  const [customCategories, setCustomCategories] = useState<Category[]>([]);
  const [loadingCategories, setLoadingCategories] = useState(true);

  // Auth token for API calls (including MQTT status)
  const [authToken, setAuthToken] = useState<string | null>(null);

  // Load custom categories from API on mount
  useEffect(() => {
    loadCategories();
  }, []);

  // Load auth token on mount
  useEffect(() => {
    getAuthToken().then(setAuthToken);
  }, []);

  // Check notification permission on mount
  useEffect(() => {
    if (isNotificationSupported()) {
      setNotificationPermission(getNotificationPermission());
    } else {
      setNotificationPermission('unsupported');
    }
  }, []);

  // Schedule notifications when tasks change
  useEffect(() => {
    if (notificationPermission === 'granted' && tasks.length > 0) {
      scheduleAllTaskNotifications(tasks);
    }
  }, [tasks, notificationPermission]);

  // Connect bell ring callbacks for visual animation
  useEffect(() => {
    setOnBellRing(
      // Start callback
      () => setBellRinging(true),
      // Stop callback
      () => setBellRinging(false)
    );
    return () => setOnBellRing(null, null);
  }, []);

  // Handle notification permission request
  const handleRequestNotificationPermission = async () => {
    const permission = await requestNotificationPermission();
    setNotificationPermission(permission);
    if (permission === 'granted' && tasks.length > 0) {
      scheduleAllTaskNotifications(tasks);
    }
  };

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
    loadTasks(true); // Initial load shows loading screen
  }, []);

  const loadTasks = async (isInitialLoad = false) => {
    try {
      // Only show full loading screen on initial load, not on refresh
      if (isInitialLoad) {
        setLoading(true);
      }
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
    // Use local date string (YYYY-MM-DD) to avoid timezone issues
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayStr = `${year}-${month}-${day}`;

    // View filter
    switch (activeView) {
      case "today":
        result = result.filter(t => t.due_date === todayStr && !t.is_complete);
        break;
      case "upcoming":
        result = result.filter(t => {
          if (!t.due_date || t.is_complete) return false;
          // Compare dates as strings (YYYY-MM-DD format)
          return t.due_date >= todayStr;
        });
        break;
      case "completed":
        result = result.filter(t => t.is_complete);
        break;
      // "all" - no filter
    }

    // Special handling for device_schedules category - filter by task_type
    if (activeCategory === "device_schedules") {
      result = result.filter(t => t.task_type === "device_schedule");
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

    // Sort tasks
    result.sort((a, b) => {
      let comparison = 0;
      switch (sortBy) {
        case "title":
          comparison = a.title.localeCompare(b.title);
          break;
        case "due_date":
          // Null dates go to the end
          if (!a.due_date && !b.due_date) comparison = 0;
          else if (!a.due_date) comparison = 1;
          else if (!b.due_date) comparison = -1;
          else comparison = a.due_date.localeCompare(b.due_date);
          break;
        case "priority":
          const priorityOrder = { high: 0, medium: 1, low: 2 };
          comparison = priorityOrder[a.priority] - priorityOrder[b.priority];
          break;
        case "created_at":
        default:
          comparison = a.created_at.localeCompare(b.created_at);
      }
      return sortOrder === "asc" ? comparison : -comparison;
    });

    return result;
  }, [tasks, activeView, activeCategory, activePriority, searchQuery, sortBy, sortOrder]);

  const handleCreateTask = async (taskData: TaskCreate) => {
    try {
      setError(null);
      setSuccessMessage(null);
      setSaving(true);
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
    } finally {
      setSaving(false);
    }
  };

  const handleUpdateTask = async (taskData: TaskCreate) => {
    if (!editingTask) return;
    try {
      setError(null);
      setSuccessMessage(null);
      setSaving(true);
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
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      setError(null);
      setSuccessMessage(null);
      setSaving(true);
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
    } finally {
      setSaving(false);
    }
  };

  const handleToggleComplete = async (taskId: string) => {
    try {
      setError(null);
      setSaving(true);
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
    } finally {
      setSaving(false);
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
    <div className="h-full w-full overflow-hidden flex relative">
      {/* Saving overlay with hourglass - z-[100] to be above Dialog */}
      {saving && (
        <div className="fixed inset-0 bg-black/30 z-[100] flex items-center justify-center backdrop-blur-sm">
          <div className="bg-card rounded-lg p-6 shadow-lg text-center">
            <div className="animate-spin text-4xl mb-3">⏳</div>
            <p className="text-muted-foreground font-medium">Saving...</p>
          </div>
        </div>
      )}

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

      {/* Main Content Area - flex column with fixed header, shifts left when chat is open */}
      <div className={`flex-1 flex flex-col h-full min-w-0 overflow-hidden transition-all duration-300 ${chatOpen ? "lg:mr-[630px] sm:mr-[576px]" : ""}`}>
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
              {activeCategory !== "all" && activeCategory === "device_schedules"
                ? " • 🔌 Device Schedules"
                : activeCategory !== "all" ? ` • ${activeCategory}` : ""}
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

            {/* MQTT Status Indicator */}
            {authToken && (
              <div className="hidden sm:block">
                <MqttStatus token={authToken} />
              </div>
            )}

            {/* Chat Loading Indicator - shown while loading chat history */}
            {chatLoading && (
              <span className="flex items-center gap-1.5 text-xs text-green-500 font-medium">
                <span className="animate-spin">⏳</span>
                <span className="hidden sm:inline">Loading chat history...</span>
              </span>
            )}
            {/* Chat Load Complete - shown briefly after loading finishes */}
            {chatLoadComplete && !chatLoading && (
              <span className="flex items-center gap-1.5 text-xs text-green-500 font-medium animate-pulse">
                <span>✓</span>
                <span className="hidden sm:inline">Chat history loaded</span>
              </span>
            )}

            {/* Notification Toggle with Bell Animation */}
            {notificationPermission !== 'unsupported' && (
              <button
                onClick={() => {
                  if (notificationPermission !== 'granted') {
                    handleRequestNotificationPermission();
                  } else {
                    // Toggle bell ringing (test or stop)
                    toggleBellRing();
                  }
                }}
                className={`p-2 rounded-lg transition-colors ${
                  bellRinging
                    ? 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400'
                    : notificationPermission === 'granted'
                    ? 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400'
                    : notificationPermission === 'denied'
                    ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
                    : 'bg-secondary hover:bg-secondary/80 text-muted-foreground'
                }`}
                title={
                  bellRinging
                    ? 'Click to stop alarm'
                    : notificationPermission === 'granted'
                    ? 'Click to test notification'
                    : notificationPermission === 'denied'
                    ? 'Notifications blocked (enable in browser settings)'
                    : 'Enable task reminders'
                }
              >
                <span
                  className={`inline-block text-lg ${bellRinging ? 'animate-bell-ring' : ''}`}
                  style={{
                    transformOrigin: 'top center',
                  }}
                >
                  {notificationPermission === 'granted' ? '🔔' : notificationPermission === 'denied' ? '🔕' : '🔔'}
                </span>
              </button>
            )}

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
                  onClick={() => loadTasks()}
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
              {([
                { value: "all", label: "All", icon: "🏷️" },
                { value: "work", label: "Work", icon: "💼" },
                { value: "personal", label: "Personal", icon: "🏠" },
                { value: "study", label: "Study", icon: "📚" },
                { value: "shopping", label: "Shopping", icon: "🛒" },
                { value: "general", label: "General", icon: "📋" },
              ] as const).map((cat) => (
                <button
                  key={cat.value}
                  onClick={() => setActiveCategory(cat.value)}
                  className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors flex items-center gap-1 ${
                    activeCategory === cat.value
                      ? "bg-primary text-primary-foreground"
                      : "bg-card hover:bg-secondary text-muted-foreground border border-border"
                  }`}
                >
                  <span>{cat.icon}</span>
                  <span>{cat.label}</span>
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

            {/* Task Count & Sort */}
            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>
                Showing {filteredTasks.length} of {tasks.length} tasks
              </span>
              <div className="flex items-center gap-3">
                {/* Sort Dropdown */}
                <div className="flex items-center gap-2">
                  <span className="hidden sm:inline">Sort:</span>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
                    className="h-8 px-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                  >
                    <option value="created_at">Date Created</option>
                    <option value="due_date">Due Date</option>
                    <option value="priority">Priority</option>
                    <option value="title">Title (A-Z)</option>
                  </select>
                  <button
                    onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
                    className="h-8 w-8 flex items-center justify-center rounded-md border border-input bg-background hover:bg-secondary transition-colors"
                    title={sortOrder === "asc" ? "Ascending" : "Descending"}
                  >
                    {sortOrder === "asc" ? "↑" : "↓"}
                  </button>
                </div>
                {/* Clear Filters */}
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
              customCategories={customCategories}
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
            customCategories={customCategories}
          />
        </DialogContent>
      </Dialog>

      {/* Chat Panel - preloadOnMount loads conversations in background when page loads */}
      <ChatKitPanel
        isOpen={chatOpen}
        onClose={() => setChatOpen(false)}
        onTasksChanged={loadTasks}
        preloadOnMount={true}
        onLoadingChange={handleChatLoadingChange}
      />
    </div>
  );
}
