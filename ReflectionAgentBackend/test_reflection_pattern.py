import unittest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from reflection_agent import ReflectionPatternAgent

class TestReflectionPatternAgent(unittest.TestCase):
    
    @patch('reflection_agent.initialize_llm')
    def setUp(self, mock_initialize_llm):
        """Set up test fixtures before each test"""
        # Configure the mock LLM
        self.mock_main_llm = MagicMock()
        self.mock_reflection_llm = MagicMock()
        mock_initialize_llm.side_effect = [self.mock_main_llm, self.mock_reflection_llm]
        
        # Create the agent
        self.agent = ReflectionPatternAgent(
            google_api_key="fake_api_key",
            max_iterations=2,
            verbose=True
        )
    
    def test_initialization(self):
        """Test that the agent initializes correctly"""
        # Test that the agent was initialized correctly
        self.assertEqual(self.agent.max_iterations, 2)
        self.assertTrue(self.agent.verbose)
        self.assertEqual(self.agent.iteration_count, 0)
        self.assertFalse(self.agent.no_reflection_needed)
    
    @patch('reflection_agent.generate_response')
    @patch('reflection_agent.evaluate_response')
    def test_run_no_reflection_needed(self, mock_evaluate_response, mock_generate_response):
        """Test agent run with no reflection needed"""
        # Setup mocks
        initial_response = AIMessage(content="This is a good response.")
        initial_messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Test query"),
            initial_response
        ]
        
        # Mock generate to return a response
        mock_generate_response.return_value = initial_messages
        
        # Mock evaluate to indicate no reflection needed
        mock_evaluate_response.return_value = {
            "messages": initial_messages,
            "needs_improvement": False,
            "critique": "No critique needed"
        }
        
        # Execute
        result = self.agent.run("Test query")
        
        # Assert
        self.assertEqual(result["response"], "This is a good response.")
        self.assertEqual(result["iterations"], 1)
        mock_generate_response.assert_called_once()
        mock_evaluate_response.assert_called_once()
    
    @patch('reflection_agent.generate_response')
    @patch('reflection_agent.evaluate_response')
    def test_run_with_reflection(self, mock_evaluate_response, mock_generate_response):
        """Test agent run with reflection and improvement"""
        # Setup for a scenario where reflection generates feedback
        initial_messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Test query"),
            AIMessage(content="Initial response")
        ]
        
        feedback_messages = initial_messages + [
            HumanMessage(content="Please improve your response based on this feedback: Add more details.")
        ]
        
        improved_messages = feedback_messages + [
            AIMessage(content="Improved response with more details")
        ]
        
        # Configure the mocks
        mock_generate_response.side_effect = [initial_messages, improved_messages]
        
        mock_evaluate_response.side_effect = [
            {
                "messages": feedback_messages,
                "needs_improvement": True,
                "critique": "Add more details."
            },
            {
                "messages": improved_messages,
                "needs_improvement": False,
                "critique": "No critique needed"
            }
        ]
        
        # Execute
        result = self.agent.run("Test query")
        
        # Assert
        self.assertEqual(result["response"], "Improved response with more details")
        self.assertEqual(result["iterations"], 2)
        self.assertEqual(mock_generate_response.call_count, 2)
        self.assertEqual(mock_evaluate_response.call_count, 2)
    
    @patch('reflection_agent.generate_response')
    @patch('reflection_agent.evaluate_response')
    def test_run_max_iterations(self, mock_evaluate_response, mock_generate_response):
        """Test agent reaching max iterations"""
        # Setup for reaching max iterations
        self.agent.max_iterations = 1
        
        initial_messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Test query"),
            AIMessage(content="Initial response")
        ]
        
        # First and only generation
        mock_generate_response.return_value = initial_messages
        
        # Configure evaluate to suggest improvement, but we should stop due to max iterations
        mock_evaluate_response.return_value = {
            "messages": initial_messages + [HumanMessage(content="Please improve...")],
            "needs_improvement": True,
            "critique": "Needs improvement"
        }
        
        # Execute
        result = self.agent.run("Test query")
        
        # Assert
        self.assertEqual(result["iterations"], 1)
        self.assertEqual(result["response"], "Initial response")
        mock_generate_response.assert_called_once()
        mock_evaluate_response.assert_called_once()
    
    @patch('reflection_agent.initialize_llm')
    def test_custom_system_prompts(self, mock_initialize_llm):
        """Test initialization with custom system prompts"""
        # Setup
        mock_initialize_llm.side_effect = [Mock(), Mock()]
        
        # Custom prompts
        main_prompt = "You are a scientific expert assistant."
        reflection_prompt = "You are a scientific peer reviewer."
        
        # Initialize with custom prompts
        agent = ReflectionPatternAgent(
            google_api_key="fake_api_key",
            main_system_prompt=main_prompt,
            reflection_system_prompt=reflection_prompt
        )
        
        # Assert
        self.assertEqual(agent.main_system_message.content, main_prompt)
        self.assertEqual(agent.reflection_system_prompt, reflection_prompt)
    
    @patch('reflection_agent.generate_response')
    def test_error_handling_in_run(self, mock_generate_response):
        """Test error handling during agent run"""
        # Setup
        mock_generate_response.side_effect = Exception("Generation error")
        
        # Execute
        result = self.agent.run("Test query with error")
        
        # Assert
        self.assertTrue("error" in result)
        self.assertEqual(result["iterations"], 1)  # Should increment before error
        self.assertTrue("I encountered an error" in result["response"])

if __name__ == '__main__':
    unittest.main()
