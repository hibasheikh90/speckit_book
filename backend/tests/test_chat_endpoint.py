"""Tests for FastAPI chat endpoint."""
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.exceptions import EmptyAIResponse, AIServiceError
from backend.agent import initialize_agent


@pytest.fixture(scope="module", autouse=True)
def setup_agent_for_endpoint_tests():
    """Initialize agent once for all endpoint tests."""
    # Initialize the agent with mocked constitution (already patched by conftest)
    initialize_agent()
    yield
    # Cleanup after all tests in module
    import backend.agent as agent_module
    agent_module.agent = None


@pytest_asyncio.fixture
async def test_client():
    """Create async test client for FastAPI app."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_agent_dependency():
    """Mock the get_agent dependency."""
    from backend.agent import AITutor
    from unittest.mock import MagicMock

    mock_agent = MagicMock(spec=AITutor)
    mock_agent.system_prompt = "Test constitution"
    mock_agent.generate_response = AsyncMock(return_value="This is a test response about Physical AI.")

    return mock_agent


@pytest.mark.asyncio
async def test_chat_endpoint_success(test_client, mock_agent_dependency):
    """Test /chat endpoint returns successful response for valid question."""
    from backend.main import app
    from backend.agent import get_agent

    # Override the dependency
    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        response = await test_client.post(
            "/chat",
            json={"message": "What is Physical AI?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "This is a test response about Physical AI."

        # Verify agent was called with correct message
        mock_agent_dependency.generate_response.assert_called_once_with("What is Physical AI?")

    finally:
        # Clean up dependency override
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_endpoint_valid_long_message(test_client, mock_agent_dependency):
    """Test /chat endpoint accepts long message within limit."""
    from backend.main import app
    from backend.agent import get_agent

    long_message = "A" * 10000
    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        response = await test_client.post(
            "/chat",
            json={"message": long_message}
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data

        # Verify agent was called
        mock_agent_dependency.generate_response.assert_called_once()

    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_endpoint_strips_whitespace(test_client, mock_agent_dependency):
    """Test /chat endpoint strips whitespace from message."""
    from backend.main import app
    from backend.agent import get_agent

    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        response = await test_client.post(
            "/chat",
            json={"message": "  What is Physical AI?  "}
        )

        assert response.status_code == 200

        # Verify agent was called with stripped message
        mock_agent_dependency.generate_response.assert_called_once_with("What is Physical AI?")

    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_endpoint_validation_too_short(test_client):
    """Test /chat endpoint returns 422 for message too short."""
    response = await test_client.post(
        "/chat",
        json={"message": "Hi"}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_chat_endpoint_validation_too_long(test_client):
    """Test /chat endpoint returns 422 for message too long."""
    long_message = "A" * 10001

    response = await test_client.post(
        "/chat",
        json={"message": long_message}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_chat_endpoint_validation_whitespace_only(test_client):
    """Test /chat endpoint returns 422 for whitespace-only message."""
    response = await test_client.post(
        "/chat",
        json={"message": "   "}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_chat_endpoint_validation_missing_message(test_client):
    """Test /chat endpoint returns 422 for missing message field."""
    response = await test_client.post(
        "/chat",
        json={}
    )

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_chat_endpoint_empty_response_error(test_client, mock_agent_dependency):
    """Test /chat endpoint handles EmptyAIResponse error."""
    from backend.main import app
    from backend.agent import get_agent

    # Configure mock to raise EmptyAIResponse
    mock_agent_dependency.generate_response = AsyncMock(
        side_effect=EmptyAIResponse("AI returned empty response")
    )

    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        response = await test_client.post(
            "/chat",
            json={"message": "What is Physical AI?"}
        )

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "unable to generate a response" in data["detail"].lower()
        assert "rephrasing" in data["detail"].lower()

    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_endpoint_timeout_error(test_client, mock_agent_dependency):
    """Test /chat endpoint handles timeout error."""
    from backend.main import app
    from backend.agent import get_agent

    # Configure mock to raise AIServiceError with timeout message
    mock_agent_dependency.generate_response = AsyncMock(
        side_effect=AIServiceError("Request timed out after 30 seconds")
    )

    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        response = await test_client.post(
            "/chat",
            json={"message": "What is Physical AI?"}
        )

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "took too long" in data["detail"].lower()

    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_endpoint_ai_service_error(test_client, mock_agent_dependency):
    """Test /chat endpoint handles generic AI service error."""
    from backend.main import app
    from backend.agent import get_agent

    # Configure mock to raise generic AIServiceError
    mock_agent_dependency.generate_response = AsyncMock(
        side_effect=AIServiceError("API connection failed")
    )

    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        response = await test_client.post(
            "/chat",
            json={"message": "What is Physical AI?"}
        )

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "temporarily unavailable" in data["detail"].lower()

    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_endpoint_success(mock_agent_dependency):
    """Test /health endpoint returns healthy status."""
    from backend.main import app
    from backend.agent import get_agent

    app.dependency_overrides[get_agent] = lambda: mock_agent_dependency

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["constitution_loaded"] is True

    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_endpoint_constitution_not_loaded():
    """Test /health endpoint shows constitution not loaded."""
    from backend.main import app
    from backend.agent import get_agent, AITutor
    from unittest.mock import MagicMock

    # Create mock agent with no constitution
    mock_agent = MagicMock(spec=AITutor)
    mock_agent.system_prompt = ""

    app.dependency_overrides[get_agent] = lambda: mock_agent

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["constitution_loaded"] is False

    finally:
        app.dependency_overrides.clear()
