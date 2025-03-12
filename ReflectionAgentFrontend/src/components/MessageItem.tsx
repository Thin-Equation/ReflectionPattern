// src/components/MessageItem.tsx
import React from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import { Message } from '../types';

interface MessageItemProps {
  message: Message;
  index: number;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, index }) => {
  return (
    <Container
      className={message.type}
      initial={{ opacity: 0, x: message.type === 'human' ? -20 : 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1, duration: 0.3 }}
    >
      <Header>
        {message.type === 'system' && <span>System</span>}
        {message.type === 'human' && <span>User/Feedback</span>}
        {message.type === 'ai' && <span>AI Response</span>}
      </Header>
      <Content>
        <p>{message.content}</p>
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
  }

  &.ai {
    align-self: flex-end;
    background-color: rgba(56, 142, 60, 0.1);
    border-top-right-radius: 0;
  }
`;

const Header = styled.div`
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  font-weight: 600;

  .system & {
    color: var(--text-secondary);
  }

  .human & {
    color: #1976d2;
  }

  .ai & {
    color: #388e3c;
  }
`;

const Content = styled.div`
  p {
    margin: 0;
  }
`;

export default MessageItem;
