from typing import List
import logging
from langchain_core.messages import BaseMessage, AIMessage
from utils import call_with_retry, logger

def generate_response(messages: List[BaseMessage], main_llm, verbose: bool = False, 
                     retry_delay: float = 2.0, max_retries: int = 3,
                     iteration_count: int = 1) -> List[BaseMessage]:
    """
    Generate a response with robust error handling
    
    Args:
        messages: The conversation history
        main_llm: The language model to use for generation
        verbose: Whether to log detailed information
        retry_delay: Base delay between retries in seconds
        max_retries: Maximum number of retry attempts
        iteration_count: Current iteration number
        
    Returns:
        Updated list of messages with the new AI response
    """
    if verbose:
        logger.info(f"\n--- Generation Attempt #{iteration_count} ---")
    
    try:
        # Generate with retry mechanism
        response = call_with_retry(
            main_llm.invoke, 
            messages, 
            max_retries, 
            retry_delay, 
            verbose
        )
        
        if verbose:
            logger.info(f"Generated response: {response.content[:100]}...")
        
        return messages + [response]
    except Exception as e:
        # Fallback response
        logger.error(f"Error generating response: {str(e)}")
        fallback_content = (
            "I apologize, but I'm currently experiencing technical difficulties. "
            "This could be due to system limitations or high demand. Please try again later."
        )
        return messages + [AIMessage(content=fallback_content)]
