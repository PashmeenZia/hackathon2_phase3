// API-related types

export interface ApiConfig {
  baseURL: string;
  timeout: number;
  headers: {
    'Content-Type': 'application/json';
    'Authorization'?: string;
  };
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}