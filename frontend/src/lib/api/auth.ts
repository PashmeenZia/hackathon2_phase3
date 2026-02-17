import { apiClient } from './client';
import { LoginResponse, RegisterResponse, AuthUser } from '@/types/auth';

/**
 * Authentication API service
 * Contains functions for user registration, login, and logout
 */

// Register a new user
export const registerUser = async (
  email: string,
  password: string,
  name: string
): Promise<RegisterResponse> => {
  const response = await apiClient.post('/api/auth/register', {
    email,
    password,
    name,
  });
  return response.data;
};

// Login user and return token
export const loginUser = async (
  email: string,
  password: string
): Promise<LoginResponse> => {
  const response = await apiClient.post('/api/auth/login', {
    email,
    password,
  });
  return response.data;
};

// Logout user (invalidate session)
export const logoutUser = async (): Promise<void> => {
  try {
    await apiClient.post('/api/auth/logout');
  } catch (error) {
    // If logout fails, still clear local data
    console.warn('Logout API call failed, but clearing local data anyway', error);
  }
};

// Get current user details
export const getCurrentUser = async (): Promise<AuthUser> => {
  const response = await apiClient.get('/api/auth/me');
  return response.data.user;
};

// Refresh access token (if refresh token is implemented)
export const refreshToken = async (): Promise<string> => {
  // Implementation would depend on backend refresh token strategy
  // This is a placeholder that would need to be implemented based on your backend design
  throw new Error('Refresh token functionality not implemented');
};