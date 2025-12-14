# Implementation Plan: Backend Chat Communication Service

**Branch**: `001-fastapi-chat-endpoint` | **Date**: 2025-12-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fastapi-chat-endpoint/spec.md`

## Summary

Implement a minimalist FastAPI backend service that provides a single `/chat` POST endpoint, enabling students to interact with an AI tutor powered by the Gemini API (via OpenAI SDK). The AI tutor is initialized with the project's Global Constitution as its system prompt to ensure educational-first, accessible responses about Physical AI and Human

oid Robotics. This phase focuses on core chat functionality without authentication or RAG integration (deferred to future phases).

**Technical Approach**: Leverage FastAPI's async/await capabilities for concurrent request handling, use Pydantic for request validation (3-10,000 chars), implement in-memory rate limiting (10 req/min per student), enforce 30-second timeouts on AI API calls, and provide graceful error handling for all failure modes.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: FastAPI 0.115+, Uvicorn (ASGI server), Pydantic 2.x, OpenAI Python SDK 1.x, python-dotenv
**Storage**: In-memory (dict-based rate limiting; no persistence required this phase)
**Testing**: pytest, pytest-asyncio, httpx (async HTTP testing)
**Target Platform**: Linux/Windows server (local development via `uv run`)
**Project Type**: Web backend (single service)
**Performance Goals**:
- <5s startup time (FR-011)
- <10s response time p95 for valid requests (SC-002)
- <200ms validation response time (Pydantic)
- Support 10 concurrent students (SC-005)

**Constraints**:
- 30-second maximum timeout per request (FR-008)
- 10 requests/minute rate limit per student (FR-013)
- Must use `uv` environment for dependency management
- Backend directory pre-initialized at `F:\speckit_book\backend`

**Scale/Scope**: MVP phase - single endpoint, ~300 LOC total, 10 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Alignment

✅ **I. Educational-First Design**: AI tutor initialized with Global Constitution ensures educational responses
✅ **II. AI-Native Content Creation**: This plan follows spec-driven development; will document ADRs
⏭️ **III. RAG-First Information Architecture**: Deferred to Phase 5 (explicitly out of scope)
⏭️ **IV. Personalization & Accessibility**: Deferred to Phase 6 (no authentication this phase)
✅ **V. Security & Privacy by Design**: API keys via `.env`, input validation (3-10,000 chars), rate limiting, OWASP protections (input validation, no SQL injection risk)
✅ **VI. Performance & Scalability Standards**: FastAPI async endpoints target <200ms p95; constitution mentions <200ms for RAG (this is pre-RAG baseline)
✅ **VII. Open Source & Reproducibility**: `.env.example` provided, dependencies in `pyproject.toml`, documented setup

### Constitution-Mandated Technical Requirements

- ✅ **API Keys in `.env`** (Principle V): `GEMINI_API_KEY` environment variable
- ✅ **Input Validation** (Principle V, OWASP Top 10): Pydantic models validate 3-10,000 char constraint
- ✅ **FastAPI Framework** (Constitution § Technical Architecture → Backend): Explicitly mandated
- ✅ **OpenAI Agents SDK** (Constitution § Technical Architecture → Backend Dependencies): Listed as required dependency
- ⏭️ **Async/await for concurrency** (Principle VI): FastAPI handles this; explicit async route definitions planned

**Violations**: None - all requirements align with constitution

## Project Structure

### Documentation (this feature)

```text
specs/001-fastapi-chat-endpoint/
├── spec.md                  # Feature specification (completed)
├── plan.md                  # This file (implementation plan)
├── checklists/
│   └── requirements.md      # Specification quality validation
└── tasks.md                 # Phase 2 output (/sp.tasks command - NOT created yet)
```

### Source Code (repository root → backend directory)

```text
backend/
├── .env.example             # Sample environment variables (GEMINI_API_KEY)
├── .env                     # Local environment (gitignored)
├── .python-version          # Python 3.13 (existing)
├── pyproject.toml           # uv dependencies (existing, needs updates)
├── README.md                # Setup instructions (existing, needs updates)
├── src/
│   └── backend/
│       ├── __init__.py      # Package init (existing)
│       ├── main.py          # FastAPI app + /chat endpoint (NEW)
│       ├── models.py        # Pydantic request/response models (NEW)
│       ├── agent.py         # AI agent initialization & interaction (NEW)
│       ├── config.py        # Configuration loading (.env, constitution path) (NEW)
│       ├── rate_limiter.py  # In-memory rate limiting (NEW)
│       └── exceptions.py    # Custom exception classes (NEW)
└── tests/
    ├── __init__.py          # Test package init (NEW)
    ├── conftest.py          # Pytest fixtures (NEW)
    ├── test_chat_endpoint.py        # /chat endpoint tests (NEW)
    ├── test_validation.py           # Pydantic validation tests (NEW)
    ├── test_agent.py                # Agent initialization tests (NEW)
    └── test_rate_limiter.py         # Rate limiter tests (NEW)
```

**Structure Decision**: Web application structure (Option 2 from template) - backend service only. Frontend exists separately in `frontend/` but is out of scope for this phase. The backend uses a flat module structure within `src/backend/` since this is a single-endpoint MVP. Future phases will refactor into `api/`, `services/`, `models/` subdirectories as complexity grows.

## Complexity Tracking

> **No constitution violations** - this section documents why certain architectural choices are needed despite appearing complex.

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|-------------------------------------|
| Separate `agent.py` module | Encapsulates Gemini API config, constitution loading, prompt construction | Inline in `main.py` would violate single responsibility; constitution loading is >20 LOC |
| In-memory rate limiter (dict + timestamps) | No auth means no user IDs; must track by request origin/session | Using a library (slowapi) adds dependency; MVP scope doesn't justify external service (Redis) |
| Custom exception classes | Distinguish validation errors (422) from service errors (500) from rate limit (429) | FastAPI's HTTPException works but lacks semantic clarity for AI-specific errors (empty response) |

---

## Phase 0: Research & Validation

### Objective
Validate that Gemini API can be accessed via the OpenAI Python SDK and confirm the Global Constitution file is accessible.

### Tasks

1. **Research Gemini API + OpenAI SDK compatibility**
   - **Action**: Review Gemini API docs and OpenAI SDK docs to confirm configuration method
   - **Expected Output**: Confirmation that `openai.OpenAI(base_url=..., api_key=...)` can target Gemini API
   - **Decision Point**: If incompatible, evaluate using `google-generativeai` SDK directly (requires ADR)

2. **Verify Global Constitution file location**
   - **Action**: Confirm `.specify/memory/constitution.md` exists relative to backend directory
   - **Expected Path**: `../. specify/memory/constitution.md` from `backend/src/backend/`
   - **Fallback**: If not found, update constitution path in `config.py` based on actual location

3. **Validate Python 3.13 + uv environment**
   - **Action**: Run `uv --version` and `python --version` in backend directory
   - **Expected Output**: uv installed, Python 3.13.x active
   - **Blocker**: If uv not installed, halt and instruct user to install uv

### Research Artifacts
- Document Gemini API configuration in ADR-001
- Document Global Constitution loading strategy in ADR-002

---

## Phase 1: Core Architecture & Design

### Objective
Design the data models, API contracts, and module boundaries. Create detailed ADRs for all architecturally significant decisions.

### 1.1 API Contract Design

#### POST /chat Endpoint

**Request**:
```json
{
  "message": "string (3-10,000 characters)"
}
```

**Response (Success - 200 OK)**:
```json
{
  "response": "string (AI-generated educational response)"
}
```

**Response (Validation Error - 422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "type": "string_too_short | string_too_long | missing",
      "loc": ["body", "message"],
      "msg": "String should have at least 3 characters | String should have at most 10000 characters | Field required",
      "input": "..."
    }
  ]
}
```
*(Pydantic's default validation error format)*

**Response (Rate Limit - 429 Too Many Requests)**:
```json
{
  "error": "Rate limit exceeded. You can submit up to 10 questions per minute. Please wait before trying again."
}
```

**Response (AI Service Error - 500 Internal Server Error)**:
```json
{
  "error": "The AI tutor service is temporarily unavailable. Please try again later."
}
```

**Response (Empty AI Response - 500 Internal Server Error)**:
```json
{
  "error": "Unable to generate a response. Please try rephrasing your question or try again later."
}
```

**Response (Timeout - 500 Internal Server Error)**:
```json
{
  "error": "The request took too long to process. Please try again later."
}
```

#### Health Check Endpoint (Optional but Recommended)

**GET /health**

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "constitution_loaded": true,
  "timestamp": "2025-12-14T08:30:00Z"
}
```

### 1.2 Data Models (Pydantic)

**File**: `backend/src/backend/models.py`

```python
from pydantic import BaseModel, Field, field_validator

class ChatRequest(BaseModel):
    """Student question input model"""
    message: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="Student question (3-10,000 characters)"
    )

    @field_validator('message')
    @classmethod
    def validate_message_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Message cannot be only whitespace')
        return v.strip()

class ChatResponse(BaseModel):
    """Successful AI tutor response"""
    response: str = Field(..., description="AI-generated educational response")

class ErrorResponse(BaseModel):
    """Error response for all failure modes"""
    error: str = Field(..., description="Human-readable error message")
```

### 1.3 Configuration Management

**File**: `backend/src/backend/config.py`

```python
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration loaded from environment"""

    # Gemini API Configuration
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/openai/",
        alias="GEMINI_BASE_URL"
    )
    gemini_model: str = Field(default="gemini-2.0-flash", alias="GEMINI_MODEL")

    # Application Configuration
    constitution_path: Path = Field(
        default=Path(__file__).parent.parent.parent.parent / ".specify" / "memory" / "constitution.md",
        alias="CONSTITUTION_PATH"
    )
    request_timeout: int = Field(default=30, alias="REQUEST_TIMEOUT_SECONDS")
    rate_limit_requests: int = Field(default=10, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")

    # Server Configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()
```

### 1.4 Module Boundaries

1. **`main.py`**: FastAPI app, route definitions, dependency injection, lifespan management
2. **`models.py`**: Pydantic request/response models, validation logic
3. **`agent.py`**: AI agent initialization, Gemini API interaction, constitution loading
4. **`config.py`**: Environment variable loading, configuration validation
5. **`rate_limiter.py`**: In-memory rate limiting (dict-based, key = client identifier)
6. **`exceptions.py`**: Custom exception classes (RateLimitExceeded, EmptyAIResponse, AIServiceError)

**Rationale**: Single responsibility per module; enables isolated unit testing; constitution loading decoupled from API logic.

---

## Phase 2: Implementation Sequence

### Objective
Build the backend service incrementally, following test-driven development (TDD) principles where feasible.

### 2.1 Setup & Dependencies

**Tasks**:
1. Update `backend/pyproject.toml` dependencies:
   ```toml
   dependencies = [
       "fastapi>=0.115.0",
       "uvicorn[standard]>=0.32.0",
       "pydantic>=2.10.0",
       "pydantic-settings>=2.7.0",
       "openai>=1.58.0",
       "python-dotenv>=1.0.0",
   ]

   [dependency-groups]
   dev = [
       "pytest>=8.3.0",
       "pytest-asyncio>=0.24.0",
       "httpx>=0.28.0",
   ]
   ```

2. Create `.env.example`:
   ```env
   # Gemini API Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   GEMINI_MODEL=gemini-2.0-flash

   # Application Configuration
   CONSTITUTION_PATH=../.specify/memory/constitution.md
   REQUEST_TIMEOUT_SECONDS=30
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW_SECONDS=60

   # Server Configuration
   HOST=0.0.0.0
   PORT=8000
   ```

3. Install dependencies: `uv sync --dev`

**Acceptance**: `uv run python -c "import fastapi, openai; print('Dependencies installed')"` succeeds

### 2.2 Configuration Module

**File**: `backend/src/backend/config.py` (implement as designed in Phase 1.3)

**Test**: `backend/tests/test_config.py`
```python
import pytest
from backend.config import Settings

def test_config_loads_from_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
    settings = Settings()
    assert settings.gemini_api_key == "test-key-123"
    assert settings.request_timeout == 30  # default

def test_config_missing_api_key_raises_error():
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        Settings(_env_file=None)
```

**Acceptance**: Tests pass; constitution path resolves correctly

### 2.3 Data Models

**File**: `backend/src/backend/models.py` (implement as designed in Phase 1.2)

**Test**: `backend/tests/test_validation.py`
```python
import pytest
from pydantic import ValidationError
from backend.models import ChatRequest

def test_valid_message():
    req = ChatRequest(message="What is Physical AI?")
    assert req.message == "What is Physical AI?"

def test_message_too_short():
    with pytest.raises(ValidationError, match="at least 3 characters"):
        ChatRequest(message="Hi")

def test_message_too_long():
    with pytest.raises(ValidationError, match="at most 10000 characters"):
        ChatRequest(message="x" * 10001)

def test_message_whitespace_only():
    with pytest.raises(ValidationError, match="cannot be only whitespace"):
        ChatRequest(message="   ")
```

**Acceptance**: All validation edge cases pass (3 chars min, 10,000 max, whitespace rejection)

### 2.4 Rate Limiter

**File**: `backend/src/backend/rate_limiter.py`

**Design**:
```python
import time
from collections import defaultdict, deque
from typing import Dict, Deque

class InMemoryRateLimiter:
    """Track request timestamps per client identifier"""

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, Deque[float]] = defaultdict(deque)

    def is_allowed(self, client_id: str) -> bool:
        """Check if client can make a request; clean old timestamps"""
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove timestamps outside the window
        timestamps = self._requests[client_id]
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()

        # Check if under limit
        if len(timestamps) < self.max_requests:
            timestamps.append(now)
            return True
        return False

    def reset(self, client_id: str):
        """Clear rate limit for a client (for testing)"""
        self._requests.pop(client_id, None)
```

**Client Identifier Strategy** (ADR-003 decision):
- **This Phase (No Auth)**: Use request IP address from `request.client.host`
- **Future Phase (With Auth)**: Use authenticated user ID
- **Limitation**: IP-based tracking can't distinguish multiple students behind same NAT

**Test**: `backend/tests/test_rate_limiter.py`
```python
import time
from backend.rate_limiter import InMemoryRateLimiter

def test_allows_requests_under_limit():
    limiter = InMemoryRateLimiter(max_requests=10, window_seconds=60)
    for _ in range(10):
        assert limiter.is_allowed("client1") is True

def test_blocks_requests_over_limit():
    limiter = InMemoryRateLimiter(max_requests=10, window_seconds=60)
    for _ in range(10):
        limiter.is_allowed("client1")
    assert limiter.is_allowed("client1") is False

def test_allows_after_window_expires():
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=1)
    assert limiter.is_allowed("client1") is True
    assert limiter.is_allowed("client1") is True
    assert limiter.is_allowed("client1") is False  # limit reached
    time.sleep(1.1)  # wait for window to expire
    assert limiter.is_allowed("client1") is True  # allowed again
```

**Acceptance**: Rate limiter correctly enforces 10 req/60s per client

### 2.5 AI Agent Module

**File**: `backend/src/backend/agent.py`

**Design**:
```python
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from backend.config import settings
from backend.exceptions import EmptyAIResponse, AIServiceError

class AITutor:
    """Gemini-powered AI tutor initialized with Global Constitution"""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
        )
        self.model = settings.gemini_model
        self.system_prompt = self._load_constitution()

    def _load_constitution(self) -> str:
        """Load Global Constitution from filesystem"""
        try:
            constitution_path = settings.constitution_path
            if not constitution_path.exists():
                raise FileNotFoundError(f"Constitution not found: {constitution_path}")
            return constitution_path.read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to load Global Constitution: {e}")

    async def generate_response(self, message: str) -> str:
        """Generate educational response using Gemini API"""
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": message},
                    ],
                    timeout=settings.request_timeout,
                ),
                timeout=settings.request_timeout,
            )

            # Extract response text
            content = response.choices[0].message.content
            if not content or not content.strip():
                raise EmptyAIResponse("AI service returned empty response")

            return content.strip()

        except asyncio.TimeoutError:
            raise AIServiceError("Request timed out after 30 seconds")
        except EmptyAIResponse:
            raise
        except Exception as e:
            raise AIServiceError(f"AI service error: {str(e)}")

# Global agent instance (initialized on startup)
agent: AITutor | None = None

def initialize_agent() -> AITutor:
    """Initialize AI agent (called during app lifespan)"""
    global agent
    agent = AITutor()
    return agent

def get_agent() -> AITutor:
    """FastAPI dependency to get initialized agent"""
    if agent is None:
        raise RuntimeError("AI agent not initialized")
    return agent
```

**Test**: `backend/tests/test_agent.py`
```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.agent import AITutor
from backend.exceptions import EmptyAIResponse, AIServiceError

@pytest.mark.asyncio
async def test_agent_generates_response():
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Physical AI integrates..."))]
    mock_client.chat.completions.create.return_value = mock_response

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        agent = AITutor()
        response = await agent.generate_response("What is Physical AI?")
        assert "Physical AI" in response

@pytest.mark.asyncio
async def test_agent_raises_empty_response_error():
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=""))]
    mock_client.chat.completions.create.return_value = mock_response

    with patch("backend.agent.AsyncOpenAI", return_value=mock_client):
        agent = AITutor()
        with pytest.raises(EmptyAIResponse):
            await agent.generate_response("test")
```

**Acceptance**: Agent initializes with constitution, makes API calls, handles errors

### 2.6 Custom Exceptions

**File**: `backend/src/backend/exceptions.py`

```python
class RateLimitExceeded(Exception):
    """Raised when client exceeds rate limit"""
    pass

class EmptyAIResponse(Exception):
    """Raised when AI service returns empty/unusable response"""
    pass

class AIServiceError(Exception):
    """Raised when AI service fails (network, auth, timeout)"""
    pass
```

### 2.7 FastAPI Application

**File**: `backend/src/backend/main.py`

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.models import ChatRequest, ChatResponse, ErrorResponse
from backend.agent import initialize_agent, get_agent, AITutor
from backend.rate_limiter import InMemoryRateLimiter
from backend.config import settings
from backend.exceptions import RateLimitExceeded, EmptyAIResponse, AIServiceError

# Initialize rate limiter
rate_limiter = InMemoryRateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize AI agent on startup"""
    initialize_agent()
    yield

app = FastAPI(
    title="Physical AI Textbook Chat Service",
    description="AI tutor backend for Physical AI & Humanoid Robotics textbook",
    version="0.1.0",
    lifespan=lifespan,
)

def get_client_identifier(request: Request) -> str:
    """Extract client identifier for rate limiting"""
    # Phase 2: Use IP address (will be replaced with user ID in Phase 6)
    return request.client.host if request.client else "unknown"

@app.post("/chat", response_model=ChatResponse, responses={
    422: {"model": ErrorResponse, "description": "Validation error"},
    429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
    500: {"model": ErrorResponse, "description": "Service error"},
})
async def chat(
    chat_request: ChatRequest,
    request: Request,
    agent: AITutor = Depends(get_agent),
):
    """
    Submit a question to the AI tutor and receive an educational response.

    Rate limit: 10 requests per minute per client.
    Timeout: 30 seconds maximum.
    """
    # Rate limiting
    client_id = get_client_identifier(request)
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. You can submit up to 10 questions per minute. Please wait before trying again."
        )

    # Generate AI response
    try:
        response_text = await agent.generate_response(chat_request.message)
        return ChatResponse(response=response_text)

    except EmptyAIResponse:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate a response. Please try rephrasing your question or try again later."
        )

    except AIServiceError as e:
        if "timed out" in str(e).lower():
            raise HTTPException(
                status_code=500,
                detail="The request took too long to process. Please try again later."
            )
        raise HTTPException(
            status_code=500,
            detail="The AI tutor service is temporarily unavailable. Please try again later."
        )

@app.get("/health")
async def health_check(agent: AITutor = Depends(get_agent)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "constitution_loaded": agent.system_prompt is not None,
    }
```

**Test**: `backend/tests/test_chat_endpoint.py`
```python
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_chat_endpoint_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/chat", json={"message": "What is Physical AI?"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert len(data["response"]) > 0

@pytest.mark.asyncio
async def test_chat_endpoint_validation_too_short():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/chat", json={"message": "Hi"})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_chat_endpoint_rate_limit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Make 10 requests (should all succeed)
        for _ in range(10):
            response = await client.post("/chat", json={"message": "Test question"})
            assert response.status_code == 200

        # 11th request should be rate limited
        response = await client.post("/chat", json={"message": "Test question"})
        assert response.status_code == 429
        assert "rate limit" in response.json()["detail"].lower()
```

**Acceptance**: All endpoint tests pass; rate limiting works; error handling correct

### 2.8 README Documentation

**File**: `backend/README.md`

```markdown
# Physical AI Textbook - Chat Backend

Minimalist FastAPI backend providing an AI tutor chat service for the Physical AI & Humanoid Robotics textbook.

## Quick Start

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Gemini API key

### Setup

1. **Install dependencies**:
   ```bash
   cd backend
   uv sync --dev
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run the server**:
   ```bash
   uv run uvicorn backend.main:app --reload
   ```

4. **Test the endpoint**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is Physical AI?"}'
   ```

## API Documentation

- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

## Testing

```bash
uv run pytest
```

## Configuration

All configuration via environment variables (see `.env.example`):
- `GEMINI_API_KEY` (required): Your Gemini API key
- `REQUEST_TIMEOUT_SECONDS` (default: 30): Maximum request processing time
- `RATE_LIMIT_REQUESTS` (default: 10): Max requests per window
- `RATE_LIMIT_WINDOW_SECONDS` (default: 60): Rate limit window

## Architecture

- **Framework**: FastAPI (async/await for concurrency)
- **AI Provider**: Google Gemini via OpenAI SDK
- **Validation**: Pydantic (3-10,000 character constraint)
- **Rate Limiting**: In-memory (IP-based, 10 req/min)
- **System Prompt**: Global Constitution from `.specify/memory/constitution.md`
```

**Acceptance**: README provides clear setup instructions for new developers

---

## Phase 3: Testing & Validation

### 3.1 Unit Tests

**Coverage Targets**:
- `config.py`: 100% (environment loading, defaults, validation)
- `models.py`: 100% (Pydantic validation edge cases)
- `rate_limiter.py`: 100% (limit enforcement, window expiry)
- `agent.py`: 90% (mocked API calls, constitution loading, error handling)
- `exceptions.py`: 100% (exception instantiation)

**Command**: `uv run pytest --cov=backend --cov-report=term-missing`

### 3.2 Integration Tests

**File**: `backend/tests/test_integration.py`

```python
import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_end_to_end_chat_flow():
    """Test complete chat flow: request → validation → AI → response"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/chat", json={
            "message": "Explain ROS 2 nodes in simple terms"
        })
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        # Verify response adheres to educational principles (heuristic check)
        assert len(data["response"]) > 50  # Substantive answer
        assert any(keyword in data["response"].lower() for keyword in ["ros", "node", "communication"])
```

### 3.3 Acceptance Criteria Validation

| ID | Criteria | Validation Method |
|----|----------|-------------------|
| AC.1 | `uv run main.py` launches server | Manual: `uv run uvicorn backend.main:app` succeeds, health check returns 200 |
| AC.2 | Valid POST returns 200 OK | Test: `test_chat_endpoint_success` |
| AC.3 | Response contains `response` key | Test: assert `"response" in data` |
| AC.4 | Output adheres to Global Constitution | Manual: Submit "What is Physical AI?" and verify educational tone, clarity, accessibility |
| AC.5 | Invalid request returns 422 | Test: `test_chat_endpoint_validation_too_short` |

**Additional Validations**:
- **FR-002** (3-10,000 chars): Tests `test_message_too_short`, `test_message_too_long`
- **FR-008** (30s timeout): Test with mocked slow API call
- **FR-013** (rate limit): Test `test_chat_endpoint_rate_limit`

### 3.4 Performance Testing

**Manual Load Test** (using `httpx` or `locust`):
```python
# Simple concurrent request test
import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app

async def load_test():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tasks = [
            client.post("/chat", json={"message": f"Question {i}"})
            for i in range(10)  # 10 concurrent requests
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        success = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code == 200)
        print(f"Success: {success}/10")

asyncio.run(load_test())
```

**Target**: All 10 concurrent requests complete successfully (SC-005)

---

## Phase 4: Deployment Preparation

### 4.1 Environment Configuration

**Production `.env` template**:
```env
GEMINI_API_KEY=<production-key>
GEMINI_MODEL=gemini-2.0-flash
REQUEST_TIMEOUT_SECONDS=30
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60
HOST=0.0.0.0
PORT=8000
```

**Security Checklist**:
- ✅ No secrets in version control (`.env` gitignored)
- ✅ `.env.example` provided
- ✅ Constitution file accessible at deployment (verify path)

### 4.2 Startup Command

**Development**:
```bash
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Production** (future):
```bash
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4.3 Health Check Verification

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "constitution_loaded": true}
```

**Startup Time**: Measure with `time uv run uvicorn backend.main:app` → must be <5s (SC-001)

---

## Architectural Decision Records (ADRs)

### ADR-001: Gemini API Integration via OpenAI SDK

**Status**: Accepted
**Date**: 2025-12-14
**Context**: Need to integrate Gemini API for AI tutor functionality. Two options: (1) use `google-generativeai` SDK, (2) use `openai` SDK with base URL override.

**Decision**: Use OpenAI Python SDK configured to target Gemini's OpenAI-compatible endpoint.

**Rationale**:
- **Constitution Mandate**: Technical Architecture (§ Backend) lists "OpenAI Agents/ChatKit SDKs" as required dependency
- **Compatibility**: Gemini provides OpenAI-compatible API at `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Consistency**: Using OpenAI SDK aligns with future RAG integration plans (may use OpenAI embeddings)
- **Migration Path**: If Gemini proves insufficient, switching to OpenAI GPT models requires only changing `base_url` and `api_key`

**Configuration**:
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

**Consequences**:
- ✅ Alignment with constitution
- ✅ Future-proof for provider migration
- ⚠️ Depends on Gemini maintaining OpenAI API compatibility
- ⚠️ May not access Gemini-specific features (e.g., function calling) if they differ from OpenAI

**Alternatives Considered**:
- **google-generativeai SDK**: Native SDK, but violates constitution's mandate for OpenAI SDK; harder to migrate to OpenAI later

---

### ADR-002: Global Constitution as System Prompt

**Status**: Accepted
**Date**: 2025-12-14
**Context**: AI tutor must generate educational responses aligned with project principles. Constitution is ~6KB markdown file.

**Decision**: Load entire `.specify/memory/constitution.md` as system prompt on agent initialization.

**Rationale**:
- **Specification Requirement**: FR-003, FR-010, SC-004 mandate constitution-guided responses
- **Simplicity**: Full constitution provides maximum context for educational tone
- **Token Budget**: Gemini 2.0 Flash supports 1M token context; 6KB constitution ≈1,500 tokens (negligible)
- **Caching**: Future optimization can use prompt caching (Gemini supports this)

**Implementation**:
```python
class AITutor:
    def __init__(self):
        self.system_prompt = Path("../.specify/memory/constitution.md").read_text()

    async def generate_response(self, message: str) -> str:
        response = await self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message},
            ]
        )
```

**Consequences**:
- ✅ Strong alignment with educational principles
- ✅ No need for constitution summarization
- ⚠️ Uses ~1,500 tokens per request (acceptable for Gemini's context window)
- ⚠️ Constitution updates require agent restart (future: watch file for changes)

**Alternatives Considered**:
- **Summarized Constitution**: Reduces tokens but loses nuance; rejected (premature optimization)
- **Constitution Sections Only**: Include only Educational Quality Standards; rejected (loses Security/Performance context that may inform responses)

---

### ADR-003: IP-Based Rate Limiting (Pre-Authentication)

**Status**: Accepted (Temporary)
**Date**: 2025-12-14
**Context**: Need to enforce 10 req/min rate limit (FR-013, SC-008) without authentication system.

**Decision**: Implement in-memory rate limiting using client IP address as identifier.

**Rationale**:
- **Requirement**: FR-013 mandates rate limiting; spec assumption states "no authentication this phase"
- **Simplicity**: Dict-based tracker with deque of timestamps; no external dependencies
- **Phase Alignment**: IP-based is acceptable for MVP; Phase 6 will replace with user ID-based

**Implementation**:
```python
class InMemoryRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self._requests: Dict[str, Deque[float]] = defaultdict(deque)

    def is_allowed(self, client_id: str) -> bool:
        # Track timestamps, enforce limit
```

**Client ID Source**: `request.client.host` (FastAPI Request object)

**Consequences**:
- ✅ Meets FR-013 requirement for this phase
- ✅ Zero external dependencies (no Redis, no database)
- ⚠️ **Limitation**: Multiple students behind same NAT share limit
- ⚠️ **Limitation**: Restarting server resets all limits
- ⚠️ **Limitation**: Horizontal scaling (multiple server instances) can't share state

**Migration Path** (Phase 6):
- Replace `client_id = request.client.host` with `client_id = current_user.id` (from auth middleware)
- Consider Redis-based distributed rate limiting for multi-instance deployment

**Alternatives Considered**:
- **slowapi library**: Adds dependency; similar implementation; rejected (not worth dependency for MVP)
- **No rate limiting this phase**: Violates FR-013; rejected
- **Redis-based limiting**: Over-engineered for single-instance MVP; future consideration

---

### ADR-004: Error Response Structure

**Status**: Accepted
**Date**: 2025-12-14
**Context**: Need consistent error responses for validation (422), rate limits (429), and service errors (500).

**Decision**: Use FastAPI's default Pydantic validation errors (422) and custom JSON `{"error": "message"}` for all other errors.

**Rationale**:
- **Validation Errors (422)**: Pydantic's default format is well-documented and provides detailed field-level errors
- **Service Errors (429, 500)**: Simple `{"error": "..."}` matches user-facing error messages specified in clarifications
- **Consistency**: All non-validation errors use same structure for easy client parsing

**Response Formats**:

1. **Validation Error (422)** - Pydantic default:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "message"],
      "msg": "String should have at least 3 characters"
    }
  ]
}
```

2. **Rate Limit (429)**:
```json
{
  "error": "Rate limit exceeded. You can submit up to 10 questions per minute. Please wait before trying again."
}
```

3. **Service Errors (500)**:
```json
{
  "error": "The AI tutor service is temporarily unavailable. Please try again later."
}
```

**Implementation**:
```python
raise HTTPException(status_code=500, detail="<error message>")
# FastAPI converts HTTPException.detail to {"detail": "..."} by default
# We override with custom error handler for 429/500 to use {"error": "..."}
```

**Consequences**:
- ✅ Clear distinction between validation errors (422) and service errors (429/500)
- ✅ User-friendly messages aligned with clarification session answers
- ⚠️ Frontend must handle two error formats (`detail` array vs. `error` string)

**Alternatives Considered**:
- **Uniform `{"error": "..."}` for all errors**: Simpler but loses Pydantic's detailed validation info; rejected
- **Problem Details (RFC 7807)**: Over-engineered for MVP; future consideration

---

### ADR-005: Async FastAPI with 30-Second Timeout

**Status**: Accepted
**Date**: 2025-12-14
**Context**: FR-008 requires 30s max timeout; SC-005 requires handling 10 concurrent requests.

**Decision**: Use FastAPI's native async/await with `asyncio.wait_for()` for timeout enforcement.

**Rationale**:
- **FastAPI Native**: FastAPI's async routes handle concurrency via Uvicorn's async worker pool
- **Timeout Mechanism**: `asyncio.wait_for()` wraps the AI API call with explicit timeout
- **Simplicity**: No need for Celery or background tasks for simple request/response pattern

**Implementation**:
```python
async def generate_response(self, message: str) -> str:
    try:
        response = await asyncio.wait_for(
            self.client.chat.completions.create(...),
            timeout=30.0
        )
    except asyncio.TimeoutError:
        raise AIServiceError("Request timed out")
```

**Consequences**:
- ✅ Meets FR-008 (30s timeout) and SC-005 (10 concurrent requests)
- ✅ Leverages FastAPI's async capabilities (no additional orchestration)
- ⚠️ OpenAI SDK's internal timeout must also be set (via `timeout` parameter)

**Alternatives Considered**:
- **Sync FastAPI + Threading**: Blocks event loop; rejected (poor concurrency)
- **Celery Background Tasks**: Over-engineered for request/response; rejected (future consideration for RAG indexing)

---

### ADR-006: Constitution Loading Strategy

**Status**: Accepted
**Date**: 2025-12-14
**Context**: Constitution file must be loaded on agent initialization; failure should prevent startup.

**Decision**: Load constitution synchronously during `AITutor.__init__()`; raise exception if file not found.

**Rationale**:
- **Fail-Fast**: If constitution is missing, agent cannot function per FR-003; better to crash at startup than at first request
- **Immutable**: Constitution content doesn't change during runtime (assumption: no live editing)
- **Startup Time**: Reading 6KB file adds <10ms to startup (negligible vs. 5s budget)

**Implementation**:
```python
def __init__(self):
    self.system_prompt = self._load_constitution()

def _load_constitution(self) -> str:
    path = settings.constitution_path
    if not path.exists():
        raise FileNotFoundError(f"Constitution not found: {path}")
    return path.read_text(encoding="utf-8")
```

**Error Handling**: If constitution load fails, FastAPI lifespan raises exception → server startup fails → clear error message to operator

**Consequences**:
- ✅ Guarantees agent always has valid constitution
- ✅ Clear startup failure if misconfigured
- ⚠️ Constitution updates require server restart (acceptable for MVP; future: file watching)

**Alternatives Considered**:
- **Lazy Loading** (load on first request): Delays error discovery; rejected
- **Hot Reload** (watch file for changes): Over-engineered for MVP; future consideration

---

### ADR-007: Empty Response Detection

**Status**: Accepted
**Date**: 2025-12-14
**Context**: Clarification session specified handling empty AI responses (return friendly error suggesting rephrasing).

**Decision**: Check if `response.choices[0].message.content` is None, empty string, or whitespace-only; raise `EmptyAIResponse` exception.

**Rationale**:
- **Explicit Requirement**: Clarification Q1 answer mandates this behavior
- **Gemini Behavior**: Rare but possible for Gemini to return empty content (e.g., content filtering, token exhaustion)
- **User Experience**: Specific error message ("rephrase") more helpful than generic "service unavailable"

**Implementation**:
```python
content = response.choices[0].message.content
if not content or not content.strip():
    raise EmptyAIResponse("AI service returned empty response")
```

**Error Message** (from main.py):
```python
except EmptyAIResponse:
    raise HTTPException(
        status_code=500,
        detail="Unable to generate a response. Please try rephrasing your question or try again later."
    )
```

**Consequences**:
- ✅ Meets FR-009 requirement
- ✅ Better UX than generic error
- ⚠️ Treats all empty responses same (doesn't distinguish content filter vs. bug)

**Alternatives Considered**:
- **Treat as Generic Service Error**: Less user-friendly; rejected
- **Auto-Retry Once**: Adds complexity; deferred to future phase

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Gemini API incompatibility with OpenAI SDK | Low | High | ADR-001 documents fallback; validate in Phase 0 research |
| Constitution file path incorrect in production | Medium | High | Include path verification in health check endpoint |
| Rate limiter ineffective for NAT users | High | Medium | Document limitation; Phase 6 auth migration |
| 30s timeout too short for complex questions | Low | Medium | Monitor p95 latency; adjust in config if needed |
| Gemini API rate limits/quota exceeded | Medium | High | Implement exponential backoff; document quota requirements |
| Concurrent requests exceed Gemini's limits | Low | Medium | Test with 10 concurrent; Gemini supports high concurrency |

---

## Success Criteria Mapping

| ID | Criterion | Implementation | Validation |
|----|-----------|----------------|------------|
| SC-001 | Service available <5s startup | Minimal initialization (config + constitution load) | `time uv run uvicorn...` <5s |
| SC-002 | <10s response time p95 | Async FastAPI + Gemini (typically <3s) | Monitor during testing |
| SC-003 | 100% invalid inputs get feedback | Pydantic validation (auto) | Tests cover all edge cases |
| SC-004 | Responses adhere to 3+ constitution principles | Full constitution as system prompt | Manual review + heuristic checks |
| SC-005 | 10 concurrent requests succeed | FastAPI async handles concurrency | Load test with 10 parallel requests |
| SC-006 | 100% service failures return errors | Try/except all AI calls | Tests for timeout, empty, error cases |
| SC-007 | 95% first-attempt success | Robust error handling + validation | Integration tests |
| SC-008 | Rate limiting works with clear feedback | InMemoryRateLimiter + 429 responses | Test 11th request blocked |

---

## Dependencies Summary

**Production**:
- `fastapi>=0.115.0` - Web framework
- `uvicorn[standard]>=0.32.0` - ASGI server
- `pydantic>=2.10.0` - Data validation
- `pydantic-settings>=2.7.0` - Environment config
- `openai>=1.58.0` - AI API client (configured for Gemini)
- `python-dotenv>=1.0.0` - Environment variable loading

**Development**:
- `pytest>=8.3.0` - Testing framework
- `pytest-asyncio>=0.24.0` - Async test support
- `httpx>=0.28.0` - Async HTTP client for testing

**Total**: 6 production + 3 dev dependencies

---

## Timeline Estimate

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 0 | Research (Gemini API, constitution path) | 1 hour |
| Phase 1 | Architecture & ADRs | 2 hours |
| Phase 2.1-2.3 | Setup + Config + Models | 1 hour |
| Phase 2.4-2.5 | Rate limiter + Agent | 2 hours |
| Phase 2.6-2.7 | Exceptions + FastAPI app | 2 hours |
| Phase 2.8 | README | 30 minutes |
| Phase 3 | Testing (unit + integration) | 2 hours |
| Phase 4 | Deployment prep + validation | 1 hour |
| **Total** | | **11.5 hours** |

**Note**: Timeline assumes single developer; parallel work on tests + implementation can reduce total time.

---

## Next Steps

1. **Immediate**: Run Phase 0 research tasks to validate Gemini API + constitution path
2. **Create ADRs**: Generate standalone ADR files for decisions 001-007 in `history/adr/`
3. **Generate Tasks**: Run `/sp.tasks` command to convert this plan into TDD-style implementation tasks
4. **Implementation**: Follow Phase 2 sequence, writing tests before code where feasible

---

## References

- [Feature Specification](./spec.md)
- [Global Constitution](../../.specify/memory/constitution.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Gemini API - OpenAI Compatibility](https://ai.google.dev/gemini-api/docs/openai)
- [Pydantic Documentation](https://docs.pydantic.dev/)
