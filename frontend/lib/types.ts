/**
 * Type definitions for Phase II - Evolution of Todo
 *
 * v2.0.0: Added priority, category, due_date fields
 */

// Priority levels
export type Priority = 'high' | 'medium' | 'low';

// Default categories (users can also use custom categories)
export type DefaultCategory = 'general' | 'work' | 'personal' | 'study' | 'shopping';

// Task types matching backend API
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
  // v2.0.0: New fields
  priority: Priority;
  category: string;
  due_date: string | null;
}

export interface TaskCreate {
  title: string;
  description?: string;
  // v2.0.0: New optional fields
  priority?: Priority;
  category?: string;
  due_date?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_complete?: boolean;
  // v2.0.0: New optional fields
  priority?: Priority;
  category?: string;
  due_date?: string | null;
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
