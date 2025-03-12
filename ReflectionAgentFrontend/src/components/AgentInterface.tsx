// src/components/AgentInterface.tsx
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
//import { FaSun, FaMoon } from 'react-icons/fa';
import styled from 'styled-components';
import { queryAgent } from '../services/api';
import { AgentResponse } from '../types';
import QueryForm from './QueryForm';
import ResponseDisplay from './ResponseDisplay';
import LoadingIndicator from './LoadingIndicator';

interface AgentInterfaceProps {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const AgentInterface: React.FC<AgentInterfaceProps> = ({ isDarkMode, toggleDarkMode }) => {
  const [prompt, setPrompt] = useState<string>('');
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    
    if (!prompt.trim()) return;
    
    setLoading(true);
    setResponse(null);
    setError(null);
    
    try {
      const result = await queryAgent(prompt);
      setResponse(result);
    } catch (err) {
      setError('An error occurred while processing your request. Please try again.');
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
      </ThemeToggle>
      
      <Header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Title>
          <GradientText>AI Reflection Agent</GradientText>
        </Title>
        <Subtitle>Powered by Reflection Pattern & Google Generative AI</Subtitle>
      </Header>

      <QueryForm 
        prompt={prompt} 
        setPrompt={setPrompt} 
        handleSubmit={handleSubmit} 
        loading={loading} 
      />

      <AnimatePresence>
        {loading && <LoadingIndicator />}
      </AnimatePresence>

      <AnimatePresence>
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
      </AnimatePresence>

      <AnimatePresence>
        {response && <ResponseDisplay response={response} />}
      </AnimatePresence>
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

export default AgentInterface;
