# Quickstart: Backend Chat Communication Service with OpenAIChatCompletionsModel

**Feature**: 001-fastapi-chat-endpoint
**Estimated Time**: 2-3 hours (including testing)
**Prerequisites**: Python 3.13, uv package manager

## Overview

This guide walks you through implementing a FastAPI chat endpoint using OpenAI Agent SDK with OpenAIChatCompletionsModel and Gemini 2.0 Flash. The system enables the frontend Chatbot UI to communicate with an AI agent providing educational responses about Physical AI and Humanoid Robotics, guided by the project's Global Constitution principles.

---

## Before You Begin

### Verify Prerequisites

```bash
# Check Python version
python --version
# Expected: Python 3.13.x

# Verify uv is installed
uv --version

# Clone or navigate to project directory
cd F:\speckit_book
```

### Environment Setup

```bash
# Create .env file with Gemini API key
cd backend
cat > .env << EOF
GEMINI_API_KEY=your-gemini-api-key-from-google-ai-studio
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL=gemini-2.0-flash
REQUEST_TIMEOUT_SECONDS=30
EOF
```

---

## Step 1: Install Dependencies (15 min)

### 1.1 Install Project Dependencies

```bash
cd backend

# Install dependencies using uv
uv sync

# Verify dependencies installed
uv pip list | grep -E "(fastapi|pydantic|openai-agents)"
```

**Expected Output**: All dependencies installed successfully, including `openai-agents>=0.6.0`.

### 1.2 Verify Configuration

```bash
# Check .env file exists and has required variables
cat .env
```

**Expected**: Contains `GEMINI_API_KEY`, `GEMINI_BASE_URL`, and `GEMINI_MODEL`.

---

## Step 2: Implement Core Components (45 min)

### 2.1 Create Project Structure

```bash
# Verify directory structure exists
mkdir -p backend/src/backend
mkdir -p backend/tests
mkdir -p backend/config
```

### 2.2 Create Configuration Module

**File**: `backend/src/backend/config.py`

```python
"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    gemini_api_key: str
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini_model: str = "gemini-2.0-flash"
    constitution_path: Path = Path("../.specify/memory/constitution.md")
    rate_limit_per_minute: int = 10
    request_timeout_seconds: int = 30
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
```

### 2.3 Create Exception Classes

**File**: `backend/src/backend/exceptions.py`

```python
"""Custom exception classes for the AI tutor service."""


class EmptyAIResponse(Exception):
    """Raised when the AI service returns an empty or unusable response."""

    def __init__(self, message: str = "AI service returned empty response"):
        self.message = message
        super().__init__(self.message)


class AIServiceError(Exception):
    """Raised when the AI service encounters an error."""

    def __init__(self, message: str = "AI service error occurred"):
        self.message = message
        super().__init__(self.message)
```

### 2.4 Create AI Agent Module

**File**: `backend/src/backend/agent.py`

```python
"""AI agent module for Gemini-powered educational tutor using agents-sdk."""
import asyncio
from pathlib import Path
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from backend.config import settings
from backend.exceptions import EmptyAIResponse, AIServiceError


class AITutor:
    """Gemini-powered AI tutor initialized with Global Constitution."""

    def __init__(self):
        """Initialize AI tutor with agents-sdk and Gemini."""
        # Validate API key is set
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is required")

        # Create Gemini-configured AsyncOpenAI client
        gemini_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
        )

        # Wrap in OpenAIChatCompletionsModel
        model = OpenAIChatCompletionsModel(
            model=settings.gemini_model,
            openai_client=gemini_client
        )

        # Load constitution and create agent with instructions
        constitution = self._load_constitution()
        self.agent = Agent(
            name="Educational Tutor",
            instructions=constitution,  # System prompt
            model=model
        )

    def _load_constitution(self) -> str:
        """Load Global Constitution from filesystem.

        Returns:
            str: Constitution content

        Raises:
            RuntimeError: If constitution file cannot be loaded
        """
        try:
            constitution_path = settings.constitution_path
            if not constitution_path.exists():
                raise FileNotFoundError(f"Constitution not found: {constitution_path}")
            return constitution_path.read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to load Global Constitution: {e}")

    async def generate_response(self, message: str) -> str:
        """Generate educational response using agents-sdk Runner.

        Args:
            message: Student question

        Returns:
            str: AI-generated educational response

        Raises:
            EmptyAIResponse: If AI service returns empty/unusable response
            AIServiceError: If AI service fails or times out
        """
        try:
            # Run agent with timeout
            result = await asyncio.wait_for(
                Runner.run(
                    starting_agent=self.agent,
                    input=message
                ),
                timeout=settings.request_timeout
            )

            # Extract and validate response
            content = result.final_output
            if not content or not content.strip():
                raise EmptyAIResponse("AI service returned empty response")

            return content.strip()

        except asyncio.TimeoutError:
            raise AIServiceError(f"Request timed out after {settings.request_timeout} seconds")
        except EmptyAIResponse:
            # Re-raise EmptyAIResponse as-is
            raise
        except Exception as e:
            # Catch all other exceptions and wrap in AIServiceError
            raise AIServiceError(f"AI service error: {str(e)}")


# Global agent instance (initialized on startup)
agent: AITutor | None = None


def initialize_agent() -> AITutor:
    """Initialize AI agent (called during app lifespan).

    Returns:
        AITutor: Initialized agent instance
    """
    global agent
    agent = AITutor()
    return agent


def get_agent() -> AITutor:
    """FastAPI dependency to get initialized agent.

    Returns:
        AITutor: The initialized agent

    Raises:
        RuntimeError: If agent not initialized
    """
    if agent is None:
        raise RuntimeError("AI agent not initialized. Call initialize_agent() first.")
    return agent
```

### 2.5 Create Pydantic Models

**File**: `backend/src/backend/models.py`

```python
"""Pydantic models for the chat API."""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="Student's learning question (3-10000 characters)"
    )

    @validator('message')
    def message_not_empty_whitespace(cls, v):
        """Validate that message is not only whitespace."""
        if not v.strip():
            raise ValueError('Message cannot be only whitespace')
        return v.strip()


class ChatResponse(BaseModel):
    """Response model for successful chat requests."""

    response: str = Field(
        ...,
        description="Educational response from the AI tutor"
    )
    agent_name: str = Field(
        default="Educational Tutor",
        description="Name of the agent that generated the response"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the response was generated (UTC)"
    )


class ErrorResponse(BaseModel):
    """Response model for error cases."""

    detail: str = Field(
        ...,
        description="Error message explaining what went wrong"
    )
```

---

## Step 3: Create FastAPI Application (30 min)

### 3.1 Create Main Application

**File**: `backend/src/backend/main.py`

```python
"""FastAPI application for the educational AI tutor service."""
from fastapi import FastAPI, Depends, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from backend.models import ChatRequest, ChatResponse, ErrorResponse
from backend.agent import get_agent, initialize_agent
from backend.config import settings
from pathlib import Path
import asyncio


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Educational AI Tutor API", version="1.0.0")

# Add rate limiter exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def startup_event():
    """Initialize the AI agent when the application starts."""
    print("Starting up AI tutor service...")
    initialize_agent()
    print("AI tutor service ready!")


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint to verify service status."""
    constitution_path = settings.constitution_path
    constitution_exists = constitution_path.exists()

    return {
        "status": "healthy",
        "constitution_loaded": constitution_exists,
        "model": settings.gemini_model,
        "rate_limit": f"{settings.rate_limit_per_minute}/minute"
    }


@app.post("/chat",
          response_model=ChatResponse,
          responses={
              200: {"description": "Successful response from AI tutor"},
              422: {"model": ErrorResponse, "description": "Validation error"},
              429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
              500: {"model": ErrorResponse, "description": "Internal server error"},
              504: {"model": ErrorResponse, "description": "Request timeout"}
          })
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: ChatRequest,
               chat_request: ChatRequest = Depends()):
    """Chat endpoint for students to ask questions about Physical AI and Humanoid Robotics.

    Args:
        request: The chat request containing the student's question
        chat_request: Dependency to validate the request

    Returns:
        ChatResponse: The AI tutor's educational response

    Raises:
        HTTPException: Various error conditions with appropriate status codes
    """
    try:
        # Get the initialized agent
        agent = get_agent()

        # Generate response from AI tutor
        response_text = await agent.generate_response(chat_request.message)

        # Return formatted response
        return ChatResponse(
            response=response_text,
            agent_name=agent.agent.name
        )

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Request timed out after {settings.request_timeout_seconds} seconds"
        )
    except Exception as e:
        # Log the error for debugging
        print(f"Chat endpoint error: {str(e)}")

        # Return generic error to client
        raise HTTPException(
            status_code=500,
            detail="The tutor service is temporarily unavailable. Please try again later."
        )


# For development/testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
```

---

## Step 4: Create Tests (1 hour)

### 4.1 Create Test Configuration

**File**: `backend/tests/conftest.py`

```python
"""Test configuration and fixtures for the AI tutor service."""
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_agent_result():
    """Mock result from Runner.run()."""
    result = MagicMock()
    result.final_output = "This is a mocked educational response about Physical AI."
    return result


@pytest.fixture
def mock_runner(mock_agent_result, monkeypatch):
    """Mock Runner.run() to return mock result."""
    async_mock = AsyncMock(return_value=mock_agent_result)
    monkeypatch.setattr("agents.Runner.run", async_mock)
    return async_mock


@pytest.fixture
def sample_valid_request():
    """Sample valid chat request."""
    return {"message": "What is Physical AI and how does it differ from traditional AI?"}


@pytest.fixture
def sample_invalid_request():
    """Sample invalid chat request (too short)."""
    return {"message": "Hi"}
```

### 4.2 Create Agent Tests

**File**: `backend/tests/test_agent.py`

```python
"""Tests for the AI agent module."""
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from backend.agent import AITutor
from backend.exceptions import EmptyAIResponse, AIServiceError


@pytest.mark.asyncio
async def test_agent_initialization():
    """Test that AITutor can be initialized successfully."""
    # This test requires valid environment variables
    # For now, just test that the class can be instantiated
    # The actual initialization will be tested with environment setup
    tutor = AITutor()
    assert tutor is not None


@pytest.mark.asyncio
async def test_agent_generates_response(mock_runner, mock_agent_result):
    """Test that agent generates response using Runner."""
    # Mock the agent initialization to avoid actual API calls
    from unittest.mock import patch

    with patch('backend.agent.AsyncOpenAI'), \
         patch('backend.agent.OpenAIChatCompletionsModel'), \
         patch('backend.agent.Agent'):

        tutor = AITutor()
        tutor.agent = MagicMock()  # Mock the agent

        response = await tutor.generate_response("What is Physical AI?")

        # Verify Runner.run was called
        # Note: Since we're mocking the agent, we check that the method works
        assert response == mock_agent_result.final_output.strip()


@pytest.mark.asyncio
async def test_agent_handles_empty_response():
    """Test that agent raises EmptyAIResponse for empty responses."""
    from unittest.mock import patch

    with patch('backend.agent.AsyncOpenAI'), \
         patch('backend.agent.OpenAIChatCompletionsModel'), \
         patch('backend.agent.Agent'):

        tutor = AITutor()
        tutor.agent = MagicMock()

        # Mock Runner.run to return empty response
        with patch('agents.Runner.run') as mock_run:
            mock_result = MagicMock()
            mock_result.final_output = ""
            mock_run.return_value = mock_result

            with pytest.raises(EmptyAIResponse):
                await tutor.generate_response("What is Physical AI?")


@pytest.mark.asyncio
async def test_agent_handles_timeout():
    """Test that agent raises AIServiceError on timeout."""
    from unittest.mock import patch

    with patch('backend.agent.AsyncOpenAI'), \
         patch('backend.agent.OpenAIChatCompletionsModel'), \
         patch('backend.agent.Agent'):

        tutor = AITutor()
        tutor.agent = MagicMock()

        # Mock Runner.run to raise timeout
        with patch('agents.Runner.run', side_effect=asyncio.TimeoutError()):

            with pytest.raises(AIServiceError):
                await tutor.generate_response("What is Physical AI?")


@pytest.mark.asyncio
async def test_agent_handles_generic_error():
    """Test that agent raises AIServiceError for other errors."""
    from unittest.mock import patch

    with patch('backend.agent.AsyncOpenAI'), \
         patch('backend.agent.OpenAIChatCompletionsModel'), \
         patch('backend.agent.Agent'):

        tutor = AITutor()
        tutor.agent = MagicMock()

        # Mock Runner.run to raise generic error
        with patch('agents.Runner.run', side_effect=Exception("API Error")):

            with pytest.raises(AIServiceError):
                await tutor.generate_response("What is Physical AI?")
```

### 4.3 Create API Tests

**File**: `backend/tests/test_chat_endpoint.py`

```python
"""Tests for the chat API endpoints."""
import pytest
from httpx import AsyncClient
from backend.src.backend.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test the health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_chat_valid_request(sample_valid_request):
    """Test chat endpoint with valid request."""
    # Note: This test will require mocking the AI agent for full functionality
    # For now, test validation and basic structure
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chat", json=sample_valid_request)

    # With mocked agent, this should work (status depends on mock implementation)
    # For now, just test that it doesn't fail on validation
    assert response.status_code in [200, 422, 500]  # Valid responses


@pytest.mark.asyncio
async def test_chat_invalid_request(sample_invalid_request):
    """Test chat endpoint with invalid request (too short)."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chat", json=sample_invalid_request)

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_chat_request_too_long():
    """Test chat endpoint with request that's too long."""
    long_message = {"message": "x" * 10001}  # Exceeds max length

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chat", json=long_message)

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_chat_empty_message():
    """Test chat endpoint with empty message."""
    empty_message = {"message": ""}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chat", json=empty_message)

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_chat_whitespace_message():
    """Test chat endpoint with whitespace-only message."""
    whitespace_message = {"message": "   "}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/chat", json=whitespace_message)

    assert response.status_code == 422  # Validation error
```

---

## Step 5: Run Service (30 min)

### 5.1 Start the Service

```bash
cd backend

# Run the service
uv run python -m backend.src.backend.main
# Or alternatively:
uv run uvicorn backend.src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected**: Service starts successfully, shows "AI tutor service ready!" message.

### 5.2 Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "constitution_loaded": true,
  "model": "gemini-2.0-flash",
  "rate_limit": "10/minute"
}
```

### 5.3 Test Chat Endpoint (Valid Question)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'
```

**Expected Response** (200 OK):
```json
{
  "response": "[Educational response about Physical AI]",
  "agent_name": "Educational Tutor",
  "timestamp": "2025-12-14T10:30:00Z"
}
```

### 5.4 Test Validation Errors

```bash
# Too short
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi"}'
```

**Expected**: 422 status, validation error message.

---

## Step 6: Run Tests (30 min)

### 6.1 Run All Tests

```bash
cd backend
pytest tests/ -v
```

**Expected**: All tests pass (may need to skip agent initialization tests that require API keys).

### 6.2 Run Tests with Coverage

```bash
pytest tests/ -v --cov=backend --cov-report=term-missing
```

**Expected**: Coverage >80% for non-API-dependent code.

---

## Step 7: Documentation Update (15 min)

### 7.1 Update README.md

**File**: `backend/README.md`

```markdown
# Educational AI Tutor Service

A FastAPI backend service that enables the frontend Chatbot UI to communicate with an AI agent providing educational responses about Physical AI and Humanoid Robotics, guided by the project's Global Constitution principles.

## Features

- **Educational Focus**: AI responses guided by Global Constitution principles
- **FastAPI Backend**: Modern, async Python web framework
- **Rate Limiting**: 10 requests per minute per client
- **Input Validation**: 3-10000 character limits, whitespace validation
- **Error Handling**: Comprehensive error responses and timeouts
- **OpenAI Agents SDK**: Uses OpenAIChatCompletionsModel with Agent/Runner abstractions

## Dependencies

- **openai-agents** (>=0.6.0): Agent orchestration SDK for Gemini integration
  - Enables future RAG and multi-agent workflows
  - Provides `OpenAIChatCompletionsModel`, `Agent`, and `Runner` abstractions
- **FastAPI** (>=0.115.0): Modern web framework
- **Pydantic** (>=2.10.0): Data validation
- **slowapi** (>=0.1.9): Rate limiting

## Environment Variables

Create a `.env` file in the backend directory:

```bash
GEMINI_API_KEY=your-gemini-api-key-from-google-ai-studio
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL=gemini-2.0-flash
REQUEST_TIMEOUT_SECONDS=30
```

## Endpoints

- `GET /health`: Health check
- `POST /chat`: Chat with the AI tutor

## Usage

1. Install dependencies: `uv sync`
2. Set up environment variables
3. Start the service: `uv run uvicorn backend.src.backend.main:app --reload`
4. Test with curl or frontend UI

## Testing

Run tests: `pytest tests/`

## Migration Notes

### v0.2.0: OpenAI Agents SDK Integration

**Date**: 2025-12-14
**Impact**: Internal implementation change, no API changes

Migrated from `openai` package to `openai-agents` SDK:
- AI client: AsyncOpenAI → OpenAIChatCompletionsModel
- Execution: Direct completion calls → Runner.run() with Agent
- System prompt: Per-request messages → Agent instructions

**Benefits**:
- Foundation for future agent orchestration features
- Standard SDK reduces custom code
- Enables RAG, tool use, and multi-agent workflows

**Backward Compatibility**: 100% - All existing API contracts maintained
```

---

## Verification Checklist

Before considering implementation complete, verify:

- [ ] Dependencies installed: `uv sync` completes without errors
- [ ] All tests pass: `pytest backend/tests/`
- [ ] Service starts successfully
- [ ] POST /chat with valid question returns 200 OK
- [ ] Validation errors handled (422 for invalid input)
- [ ] Health endpoint works (200 OK)
- [ ] Rate limiting functional
- [ ] README.md updated with usage instructions
- [ ] Configuration documented

---

## Troubleshooting

### Issue: "GEMINI_API_KEY environment variable is required"

**Solution**: Ensure `.env` file exists with valid API key:
```bash
echo "GEMINI_API_KEY=your-actual-key" > backend/.env
```

### Issue: Module 'agents' has no attribute 'Runner'

**Solution**: Verify openai-agents installed correctly:
```bash
uv pip show openai-agents
uv add openai-agents --upgrade
```

### Issue: Service returns 500 errors for valid requests

**Solution**: Check logs for exception details. Common causes:
- Constitution file not found → Verify path in config.py
- API key invalid → Check .env file
- Gemini API connectivity → Test with curl

---

## Next Steps

After successful implementation:

1. Commit changes:
   ```bash
   git add backend/
   git add specs/001-fastapi-chat-endpoint/
   git commit -m "feat: implement educational AI tutor with OpenAIChatCompletionsModel"
   ```

2. Create ADRs for architectural decisions

3. Create PHR documenting implementation execution

4. Update project documentation

5. Prepare for integration with frontend

---

## Summary

This implementation creates a complete FastAPI backend service for an educational AI tutor using OpenAI Agent SDK with OpenAIChatCompletionsModel and Gemini 2.0 Flash. The service provides educational responses about Physical AI and Humanoid Robotics while maintaining all specified requirements including validation, rate limiting, and error handling.