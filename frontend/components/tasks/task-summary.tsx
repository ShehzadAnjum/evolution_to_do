"use client";

interface TaskSummaryProps {
  total: number;
  completed: number;
}

export function TaskSummary({ total, completed }: TaskSummaryProps) {
  const remaining = total - completed;

  return (
    <div className="flex gap-4 text-sm text-gray-600">
      <span>
        <strong className="text-gray-900">{total}</strong> total
      </span>
      <span>
        <strong className="text-green-600">{completed}</strong> completed
      </span>
      <span>
        <strong className="text-blue-600">{remaining}</strong> remaining
      </span>
    </div>
  );
}
