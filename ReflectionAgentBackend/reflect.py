from typing import Dict, List, Tuple
import logging
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from utils import call_with_retry, logger

def evaluate_response(messages: List[BaseMessage], reflection_llm, reflection_system_prompt: str,
                     verbose: bool = False, retry_delay: float = 2.0, max_retries: int = 3,
                     iteration_count: int = 1) -> Dict:
    """
    Evaluate the AI's response, providing critique for improvement
    
    Args:
        messages: The conversation history
        reflection_llm: The language model to use for reflection
        reflection_system_prompt: System prompt for the reflection model
        verbose: Whether to log detailed information
        retry_delay: Base delay between retries in seconds
        max_retries: Maximum number of retry attempts
        iteration_count: Current iteration number
        
    Returns:
        Dictionary with 'messages' (updated messages), 'needs_improvement' (bool),
        and 'critique' (the critique content)
    """
    latest_ai_response = next((msg.content for msg in reversed(messages) 
                            if isinstance(msg, AIMessage)), "No response")
    
    user_query = next((msg.content for msg in messages 
                     if isinstance(msg, HumanMessage) and "feedback" not in msg.content), 
                   "No query")
    
    if verbose:
        logger.info(f"\n--- Reflection for Response #{iteration_count} ---")
    
    try:
        # Create reflection prompt and get critique
        reflection_prompt = ChatPromptTemplate.from_messages([
            ("system", reflection_system_prompt),
            ("user", f"Original query: {user_query}\n\nAI response to evaluate:\n{latest_ai_response}\n\nProvide critique or say 'No critique needed'.")
        ])
        
        critique_chain = reflection_prompt | reflection_llm
        critique_response = call_with_retry(
            critique_chain.invoke, 
            {}, 
            max_retries, 
            retry_delay, 
            verbose
        )
        
        critique_content = critique_response.content
        
        if verbose:
            logger.info(f"Critique: {critique_content[:100]}...")
        
        # Check if critique is needed
        needs_improvement = "No critique needed" not in critique_content
        
        if not needs_improvement:
            if verbose:
                logger.info("No further improvements needed.")
            return {
                "messages": messages,
                "needs_improvement": False,
                "critique": critique_content
            }
        
        critique_message = HumanMessage(content=f"Please improve your response based on this feedback: {critique_content}")
        return {
            "messages": messages + [critique_message],
            "needs_improvement": True,
            "critique": critique_content
        }
        
    except Exception as e:
        # Handle reflection errors gracefully
        logger.error(f"Error during reflection: {str(e)}")
        if verbose:
            logger.info("Reflection failed. Continuing with original response.")
        return {
            "messages": messages,
            "needs_improvement": False,
            "critique": f"Error performing reflection: {str(e)}"
        }
