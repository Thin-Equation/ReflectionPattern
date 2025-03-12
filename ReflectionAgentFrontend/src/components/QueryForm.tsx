// src/components/QueryForm.tsx
import React from 'react';
import { motion } from 'framer-motion';
//import { FaMicrophone } from 'react-icons/fa';
import styled from 'styled-components';

interface QueryFormProps {
  prompt: string;
  setPrompt: (prompt: string) => void;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
  loading: boolean;
}

const QueryForm: React.FC<QueryFormProps> = ({ prompt, setPrompt, handleSubmit, loading }) => {
  return (
    <FormContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.2, duration: 0.5 }}
    >
      <Form onSubmit={handleSubmit}>
        <TextareaContainer>
          <Textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter your query here..."
            rows={3}
          />
          <MicButton
            type="button"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            title="Voice input"
          >
          </MicButton>
        </TextareaContainer>
        
        <SubmitButton 
          type="submit" 
          disabled={loading || !prompt.trim()}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? "Processing..." : "Submit Query"}
        </SubmitButton>
      </Form>
    </FormContainer>
  );
};

// Styled Components
const FormContainer = styled(motion.div)`
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow);
  margin-bottom: 2rem;
  transition: var(--transition);
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
`;

const TextareaContainer = styled.div`
  position: relative;
  margin-bottom: 1rem;
`;

const Textarea = styled.textarea`
  width: 100%;
  padding: 1rem;
  border: 1px solid rgba(150, 150, 150, 0.3);
  border-radius: var(--border-radius);
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
  transition: var(--transition);
  background-color: var(--card-bg);
  color: var(--text-color);

  &:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.2);
  }
`;

const MicButton = styled(motion.button)`
  position: absolute;
  right: 10px;
  bottom: 10px;
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 50%;
  transition: var(--transition);
`;

const SubmitButton = styled(motion.button)`
  background: linear-gradient(45deg, var(--primary-color), var(--primary-light));
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: var(--transition);
  box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);

  &:hover {
    box-shadow: 0 6px 20px rgba(108, 92, 231, 0.6);
  }

  &:disabled {
    background: #b2abd9;
    cursor: not-allowed;
    box-shadow: none;
  }
`;

export default QueryForm;
