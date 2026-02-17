'use client';

import { useState, useEffect } from 'react';
import { Task } from '@/types/tasks';
import { useTasks } from '@/lib/hooks/useTasks';
import { TaskCard } from './TaskCard';
import { TaskForm } from './TaskForm';

interface TaskListProps {
  userId: string;
}

export const TaskList = ({ userId }: TaskListProps) => {
  const {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  } = useTasks(userId);

  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Fetch tasks when component mounts
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (title: string, description: string, completed: boolean) => {
    try {
      await createTask(title, description, completed);
      setShowForm(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleUpdateTask = async (id: number, updatedData: Partial<Task>) => {
    try {
      await updateTask(id, updatedData);
      setEditingTask(null);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await deleteTask(id);
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleToggleCompletion = async (id: number) => {
    try {
      await toggleTaskCompletion(id);
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center py-12">
      <div className="animate-spin rounded-full h-8 w-8 border-2 border-purple-500 border-t-transparent"></div>
    </div>
  );

  if (error) return (
    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-center">
      Error: {error}
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Your Tasks</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} assigned to you
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 duration-200 font-medium min-w-32"
        >
          {showForm ? 'Cancel' : '+ Add Task'}
        </button>
      </div>

      {showForm && (
        <div className="glass-card p-6 rounded-2xl">
          <TaskForm
            onSubmit={handleCreateTask}
            onCancel={() => setShowForm(false)}
          />
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-purple-500 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No tasks yet</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">Get started by creating your first task</p>
          <button
            onClick={() => setShowForm(true)}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl font-medium"
          >
            Create Your First Task
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggleCompletion={handleToggleCompletion}
              onEdit={(t) => setEditingTask(t)}
              onSave={handleUpdateTask}
              onDelete={handleDeleteTask}
              onCancelEdit={() => setEditingTask(null)}
            />
          ))}
        </div>
      )}

      {editingTask && (
        <div className="glass-card p-6 rounded-2xl">
          <TaskForm
            task={editingTask}
            onSubmit={(title, description, completed) =>
              handleUpdateTask(editingTask.id, { title, description, completed })
            }
            onCancel={() => setEditingTask(null)}
          />
        </div>
      )}
    </div>
  );
};