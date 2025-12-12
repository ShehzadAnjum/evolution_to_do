"use client";

import { useState } from "react";
import type { Task, Priority, Category, CategoryCreate } from "@/lib/types";

export type FilterView = "all" | "today" | "upcoming" | "completed";
export type CategoryFilter = "all" | "work" | "personal" | "study" | "shopping" | "general" | string;
export type PriorityFilter = "all" | Priority;

// Keep CustomCategory for backward compatibility (will be removed after migration)
export interface CustomCategory {
  value: string;
  label: string;
  icon: string;
}

interface SidebarProps {
  tasks: Task[];
  activeView: FilterView;
  activeCategory: CategoryFilter;
  activePriority: PriorityFilter;
  onViewChange: (view: FilterView) => void;
  onCategoryChange: (category: CategoryFilter) => void;
  onPriorityChange: (priority: PriorityFilter) => void;
  customCategories?: Category[];
  onAddCategory?: (data: CategoryCreate) => Promise<void>;
  isLoadingCategories?: boolean;
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
  // Use local date string (YYYY-MM-DD) to avoid timezone issues
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  const todayStr = `${year}-${month}-${day}`;

  // Calculate date 3 days from now
  const threeDaysLater = new Date(today);
  threeDaysLater.setDate(threeDaysLater.getDate() + 3);
  const y3 = threeDaysLater.getFullYear();
  const m3 = String(threeDaysLater.getMonth() + 1).padStart(2, '0');
  const d3 = String(threeDaysLater.getDate()).padStart(2, '0');
  const threeDaysStr = `${y3}-${m3}-${d3}`;

  const total = tasks.length;
  const completed = tasks.filter(t => t.is_complete).length;
  const todayTasks = tasks.filter(t => t.due_date === todayStr && !t.is_complete).length;
  const upcoming = tasks.filter(t => {
    if (!t.due_date || t.is_complete) return false;
    // Due within next 3 days (excluding today, including overdue)
    return t.due_date > todayStr && t.due_date <= threeDaysStr;
  }).length;
  const overdue = tasks.filter(t => {
    if (!t.due_date || t.is_complete) return false;
    // Compare dates as strings (YYYY-MM-DD format)
    return t.due_date < todayStr;
  }).length;

  return { total, completed, todayTasks, upcoming, overdue };
}

const EMOJI_OPTIONS = ["📁", "🎯", "💡", "🎨", "🏃", "📖", "🎵", "✈️", "🍔", "💰", "🏠", "❤️"];

export function Sidebar({
  tasks,
  activeView,
  activeCategory,
  activePriority,
  onViewChange,
  onCategoryChange,
  onPriorityChange,
  customCategories = [],
  onAddCategory,
  isLoadingCategories = false,
}: SidebarProps) {
  const stats = getStats(tasks);
  const [showAddCategory, setShowAddCategory] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [newCategoryIcon, setNewCategoryIcon] = useState("📁");
  const [isAdding, setIsAdding] = useState(false);

  const handleAddCategory = async () => {
    if (newCategoryName.trim() && onAddCategory) {
      setIsAdding(true);
      try {
        await onAddCategory({
          name: newCategoryName.trim(),
          icon: newCategoryIcon,
        });
        setNewCategoryName("");
        setNewCategoryIcon("📁");
        setShowAddCategory(false);
      } catch (error) {
        console.error("Failed to add category:", error);
      } finally {
        setIsAdding(false);
      }
    }
  };

  return (
    <aside className="sidebar h-screen flex flex-col">
      {/* App Title - Fixed at top */}
      <div className="flex items-center gap-2 px-4 py-4 border-b border-border/50 shrink-0">
        <span className="text-2xl">🎯</span>
        <h1 className="text-lg font-semibold text-foreground">Evolution Todo</h1>
      </div>

      {/* Scrollable content - hidden scrollbar */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-hide">
        {/* Quick Stats - Compact */}
        <div className="flex flex-wrap gap-1.5">
          <div className="bg-secondary/50 rounded-md px-2 py-1 text-center min-w-[52px]">
            <div className="text-sm font-semibold text-foreground">{stats.total}</div>
            <div className="text-[10px] text-muted-foreground">Total</div>
          </div>
          <div className="bg-secondary/50 rounded-md px-2 py-1 text-center min-w-[52px]">
            <div className="text-sm font-semibold text-green-600 dark:text-green-400">{stats.completed}</div>
            <div className="text-[10px] text-muted-foreground">Done</div>
          </div>
          <div className="bg-secondary/50 rounded-md px-2 py-1 text-center min-w-[52px]">
            <div className="text-sm font-semibold text-blue-600 dark:text-blue-400">{stats.todayTasks}</div>
            <div className="text-[10px] text-muted-foreground">Today</div>
          </div>
          <div className="bg-secondary/50 rounded-md px-2 py-1 text-center min-w-[52px]">
            <div className="text-sm font-semibold text-orange-600 dark:text-orange-400">{stats.upcoming}</div>
            <div className="text-[10px] text-muted-foreground">Next 3 Days</div>
          </div>
          <div className="bg-secondary/50 rounded-md px-2 py-1 text-center min-w-[52px]">
            <div className="text-sm font-semibold text-red-600 dark:text-red-400">{stats.overdue}</div>
            <div className="text-[10px] text-muted-foreground">Overdue</div>
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
          {/* Custom Categories from DB */}
          {isLoadingCategories ? (
            <div className="px-2 py-2 text-xs text-muted-foreground">Loading...</div>
          ) : (
            customCategories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => onCategoryChange(cat.name.toLowerCase())}
                className={`sidebar-item w-full ${activeCategory === cat.name.toLowerCase() ? "active" : ""}`}
              >
                <span>{cat.icon}</span>
                <span>{cat.name}</span>
              </button>
            ))
          )}
          {/* Add Category Button */}
          {!showAddCategory ? (
            <button
              onClick={() => setShowAddCategory(true)}
              className="sidebar-item w-full text-primary hover:text-primary"
            >
              <span>➕</span>
              <span>Add Category</span>
            </button>
          ) : (
            <div className="px-2 py-2 space-y-2 bg-secondary/50 rounded-lg">
              {/* Icon Selector */}
              <div className="flex flex-wrap gap-1">
                {EMOJI_OPTIONS.map((emoji) => (
                  <button
                    key={emoji}
                    onClick={() => setNewCategoryIcon(emoji)}
                    className={`w-7 h-7 rounded flex items-center justify-center text-sm hover:bg-secondary ${
                      newCategoryIcon === emoji ? "bg-primary/20 ring-1 ring-primary" : ""
                    }`}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
              {/* Name Input */}
              <input
                type="text"
                placeholder="Category name"
                value={newCategoryName}
                onChange={(e) => setNewCategoryName(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAddCategory()}
                className="w-full px-2 py-1.5 text-sm rounded border border-input bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                autoFocus
              />
              {/* Action Buttons */}
              <div className="flex gap-2">
                <button
                  onClick={handleAddCategory}
                  disabled={!newCategoryName.trim() || isAdding}
                  className="flex-1 px-2 py-1 text-xs font-medium bg-primary text-primary-foreground rounded hover:bg-primary/90 disabled:opacity-50"
                >
                  {isAdding ? "Adding..." : "Add"}
                </button>
                <button
                  onClick={() => {
                    setShowAddCategory(false);
                    setNewCategoryName("");
                  }}
                  disabled={isAdding}
                  className="flex-1 px-2 py-1 text-xs font-medium bg-secondary text-secondary-foreground rounded hover:bg-secondary/80 disabled:opacity-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
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
