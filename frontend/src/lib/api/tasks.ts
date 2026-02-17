import { apiClient } from './client';
import { TaskResponse, TaskListResponse, TaskFilterParams } from '@/types/tasks';

/**
 * Task API service
 * Contains functions for all task-related operations
 */

// Get all tasks for the authenticated user
export const getTasks = async (
  filters?: TaskFilterParams
): Promise<TaskResponse[]> => {
  // Build query params
  const params = new URLSearchParams();
  if (filters) {
    if (filters.status) params.append('status', filters.status);
    if (filters.search) params.append('search', filters.search);
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());
  }

  const response = await apiClient.get(`/api/tasks?${params.toString()}`);
  return response.data;
};

// Get a specific task by ID
export const getTaskById = async (id: number): Promise<TaskResponse> => {
  const response = await apiClient.get(`/api/tasks/${id}`);
  return response.data;
};

// Create a new task
export const createTask = async (
  title: string,
  description: string,
  completed: boolean
): Promise<TaskResponse> => {
  const response = await apiClient.post('/api/tasks', {
    title,
    description,
    completed,
  });
  return response.data;
};

// Update a task by ID
export const updateTask = async (
  id: number,
  updateData: Partial<Omit<TaskResponse, 'id' | 'user_id' | 'created_at' | 'updated_at'>>
): Promise<TaskResponse> => {
  const response = await apiClient.put(`/api/tasks/${id}`, updateData);
  return response.data;
};

// Delete a task by ID
export const deleteTask = async (id: number): Promise<void> => {
  await apiClient.delete(`/api/tasks/${id}`);
};

// Toggle task completion status
export const toggleTaskCompletion = async (id: number): Promise<TaskResponse> => {
  const response = await apiClient.patch(`/api/tasks/${id}/complete`);
  return response.data;
};