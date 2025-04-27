"""
FastAPI application definition for the Reflection Agent Backend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config.settings import (
    GOOGLE_API_KEY, 
    MAIN_MODEL, 
    REFLECTION_MODEL,
    MAX_ITERATIONS, 
    USE_LANGSMITH, 
    LANGSMITH_API_KEY, 
    LANGSMITH_PROJECT,
    VERBOSE,
    CORS_ORIGINS
)
from src.core.reflection_agent import ReflectionPatternAgent

# Initialize FastAPI app
app = FastAPI(
    title="Reflection Pattern API",
    description="API for the Reflection Pattern Agent using LangChain, LangGraph, and Google Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check for required environment variables
if not GOOGLE_API_KEY:
    print("Warning: GEMINI_API_KEY environment variable not set. The agent will not function properly.")

# Initialize the ReflectionPatternAgent
agent = ReflectionPatternAgent(
    google_api_key=GOOGLE_API_KEY,
    main_model=MAIN_MODEL,
    reflection_model=REFLECTION_MODEL,
    max_iterations=MAX_ITERATIONS,
    verbose=VERBOSE,
    use_langsmith=USE_LANGSMITH,
    langsmith_api_key=LANGSMITH_API_KEY,
    langsmith_project=LANGSMITH_PROJECT
)

# Define request model
class QueryRequest(BaseModel):
    query: str

# Define response model
class QueryResponse(BaseModel):
    response: str
    iterations: int
    messages: list

@app.post("/api/query", response_model=QueryResponse)
async def query_agent(query_request: QueryRequest):
    """
    Endpoint to handle queries sent by the frontend.
    """
    query = query_request.query

    if not query:
        raise HTTPException(status_code=400, detail="No query provided")

    try:
        # Run the agent with the provided query
        result = agent.run(query)

        # Format messages for frontend display
        formatted_messages = []
        for msg in result.get('messages', []):
            if hasattr(msg, 'type'):
                msg_type = msg.type
            else:
                # Determine message type based on class name
                if 'SystemMessage' in str(type(msg)):
                    msg_type = 'system'
                elif 'HumanMessage' in str(type(msg)):
                    msg_type = 'human'
                elif 'AIMessage' in str(type(msg)):
                    msg_type = 'ai'
                else:
                    msg_type = 'unknown'

            formatted_messages.append({
                'type': msg_type,
                'content': msg.content if hasattr(msg, 'content') else str(msg)
            })

        # Return the response to the frontend
        return {
            'response': result.get('response', ''),
            'iterations': result.get('iterations', 0),
            'messages': formatted_messages
        }

    except Exception as e:
        # Handle errors gracefully and return an error message
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify server status.
    """
    return {
        "status": "Server is running", 
        "config": {
            "use_langsmith": USE_LANGSMITH,
            "max_iterations": MAX_ITERATIONS,
            "verbose": VERBOSE,
            "main_model": MAIN_MODEL,
            "reflection_model": REFLECTION_MODEL
        }
    }
