'use client';

import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function SettingsPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/signin');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-2 border-purple-500 border-t-transparent mx-auto"></div>
          <p className="mt-4 text-gray-400">Loading settings...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="min-h-screen bg-black">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">Settings</h1>
          <p className="text-gray-400">Manage your account preferences and settings</p>
        </div>

        <div className="card p-8">
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-white mb-4">Account Information</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
                  <input
                    type="email"
                    value={user?.email || ''}
                    readOnly
                    className="input-field w-full bg-gray-800 cursor-not-allowed"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Name</label>
                  <input
                    type="text"
                    value={user?.name || ''}
                    readOnly
                    className="input-field w-full bg-gray-800 cursor-not-allowed"
                  />
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-gray-700">
              <h2 className="text-xl font-semibold text-white mb-4">Preferences</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-white">Dark Mode</h3>
                    <p className="text-gray-400 text-sm">Always use dark theme</p>
                  </div>
                  <div className="relative inline-block w-10 h-6 align-middle select-none">
                    <input type="checkbox" name="darkModeToggle" id="darkModeToggle" className="sr-only" defaultChecked />
                    <label htmlFor="darkModeToggle" className="block w-10 h-6 rounded-full bg-gray-600 cursor-pointer">
                      <span className="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform duration-200 transform translate-x-4"></span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-gray-700">
              <h2 className="text-xl font-semibold text-white mb-4">Danger Zone</h2>
              <div className="bg-red-900/20 border border-red-800 rounded-lg p-4">
                <h3 className="font-medium text-red-400">Delete Account</h3>
                <p className="text-red-300 text-sm mt-1">Permanently remove your account and all data.</p>
                <button className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition-colors">
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}