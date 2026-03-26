#!/usr/bin/env python3
"""
Educational AI Tutor Service for Physical AI and Humanoid Robotics

This service provides an API endpoint for students to ask questions about
Physical AI and Humanoid Robotics. It uses the OpenAI Agent SDK with
Gemini 2.0 Flash to generate educational responses guided by the project's
Global Constitution principles.

Usage:
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

Environment Variables:
    GEMINI_API_KEY: Your Google Gemini API key
    GEMINI_BASE_URL: Base URL for Gemini API (default: https://generativelanguage.googleapis.com/v1beta/openai/)
    GEMINI_MODEL: Model name (default: gemini-2.0-flash)
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
    # Add src to path for imports
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))

    # Set default environment variables if not set
    if not os.environ.get('GEMINI_API_KEY'):
        print("Warning: GEMINI_API_KEY environment variable not set.")
        print("Please set it before running the server in production.")
        os.environ.setdefault('GEMINI_API_KEY', 'dummy-key-for-development')

    from src.backend.main import app
    import uvicorn

    from src.backend.config import settings
    print(f"Starting Educational AI Tutor Service on {settings.host}:{settings.port}")
    print(f"Using model: {settings.gemini_model}")
    print(f"Rate limit: {settings.rate_limit_per_minute} requests per minute")
    print(f"Timeout: {settings.request_timeout_seconds} seconds")

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=True  # Set to False for production
    )

if __name__ == "__main__":
    run_server()