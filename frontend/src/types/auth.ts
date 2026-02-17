// Authentication-related types

export interface UserSession {
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

export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  notificationSettings: NotificationSettings;
}

export interface NotificationSettings {
  emailNotifications: boolean;
  pushNotifications: boolean;
}

export interface AuthState {
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

export interface AuthUser {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: AuthUser;
}

export interface RegisterResponse {
  user_id: string;
  email: string;
}

export interface ErrorResponse {
  detail: string;
  error_code?: string;
  field_errors?: Record<string, string[]>;
}