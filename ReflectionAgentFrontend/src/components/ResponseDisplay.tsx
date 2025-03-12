// src/components/ResponseDisplay.tsx
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
//import { FaCopy } from 'react-icons/fa';
import styled from 'styled-components';
import { AgentResponse } from '../types';
import MessageItem from './MessageItem';

interface ResponseDisplayProps {
  response: AgentResponse;
}

const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ response }) => {
  const [showIterations, setShowIterations] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const copyToClipboard = (): void => {
    if (response.response) {
      navigator.clipboard.writeText(response.response);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <Container
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1, duration: 0.5 }}
    >
      <Header>
        <Title>Response</Title>
        <Actions>
          <IterationsBadge>
            {response.iterations} {response.iterations === 1 ? 'iteration' : 'iterations'}
          </IterationsBadge>
          <CopyButton
            onClick={copyToClipboard}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            title="Copy to clipboard"
          >
            {copied && <Tooltip>Copied!</Tooltip>}
          </CopyButton>
        </Actions>
      </Header>
      
      <Content
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <p>{response.response}</p>
      </Content>

      <ToggleButton
        onClick={() => setShowIterations(!showIterations)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        {showIterations ? "Hide Reflection Process" : "Show Reflection Process"}
      </ToggleButton>

      <AnimatePresence>
        {showIterations && (
          <IterationsContainer
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.5 }}
          >
            <IterationsTitle>Reflection Process</IterationsTitle>
            <MessageList>
              {response.messages.map((message, index) => (
                <MessageItem key={index} message={message} index={index} />
              ))}
            </MessageList>
          </IterationsContainer>
        )}
      </AnimatePresence>
    </Container>
  );
};

// Styled Components
const Container = styled(motion.div)`
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow);
  transition: var(--transition);
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(150, 150, 150, 0.2);
`;

const Title = styled.h2`
  color: var(--primary-color);
  font-size: 1.5rem;
`;

const Actions = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const IterationsBadge = styled.span`
  background-color: var(--primary-light);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-right: 0.5rem;
`;

const CopyButton = styled(motion.button)`
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.4rem;
  border-radius: 50%;
  position: relative;
`;

const Tooltip = styled.span`
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--primary-color);
  color: white;
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  font-size: 0.7rem;
  white-space: nowrap;
  animation: fadeIn 0.3s ease-in-out;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translate(-50%, 10px);
    }
    to {
      opacity: 1;
      transform: translate(-50%, 0);
    }
  }
`;

const Content = styled(motion.div)`
  padding: 1rem 0;
  line-height: 1.8;
`;

const ToggleButton = styled(motion.button)`
  margin-top: 1.5rem;
  background-color: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  padding: 0.7rem 1rem;
  width: 100%;
  border-radius: var(--border-radius);
  transition: var(--transition);

  &:hover {
    background-color: rgba(108, 92, 231, 0.1);
  }
`;

const IterationsContainer = styled(motion.div)`
  margin-top: 1.5rem;
  overflow: hidden;
`;

const IterationsTitle = styled.h3`
  margin-bottom: 1rem;
  color: var(--primary-color);
`;

const MessageList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

export default ResponseDisplay;
