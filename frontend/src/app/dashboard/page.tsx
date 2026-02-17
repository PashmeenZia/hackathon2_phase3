'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useTasks } from '@/lib/hooks/useTasks';
import {
  CheckCircle2,
  Clock,
  BarChart3,
  Plus,
  List
} from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth();
  const { tasks, loading: tasksLoading, error, createTask, toggleTaskCompletion, fetchTasks } = useTasks(user?.id || '');

  const loading = authLoading || tasksLoading;

  // Fetch tasks when component mounts
  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, fetchTasks]);

  // Calculate stats based on tasks
  const stats = {
    totalTasks: tasks.length,
    completed: tasks.filter(task => task.completed).length,
    pending: tasks.filter(task => !task.completed).length,
    completionRate: tasks.length > 0 ? Math.round((tasks.filter(task => task.completed).length / tasks.length) * 100) : 0
  };

  // Recent tasks (most recent 5)
  const recentTasks = tasks.slice(0, 5);

  // State for new task form
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [charCount, setCharCount] = useState(0);
  const [descCharCount, setDescCharCount] = useState(0);

  // Handle input change for character count
  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value.length <= 50) {
      setNewTaskTitle(value);
      setCharCount(value.length);
    }
  };

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= 200) {
      setNewTaskDescription(value);
      setDescCharCount(value.length);
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newTaskTitle.trim()) {
      try {
        await createTask(newTaskTitle, newTaskDescription, false);
        
        // Reset the form
        setNewTaskTitle('');
        setNewTaskDescription('');
        setCharCount(0);
        setDescCharCount(0);
      } catch (err) {
        console.error('Failed to create task:', err);
      }
    }
  };

  // Handle task completion toggle
  const handleToggleCompletion = async (taskId: number) => {
    try {
      await toggleTaskCompletion(taskId);
    } catch (err) {
      console.error('Failed to toggle task completion:', err);
    }
  };

  if (loading) {
    return (
      <main className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-2 border-purple-500 border-t-transparent mx-auto"></div>
          <p className="mt-4 text-gray-400">Loading tasks...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <p className="text-red-500">Error: {error}</p>
        </div>
      </main>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <section className="mb-10">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">Welcome back!</h1>
              <p className="text-gray-400">Here's what's happening with your tasks today.</p>
            </div>
          </div>
        </section>

        {/* Stats Cards Section */}
        <section className="mb-10">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Total Tasks Card */}
            <div className="bg-slate-800/50 backdrop-blur border border-white/10 rounded-xl p-6">
              <div className="flex items-center">
                <div className="bg-blue-500/20 p-3 rounded-lg mr-4">
                  <BarChart3 className="h-6 w-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Total Tasks</p>
                  <p className="text-2xl font-bold text-white">{stats.totalTasks}</p>
                </div>
              </div>
            </div>

            {/* Completed Card */}
            <div className="bg-slate-800/50 backdrop-blur border border-white/10 rounded-xl p-6">
              <div className="flex items-center">
                <div className="bg-green-500/20 p-3 rounded-lg mr-4">
                  <CheckCircle2 className="h-6 w-6 text-green-400" />
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Completed</p>
                  <p className="text-2xl font-bold text-white">{stats.completed}</p>
                </div>
              </div>
            </div>

            {/* Pending Card */}
            <div className="bg-slate-800/50 backdrop-blur border border-white/10 rounded-xl p-6">
              <div className="flex items-center">
                <div className="bg-orange-500/20 p-3 rounded-lg mr-4">
                  <Clock className="h-6 w-6 text-orange-400" />
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Pending</p>
                  <p className="text-2xl font-bold text-white">{stats.pending}</p>
                </div>
              </div>
            </div>

            {/* Completion Rate Card */}
            <div className="bg-slate-800/50 backdrop-blur border border-white/10 rounded-xl p-6">
              <div className="flex items-center">
                <div className="bg-purple-500/20 p-3 rounded-lg mr-4">
                  <BarChart3 className="h-6 w-6 text-purple-400" />
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Completion Rate</p>
                  <p className="text-2xl font-bold text-white">{stats.completionRate}%</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Recent Tasks Section */}
        <section className="mb-6">
          <div className="bg-slate-800/50 backdrop-blur border border-white/10 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white">Recent Tasks</h2>
              <Link href="/tasks" className="text-purple-400 hover:text-purple-300 text-sm font-medium transition-colors">
                View All
              </Link>
            </div>
            <div>
              {recentTasks.length === 0 ? (
                <div className="text-center py-10">
                  <p className="text-gray-400">No tasks yet. Create your first task!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {recentTasks.map((task) => (
                    <div key={task.id} className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                      <div>
                        <h3 className="font-medium text-white">{task.title}</h3>
                        <p className="text-gray-400 text-sm">{task.description}</p>
                      </div>
                      <div className="flex items-center space-x-3">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          task.completed
                            ? 'bg-green-500/20 text-green-400'
                            : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {task.completed ? 'Completed' : 'Pending'}
                        </span>
                        <button
                          onClick={() => handleToggleCompletion(task.id)}
                          className={`p-1 rounded-full ${
                            task.completed
                              ? 'text-green-400 hover:bg-green-500/20'
                              : 'text-gray-400 hover:bg-gray-500/20'
                          }`}
                          title={task.completed ? 'Mark as pending' : 'Mark as completed'}
                        >
                          <CheckCircle2 className={`h-5 w-5 ${task.completed ? 'text-green-400' : 'text-gray-400'}`} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Create New Task Section */}
        <section>
          <div className="bg-slate-800/50 backdrop-blur border border-white/10 rounded-xl p-6">
            <h2 className="text-xl font-bold text-white mb-2">Create New Task</h2>
            <p className="text-gray-400 text-sm mb-4">Add a new task to your list.</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <input
                  type="text"
                  placeholder="Enter title (2-50 characters)"
                  value={newTaskTitle}
                  onChange={handleTitleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
                <div className="text-right text-xs text-gray-400 mt-1">
                  {charCount}/50
                </div>
              </div>
              <div>
                <textarea
                  placeholder="Enter description (optional, max 200 characters)"
                  value={newTaskDescription}
                  onChange={handleDescriptionChange}
                  rows={3}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-gray-600 rounded-lg text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <div className="text-right text-xs text-gray-400 mt-1">
                  {descCharCount}/200
                </div>
              </div>
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-3 px-4 rounded-lg transition-all flex items-center justify-center space-x-2"
              >
                <Plus className="h-4 w-4" />
                <span>Create Task</span>
              </button>
            </form>
          </div>
        </section>
      </main>
  );
}