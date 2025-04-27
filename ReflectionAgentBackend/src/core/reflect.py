"""
Reflection module for evaluating and critiquing AI responses.
"""
from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from src.utils.utils import logger

def evaluate_response(messages: List[BaseMessage], reflection_llm, reflection_system_prompt: str,
                     verbose: bool = False, retry_delay: float = 2.0, max_retries: int = 3, 
                     iteration_count: int = 1):
    """
    Evaluate the last AI response and provide feedback on how to improve it.
    
    Args:
        messages: List of messages in the conversation
        reflection_llm: The LLM to use for reflection
        reflection_system_prompt: System prompt for the reflection model
        verbose: Whether to print debug messages
        retry_delay: Time to wait between retries
        max_retries: Maximum number of retries
        iteration_count: Current iteration number
    
    Returns:
        Dict with feedback messages and whether improvement is needed
    """
    if verbose:
        logger.info(f"Evaluating response (iteration {iteration_count})")
    
    # Get the last user query and AI response
    last_user_msg = None
    last_ai_msg = None
    
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and last_ai_msg is None:
            last_ai_msg = msg
        elif isinstance(msg, HumanMessage) and last_user_msg is None:
            last_user_msg = msg
            break
    
    if not last_user_msg or not last_ai_msg:
        logger.warning("Could not find last user message or AI response for reflection")
        return {
            "messages": messages,
            "needs_improvement": False
        }
    
    try:
        # Create the reflection prompt
        reflection_prompt = ChatPromptTemplate.from_messages([
            ("system", reflection_system_prompt),
            ("human", f"USER QUERY:\n{last_user_msg.content}\n\nAI RESPONSE:\n{last_ai_msg.content}")
        ])
        
        # Generate the reflection
        reflection_chain = reflection_prompt | reflection_llm
        reflection_result = reflection_chain.invoke({})
        reflection_content = reflection_result.content
        
        # Check if the response needs improvement based on the reflection
        needs_improvement = False
        if "REFLECTION:" in reflection_content and "NEEDS IMPROVEMENT: " in reflection_content:
            needs_improvement_text = reflection_content.split("NEEDS IMPROVEMENT: ")[1].split("\n")[0].strip().lower()
            needs_improvement = needs_improvement_text == "yes"
        
        # Add feedback message to the conversation
        feedback = HumanMessage(content=f"FEEDBACK: {reflection_content}")
        
        return {
            "messages": messages + [feedback],
            "needs_improvement": needs_improvement
        }
    
    except Exception as e:
        logger.error(f"Error in reflection: {str(e)}")
        # In case of error, continue without reflection
        return {
            "messages": messages,
            "needs_improvement": False
        }
