"use client";

import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import type { Task } from "@/lib/types";

interface TaskStatsProps {
  tasks: Task[];
}

// Calculate comprehensive stats from tasks
function getStats(tasks: Task[]) {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");
  const todayStr = `${year}-${month}-${day}`;

  const total = tasks.length;
  const completed = tasks.filter((t) => t.is_complete).length;
  const pending = total - completed;
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const todayTasks = tasks.filter(
    (t) => t.due_date === todayStr && !t.is_complete
  ).length;

  const overdue = tasks.filter((t) => {
    if (!t.due_date || t.is_complete) return false;
    return t.due_date < todayStr;
  }).length;

  // Priority breakdown
  const highPriority = tasks.filter(
    (t) => t.priority === "high" && !t.is_complete
  ).length;
  const mediumPriority = tasks.filter(
    (t) => t.priority === "medium" && !t.is_complete
  ).length;
  const lowPriority = tasks.filter(
    (t) => t.priority === "low" && !t.is_complete
  ).length;

  return {
    total,
    completed,
    pending,
    completionRate,
    todayTasks,
    overdue,
    highPriority,
    mediumPriority,
    lowPriority,
  };
}

export function TaskStats({ tasks }: TaskStatsProps) {
  const stats = getStats(tasks);

  // Data for donut chart
  const chartData = [
    { name: "Completed", value: stats.completed, color: "#22c55e" }, // green-500
    { name: "Pending", value: stats.pending, color: "#64748b" }, // slate-500
  ];

  // If no tasks, show empty state
  if (stats.total === 0) {
    return (
      <div className="text-center py-4">
        <div className="text-3xl mb-2">📋</div>
        <p className="text-xs text-muted-foreground">No tasks yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Donut Chart with center label */}
      <div className="relative h-32">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={35}
              outerRadius={50}
              paddingAngle={2}
              dataKey="value"
              strokeWidth={0}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        {/* Center label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="text-xl font-bold text-foreground">
            {stats.completionRate}%
          </span>
          <span className="text-[10px] text-muted-foreground">Complete</span>
        </div>
      </div>

      {/* Legend */}
      <div className="flex justify-center gap-4 text-xs">
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-green-500"></div>
          <span className="text-muted-foreground">
            Done ({stats.completed})
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-slate-500"></div>
          <span className="text-muted-foreground">
            Pending ({stats.pending})
          </span>
        </div>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-2 gap-2">
        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-2 text-center">
          <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
            {stats.todayTasks}
          </div>
          <div className="text-[10px] text-muted-foreground">Due Today</div>
        </div>
        <div
          className={`rounded-lg p-2 text-center ${
            stats.overdue > 0
              ? "bg-red-500/10 border border-red-500/20"
              : "bg-secondary/50 border border-transparent"
          }`}
        >
          <div
            className={`text-lg font-bold ${
              stats.overdue > 0
                ? "text-red-600 dark:text-red-400"
                : "text-muted-foreground"
            }`}
          >
            {stats.overdue}
          </div>
          <div className="text-[10px] text-muted-foreground">Overdue</div>
        </div>
      </div>

      {/* Priority Breakdown */}
      <div className="space-y-1.5">
        <div className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-1">
          By Priority
        </div>
        {/* High */}
        <div className="flex items-center gap-2">
          <span className="text-xs w-14">High</span>
          <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-red-500 rounded-full transition-all"
              style={{
                width: `${
                  stats.pending > 0
                    ? (stats.highPriority / stats.pending) * 100
                    : 0
                }%`,
              }}
            ></div>
          </div>
          <span className="text-xs w-5 text-right text-muted-foreground">
            {stats.highPriority}
          </span>
        </div>
        {/* Medium */}
        <div className="flex items-center gap-2">
          <span className="text-xs w-14">Medium</span>
          <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-yellow-500 rounded-full transition-all"
              style={{
                width: `${
                  stats.pending > 0
                    ? (stats.mediumPriority / stats.pending) * 100
                    : 0
                }%`,
              }}
            ></div>
          </div>
          <span className="text-xs w-5 text-right text-muted-foreground">
            {stats.mediumPriority}
          </span>
        </div>
        {/* Low */}
        <div className="flex items-center gap-2">
          <span className="text-xs w-14">Low</span>
          <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 rounded-full transition-all"
              style={{
                width: `${
                  stats.pending > 0
                    ? (stats.lowPriority / stats.pending) * 100
                    : 0
                }%`,
              }}
            ></div>
          </div>
          <span className="text-xs w-5 text-right text-muted-foreground">
            {stats.lowPriority}
          </span>
        </div>
      </div>
    </div>
  );
}
