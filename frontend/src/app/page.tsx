'use client';

import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-2 border-purple-500 border-t-transparent mx-auto"></div>
          <p className="mt-4 text-gray-400">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // If user is authenticated, redirect to dashboard (this will be handled by useEffect)
  // If not authenticated, show the landing page content
  if (isAuthenticated) {
    // This will be handled by the useEffect, but we return null here to prevent flickering
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 text-white">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Navigation */}
        <nav className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg w-10 h-10 flex items-center justify-center mr-3">
              <span className="text-white font-bold">TF</span>
            </div>
            <div className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">TaskFlow</div>
          </div>
          <div className="space-x-4">
            <Link
              href="/auth/signin"
              className="px-6 py-3 text-gray-300 hover:text-purple-300 transition-colors font-medium rounded-lg hover:bg-white/10 transition-all duration-200"
            >
              Sign In
            </Link>
            <Link
              href="/auth/signup"
              className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 duration-200 font-medium"
            >
              Get Started
            </Link>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="max-w-4xl mx-auto text-center py-16 md:py-24">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Manage Your Tasks <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Effortlessly</span>
          </h1>
          <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed">
            A sophisticated task management application designed to elevate your productivity with intuitive features and seamless experience.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/auth/signup"
              className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-lg font-semibold rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1 duration-200 min-w-48"
            >
              Start Free Trial
            </Link>
            <Link
              href="/auth/signin"
              className="px-8 py-4 bg-gray-800 text-purple-400 text-lg font-semibold rounded-xl border border-gray-700 hover:border-purple-500 hover:bg-gray-700/50 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-1 duration-200 min-w-48"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="max-w-6xl mx-auto py-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass-card p-8 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 text-center group hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-white">Organize Tasks</h3>
              <p className="text-gray-300 leading-relaxed">Create, categorize, and manage your tasks efficiently with our intuitive interface designed for maximum productivity.</p>
            </div>

            <div className="glass-card p-8 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 text-center group hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-white">Track Progress</h3>
              <p className="text-gray-300 leading-relaxed">Monitor your productivity and gain insights with detailed analytics and progress tracking features.</p>
            </div>

            <div className="glass-card p-8 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 text-center group hover:-translate-y-2">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-white">Secure & Private</h3>
              <p className="text-gray-300 leading-relaxed">Your data is protected with enterprise-grade security measures and end-to-end encryption.</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="py-8 text-center text-gray-400 border-t border-gray-700 mt-12">
          <p className="text-sm">© 2026 TaskFlow. Crafted with precision for professionals.</p>
        </footer>
      </div>
    </div>
  );
}