"use client";

interface TaskSummaryProps {
  total: number;
  completed: number;
}

export function TaskSummary({ total, completed }: TaskSummaryProps) {
  const remaining = total - completed;

  return (
    <div className="flex gap-4 text-sm text-muted-foreground">
      <span>
        <strong className="text-white font-semibold">{total}</strong> Total
      </span>
      <span>
        <strong className="text-green-400 font-semibold">{completed}</strong> Completed
      </span>
      <span>
        <strong className="text-blue-400 font-semibold">{remaining}</strong> Remaining
      </span>
    </div>
  );
}
