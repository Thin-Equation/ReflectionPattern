// src/components/MessageItem.tsx
import React from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import { Message } from '../types';

interface MessageItemProps {
  message: Message;
  index: number;
  isReflection?: boolean;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, index, isReflection = false }) => {
  return (
    <Container
      className={`${message.type} ${isReflection ? 'reflection' : ''}`}
      initial={{ opacity: 0, x: message.type === 'human' ? -20 : 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1, duration: 0.3 }}
    >
      <Header>
        {message.type === 'system' && <span>System</span>}
        {message.type === 'human' && <span>{isReflection ? 'Reflection Feedback' : 'User Query'}</span>}
        {message.type === 'ai' && <span>{isReflection ? 'Improved Response' : 'AI Response'}</span>}
        {isReflection && <ReflectionBadge>Reflection</ReflectionBadge>}
      </Header>
      <Content className={isReflection ? 'reflection-content' : ''}>
        <pre>{message.content}</pre>
      </Content>
    </Container>
  );
};

// Styled Components
const Container = styled(motion.div)`
  padding: 1rem;
  border-radius: var(--border-radius);
  max-width: 90%;
  transition: var(--transition);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

  &.system {
    align-self: center;
    background-color: rgba(150, 150, 150, 0.1);
    width: 100%;
  }

  &.human {
    align-self: flex-start;
    background-color: rgba(25, 118, 210, 0.1);
    border-top-left-radius: 0;
    
    &.reflection {
      background-color: rgba(156, 39, 176, 0.1);
      border-left: 2px solid #9c27b0;
    }
  }

  &.ai {
    align-self: flex-end;
    background-color: rgba(56, 142, 60, 0.1);
    border-top-right-radius: 0;
    
    &.reflection {
      background-color: rgba(76, 175, 80, 0.15);
      border-right: 2px solid #4caf50;
    }
  }
`;

const Header = styled.div`
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .system & {
    color: var(--text-secondary);
  }

  .human & {
    color: #1976d2;
    
    &.reflection {
      color: #9c27b0;
    }
  }

  .ai & {
    color: #388e3c;
  }
`;

const ReflectionBadge = styled.span`
  background-color: #9c27b0;
  color: white;
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
  margin-left: 0.5rem;
`;

const Content = styled.div`
  pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
    font-family: inherit;
  }
  
  &.reflection-content {
    font-size: 0.9rem;
  }
`;

export default MessageItem;
