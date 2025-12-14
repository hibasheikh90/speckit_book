"""Pytest fixtures for testing."""
import os

# Set environment variables BEFORE any imports that might use them
os.environ["GEMINI_API_KEY"] = "test-api-key-for-testing"

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)
def mock_constitution_file():
    """Mock constitution file for all tests."""
    mock_content = """# Test Constitution

Educational-First Design: All responses must be educational and accessible.
"""
    with patch.object(Path, "read_text", return_value=mock_content):
        with patch.object(Path, "exists", return_value=True):
            yield


@pytest.fixture
def mock_constitution_content():
    """Mock Global Constitution content."""
    return """# Test Constitution

Educational-First Design: All responses must be educational and accessible.
"""


@pytest.fixture
def mock_agent(mock_constitution_content):
    """Mock AITutor for testing."""
    agent = MagicMock()
    agent.system_prompt = mock_constitution_content
    agent.generate_response = AsyncMock(return_value="This is a test response about Physical AI.")
    return agent


@pytest.fixture
async def client():
    """Async HTTP client for testing FastAPI app."""
    # Import here to avoid circular imports
    from backend.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    from backend.config import Settings

    with patch('backend.config.settings') as mock:
        mock.gemini_api_key = "test-api-key"
        mock.gemini_base_url = "https://test.api/"
        mock.gemini_model = "test-model"
        mock.request_timeout = 30
        mock.rate_limit_requests = 10
        mock.rate_limit_window = 60
        yield mock
