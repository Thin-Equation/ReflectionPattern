from typing import List, Dict, Any, Optional, Callable
import time
import logging
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def call_with_retry(llm_call: Callable, messages: Any, max_retries: int = 3, 
                    retry_delay: float = 2.0, verbose: bool = False) -> Any:
    """
    Helper method to retry LLM calls with exponential backoff
    
    Args:
        llm_call: Function to call the LLM
        messages: Input to the LLM call
        max_retries: Maximum number of retry attempts
        retry_delay: Base delay between retries in seconds
        verbose: Whether to log detailed information
        
    Returns:
        The response from the LLM
    """
    retries = 0
    while retries <= max_retries:
        try:
            return llm_call(messages)
        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise
            
            # Exponential backoff with jitter
            delay = retry_delay * (2 ** (retries - 1)) * (0.5 + 0.5 * (hash(str(e)) % 100) / 100)
            
            if verbose:
                logger.warning(f"API call failed (attempt {retries}/{max_retries}): {str(e)}")
                logger.info(f"Retrying in {delay:.2f} seconds")
            
            time.sleep(delay)

def initialize_llm(model_name: str, api_key: str, is_main_model: bool = True, 
                  verbose: bool = False) -> ChatGoogleGenerativeAI:
    """
    Initialize an LLM with fallback options
    
    Args:
        model_name: Name of the model to initialize
        api_key: Google API key
        is_main_model: Whether this is the main model (vs reflection model)
        verbose: Whether to log detailed information
        
    Returns:
        Initialized ChatGoogleGenerativeAI instance
    """
    try:
        if is_main_model:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.7,
                max_output_tokens=1024,
                retry_on_failure=True,
                timeout=60
            )
        else:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.3,
                max_output_tokens=512,
                retry_on_failure=True,
                timeout=30
            )
        
        if verbose:
            logger.info(f"Successfully initialized {'main' if is_main_model else 'reflection'} model: {model_name}")
        return llm
    
    except Exception as e:
        model_type = "main" if is_main_model else "reflection"
        logger.warning(f"Error initializing {model_type} model {model_name}: {str(e)}")
        
        # Fallback to alternative model
        fallback_llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.7 if is_main_model else 0.3
        )
        return fallback_llm

def get_default_system_prompts() -> Dict[str, str]:
    """
    Get default system prompts for main and reflection models
    
    Returns:
        Dictionary with 'main' and 'reflection' system prompts
    """
    main_system_prompt = """You are a helpful AI assistant. Your goal is to provide accurate, 
    helpful, and clear responses to the user's queries."""
    
    reflection_system_prompt = """You are a critical evaluator. Your job is to analyze the AI's response 
    and provide constructive criticism. Focus on accuracy, completeness, clarity, and helpfulness.
    
    If the response has issues, explain them clearly.
    If the response is satisfactory, respond with just the phrase 'No critique needed'.
    
    Your critique will be used to improve the response, so be specific and constructive."""
    
    return {
        'main': main_system_prompt,
        'reflection': reflection_system_prompt
    }
