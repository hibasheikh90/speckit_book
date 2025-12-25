#!/usr/bin/env python3
"""
Educational AI Tutor Service for Physical AI and Humanoid Robotics

This service provides an API endpoint for students to ask questions about
Physical AI and Humanoid Robotics. It uses the OpenAI Agent SDK with
Cohere Command A to generate educational responses guided by the project's
Global Constitution principles.

Usage:
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

Environment Variables:
    COHERE_API_KEY: Your Cohere API key
    COHERE_BASE_URL: Base URL for Cohere API (default: https://api.cohere.ai/compatibility/v1)
    COHERE_MODEL: Model name (default: command-a-03-2025)
    REQUEST_TIMEOUT_SECONDS: Request timeout in seconds (default: 30)
    RATE_LIMIT_PER_MINUTE: Rate limit per minute (default: 10)

API Endpoints:
    POST /chat - Submit a question and receive an educational response
    GET  /health - Health check endpoint
"""
import sys
from pathlib import Path

def run_server():
    """Run the backend server."""
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

    # Add src to path for imports
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))

    # Set default environment variables if not set
    if not os.environ.get('COHERE_API_KEY'):
        print("Warning: COHERE_API_KEY environment variable not set.")
        print("Please set it before running the server in production.")
        os.environ.setdefault('COHERE_API_KEY', 'dummy-key-for-development')

    from src.backend.main import app
    import uvicorn

    from src.backend.config import settings
    print(f"Starting Educational AI Tutor Service on {settings.host}:{settings.port}")
    print(f"Using model: {settings.cohere_model}")
    print(f"Rate limit: {settings.rate_limit_per_minute} requests per minute")
    print(f"Timeout: {settings.request_timeout_seconds} seconds")

    uvicorn.run(
        "src.backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=False  # Set to False to avoid the import string issue
    )

if __name__ == "__main__":
    run_server()