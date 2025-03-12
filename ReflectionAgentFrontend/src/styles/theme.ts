// src/styles/theme.ts
import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle<{ isDarkMode: boolean }>`
  :root {
    --primary-color: ${props => props.isDarkMode ? '#a29bfe' : '#6c5ce7'};
    --primary-light: ${props => props.isDarkMode ? '#6c5ce7' : '#a29bfe'};
    --secondary-color: #00cec9;
    --background-color: ${props => props.isDarkMode ? '#1a1a2e' : '#f9f9f9'};
    --card-bg: ${props => props.isDarkMode ? '#242447' : 'white'};
    --text-color: ${props => props.isDarkMode ? '#f1f1f1' : '#333'};
    --text-secondary: ${props => props.isDarkMode ? '#b8b8b8' : '#666'};
    --border-radius: 12px;
    --shadow: ${props => props.isDarkMode ? '0 8px 30px rgba(0, 0, 0, 0.4)' : '0 8px 30px rgba(0, 0, 0, 0.12)'};
    --transition: all 0.3s ease;
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
    transition: background-color 0.3s ease, color 0.3s ease;
  }
`;
