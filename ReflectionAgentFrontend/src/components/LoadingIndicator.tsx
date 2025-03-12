// src/components/LoadingIndicator.tsx
import React from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';

const LoadingIndicator: React.FC = () => {
  return (
    <Container
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <Spinner />
      <LoadingText>Generating response with reflection...</LoadingText>
      <Stages>
        <Stage className="active">Generating</Stage>
        <Connector />
        <Stage>Reflecting</Stage>
        <Connector />
        <Stage>Refining</Stage>
      </Stages>
    </Container>
  );
};

// Styled Components
const Container = styled(motion.div)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  margin-bottom: 2rem;
  transition: var(--transition);
`;

const Spinner = styled.div`
  width: 50px;
  height: 50px;
  border: 5px solid rgba(108, 92, 231, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const LoadingText = styled.p`
  color: var(--text-color);
`;

const Stages = styled.div`
  display: flex;
  align-items: center;
  margin-top: 1.5rem;
  width: 100%;
  max-width: 400px;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 0.5rem;
  }
`;

const Stage = styled.div`
  background-color: rgba(108, 92, 231, 0.1);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
  flex: 1;

  &.active {
    background-color: var(--primary-color);
    color: white;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 1;
    }
    50% {
      opacity: 0.7;
    }
    100% {
      opacity: 1;
    }
  }
`;

const Connector = styled.div`
  height: 2px;
  background-color: rgba(108, 92, 231, 0.3);
  flex: 1;
  max-width: 30px;

  @media (max-width: 768px) {
    width: 2px;
    height: 15px;
    max-width: none;
  }
`;

export default LoadingIndicator;
