import os
import logging
from reflection_agent import ReflectionPatternAgent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get API key from environment variable
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", "your_api_key_here")

def example_basic_usage():
    """Basic usage example with minimal configuration."""
    print("\n=== Basic Usage Example ===\n")
    
    # Initialize the agent with minimal parameters
    agent = ReflectionPatternAgent(google_api_key=GOOGLE_API_KEY)
    
    # Run a simple query
    query = "What are three major impacts of climate change?"
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print(f"Final response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

def example_custom_prompts():
    """Example with custom system prompts."""
    print("\n=== Custom System Prompts Example ===\n")
    
    # Define custom system prompts
    main_prompt = """You are a scientific expert assistant. You provide detailed, 
    accurate, and evidence-based responses. Always cite relevant studies when possible.
    Use a formal, academic tone in your responses."""
    
    reflection_prompt = """You are a scientific peer reviewer. Evaluate the AI's response 
    for scientific accuracy, completeness, and proper citation of evidence.
    
    Check for:
    1. Scientific accuracy and alignment with current consensus
    2. Completeness of the explanation
    3. Proper citation of relevant studies
    4. Clarity and organization of the response
    
    If the response meets scientific standards, respond with 'No critique needed'.
    Otherwise, provide specific feedback for improvement."""
    
    # Initialize agent with custom prompts
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        main_system_prompt=main_prompt,
        reflection_system_prompt=reflection_prompt,
        max_iterations=2
    )
    
    # Run a scientific query
    query = "Explain the relationship between gut microbiome and mental health."
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print(f"Final response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

def example_verbose_debugging():
    """Example using verbose mode for debugging."""
    print("\n=== Verbose Debugging Example ===\n")
    
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        verbose=True,
        max_iterations=2
    )
    
    query = "Explain how neural networks learn patterns in data."
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print(f"\nFinal response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

def example_different_models():
    """Example using different models for main and reflection."""
    print("\n=== Different Models Example ===\n")
    
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        main_model="gemini-2.0-flash",
        reflection_model="gemini-2.0-pro-exp-02-05",
        verbose=True
    )
    
    query = "What are the ethical considerations of artificial intelligence?"
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print(f"\nFinal response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

def example_complex_query():
    """Example handling a more complex query requiring reflection."""
    print("\n=== Complex Query Example ===\n")
    
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        max_iterations=3,
        verbose=True
    )
    
    query = """Compare and contrast three different approaches to renewable energy storage, 
    including their efficiency, cost-effectiveness, and environmental impact. 
    Which approach holds the most promise for large-scale implementation?"""
    
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print(f"\nFinal response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

def example_full_conversation_history():
    """Example showing how to access the full conversation history."""
    print("\n=== Full Conversation History Example ===\n")
    
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        max_iterations=2
    )
    
    query = "What are the major challenges in quantum computing?"
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print("Full conversation history:")
    for i, message in enumerate(result["messages"]):
        print(f"\n[{i}] {message.__class__.__name__}: {message.content[:75]}...")
    
    print(f"\nFinal response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

# def example_error_handling():
#     """Example demonstrating error handling capabilities."""
#     print("\n=== Error Handling Example ===\n")
    
#     # Use a non-existent model to trigger fallback behavior
#     agent = ReflectionPatternAgent(
#         google_api_key=GOOGLE_API_KEY,
#         main_model="non-existent-model",
#         verbose=True
#     )
    
#     query = "What is the significance of quantum computing?"
#     print(f"Query: {query}\n")
    
#     result = agent.run(query)
    
#     print(f"Final response with fallback handling:\n")
#     print(result["response"])
    
#     return result

def example_with_batches():
    """Example processing multiple queries in batch."""
    print("\n=== Batch Processing Example ===\n")
    
    # Create a single agent instance to process multiple queries
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        max_iterations=2
    )
    
    queries = [
        "What is the impact of social media on mental health?",
        "Explain the concept of blockchain in simple terms.",
        "What are three strategies for effective time management?"
    ]
    
    results = []
    
    for i, query in enumerate(queries):
        print(f"\nQuery {i+1}: {query}")
        result = agent.run(query)
        results.append(result)
        print(f"Response {i+1} (after {result['iterations']} iterations):\n{result['response']}...\n")
    
    return results

def example_tuning_parameters():
    """Example showing how to tune agent parameters for different needs."""
    print("\n=== Parameter Tuning Example ===\n")
    
    # Configure for maximum quality with more iterations
    agent = ReflectionPatternAgent(
        google_api_key=GOOGLE_API_KEY,
        max_iterations=4,  # More iterations for complex topics
        max_retries=5,     # More retries for reliability
        retry_delay=3.0,   # Longer delay between retries
        verbose=True
    )
    
    query = "Explain the concept of quantum entanglement and its implications for computing."
    print(f"Query: {query}\n")
    
    result = agent.run(query)
    
    print(f"\nFinal response after {result['iterations']} iterations:\n")
    print(result["response"])
    
    return result

if __name__ == "__main__":
    print("ReflectionPatternAgent Examples\n")
    print("Make sure you have set your GOOGLE_API_KEY environment variable or replaced 'your_api_key_here'")
    
    # Uncomment the examples you want to run
    # example_basic_usage()
    # example_custom_prompts()
    # example_verbose_debugging()
    # example_different_models()
    # example_complex_query()
    # example_full_conversation_history()
    # example_with_batches()
    # example_tuning_parameters()
