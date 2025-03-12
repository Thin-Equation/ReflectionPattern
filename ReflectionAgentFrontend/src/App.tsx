// src/App.tsx
import React, { useState } from 'react';
import { ThemeProvider } from 'styled-components';
import { GlobalStyle } from './styles/theme';
import AgentInterface from './components/AgentInterface';

const App: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(true);

  const toggleDarkMode = (): void => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <ThemeProvider theme={{ isDarkMode }}>
      <GlobalStyle isDarkMode={isDarkMode} />
      <AgentInterface isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
    </ThemeProvider>
  );
};

export default App;
