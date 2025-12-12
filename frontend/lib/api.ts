/**
 * API client for Phase II - Evolution of Todo
 *
 * Provides typed functions for all backend API endpoints.
 */

import type { Task, TaskCreate, TaskListResponse, TaskUpdate, Category, CategoryCreate, TaskFilterOptions } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * API error class for handling backend errors.
 */
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Fetch wrapper with error handling and auth.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: "An error occurred",
    }));
    throw new ApiError(response.status, error.detail || "Request failed");
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * Health check endpoint.
 */
export async function checkHealth(): Promise<{ status: string; timestamp: string }> {
  return fetchApi("/health");
}

/**
 * Get all tasks for the current user with optional filters and sorting.
 */
export async function getTasks(
  token: string,
  options?: TaskFilterOptions
): Promise<TaskListResponse> {
  // Build query string from options
  const params = new URLSearchParams();
  if (options?.search) params.set("search", options.search);
  if (options?.category) params.set("category", options.category);
  if (options?.priority) params.set("priority", options.priority);
  if (options?.status) params.set("status", options.status);
  if (options?.sort_by) params.set("sort_by", options.sort_by);
  if (options?.sort_order) params.set("sort_order", options.sort_order);

  const queryString = params.toString();
  const endpoint = queryString ? `/api/tasks/?${queryString}` : "/api/tasks/";

  return fetchApi(endpoint, {}, token);
}

/**
 * Create a new task.
 */
export async function createTask(
  token: string,
  data: TaskCreate
): Promise<Task> {
  return fetchApi(
    "/api/tasks/",
    {
      method: "POST",
      body: JSON.stringify(data),
    },
    token
  );
}

/**
 * Get a single task by ID.
 */
export async function getTask(token: string, taskId: string): Promise<Task> {
  return fetchApi(`/api/tasks/${taskId}`, {}, token);
}

/**
 * Update a task.
 */
export async function updateTask(
  token: string,
  taskId: string,
  data: TaskUpdate
): Promise<Task> {
  return fetchApi(
    `/api/tasks/${taskId}`,
    {
      method: "PUT",
      body: JSON.stringify(data),
    },
    token
  );
}

/**
 * Delete a task.
 */
export async function deleteTask(token: string, taskId: string): Promise<void> {
  return fetchApi(
    `/api/tasks/${taskId}`,
    {
      method: "DELETE",
    },
    token
  );
}

/**
 * Toggle task completion status.
 */
export async function toggleComplete(
  token: string,
  taskId: string
): Promise<Task> {
  return fetchApi(
    `/api/tasks/${taskId}/complete`,
    {
      method: "PATCH",
    },
    token
  );
}

// ============================================================
// Category API Functions
// ============================================================

/**
 * Get all custom categories for the current user.
 */
export async function getCategories(token: string): Promise<Category[]> {
  return fetchApi("/api/categories/", {}, token);
}

/**
 * Create a new custom category.
 */
export async function createCategory(
  token: string,
  data: CategoryCreate
): Promise<Category> {
  return fetchApi(
    "/api/categories/",
    {
      method: "POST",
      body: JSON.stringify(data),
    },
    token
  );
}

/**
 * Delete a custom category.
 */
export async function deleteCategory(token: string, categoryId: string): Promise<void> {
  return fetchApi(
    `/api/categories/${categoryId}`,
    {
      method: "DELETE",
    },
    token
  );
}
