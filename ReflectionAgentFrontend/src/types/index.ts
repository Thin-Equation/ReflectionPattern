// src/types/index.ts
export interface Message {
    type: 'system' | 'human' | 'ai';
    content: string;
  }
  
  export interface AgentResponse {
    response: string;
    iterations: number;
    messages: Message[];
    error?: string;
  }
  
  export interface ThemeProps {
    isDarkMode: boolean;
  }
  