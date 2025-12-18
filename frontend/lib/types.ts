/**
 * Type definitions for Phase II - Evolution of Todo
 *
 * v2.0.0: Added priority, category, due_date fields
 * v4.0.0: Added IoT device scheduling fields
 */

// Priority levels
export type Priority = 'high' | 'medium' | 'low';

// Recurrence patterns
export type RecurrencePattern = 'none' | 'daily' | 'weekly' | 'biweekly' | 'monthly';

// v4.0.0: Task types
export type TaskType = 'regular' | 'device_schedule';

// v4.0.0: Device actions
export type DeviceAction = 'on' | 'off' | 'toggle';

// v4.0.0: Weekday for weekly schedules
export type Weekday = 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday';

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
  // v3.0.0: Time picker support
  due_time: string | null;
  // v3.1.0: Recurring tasks
  recurrence_pattern: RecurrencePattern;
  // v4.0.0: Device scheduling fields
  task_type: TaskType;
  device_id: string | null;
  relay_number: number | null;
  device_action: DeviceAction | null;
  weekday: Weekday | null;
  mqtt_command_id: string | null;
  schedule_synced: boolean;
}

export interface TaskCreate {
  title: string;
  description?: string;
  // v2.0.0: New optional fields
  priority?: Priority;
  category?: string;
  due_date?: string;
  // v3.0.0: Time picker
  due_time?: string;
  // v3.1.0: Recurring tasks
  recurrence_pattern?: RecurrencePattern;
  // v4.0.0: Device scheduling fields
  task_type?: TaskType;
  device_id?: string;
  relay_number?: number;
  device_action?: DeviceAction;
  weekday?: Weekday;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_complete?: boolean;
  // v2.0.0: New optional fields
  priority?: Priority;
  category?: string;
  due_date?: string | null;
  // v3.0.0: Time picker
  due_time?: string | null;
  // v3.1.0: Recurring tasks
  recurrence_pattern?: RecurrencePattern;
  // v4.0.0: Device scheduling fields
  task_type?: TaskType;
  device_id?: string | null;
  relay_number?: number | null;
  device_action?: DeviceAction | null;
  weekday?: Weekday | null;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  completed: number;
  filtered_count?: number;
}

// Filter and sort options for task list
export type TaskStatus = 'all' | 'complete' | 'incomplete';
export type SortBy = 'created_at' | 'due_date' | 'priority' | 'title' | 'updated_at';
export type SortOrder = 'asc' | 'desc';

export interface TaskFilterOptions {
  search?: string;
  category?: string;
  priority?: Priority;
  status?: TaskStatus;
  sort_by?: SortBy;
  sort_order?: SortOrder;
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

// Custom category types
export interface Category {
  id: string;
  user_id: string;
  name: string;
  icon: string;
  created_at: string;
}

export interface CategoryCreate {
  name: string;
  icon?: string;
}

// v4.0.0: IoT Device types
export interface RelayStatus {
  number: number;
  name: string;
  state: 'on' | 'off';
}

export interface DeviceStatus {
  online: boolean;
  relays: RelayStatus[];
  last_heartbeat: string | null;
  wifi_rssi: number | null;
  last_updated: string | null;
  mqtt_connected: boolean;
}

export interface DeviceCommandRequest {
  relay_number: number;
  action: DeviceAction;
}

export interface DeviceCommandResponse {
  success: boolean;
  command_id: string | null;
  relay_name: string | null;
  action: string | null;
  message: string;
  error: string | null;
}

// Relay name mapping for display
export const RELAY_NAMES: Record<number, string> = {
  1: 'Light',
  2: 'Fan',
  3: 'Aquarium',
  4: 'Relay 4',
};
