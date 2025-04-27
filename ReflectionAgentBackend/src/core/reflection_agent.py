"""
Core implementation of the Reflection Pattern Agent.
"""
import os
from typing import List, Dict, Any, Optional
import logging
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import MessageGraph, END
from langsmith import Client

# Import the new modular components
from src.core.generate import generate_response
from src.core.reflect import evaluate_response
from src.utils.utils import initialize_llm, get_default_system_prompts, logger

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')

class ReflectionPatternAgent:
    def __init__(
        self,
        google_api_key: str,
        main_model: str = "gemini-2.0-flash-exp",
        reflection_model: str = "gemini-2.0-flash",
        max_iterations: int = 3,
        main_system_prompt: Optional[str] = None,
        reflection_system_prompt: Optional[str] = None,
        verbose: bool = False,
        retry_delay: float = 2.0,
        max_retries: int = 3,
        use_langsmith: bool = False,
        langsmith_api_key: Optional[str] = None,
        langsmith_project: str = "reflection-pattern-agent"
    ):
        """Initialize the Reflection Pattern Agent with improved error handling."""
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.iteration_count = 0
        self.retry_delay = retry_delay
        self.max_retries = max_retries
        # Flag to track if no further reflection is needed
        self.no_reflection_needed = False
        
        # Initialize models using the utility function
        self.main_llm = initialize_llm(main_model, google_api_key, True, verbose)
        self.reflection_llm = initialize_llm(reflection_model, google_api_key, False, verbose)
        
        # Set up default system prompts if not provided
        default_prompts = get_default_system_prompts()
        if not main_system_prompt:
            main_system_prompt = default_prompts['main']
            
        if not reflection_system_prompt:
            reflection_system_prompt = default_prompts['reflection']
        
        self.main_system_message = SystemMessage(content=main_system_prompt)
        self.reflection_system_prompt = reflection_system_prompt
        
        # Initialize LangSmith client if enabled
        self.use_langsmith = use_langsmith
        self.langsmith_project = langsmith_project
        if use_langsmith:
            if langsmith_api_key:
                os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
            elif "LANGCHAIN_API_KEY" not in os.environ:
                logger.warning("LangSmith enabled but no API key provided. Set LANGCHAIN_API_KEY environment variable.")
                self.use_langsmith = False
            
            if self.use_langsmith:
                try:
                    self.langsmith_client = Client()
                    if verbose:
                        logger.info("Successfully initialized LangSmith client")
                except Exception as e:
                    logger.warning(f"Failed to initialize LangSmith client: {str(e)}")
                    self.use_langsmith = False
        
        # Initialize the message graph
        self._create_graph()
    
    def generate(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """Generate a response with robust error handling"""
        self.iteration_count += 1
        return generate_response(
            messages, 
            self.main_llm, 
            self.verbose, 
            self.retry_delay, 
            self.max_retries,
            self.iteration_count
        )
    
    def reflect(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """Reflect on the response with error handling"""
        result = evaluate_response(
            messages, 
            self.reflection_llm, 
            self.reflection_system_prompt,
            self.verbose, 
            self.retry_delay, 
            self.max_retries,
            self.iteration_count
        )
        
        # Update the flag based on the reflection result
        self.no_reflection_needed = not result["needs_improvement"]
        
        return result["messages"]
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        builder = MessageGraph()
        
        builder.add_node("generate", self.generate)
        builder.add_node("reflect", self.reflect)
        
        builder.set_entry_point("generate")
        
        def should_continue(messages: List[BaseMessage]) -> str:
            ai_responses = sum(1 for msg in messages if isinstance(msg, AIMessage))
            
            if ai_responses >= self.max_iterations:
                if self.verbose:
                    logger.info(f"\n--- Reached maximum iterations ({self.max_iterations}) ---")
                return END
            
            # Check the flag to see if no reflection is needed
            if self.no_reflection_needed:
                if self.verbose:
                    logger.info("\n--- No further reflection needed ---")
                return END
            
            last_message = messages[-1] if messages else None
            
            if isinstance(last_message, AIMessage):
                return "reflect"
            
            if isinstance(last_message, HumanMessage) and "feedback" in last_message.content:
                return "generate"
            
            return END
        
        builder.add_conditional_edges("generate", should_continue)
        builder.add_conditional_edges("reflect", should_continue)
        
        # Configure LangSmith tracing if enabled
        if self.use_langsmith:
            # In newer versions of LangGraph, LangSmith config is handled via environment variables
            # and the project name can be set when running the graph
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = self.langsmith_project
            
            # Compile without passing langsmith_config directly
            self.graph = builder.compile()
            
            if self.verbose:
                logger.info(f"LangSmith tracing enabled for project: {self.langsmith_project}")
        else:
            # If LangSmith is not enabled, just compile without any config
            self.graph = builder.compile()
    
    def run(self, query: str) -> Dict[str, Any]:
        """Run the agent with comprehensive error handling"""
        self.iteration_count = 0
        # Reset the flag at the start of each run
        self.no_reflection_needed = False
        
        messages = [self.main_system_message, HumanMessage(content=query)]
        
        if self.verbose:
            logger.info(f"User query: {query}")
        
        try:
            final_messages = self.graph.invoke(messages)
            
            final_response = None
            for message in reversed(final_messages):
                if isinstance(message, AIMessage):
                    final_response = message.content
                    break
            
            return {
                "response": final_response or "No response generated.",
                "iterations": self.iteration_count,
                "messages": final_messages
            }
            
        except Exception as e:
            logger.error(f"Error running reflection agent: {str(e)}")
            
            return {
                "response": "I encountered an error while processing your request. This might be due to technical limitations or temporary issues.",
                "iterations": self.iteration_count,
                "error": str(e),
                "messages": messages
            }
