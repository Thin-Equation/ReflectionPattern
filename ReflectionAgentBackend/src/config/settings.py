"""
Configuration settings for the Reflection Agent Backend.
Loads environment variables and provides defaults.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Settings
PORT = int(os.environ.get("PORT", 5001))
HOST = os.environ.get("HOST", "0.0.0.0")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# Model Settings
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MAIN_MODEL = os.environ.get("MAIN_MODEL", "gemini-2.0-flash-exp")
REFLECTION_MODEL = os.environ.get("REFLECTION_MODEL", "gemini-2.0-flash")
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS", "3"))
VERBOSE = os.environ.get("VERBOSE", "true").lower() == "true"

# LangSmith Settings
LANGSMITH_API_KEY = os.environ.get("LANGCHAIN_API_KEY", "")
USE_LANGSMITH = os.environ.get("USE_LANGSMITH", "false").lower() == "true"
LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "reflection-pattern-agent")

# SSL Settings
USE_SSL = os.environ.get("USE_SSL", "false").lower() == "true"
SSL_CERT = "cert.pem" if os.path.exists("cert.pem") else None
SSL_KEY = "key.pem" if os.path.exists("key.pem") else None

# CORS Settings
CORS_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")