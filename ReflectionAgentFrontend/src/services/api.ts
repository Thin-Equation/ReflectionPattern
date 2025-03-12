// src/services/api.ts
import axios from 'axios';
import { AgentResponse } from '../types';

const API_URL = 'https://127.0.0.1:5000/api';

export const queryAgent = async (query: string): Promise<AgentResponse> => {
  try {
    const response = await axios.post(`${API_URL}/query`, { query });
    return response.data;
  } catch (error) {
    console.error('Error querying agent:', error);
    throw error;
  }
};
