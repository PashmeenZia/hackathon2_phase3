'use client';

import { useAuth } from '@/context/AuthContext';
import { TaskList } from '@/components/tasks/TaskList';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthUser } from '@/types/auth';

export default function TasksPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/signin');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="glass-card p-8 rounded-xl">
      <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-6">My Tasks</h1>
      <TaskList userId={user.id} />
    </div>
  );
}