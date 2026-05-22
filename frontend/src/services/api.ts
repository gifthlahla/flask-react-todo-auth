// API service for communicating with the backend

const API_BASE_URL = 'http://localhost:8000';

interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  ok: boolean;
}

class ApiError extends Error {
  status: number;
  
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
  const contentType = response.headers.get('content-type');
  let data: T;
  
  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = (await response.text()) as unknown as T;
  }
  
  if (!response.ok) {
    const errorMessage = typeof data === 'object' && data !== null && 'detail' in data
      ? (data as { detail: string }).detail
      : `HTTP Error ${response.status}`;
    throw new ApiError(errorMessage, response.status);
  }
  
  return {
    data,
    status: response.status,
    ok: response.ok
  };
}

function getAuthHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  const token = localStorage.getItem('token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
}

export async function registerUser(username: string, password: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  
  const result = await handleResponse<{ message: string }>(response);
  return result.data;
}

export async function loginUser(username: string, password: string): Promise<{ access_token: string; token_type: string }> {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  
  const result = await handleResponse<{ access_token: string; token_type: string }>(response);
  return result.data;
}

export async function getProtectedData(): Promise<{ message: string; username: string }> {
  const response = await fetch(`${API_BASE_URL}/protected`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });
  
  const result = await handleResponse<{ message: string; username: string }>(response);
  return result.data;
}

export { ApiError };
export type { ApiResponse };