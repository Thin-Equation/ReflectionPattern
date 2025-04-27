# ReflectionPattern - Enhanced AI Agent

A comprehensive implementation of the Reflection Pattern, enabling systems to examine, critique, and modify their own structure and behavior dynamically. This enhanced implementation leverages LangChain, Google Gemini, LangSmith, and LangGraph.

## Overview

The Reflection Pattern allows programs to reflect on and critique their outputs through an iterative process. This implementation splits the application into two key layers:

- **Generation Module**: Creates initial outputs based on user prompts using Google Gemini
- **Reflection Module**: Analyzes and critiques generated content using configurable prompts

## Key Features

- **LangChain Integration**: Full integration with LangChain for flexible prompt management and LLM orchestration
- **Google Gemini 2.0 Models**: Uses Gemini 2.0 Flash and Gemini 2.0 Flash Experimental for improved responses
- **LangGraph Workflow**: Implements a sophisticated reflection workflow with conditional paths
- **LangSmith Tracing**: Optional tracing for monitoring performance and debugging
- **Robust Frontend**: Dynamic React/TypeScript interface with real-time feedback and dark/light mode
- **Custom SVG Icons**: TypeScript-compatible SVG icons for better UI experience

## Technology Stack

- **Backend**: Python with FastAPI, LangChain, LangGraph, and Google Generative AI
- **Frontend**: React 19 with TypeScript, Styled Components, and Framer Motion
- **Observability**: LangSmith for tracing and monitoring

## Project Structure

```
ReflectionPattern/
├── README.md                       # Project documentation
├── ReflectionAgentBackend/         # Backend Python code
│   ├── main.py                     # Main entry point
│   ├── requirements.txt            # Python dependencies
│   └── src/                        # Source code directory
│       ├── api/                    # API endpoints
│       │   └── app.py              # FastAPI application
│       ├── config/                 # Configuration
│       │   └── settings.py         # Environment and app settings
│       ├── core/                   # Business logic
│       │   ├── generate.py         # Response generation logic
│       │   ├── reflect.py          # Reflection and evaluation logic
│       │   └── reflection_agent.py # Core reflection agent implementation
│       ├── tests/                  # Test directory
│       └── utils/                  # Utility functions
│           └── utils.py            # Helper utilities
└── ReflectionAgentFrontend/        # Frontend React code
    ├── build/                      # Production build
    ├── public/                     # Static assets
    ├── src/                        # Source code
    │   ├── components/             # React UI components
    │   │   ├── AgentInterface.tsx  # Main interface component
    │   │   ├── IconComponent.tsx   # Custom TypeScript SVG icons
    │   │   ├── QueryForm.tsx       # User input form
    │   │   └── ResponseDisplay.tsx # Response visualization
    │   ├── services/               # API services
    │   ├── styles/                 # Theme and global styles
    │   └── types/                  # TypeScript type definitions
    ├── package.json                # Node.js dependencies
    └── tsconfig.json               # TypeScript configuration
```

## Installation

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/Thin-Equation/ReflectionPattern.git
cd ReflectionPattern
cd ReflectionAgentBackend/

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt
```

### Setting Environment Variables

Create a `.env` file in the ReflectionAgentBackend directory with the following variables:

```
GEMINI_API_KEY=your_google_api_key_here
LANGCHAIN_API_KEY=your_langsmith_api_key_here  # Optional
USE_LANGSMITH=false  # Set to true to enable LangSmith
LANGSMITH_PROJECT=reflection-pattern-agent  # Optional custom project name
MAX_ITERATIONS=3
VERBOSE=true
DEBUG=false
PORT=5001
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd ../ReflectionAgentFrontend/

# Install frontend dependencies
npm install

# Create a .env file for frontend configuration
echo "REACT_APP_API_URL=http://127.0.0.1:5001/api" > .env
```

## Usage

### Starting the Backend Server

```bash
# From the ReflectionAgentBackend directory
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py  # Use main.py instead of app.py with the new structure
```

### Starting the Frontend Development Server

```bash
# From the ReflectionAgentFrontend directory
npm start
```

The application should be accessible at:
- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:5001/api

### Using the Application

1. Enter your query in the input field
2. The agent will process your query through:
   - Initial generation with Gemini 2.0 Flash Experimental
   - Reflection and critique with Gemini 2.0 Flash
   - Improvement based on reflection feedback
3. View the final response and optionally explore the full reflection process
4. Toggle between dark and light mode using the theme button

### Customizing Reflection Behavior

You can customize the reflection behavior by modifying the system prompts in `src/utils/utils.py`.

## Advanced Configuration

### LangSmith Integration

To enable LangSmith tracing:

1. Set `USE_LANGSMITH=true` in your environment
2. Add your LangSmith API key as `LANGCHAIN_API_KEY`
3. Optionally set a custom project name with `LANGSMITH_PROJECT`

### Controlling Reflection Iterations

The number of reflection iterations can be controlled by:
- Setting `MAX_ITERATIONS` environment variable
- The agent will also stop early if it determines no further improvements are needed

## API Endpoints

- `GET /api/health`: Health check endpoint that returns server status and configuration
- `POST /api/query`: Main query endpoint, accepts JSON with a `query` field

## Recent Updates (April 2025)

- Restructured backend to follow industry-standard modular architecture
- Implemented proper configuration management with centralized settings
- Upgraded to Gemini 2.0 models for better performance
- Fixed TypeScript compatibility issues with custom SVG icons
- Improved UI with better server status indicators at bottom of interface
- Enhanced error handling and retry logic
- Optimized project structure for maintainability and testability
- Added comprehensive .gitignore file

## Development Practices

- **Backend Modularity**: The backend follows separation of concerns principles with distinct modules
- **Configuration Management**: All settings are centralized in the `config/settings.py` file
- **Testability**: Directory structure supports adding tests for each component
- **API Documentation**: FastAPI provides automatic Swagger documentation at `/docs` endpoint
- **TypeScript Safety**: Frontend uses proper typing throughout the codebase

## Troubleshooting

### Server Connection Issues

If the frontend cannot connect to the backend:
1. Check that the backend server is running (`python main.py`)
2. Verify the `REACT_APP_API_URL` in the frontend `.env` file matches the backend port
3. Check for any CORS issues in the browser console

### SSL Certificate Issues

If you encounter SSL certificate issues with the frontend-backend communication:
1. You may need to add a certificate exception in your browser
2. For development, you can set `NODE_TLS_REJECT_UNAUTHORIZED=0` to bypass certificate validation

### Model API Errors

If you encounter errors with the Google Generative AI API:
1. Verify your API key is valid and has appropriate permissions
2. Check that you're using supported model names (model names may change over time)
3. Ensure you're not exceeding rate limits or token quotas