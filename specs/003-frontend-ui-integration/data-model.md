# Data Model: Frontend UI with Full Backend Integration

**Feature**: Frontend UI with Full Backend Integration
**Date**: 2026-02-05
**Model Version**: 1.0

## Entity Relationships

### Core Frontend Entities

```
┌─────────────────┐      ┌─────────────────┐
│   User Session  │      │  Authentication │
│─────────────────│      │   State         │
│ - token         │─────▶│─────────────────│
│ - user_id       │      │ - isAuthenticated│
│ - expires_at    │      │ - user          │
│ - permissions   │      │ - token         │
│ - preferences   │      │ - loading       │
└─────────────────┘      └─────────────────┘
         │
         ▼
┌─────────────────┐
│      Task       │
│─────────────────│
│ - id            │
│ - title         │
│ - description   │
│ - completed     │
│ - created_at    │
│ - updated_at    │
│ - user_id       │
└─────────────────┘
```

## Frontend Data Structures

### User Session Entity
```typescript
interface UserSession {
  // Authentication data
  token: string;
  refreshToken?: string;
  user_id: string;
  email: string;

  // Session metadata
  expires_at: Date;
  created_at: Date;

  // User preferences
  preferences: UserPreferences;
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  notificationSettings: NotificationSettings;
}

interface NotificationSettings {
  emailNotifications: boolean;
  pushNotifications: boolean;
}
```

**Validation Rules:**
- `token` must be a valid JWT format
- `expires_at` must be in the future
- `email` must be a valid email format
- `theme` restricted to enum values

### Authentication State Entity
```typescript
interface AuthState {
  // Authentication status
  isAuthenticated: boolean;
  isChecking: boolean;
  error?: string;

  // User data
  user?: AuthUser;

  // Token management
  token?: string;
  refreshToken?: string;
}

interface AuthUser {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}
```

**State Transitions:**
- `uninitialized` → `checking` (on app load)
- `checking` → `authenticated` (with valid token)
- `checking` → `unauthenticated` (with invalid/missing token)
- `authenticated` → `unauthenticated` (on logout/expiry)

### Task Entity (Frontend Representation)
```typescript
interface Task {
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

interface CreateTaskRequest {
  title: string;
  description: string;
  completed: boolean;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}
```

**Validation Rules:**
- `title` required, max 200 characters
- `description` max 1000 characters
- `user_id` must match authenticated user
- `completed` is boolean value

## API Response Structures

### Authentication API Responses
```typescript
// Login response
interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: AuthUser;
}

// Registration response
interface RegisterResponse {
  user_id: string;
  email: string;
}

// Error response (consistent across all APIs)
interface ErrorResponse {
  detail: string;
  error_code?: string;
  field_errors?: Record<string, string[]>;
}
```

### Task API Responses
```typescript
// Single task response
interface TaskResponse {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

// List response
interface TaskListResponse {
  tasks: TaskResponse[];
}

// Filter parameters
interface TaskFilterParams {
  status?: 'all' | 'pending' | 'completed';
  search?: string;
  limit?: number;
  offset?: number;
}
```

## Frontend State Management

### Global State Structure
```typescript
interface AppState {
  // Authentication state
  auth: AuthState;

  // Task management
  tasks: {
    items: Record<number, Task>; // Dictionary for fast lookup
    ids: number[]; // Ordered list of task IDs
    filters: TaskFilterParams;
    loading: boolean;
    error?: string;
  };

  // UI state
  ui: {
    toast: ToastState[];
    loadingStates: Record<string, boolean>;
  };
}
```

## Data Flow Patterns

### Authentication Flow
```
User Login Action → API Call → Token Received → Context Update → Route Redirect
```

### Task Operations Flow
```
Create Task Action → API Validation → Request Sent → Response Handling → State Update
```

### Error Handling Flow
```
API Error → Error Parser → User-Friendly Message → Toast Display → State Update
```

## Type Definitions for API Integration

### HTTP Client Configuration
```typescript
interface ApiConfig {
  baseURL: string;
  timeout: number;
  headers: {
    'Content-Type': 'application/json';
    'Authorization'?: string;
  };
}

interface ApiResponse<T> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}
```

### API Client Interceptors
```typescript
// Request interceptor
// - Add authorization header
// - Add correlation ID
// - Transform request data

// Response interceptor
// - Handle 401 redirects
// - Parse error messages
// - Refresh expired tokens
```

## Data Validation Schema

### Frontend Validation (using Zod)
```typescript
import { z } from 'zod';

const TaskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(1000, 'Description too long').optional(),
  completed: z.boolean().default(false),
});

const LoginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

const RegisterSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().max(100, 'Name too long').optional(),
});
```

## Security Considerations

### Data Storage
- Sensitive tokens stored in httpOnly cookies
- Session data encrypted in storage
- No sensitive data in URL parameters

### Validation
- Input validation at component level
- API response validation
- Cross-site scripting protection

### Error Handling
- Generic error messages to prevent information disclosure
- Logging of errors without sensitive data
- Secure error reporting mechanism
```