"""
Utility functions for the Reflection Agent Backend.
"""
from typing import Callable
import time
import logging
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def call_with_retry(func: Callable, *args, max_retries=3, retry_delay=2.0, verbose=False, **kwargs):
    """
    Call a function with retry logic in case of exceptions
    
    Args:
        func: The function to call
        *args: Arguments to pass to the function
        max_retries: Maximum number of retries
        retry_delay: Delay between retries in seconds
        verbose: Whether to print debug messages
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The result of the function call
    """
    for attempt in range(max_retries + 1):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if attempt < max_retries:
                if verbose:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                if verbose:
                    logger.error(f"All {max_retries + 1} attempts failed. Last error: {str(e)}")
                raise

def get_default_system_prompts():
    """
    Return default system prompts for main and reflection models
    
    Returns:
        Dict with main and reflection system prompts
    """
    main_prompt = """You are a helpful AI assistant. Your goal is to provide accurate, helpful, and clear responses to user queries. 
Consider the user's question carefully and provide a thoughtful, comprehensive answer.
Use specific examples and structured explanations when helpful.
If you're uncertain about something, acknowledge the limits of your knowledge rather than speculating.
If a query seems ambiguous, clarify what the user is asking before providing a detailed response."""

    reflection_prompt = """As a reflection assistant, your job is to analyze and evaluate the AI's response to the user's query.

For each response, provide:
1. REFLECTION: A thoughtful analysis of the response's strengths and weaknesses. Consider factors like accuracy, clarity, relevance, completeness, and helpfulness.
2. STRENGTHS: List specific aspects of the response that were effective.
3. WEAKNESSES: Identify areas where the response could be improved.
4. SUGGESTIONS: Provide specific recommendations to enhance the response.
5. NEEDS IMPROVEMENT: Conclude with "yes" if the response requires significant improvement, or "no" if the response is satisfactory.

Your feedback should be constructive, specific, and focused on helping improve the AI's response."""

    return {
        'main': main_prompt,
        'reflection': reflection_prompt
    }

def initialize_llm(model_name, api_key, is_main=True, verbose=False):
    """
    Initialize a ChatGoogleGenerativeAI model with error handling
    
    Args:
        model_name: Name of the Gemini model to use
        api_key: Google API key
        is_main: Whether this is the main model or reflection model
        verbose: Whether to print debug messages
    
    Returns:
        Initialized ChatGoogleGenerativeAI model
    """
    try:
        # Check for LangSmith tracing
        use_langsmith = os.environ.get("USE_LANGSMITH", "false").lower() == "true"
        
        # Configure model with optimized parameters
        temperature = 0.7 if is_main else 0.2
        model_type = "main" if is_main else "reflection"
        
        if verbose:
            logger.info(f"Initializing {model_type} model: {model_name}")
        
        # Create model with appropriate configurations
        model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True,
            max_output_tokens=4096 if is_main else 2048,
            top_p=0.95 if is_main else 0.8,
            top_k=40 if is_main else 20
        )
        
        if verbose:
            logger.info("Model initialized successfully")
        
        return model
    
    except Exception as e:
        error_msg = f"Failed to initialize {model_name}: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
