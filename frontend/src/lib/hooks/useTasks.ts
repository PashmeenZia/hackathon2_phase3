import { useState, useEffect, useCallback } from 'react';
import { Task, TaskFilterParams } from '@/types/tasks';
import {
  getTasks as getTasksAPI,
  createTask as createTaskAPI,
  updateTask as updateTaskAPI,
  deleteTask as deleteTaskAPI,
  toggleTaskCompletion as toggleTaskCompletionAPI
} from '@/lib/api/tasks';

// Hook for managing tasks state and API calls
export const useTasks = (userId: string) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Memoize the fetchTasks function to prevent infinite loop
  const fetchTasks = useCallback(async (filters?: TaskFilterParams) => {
    setLoading(true);
    setError(null);

    try {
      const tasksData = await getTasksAPI(filters);
      // Convert API response to frontend Task type
      const frontendTasks: Task[] = tasksData.map(task => ({
        id: task.id,
        title: task.title,
        description: task.description,
        completed: task.completed,
        user_id: task.user_id,
        created_at: task.created_at,
        updated_at: task.updated_at,
        isEditing: false,
        isSaving: false
      }));

      setTasks(frontendTasks);
    } catch (err) {
      // Only set error if it's different from current error to prevent infinite loop
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch tasks';
      if (errorMessage !== error) {
        setError(errorMessage);
      }
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [error]); // Add error to dependencies to prevent infinite loop

  // Memoize other functions as well
  const createTask = useCallback(async (
    title: string,
    description: string,
    completed: boolean = false
  ) => {
    setLoading(true);
    setError(null);

    try {
      const newTask = await createTaskAPI(title, description, completed);
      // Convert to frontend Task type and add to state
      const frontendTask: Task = {
        id: newTask.id,
        title: newTask.title,
        description: newTask.description,
        completed: newTask.completed,
        user_id: newTask.user_id,
        created_at: newTask.created_at,
        updated_at: newTask.updated_at,
        isEditing: false,
        isSaving: false
      };

      setTasks(prevTasks => [...prevTasks, frontendTask]);
      return frontendTask;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
      console.error('Error creating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateTask = useCallback(async (id: number, updateData: Partial<Task>) => {
    setLoading(true);
    setError(null);

    try {
      // Find the current task to get its current state
      const currentTask = tasks.find(task => task.id === id);
      if (!currentTask) {
        throw new Error('Task not found');
      }

      // Update the task in the UI optimistically
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id ? { ...task, ...updateData, isSaving: true } : task
        )
      );

      // Update the task in the API
      const updatedTask = await updateTaskAPI(id, updateData);

      // Update the task in the UI with the server response
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id
            ? {
                ...task,
                ...updatedTask,
                isEditing: false,
                isSaving: false
              }
            : task
        )
      );

      return updatedTask;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
      console.error('Error updating task:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [tasks]);

  const deleteTask = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);

    try {
      // Remove the task from UI optimistically
      setTasks(prevTasks => prevTasks.filter(task => task.id !== id));

      // Delete the task from the API
      await deleteTaskAPI(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      console.error('Error deleting task:', err);
      // Revert the optimistic update on failure
      const taskToRestore = tasks.find(task => task.id === id);
      if (taskToRestore) {
        setTasks(prevTasks => [...prevTasks, taskToRestore]);
      }
      throw err;
    } finally {
      setLoading(false);
    }
  }, [tasks]);

  const toggleTaskCompletion = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);

    try {
      // Find the current task to get its current state
      const currentTask = tasks.find(task => task.id === id);
      if (!currentTask) {
        throw new Error('Task not found');
      }

      // Update the task in the UI optimistically
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id
            ? { ...task, completed: !task.completed, isSaving: true }
            : task
        )
      );

      // Toggle completion in the API
      const updatedTask = await toggleTaskCompletionAPI(id);

      // Update the task in the UI with the server response
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id
            ? {
                ...task,
                ...updatedTask,
                isSaving: false
              }
            : task
        )
      );

      return updatedTask;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to toggle task completion');
      console.error('Error toggling task completion:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [tasks]);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
};