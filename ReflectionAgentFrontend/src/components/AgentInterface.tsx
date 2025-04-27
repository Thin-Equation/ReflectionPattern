// src/components/AgentInterface.tsx
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import { queryAgent, checkServerHealth } from '../services/api';
import { AgentResponse } from '../types';
import QueryForm from './QueryForm';
import ResponseDisplay from './ResponseDisplay';
import LoadingIndicator from './LoadingIndicator';
import IconComponent from './IconComponent';

interface AgentInterfaceProps {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const AgentInterface: React.FC<AgentInterfaceProps> = ({ isDarkMode, toggleDarkMode }) => {
  const [prompt, setPrompt] = useState<string>('');
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [serverStatus, setServerStatus] = useState<{status: string, config?: any} | null>(null);
  const [serverChecking, setServerChecking] = useState<boolean>(true);

  // Check server health on component mount
  useEffect(() => {
    const checkServer = async () => {
      try {
        setServerChecking(true);
        const status = await checkServerHealth();
        setServerStatus(status);
        setError(null);
      } catch (err) {
        setServerStatus(null);
        setError('Cannot connect to the Reflection Agent server. Please make sure it is running.');
      } finally {
        setServerChecking(false);
      }
    };

    checkServer();
    
    // Set up periodic health checks
    const intervalId = setInterval(checkServer, 60000); // Check every minute
    
    return () => clearInterval(intervalId);
  }, []);

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    
    if (!prompt.trim()) return;
    
    setLoading(true);
    setResponse(null);
    setError(null);
    
    try {
      const result = await queryAgent(prompt);
      setResponse(result);
    } catch (err: any) {
      setError(err.message || 'An error occurred while processing your request. Please try again.');
      console.error('Error querying agent:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <ThemeToggle 
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={toggleDarkMode}
      >
        {isDarkMode ? 
          <IconComponent name="sun" size={20} /> : 
          <IconComponent name="moon" size={20} />
        }
      </ThemeToggle>
      
      <Header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Title>
          <GradientText>AI Reflection Agent</GradientText>
        </Title>
        <Subtitle>Powered by LangChain, LangGraph, LangSmith & Google Gemini</Subtitle>
      </Header>

      {serverChecking && (
        <ServerChecking
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          Checking server connection...
        </ServerChecking>
      )}

      <QueryForm 
        prompt={prompt} 
        setPrompt={setPrompt} 
        handleSubmit={handleSubmit} 
        loading={loading}
        disabled={serverStatus?.status !== "Server is running" || serverChecking}
      />

      {loading && <LoadingIndicator />}

      {error && (
        <ErrorMessage
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {error}
        </ErrorMessage>
      )}

      {response && <ResponseDisplay response={response} />}
      
      {(serverStatus || serverChecking) && (
        <ConfigInfo>
          {serverStatus && (
            <ServerStatusRow>
              <ServerStatusIndicator status={serverStatus.status === "Server is running"} />
              <div>
                {serverStatus.status === "Server is running" ? "Server Connected" : "Server Disconnected"}
              </div>
            </ServerStatusRow>
          )}
          {serverStatus?.config && (
            <>
              <div>Max iterations: {serverStatus.config.max_iterations}</div>
              <div>LangSmith tracing: {serverStatus.config.use_langsmith ? 'Enabled' : 'Disabled'}</div>
            </>
          )}
        </ConfigInfo>
      )}
    </Container>
  );
};

// Styled Components
const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  position: relative;
  min-height: 100vh;
`;

const ThemeToggle = styled(motion.button)`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 50%;
  background-color: var(--card-bg);
  box-shadow: var(--shadow);
`;

const Header = styled(motion.div)`
  text-align: center;
  margin-bottom: 2rem;
  padding-top: 1rem;
  position: relative;
`;

const Title = styled.h1`
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
`;

const GradientText = styled.span`
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  display: inline-block;
`;

const Subtitle = styled.p`
  color: var(--text-secondary);
  font-size: 1rem;
`;

const ErrorMessage = styled(motion.div)`
  background-color: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: var(--border-radius);
  margin-bottom: 1rem;
  border-left: 4px solid #c62828;
`;

const ServerChecking = styled(motion.div)`
  text-align: center;
  margin-bottom: 1rem;
  font-style: italic;
  color: var(--text-secondary);
`;

const ConfigInfo = styled.div`
  margin-top: 1rem;
  padding: 1rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
  text-align: center;
  border-top: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const ServerStatusRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
`;

const ServerStatusIndicator = styled.div<{ status: boolean }>`
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: ${props => props.status ? '#4caf50' : '#f44336'};
`;

export default AgentInterface;
