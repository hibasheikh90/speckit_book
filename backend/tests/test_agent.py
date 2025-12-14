"""Tests for AI agent module."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from pathlib import Path
from backend.agent import AITutor, initialize_agent, get_agent
from backend.exceptions import EmptyAIResponse, AIServiceError


@pytest.fixture
def mock_openai_client():
    """Mock AsyncOpenAI client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test response about Physical AI."
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    return mock_client


@pytest.fixture
def mock_constitution():
    """Mock constitution file content."""
    return """# Test Constitution

Educational-First Design: All responses must be educational and accessible.
"""


def test_agent_initialization(mock_constitution):
    """Test AITutor initializes with OpenAI client and constitution."""
    with patch("backend.agent.AsyncOpenAI") as mock_openai:
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                # Verify OpenAI client was initialized
                mock_openai.assert_called_once()
                # Verify constitution was loaded
                assert agent.system_prompt == mock_constitution


def test_agent_constitution_loading_success(mock_constitution):
    """Test constitution loading from filesystem."""
    with patch("backend.agent.AsyncOpenAI"):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                assert agent.system_prompt == mock_constitution
                assert len(agent.system_prompt) > 0


def test_agent_constitution_loading_file_not_found():
    """Test constitution loading fails when file doesn't exist."""
    with patch("backend.agent.AsyncOpenAI"):
        with patch.object(Path, "exists", return_value=False):
            with pytest.raises(RuntimeError) as exc_info:
                AITutor()

            assert "Failed to load Global Constitution" in str(exc_info.value)


def test_agent_constitution_loading_read_error():
    """Test constitution loading fails on read error."""
    with patch("backend.agent.AsyncOpenAI"):
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", side_effect=IOError("Permission denied")):
                with pytest.raises(RuntimeError) as exc_info:
                    AITutor()

                assert "Failed to load Global Constitution" in str(exc_info.value)


@pytest.mark.asyncio
async def test_generate_response_success(mock_constitution, mock_openai_client):
    """Test successful response generation."""
    with patch("backend.agent.AsyncOpenAI", return_value=mock_openai_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()
                response = await agent.generate_response("What is Physical AI?")

                assert response == "This is a test response about Physical AI."
                # Verify API was called with correct parameters
                mock_openai_client.chat.completions.create.assert_called_once()
                call_args = mock_openai_client.chat.completions.create.call_args
                assert call_args.kwargs["messages"][0]["role"] == "system"
                assert call_args.kwargs["messages"][0]["content"] == mock_constitution
                assert call_args.kwargs["messages"][1]["role"] == "user"
                assert call_args.kwargs["messages"][1]["content"] == "What is Physical AI?"


@pytest.mark.asyncio
async def test_generate_response_strips_whitespace(mock_constitution, mock_openai_client):
    """Test response is stripped of leading/trailing whitespace."""
    mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "  Test response  "

    with patch("backend.agent.AsyncOpenAI", return_value=mock_openai_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()
                response = await agent.generate_response("Test question")

                assert response == "Test response"


@pytest.mark.asyncio
async def test_generate_response_empty_content_raises_error(mock_constitution):
    """Test empty response content raises EmptyAIResponse."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = ""
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                with pytest.raises(EmptyAIResponse) as exc_info:
                    await agent.generate_response("Test question")

                assert "empty response" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_generate_response_none_content_raises_error(mock_constitution):
    """Test None response content raises EmptyAIResponse."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = None
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                with pytest.raises(EmptyAIResponse):
                    await agent.generate_response("Test question")


@pytest.mark.asyncio
async def test_generate_response_whitespace_only_raises_error(mock_constitution):
    """Test whitespace-only response raises EmptyAIResponse."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "   \n  \t  "
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                with pytest.raises(EmptyAIResponse):
                    await agent.generate_response("Test question")


@pytest.mark.asyncio
async def test_generate_response_timeout_raises_error(mock_constitution):
    """Test timeout raises AIServiceError."""
    import asyncio

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(side_effect=asyncio.TimeoutError())

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                with pytest.raises(AIServiceError) as exc_info:
                    await agent.generate_response("Test question")

                assert "timed out" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_generate_response_generic_exception_raises_ai_service_error(mock_constitution):
    """Test generic exception raises AIServiceError."""
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API error"))

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                agent = AITutor()

                with pytest.raises(AIServiceError) as exc_info:
                    await agent.generate_response("Test question")

                assert "AI service error" in str(exc_info.value)


def test_initialize_agent(mock_constitution):
    """Test initialize_agent creates global agent instance."""
    import backend.agent as agent_module

    with patch("backend.agent.AsyncOpenAI"):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                result = initialize_agent()

                assert result is not None
                assert isinstance(result, AITutor)
                assert agent_module.agent is result


def test_get_agent_success(mock_constitution):
    """Test get_agent returns initialized agent."""
    import backend.agent as agent_module

    with patch("backend.agent.AsyncOpenAI"):
        with patch.object(Path, "read_text", return_value=mock_constitution):
            with patch.object(Path, "exists", return_value=True):
                # Initialize agent first
                initialize_agent()

                # Get agent
                result = get_agent()

                assert result is not None
                assert isinstance(result, AITutor)
                assert result is agent_module.agent


def test_get_agent_not_initialized():
    """Test get_agent raises error when agent not initialized."""
    import backend.agent as agent_module

    # Reset global agent
    agent_module.agent = None

    with pytest.raises(RuntimeError) as exc_info:
        get_agent()

    assert "not initialized" in str(exc_info.value).lower()
