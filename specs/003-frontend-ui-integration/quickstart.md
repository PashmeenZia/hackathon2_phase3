# Quickstart Guide: Frontend UI Integration

**Feature**: Frontend UI with Full Backend Integration
**Difficulty**: Intermediate
**Time Estimate**: 3-4 hours for full setup

## Prerequisites

### System Requirements
- Node.js 18+
- npm or yarn package manager
- Git
- Access to running backend server

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd <frontend-directory>

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local
```

### Environment Configuration
Update `.env.local` with:
```env
# Backend API URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Better Auth Configuration (if applicable)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── signin/page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── tasks/page.tsx
│   │   │   ├── create/page.tsx
│   │   │   └── [taskId]/page.tsx
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── ui/
│   ├── lib/
│   │   ├── api/
│   │   ├── hooks/
│   │   └── utils/
│   ├── context/
│   └── types/
├── tests/
├── public/
└── package.json
```

## Setup Instructions

### 1. Initialize Project
```bash
# Create Next.js app (if starting fresh)
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/"

# Navigate to project
cd frontend
```

### 2. Install Required Dependencies
```bash
npm install axios react-hot-toast lucide-react framer-motion better-auth
npm install -D @types/react @types/node
```

### 3. Configure API Client
Create the API client with JWT interceptor:

`src/lib/api/client.ts`:
```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for handling errors and redirects
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login on 401
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);
```

### 4. Set up Authentication Context
`src/context/AuthContext.tsx`:
```typescript
'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api/client';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string, name: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check for existing token on mount
    const savedToken = localStorage.getItem('access_token');
    if (savedToken) {
      setToken(savedToken);
      // Verify token and get user data
      verifyTokenAndFetchUser(savedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const verifyTokenAndFetchUser = async (token: string) => {
    try {
      const response = await apiClient.get('/api/auth/me');
      setUser(response.data.user);
      setToken(token);
    } catch (error) {
      // Token invalid, clear storage
      localStorage.removeItem('access_token');
      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/api/auth/login', {
        email,
        password
      });

      const { access_token, user } = response.data;

      localStorage.setItem('access_token', access_token);
      setToken(access_token);
      setUser(user);

      router.push('/dashboard');
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await apiClient.post('/api/auth/register', {
        email,
        password,
        name
      });

      // Automatically log in after registration
      await login(email, password);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
    router.push('/signin');
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      isAuthenticated: !!token,
      isLoading,
      login,
      logout,
      register
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

### 5. API Service Implementation
`src/lib/api/auth.ts`:
```typescript
import { apiClient } from './client';

export const authApi = {
  login: async (email: string, password: string) => {
    return await apiClient.post('/api/auth/login', { email, password });
  },

  register: async (email: string, password: string, name: string) => {
    return await apiClient.post('/api/auth/register', { email, password, name });
  },

  logout: async () => {
    return await apiClient.post('/api/auth/logout');
  },

  getProfile: async () => {
    return await apiClient.get('/api/auth/profile');
  }
};
```

`src/lib/api/tasks.ts`:
```typescript
import { apiClient } from './client';
import { Task } from '@/types';

export const tasksApi = {
  getAll: async () => {
    return await apiClient.get<Task[]>('/api/tasks');
  },

  getById: async (id: number) => {
    return await apiClient.get<Task>(`/api/tasks/${id}`);
  },

  create: async (task: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    return await apiClient.post<Task>('/api/tasks', task);
  },

  update: async (id: number, task: Partial<Task>) => {
    return await apiClient.put<Task>(`/api/tasks/${id}`, task);
  },

  delete: async (id: number) => {
    return await apiClient.delete(`/api/tasks/${id}`);
  },

  toggleComplete: async (id: number) => {
    return await apiClient.patch<Task>(`/api/tasks/${id}/complete`);
  }
};
```

## Key Implementation Files

### Protected Route Component
`src/components/auth/ProtectedRoute.tsx`:
```typescript
'use client';

import { useAuth } from '@/context/AuthContext';
import { Spinner } from '../ui/Spinner';
import { useRouter } from 'next/navigation';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  if (isLoading) {
    return <Spinner />;
  }

  if (!isAuthenticated) {
    router.push('/signin');
    return null;
  }

  return <>{children}</>;
}
```

### Task List Component
`src/components/tasks/TaskList.tsx`:
```typescript
'use client';

import { useState, useEffect } from 'react';
import { Task } from '@/types';
import { tasksApi } from '@/lib/api/tasks';
import { TaskCard } from './TaskCard';
import { TaskForm } from './TaskForm';
import { useToast } from '@/hooks/use-toast';

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await tasksApi.getAll();
      setTasks(response.data);
    } catch (error) {
      toast.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    try {
      const response = await tasksApi.create(taskData);
      setTasks([response.data, ...tasks]);
      setShowForm(false);
      toast.success('Task created successfully');
    } catch (error) {
      toast.error('Failed to create task');
    }
  };

  const handleToggleComplete = async (id: number) => {
    try {
      const response = await tasksApi.toggleComplete(id);
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, completed: response.data.completed } : task
      ));
    } catch (error) {
      toast.error('Failed to update task');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await tasksApi.delete(id);
      setTasks(tasks.filter(task => task.id !== id));
      toast.success('Task deleted successfully');
    } catch (error) {
      toast.error('Failed to delete task');
    }
  };

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">My Tasks</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          {showForm ? 'Cancel' : 'Add Task'}
        </button>
      </div>

      {showForm && (
        <TaskForm onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No tasks yet. Create your first task!
        </div>
      ) : (
        <div className="space-y-2">
          {tasks.map(task => (
            <TaskCard
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

## Running the Application

### Development
```bash
# Start development server
npm run dev

# Visit http://localhost:3000
```

### Build and Production
```bash
# Build for production
npm run build

# Start production server
npm start
```

## Testing Commands

### Unit Tests
```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch
```

### E2E Tests
```bash
# Run end-to-end tests
npm run test:e2e
```

## Troubleshooting

### Common Issues

**Issue**: 401 errors after login
**Solution**: Check if JWT token is being properly stored and sent in requests

**Issue**: API calls failing
**Solution**: Verify NEXT_PUBLIC_API_BASE_URL is set correctly in .env.local

**Issue**: Redirect loops
**Solution**: Ensure authentication state is properly managed in context

### Environment Variable Check
```bash
# Verify environment variables
echo $NEXT_PUBLIC_API_BASE_URL
```

### API Connectivity Test
```bash
# Test backend connectivity
curl http://localhost:8000/health
```

## Next Steps

1. **Styling**: Customize Tailwind classes to match design requirements
2. **Error Handling**: Add comprehensive error handling throughout
3. **Loading States**: Implement skeleton loaders and loading states
4. **Validation**: Add form validation with user feedback
5. **Accessibility**: Ensure WCAG compliance
6. **Responsive Design**: Test across different screen sizes