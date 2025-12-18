#!/usr/bin/env python3
"""Test script to check backend health endpoint."""
import asyncio
import sys
from pathlib import Path

# Load environment variables first
import os
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_health_endpoint():
    """Test the health endpoint without starting the full server."""
    from src.backend.main import health_check
    import asyncio

    print("Testing health endpoint...")
    try:
        # Run the health check function directly
        result = asyncio.run(health_check())
        print(f"Health check result: {result}")
        print("[PASS] Health endpoint is working correctly!")
        return True
    except Exception as e:
        print(f"[FAIL] Health endpoint failed: {str(e)}")
        return False

def test_agent_initialization():
    """Test AI agent initialization."""
    print("\nTesting AI agent initialization...")
    try:
        from src.backend.agent import initialize_agent
        agent = initialize_agent()
        print(f"[PASS] AI agent initialized successfully: {agent.agent.name}")
        return True
    except Exception as e:
        print(f"[FAIL] AI agent initialization failed: {str(e)}")
        return False

def test_settings_validation():
    """Test configuration settings."""
    print("\nTesting configuration settings...")
    try:
        from src.config.settings import settings, validate_auth_settings
        print(f"[PASS] Settings loaded successfully")
        print(f"  - Host: {settings.backend_host}")
        print(f"  - Port: {settings.backend_port}")
        print(f"  - Model: {settings.gemini_model}")
        print(f"  - Rate limit: {settings.rate_limit_per_minute}/minute")

        # Validate auth settings
        is_valid, message = validate_auth_settings()
        print(f"  - Auth validation: {message}")
        return True
    except Exception as e:
        print(f"[FAIL] Settings validation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running backend functionality tests...\n")

    tests = [
        test_settings_validation,
        test_agent_initialization,
        test_health_endpoint
    ]

    results = []
    for test in tests:
        results.append(test())

    print(f"\nTest Results: {sum(results)}/{len(results)} tests passed")

    if all(results):
        print("[PASS] All backend components are functioning correctly!")
    else:
        print("[FAIL] Some tests failed")
        sys.exit(1)