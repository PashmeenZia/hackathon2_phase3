import { useState } from 'react';
import { Task } from '@/types/tasks';

interface TaskCardProps {
  task: Task;
  onToggleCompletion: (id: number) => void;
  onEdit: (task: Task) => void;
  onSave: (id: number, updatedData: Partial<Task>) => void;
  onDelete: (id: number) => void;
  onCancelEdit: () => void;
}

export const TaskCard = ({
  task,
  onToggleCompletion,
  onEdit,
  onSave,
  onDelete,
  onCancelEdit,
}: TaskCardProps) => {
  const [editedTask, setEditedTask] = useState({
    title: task.title,
    description: task.description,
    completed: task.completed,
  });

  const handleSaveEdit = () => {
    onSave(task.id, editedTask);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setEditedTask(prev => ({
      ...prev,
      [name]: name === 'completed' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  return (
    <div className={`glass-card rounded-xl p-6 transition-all duration-300 hover:shadow-md group ${task.completed ? 'opacity-75' : ''}`}>
      {task.isEditing ? (
        <div className="space-y-4">
          <input
            type="text"
            name="title"
            value={editedTask.title}
            onChange={handleInputChange}
            className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors text-gray-900 dark:text-white"
            placeholder="Task title..."
          />
          <textarea
            name="description"
            value={editedTask.description}
            onChange={handleInputChange}
            rows={3}
            className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors resize-none text-gray-900 dark:text-white"
            placeholder="Task description..."
          />
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                type="checkbox"
                name="completed"
                checked={editedTask.completed}
                onChange={handleInputChange}
                className="h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
              />
              <span className="ml-2 text-gray-700 dark:text-gray-300">Completed</span>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={onCancelEdit}
                className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all shadow-sm hover:shadow-md font-medium"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1 min-w-0">
              <button
                onClick={() => onToggleCompletion(task.id)}
                className={`flex-shrink-0 w-5 h-5 mt-1 rounded border-2 transition-all duration-200 ${
                  task.completed
                    ? 'bg-indigo-500 border-indigo-500 text-white'
                    : 'border-gray-300 dark:border-gray-500 hover:border-indigo-400'
                }`}
              >
                {task.completed && (
                  <svg className="w-3 h-3 m-0.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
              <div className="flex-1 min-w-0">
                <h3 className={`text-lg font-semibold text-gray-900 dark:text-white break-words ${
                  task.completed ? 'line-through text-gray-500 dark:text-gray-400' : ''
                }`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className={`mt-2 text-gray-600 dark:text-gray-400 break-words ${
                    task.completed ? 'line-through text-gray-400 dark:text-gray-500' : ''
                  }`}>
                    {task.description}
                  </p>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-2 ml-4 flex-shrink-0">
              <button
                onClick={() => onEdit(task)}
                className="p-2 text-gray-500 hover:text-indigo-600 dark:text-gray-400 dark:hover:text-indigo-400 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors"
                title="Edit task"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="p-2 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors"
                title="Delete task"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100 dark:border-gray-600">
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Created: {new Date(task.created_at).toLocaleDateString()}
            </div>
            {task.completed && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                Completed
              </span>
            )}
            {!task.completed && task.isSaving && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                Saving...
              </span>
            )}
          </div>
        </>
      )}
    </div>
  );
};