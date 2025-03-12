import unittest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from generate import generate_response

class TestGeneration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test"""
        self.mock_llm = Mock()
        self.messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Hello, world!")
        ]
    
    def test_generate_response_success(self):
        """Test successful response generation"""
        # Setup
        self.mock_llm.invoke.return_value = AIMessage(content="Hello! How can I help you today?")
        
        # Execute
        result = generate_response(
            self.messages,
            self.mock_llm,
            verbose=False
        )
        
        # Assert
        self.assertEqual(len(result), 3)  # Original 2 messages + new response
        self.assertIsInstance(result[-1], AIMessage)
        self.assertEqual(result[-1].content, "Hello! How can I help you today?")
        self.mock_llm.invoke.assert_called_once()
    
    @patch('generate.call_with_retry')
    def test_generate_response_with_retry(self, mock_call_with_retry):
        """Test response generation with retry mechanism"""
        # Setup
        mock_call_with_retry.return_value = AIMessage(content="Response after retry")
        
        # Execute
        result = generate_response(
            self.messages,
            self.mock_llm,
            verbose=True,
            retry_delay=1.0,
            max_retries=2,
            iteration_count=3
        )
        
        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[-1].content, "Response after retry")
        mock_call_with_retry.assert_called_once_with(
            self.mock_llm.invoke,
            self.messages,
            2,  # max_retries
            1.0,  # retry_delay
            True  # verbose
        )
    
    @patch('generate.call_with_retry')
    def test_generate_response_failure(self, mock_call_with_retry):
        """Test fallback behavior when generation fails"""
        # Setup
        mock_call_with_retry.side_effect = Exception("API error")
        
        # Execute
        result = generate_response(
            self.messages,
            self.mock_llm,
            verbose=True
        )
        
        # Assert
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[-1], AIMessage)
        # Check that we got a fallback error message
        self.assertTrue("I apologize" in result[-1].content)
        self.assertTrue("technical difficulties" in result[-1].content)

if __name__ == '__main__':
    unittest.main()
