import unittest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from reflect import evaluate_response

class TestReflection(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test"""
        self.mock_reflection_llm = Mock()
        self.reflection_system_prompt = "You are a critical evaluator."
        self.messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="What is machine learning?"),
            AIMessage(content="Machine learning is a subfield of artificial intelligence.")
        ]
    
    @patch('reflect.call_with_retry')
    def test_evaluate_response_needs_improvement(self, mock_call_with_retry):
        """Test when reflection indicates improvements are needed"""
        # Setup a mock response that indicates improvements are needed
        mock_response = MagicMock()
        mock_response.content = "The response is too brief and lacks details."
        mock_call_with_retry.return_value = mock_response
        
        # Execute
        result = evaluate_response(
            self.messages,
            self.mock_reflection_llm,
            self.reflection_system_prompt,
            verbose=False
        )
        
        # Assert
        self.assertTrue(result["needs_improvement"])
        self.assertEqual(result["critique"], "The response is too brief and lacks details.")
        self.assertEqual(len(result["messages"]), 4)  # Original 3 + feedback message
        self.assertTrue("Please improve your response" in result["messages"][-1].content)
    
    @patch('reflect.call_with_retry')
    def test_evaluate_response_no_improvement_needed(self, mock_call_with_retry):
        """Test when reflection indicates no improvements are needed"""
        # Setup a mock response that indicates no improvements are needed
        mock_response = MagicMock()
        mock_response.content = "No critique needed"
        mock_call_with_retry.return_value = mock_response
        
        # Execute
        result = evaluate_response(
            self.messages,
            self.mock_reflection_llm,
            self.reflection_system_prompt,
            verbose=True
        )
        
        # Assert
        self.assertFalse(result["needs_improvement"])
        self.assertEqual(result["critique"], "No critique needed")
        self.assertEqual(len(result["messages"]), 3)  # Same as original, no new messages
    
    @patch('reflect.call_with_retry')
    def test_evaluate_response_error_handling(self, mock_call_with_retry):
        """Test error handling during reflection"""
        # Setup
        mock_call_with_retry.side_effect = Exception("API Error")
        
        # Execute
        result = evaluate_response(
            self.messages,
            self.mock_reflection_llm,
            self.reflection_system_prompt,
            verbose=True
        )
        
        # Assert
        self.assertFalse(result["needs_improvement"])  # Should default to False on error
        self.assertTrue("Error performing reflection" in result["critique"])
        self.assertEqual(len(result["messages"]), 3)  # Same as original, no changes on error
    
    @patch('reflect.call_with_retry')
    def test_evaluate_response_with_custom_parameters(self, mock_call_with_retry):
        """Test reflection with custom parameters"""
        # Setup
        mock_response = MagicMock()
        mock_response.content = "The response could use more examples."
        mock_call_with_retry.return_value = mock_response
        
        # Execute with custom parameters
        result = evaluate_response(
            self.messages,
            self.mock_reflection_llm,
            self.reflection_system_prompt,
            verbose=True,
            retry_delay=3.0,
            max_retries=5,
            iteration_count=2
        )
        
        # Assert
        self.assertTrue(result["needs_improvement"])
        mock_call_with_retry.assert_called_once_with(
            unittest.mock.ANY,  # We don't need to verify the exact chain
            {}, 
            5,  # max_retries
            3.0,  # retry_delay
            True  # verbose
        )

if __name__ == '__main__':
    unittest.main()
