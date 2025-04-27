// src/services/api.ts
import axios, { AxiosError } from 'axios';
import { AgentResponse } from '../types';

// Get the API URL from environment variables or use default
const API_URL = process.env.REACT_APP_API_URL || 'https://127.0.0.1:5000/api';

// Create an axios instance with custom config
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 60000, // 60 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queryAgent = async (query: string): Promise<AgentResponse> => {
  try {
    const response = await apiClient.post('/query', { query });
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError;
    // Enhanced error logging
    console.error('Error querying agent:', {
      status: axiosError.response?.status,
      statusText: axiosError.response?.statusText,
      data: axiosError.response?.data,
      message: axiosError.message,
    });
    
    // Format and return a user-friendly error
    const errorMessage = getErrorMessage(axiosError);
    throw new Error(errorMessage);
  }
};

export const checkServerHealth = async (): Promise<{ status: string; config?: any }> => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw new Error('Server health check failed. The backend may be unavailable.');
  }
};

// Helper function to get user-friendly error messages - Updated for FastAPI
function getErrorMessage(error: AxiosError): string {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    const data = error.response.data as any;
    
    // Handle FastAPI's standard error format
    if (data?.detail) return data.detail;
    
    // Fall back to previous error format handling
    if (data?.error) return data.error;
    
    return `Server error: ${error.response.status} ${error.response.statusText}`;
  } else if (error.request) {
    // The request was made but no response was received
    return 'No response received from server. The backend may be offline.';
  } else {
    // Something happened in setting up the request that triggered an Error
    return `Request failed: ${error.message}`;
  }
}
