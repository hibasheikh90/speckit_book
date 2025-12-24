# Quickstart Guide: Cohere API Integration

**Feature**: Replace Gemini with Cohere API
**Branch**: `010-replace-gemini-cohere`
**Date**: 2025-12-25

## Overview

This quickstart guide provides step-by-step instructions for developers to migrate the backend from Google Gemini to Cohere API. The migration affects **backend code only** - no frontend, database, or authentication changes are required.

**Time Estimate**: 30-45 minutes (excluding testing)

---

## Prerequisites

### Required

1. **Cohere API Key**
   - Sign up at [https://dashboard.cohere.com/](https://dashboard.cohere.com/)
   - Navigate to API Keys section
   - Generate a new API key (Trial or Production)
   - Trial keys: 1,000 calls/month, 20 req/min for chat
   - Production keys: Pay-as-you-go, 500 req/min for chat

2. **Python Environment**
   - Python >= 3.9
   - Virtual environment (recommended)

3. **Existing Backend Setup**
   - FastAPI application running
   - Existing `.env` file with configuration

### Recommended

- **Git**: For version control and branch management
- **Postman or curl**: For API testing
- **IDE**: VS Code, PyCharm, or similar with Python support

---

## Step 1: Update Dependencies

### 1.1 Uninstall Old Dependencies

```bash
cd backend
pip uninstall openai-agents google-generativeai -y
```

**Why**: Removes Gemini-specific packages that are no longer needed.

### 1.2 Install Cohere SDK

```bash
pip install cohere
```

**Version**: This installs the latest stable version (>=5.0.0).

### 1.3 Update pyproject.toml

**File**: `backend/pyproject.toml`

**Remove** these lines:
```toml
"openai-agents>=0.6.0",
"google-generativeai>=0.8.0",
```

**Add** this line:
```toml
"cohere>=5.0.0",
```

**Full dependencies section should look like**:
```toml
[project]
name = "backend"
version = "0.1.0"
description = "Educational AI Tutor Service for Physical AI and Humanoid Robotics"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "cohere>=5.0.0",
    "slowapi>=0.1.9",
    "python-dotenv>=1.0.0",
    "qdrant-client>=1.12.0",
    "langchain-text-splitters>=0.3.0",
    "tiktoken>=0.8.0",
]
```

### 1.4 Verify Installation

```bash
python -c "import cohere; print(cohere.__version__)"
```

**Expected output**: `5.x.x` (e.g., `5.11.4`)

---

## Step 2: Update Configuration

### 2.1 Update settings.py

**File**: `backend/src/config/settings.py`

**Find** the Gemini configuration section (around line 16-20):
```python
# Google Gemini API Configuration
gemini_api_key: str
gemini_model_name: str = "models/text-embedding-004"
gemini_model: str = "gemini-2.0-flash"
gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
```

**Replace** with Cohere configuration:
```python
# Cohere API Configuration
cohere_api_key: str
cohere_model: str = "command-r-plus-08-2024"
```

**Full updated Settings class**:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    # Authentication Settings
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    neon_database_url: str = ""

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_chunks"

    # Cohere API Configuration
    cohere_api_key: str
    cohere_model: str = "command-r-plus-08-2024"

    # Application Configuration
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = False
    constitution_path: Path = Path("../.specify/memory/constitution.md")
    request_timeout_seconds: int = 30

    # JWT Configuration
    jwt_access_token_expire_minutes: int = 1440  # 24 hours

    # Rate Limit Configuration
    rate_limit_per_minute: int = 10

    # RAG Configuration
    max_search_results: int = 5
    chunk_token_limit: int = 150
    embedding_dimension: int = 768

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create a singleton instance
settings = Settings()


def validate_auth_settings():
    """Validate that all required authentication settings are properly configured."""
    errors = []

    if not settings.neon_database_url:
        errors.append("NEON_DATABASE_URL environment variable must be set")

    if not settings.jwt_secret_key or settings.jwt_secret_key == "your-super-secret-key-change-in-production":
        errors.append("JWT_SECRET_KEY environment variable must be set to a secure value")

    if errors:
        return False, "; ".join(errors)

    return True, "All authentication settings are valid"
```

### 2.2 Update config.py (if duplicate exists)

**File**: `backend/src/backend/config.py`

**Find** the Gemini configuration (lines 13-16):
```python
# Gemini API Configuration
gemini_api_key: str
gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_model: str = "gemini-2.0-flash"
```

**Replace** with:
```python
# Cohere API Configuration
cohere_api_key: str
cohere_model: str = "command-r-plus-08-2024"
```

### 2.3 Update .env File

**File**: `backend/.env`

**Find** and remove:
```bash
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-2.0-flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

**Add**:
```bash
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=command-r-plus-08-2024
```

**Example .env after update**:
```bash
# Cohere Configuration
COHERE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
COHERE_MODEL=command-r-plus-08-2024

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_key_here
QDRANT_COLLECTION_NAME=textbook_chunks

# Database Configuration
NEON_DATABASE_URL=postgresql://user:password@host/db

# JWT Configuration
JWT_SECRET_KEY=your-secure-secret-key-here

# Application Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=false
RATE_LIMIT_PER_MINUTE=10
REQUEST_TIMEOUT_SECONDS=30
```

**Security Note**: Never commit `.env` to version control. Ensure `.env` is in `.gitignore`.

---

## Step 3: Rewrite agent.py

### 3.1 Backup Current File

```bash
cp backend/src/backend/agent.py backend/src/backend/agent.py.backup
```

### 3.2 Replace agent.py Content

**File**: `backend/src/backend/agent.py`

**Delete all existing content** and replace with:

```python
"""AI agent module for Cohere-powered educational tutor."""
import asyncio
import sys
from pathlib import Path
import cohere
from .config import settings
from .exceptions import EmptyAIResponse, AIServiceError

# Add parent directory to path for tools import
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.textbook_search_tool import textbook_search_tool


class AITutor:
    """Cohere-powered AI tutor initialized with Global Constitution."""

    def __init__(self):
        """Initialize AI tutor with Cohere AsyncClientV2."""
        # Validate API key is set
        if not settings.cohere_api_key:
            raise RuntimeError("COHERE_API_KEY environment variable is required")

        # Create Cohere async client with timeout
        self.client = cohere.AsyncClientV2(
            api_key=settings.cohere_api_key,
            timeout=float(settings.request_timeout_seconds)
        )

        # Load constitution for system instructions
        self.constitution = self._load_constitution()
        self.model = settings.cohere_model
        print(f"AITutor initialized with Cohere model: {self.model}")

    def _load_constitution(self) -> str:
        """Load Global Constitution from filesystem.

        Returns:
            str: Constitution content

        Raises:
            RuntimeError: If constitution file cannot be loaded
        """
        try:
            constitution_path = Path(settings.constitution_path)
            if not constitution_path.exists():
                raise FileNotFoundError(f"Constitution not found: {constitution_path}")
            return constitution_path.read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to load Global Constitution: {e}")

    async def generate_response(self, message: str) -> str:
        """Generate educational response using Cohere Chat API.

        Args:
            message: Student question

        Returns:
            str: AI-generated educational response

        Raises:
            EmptyAIResponse: If AI service returns empty/unusable response
            AIServiceError: If AI service fails or times out
        """
        try:
            # Call Cohere chat API with timeout
            response = await asyncio.wait_for(
                self.client.chat(
                    model=self.model,
                    messages=[
                        {
                            "role": "developer",  # System prompt role in Cohere
                            "content": self.constitution
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    temperature=0.7,  # Balanced creativity for education
                    max_tokens=2000,  # Reasonable response length
                ),
                timeout=settings.request_timeout_seconds
            )

            # Extract and validate response
            if not response.message or not response.message.content:
                raise EmptyAIResponse("Cohere returned empty response")

            content = response.message.content[0].text
            if not content or not content.strip():
                raise EmptyAIResponse("Cohere response content is empty")

            return content.strip()

        except asyncio.TimeoutError:
            raise AIServiceError(f"Request timed out after {settings.request_timeout_seconds} seconds")

        except cohere.errors.UnauthorizedError:
            raise AIServiceError("Invalid Cohere API key - check configuration")

        except cohere.errors.RateLimitError:
            raise AIServiceError("Rate limit exceeded - please try again later")

        except cohere.errors.BadRequestError as e:
            raise AIServiceError(f"Invalid request to Cohere API: {str(e)}")

        except cohere.errors.ServiceUnavailableError:
            raise AIServiceError("Cohere service temporarily unavailable")

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

**Key Changes**:
- Replaced `agents` imports with `cohere`
- Removed `Agent`, `Runner`, `AsyncOpenAI`, `OpenAIChatCompletionsModel`
- Direct `AsyncClientV2` initialization
- Messages format: `[{developer: constitution}, {user: message}]`
- Explicit error handling for Cohere exceptions

---

## Step 4: Update Health Check

### 4.1 Update main.py

**File**: `backend/src/backend/main.py`

**Find** the health check endpoint (around line 46-57):
```python
@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint to verify service status."""
    constitution_path = Path(settings.constitution_path)
    constitution_exists = constitution_path.exists()

    return {
        "status": "healthy",
        "constitution_loaded": constitution_exists,
        "model": settings.gemini_model,  # OLD
        "rate_limit": f"{settings.rate_limit_per_minute}/minute"
    }
```

**Replace** the `model` line:
```python
@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint to verify service status."""
    constitution_path = Path(settings.constitution_path)
    constitution_exists = constitution_path.exists()

    return {
        "status": "healthy",
        "constitution_loaded": constitution_exists,
        "model": settings.cohere_model,  # NEW
        "rate_limit": f"{settings.rate_limit_per_minute}/minute"
    }
```

**That's the only change in main.py** - everything else remains identical.

---

## Step 5: Testing

### 5.1 Start the Backend

```bash
cd backend/src
uvicorn backend.main:app --reload
```

**Expected startup output**:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend/src']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
Starting up AI tutor service...
AITutor initialized with Cohere model: command-r-plus-08-2024
AI tutor service ready!
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**If you see errors**:
- `RuntimeError: COHERE_API_KEY environment variable is required` → Check `.env` file
- `ModuleNotFoundError: No module named 'cohere'` → Run `pip install cohere`
- `FileNotFoundError: Constitution not found` → Verify `constitution_path` in settings

### 5.2 Test Health Check

```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "constitution_loaded": true,
  "model": "command-r-plus-08-2024",
  "rate_limit": "10/minute"
}
```

**Verify**:
- ✅ `model` is `"command-r-plus-08-2024"` (not `"gemini-2.0-flash"`)
- ✅ `constitution_loaded` is `true`

### 5.3 Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is physical AI?"}'
```

**Expected response** (example):
```json
{
  "response": "Physical AI combines artificial intelligence with physical embodiment, enabling machines to interact with and understand the physical world. Unlike traditional AI that operates purely in digital spaces, Physical AI powers robots and autonomous systems that perceive, reason about, and act upon their environment using sensors, actuators, and control systems...",
  "agent_name": "AI Tutor"
}
```

**Verify**:
- ✅ Response is relevant and educational
- ✅ Response format matches `ChatResponse` schema
- ✅ No error messages or empty responses

### 5.4 Test Error Handling

**Invalid API key test**:
1. Temporarily modify `.env` to use invalid key: `COHERE_API_KEY=invalid_key`
2. Restart backend
3. Send chat request

**Expected**:
```json
{
  "detail": "The tutor service is temporarily unavailable. Please try again later."
}
```

**Restore valid API key** after test.

### 5.5 Test Rate Limiting

```bash
# Send 11 requests rapidly (exceeds 10 req/min limit)
for i in {1..11}; do
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Test"}' &
done
wait
```

**Expected**: 11th request returns HTTP 429 with:
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

---

## Step 6: Verification Checklist

Before considering the migration complete, verify:

- [ ] **Dependencies updated**: `pip list | grep cohere` shows Cohere installed
- [ ] **No Gemini references**: `grep -r "gemini" backend/src/` returns only comments/docs
- [ ] **Configuration updated**: `.env` has `COHERE_API_KEY` and `COHERE_MODEL`
- [ ] **Health check reports Cohere**: `/health` endpoint shows `"model": "command-r-plus-08-2024"`
- [ ] **Chat works**: `/chat` endpoint returns relevant responses
- [ ] **Error handling works**: Invalid API key returns 500 error gracefully
- [ ] **Rate limiting works**: 11th rapid request returns 429 error
- [ ] **No frontend changes**: Frontend still works without modifications
- [ ] **No database changes**: Database schema unchanged
- [ ] **No auth changes**: Authentication system unchanged

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'cohere'"

**Solution**:
```bash
pip install cohere
```

---

### Issue: "RuntimeError: COHERE_API_KEY environment variable is required"

**Solution**:
1. Check `.env` file exists in `backend/` directory
2. Verify `.env` contains: `COHERE_API_KEY=your_key_here`
3. Restart backend to reload environment variables

---

### Issue: "Invalid Cohere API key - check configuration"

**Solution**:
1. Verify API key is correct (no extra spaces, quotes, or newlines)
2. Check API key is active in Cohere dashboard
3. Ensure API key has chat API access enabled

---

### Issue: "Rate limit exceeded - please try again later"

**Causes**:
- **Trial key limits**: Trial keys limited to 20 req/min, 1,000 calls/month
- **Application rate limit**: 10 req/min per IP (slowapi)

**Solution**:
- Wait 1 minute for rate limit to reset
- Upgrade to production API key for higher limits (500 req/min)
- Increase `RATE_LIMIT_PER_MINUTE` in `.env` (if needed)

---

### Issue: Empty or irrelevant responses

**Solution**:
1. Check constitution file is loading correctly (health check shows `constitution_loaded: true`)
2. Verify constitution path in settings: `constitution_path = Path("../.specify/memory/constitution.md")`
3. Test with simpler questions to isolate issue
4. Adjust `temperature` parameter in `agent.py` (lower = more focused, higher = more creative)

---

### Issue: Slow responses (>10 seconds)

**Causes**:
- Cohere API latency
- Large constitution size
- Network issues

**Solution**:
1. Check Cohere API status: [https://status.cohere.com/](https://status.cohere.com/)
2. Consider using `command-r` instead of `command-r-plus` for faster responses
3. Reduce `max_tokens` in `agent.py` if responses are too long
4. Increase `request_timeout_seconds` in `.env` if timeouts occur

---

## Next Steps

After successful migration:

1. **Deploy to production**:
   - Update production `.env` with Cohere API key
   - Deploy backend code
   - Monitor error logs for issues

2. **Monitor usage**:
   - Track Cohere API usage in dashboard
   - Monitor response quality and user feedback
   - Adjust `temperature` and `max_tokens` as needed

3. **Optimize if needed**:
   - Consider upgrading to `command-a-03-2025` for advanced reasoning
   - Implement caching for common questions
   - Fine-tune prompts in constitution for better responses

4. **Re-enable tools (optional)**:
   - Integrate textbook search tool with Cohere's tool use feature
   - Update `agent.py` to include tool definitions in chat API call

---

## Rollback Plan

If issues arise, rollback by:

1. **Restore dependencies**:
   ```bash
   pip install openai-agents google-generativeai
   pip uninstall cohere -y
   ```

2. **Restore agent.py**:
   ```bash
   cp backend/src/backend/agent.py.backup backend/src/backend/agent.py
   ```

3. **Restore configuration**:
   - Revert `settings.py` and `config.py` to Gemini config
   - Update `.env` with `GEMINI_API_KEY`

4. **Restart backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Verify**:
   - Health check shows `"model": "gemini-2.0-flash"`
   - Chat endpoint works with Gemini

---

## Summary

**Files Modified**:
1. `backend/pyproject.toml` - Dependencies updated
2. `backend/src/config/settings.py` - Configuration updated
3. `backend/src/backend/config.py` - Configuration updated
4. `backend/src/backend/agent.py` - Completely rewritten
5. `backend/src/backend/main.py` - Health check updated (1 line)
6. `backend/.env` - Environment variables updated

**Files Unchanged**:
- `backend/src/backend/models.py`
- `backend/src/backend/exceptions.py`
- `backend/src/auth/*`
- `backend/src/config/database.py`
- `backend/src/tools/*`
- All frontend files

**Result**: Backend now uses Cohere API with identical external API contract.

**Questions?** Refer to:
- [Cohere Python SDK Docs](https://docs.cohere.com/docs/python-sdk)
- [Cohere Chat API Reference](https://docs.cohere.com/reference/chat)
- Research report: `specs/010-replace-gemini-cohere/research.md`
