"""
Response generation module for the Reflection Agent.
"""
from typing import List
from langchain_core.messages import BaseMessage, AIMessage
from src.utils.utils import logger

def generate_response(messages: List[BaseMessage], main_llm, verbose: bool = False, 
                    retry_delay: float = 2.0, max_retries: int = 3, iteration_count: int = 1):
    """
    Generate a response from the main LLM with improved error handling.
    
    Args:
        messages: List of messages in the conversation
        main_llm: The LLM to use for generation
        verbose: Whether to print debug messages
        retry_delay: Time to wait between retries
        max_retries: Maximum number of retries
        iteration_count: Current iteration number
    
    Returns:
        List[BaseMessage]: Updated message list with the new AI response
    """
    if verbose:
        logger.info(f"Generating response (iteration {iteration_count})")
    
    try:
        # Use the LLM's invoke method to generate a response
        ai_message = None
        
        try:
            # Generate the response
            ai_message = main_llm.invoke(messages)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            # Create a simple error message if generation fails
            ai_message = AIMessage(content="I encountered an error processing your request. Let me try again.")
        
        # Return the extended message list with the new AI response
        return messages + [ai_message]
        
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        # Return a fallback response in case of error
        error_message = AIMessage(content="I'm sorry, I encountered an error while processing your request. Please try again.")
        return messages + [error_message]
