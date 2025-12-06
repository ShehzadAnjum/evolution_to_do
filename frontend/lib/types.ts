/**
 * Type definitions for Phase II - Evolution of Todo
 */

// Task types matching backend API
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_complete?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  completed: number;
}

// User types
export interface User {
  id: string;
  email: string;
  name?: string;
  image?: string;
}

// API error type
export interface ApiError {
  detail: string;
  status_code?: number;
}
