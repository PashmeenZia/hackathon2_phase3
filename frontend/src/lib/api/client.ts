import axios from 'axios';

// Get the API base URL from environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

console.log('API Client initialized with baseURL:', API_BASE_URL); // Debug log

// Create the axios instance with base configuration
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Request interceptor to add authorization header
apiClient.interceptors.request.use(
  (config) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    console.log('API Request:', config.method?.toUpperCase(), config.url); // Debug log
    console.log('API Client - Token:', token ? 'Present' : 'Missing'); // Debug log
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('API Client - Authorization header set'); // Debug log
    } else {
      console.log('API Client - No token found in localStorage'); // Debug log
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle common error cases
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Enhanced error logging
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      url: error.config?.url,
      method: error.config?.method,
    });

    // Handle network errors
    if (!error.response) {
      console.error('Network Error: Could not reach the backend server');
      console.error('Please check if the backend is running at:', error.config?.baseURL);
    }

    // Handle 401 Unauthorized errors
    if (error.response?.status === 401) {
      console.warn('Unauthorized: Clearing authentication and redirecting to login');
      // Clear authentication data and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        window.location.href = '/auth/signin';
      }
    }

    // Handle 404 errors
    if (error.response?.status === 404) {
      console.error('Resource not found:', error.config?.url);
    }

    // Handle 500 server errors
    if (error.response?.status === 500) {
      console.error('Server error:', error.response.data);
    }

    return Promise.reject(error);
  }
);