// Task-related types

export interface Task {
  // Core attributes (matching backend)
  id: number;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;

  // Metadata
  created_at: string; // ISO date string
  updated_at: string; // ISO date string

  // UI-specific
  isEditing?: boolean;
  isSaving?: boolean;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  completed: boolean;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskResponse {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: TaskResponse[];
}

export interface TaskFilterParams {
  status?: 'all' | 'pending' | 'completed';
  search?: string;
  limit?: number;
  offset?: number;
}