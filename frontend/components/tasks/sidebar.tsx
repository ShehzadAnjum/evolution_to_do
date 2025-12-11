"use client";

import type { Task, Priority } from "@/lib/types";

export type FilterView = "all" | "today" | "upcoming" | "completed";
export type CategoryFilter = "all" | "work" | "personal" | "study" | "shopping" | "general";
export type PriorityFilter = "all" | Priority;

interface SidebarProps {
  tasks: Task[];
  activeView: FilterView;
  activeCategory: CategoryFilter;
  activePriority: PriorityFilter;
  onViewChange: (view: FilterView) => void;
  onCategoryChange: (category: CategoryFilter) => void;
  onPriorityChange: (priority: PriorityFilter) => void;
}

const VIEW_OPTIONS: { value: FilterView; label: string; icon: string }[] = [
  { value: "all", label: "All Tasks", icon: "📋" },
  { value: "today", label: "Today", icon: "📅" },
  { value: "upcoming", label: "Upcoming", icon: "📆" },
  { value: "completed", label: "Completed", icon: "✅" },
];

const CATEGORY_OPTIONS: { value: CategoryFilter; label: string; icon: string }[] = [
  { value: "all", label: "All Categories", icon: "🏷️" },
  { value: "work", label: "Work", icon: "💼" },
  { value: "personal", label: "Personal", icon: "🏠" },
  { value: "study", label: "Study", icon: "📚" },
  { value: "shopping", label: "Shopping", icon: "🛒" },
  { value: "general", label: "General", icon: "📋" },
];

const PRIORITY_OPTIONS: { value: PriorityFilter; label: string; icon: string }[] = [
  { value: "all", label: "All Priorities", icon: "⚡" },
  { value: "high", label: "High", icon: "🔴" },
  { value: "medium", label: "Medium", icon: "🟡" },
  { value: "low", label: "Low", icon: "🟢" },
];

// Calculate stats from tasks
function getStats(tasks: Task[]) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayStr = today.toISOString().split('T')[0];

  const total = tasks.length;
  const completed = tasks.filter(t => t.is_complete).length;
  const todayTasks = tasks.filter(t => t.due_date === todayStr && !t.is_complete).length;
  const overdue = tasks.filter(t => {
    if (!t.due_date || t.is_complete) return false;
    return new Date(t.due_date) < today;
  }).length;

  return { total, completed, todayTasks, overdue };
}

export function Sidebar({
  tasks,
  activeView,
  activeCategory,
  activePriority,
  onViewChange,
  onCategoryChange,
  onPriorityChange,
}: SidebarProps) {
  const stats = getStats(tasks);

  return (
    <aside className="sidebar h-screen flex flex-col">
      {/* App Title - Fixed at top */}
      <div className="flex items-center gap-2 px-4 py-4 border-b border-border/50 shrink-0">
        <span className="text-2xl">🎯</span>
        <h1 className="text-lg font-semibold text-foreground">Evolution Todo</h1>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-secondary/50 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-foreground">{stats.total}</div>
            <div className="text-xs text-muted-foreground">Total</div>
          </div>
          <div className="bg-secondary/50 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-success">{stats.completed}</div>
            <div className="text-xs text-muted-foreground">Done</div>
          </div>
          <div className="bg-secondary/50 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-warning">{stats.todayTasks}</div>
            <div className="text-xs text-muted-foreground">Today</div>
          </div>
          <div className="bg-secondary/50 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-danger">{stats.overdue}</div>
            <div className="text-xs text-muted-foreground">Overdue</div>
          </div>
        </div>

        {/* View Filters */}
        <div className="space-y-1">
          <h2 className="px-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Views
          </h2>
          {VIEW_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => onViewChange(opt.value)}
              className={`sidebar-item w-full ${activeView === opt.value ? "active" : ""}`}
            >
              <span>{opt.icon}</span>
              <span>{opt.label}</span>
            </button>
          ))}
        </div>

        {/* Category Filters */}
        <div className="space-y-1">
          <h2 className="px-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Categories
          </h2>
          {CATEGORY_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => onCategoryChange(opt.value)}
              className={`sidebar-item w-full ${activeCategory === opt.value ? "active" : ""}`}
            >
              <span>{opt.icon}</span>
              <span>{opt.label}</span>
            </button>
          ))}
        </div>

        {/* Priority Filters */}
        <div className="space-y-1">
          <h2 className="px-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Priority
          </h2>
          {PRIORITY_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => onPriorityChange(opt.value)}
              className={`sidebar-item w-full ${activePriority === opt.value ? "active" : ""}`}
            >
              <span>{opt.icon}</span>
              <span>{opt.label}</span>
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
}
