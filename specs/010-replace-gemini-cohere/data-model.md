# Data Model: Replace Gemini with Cohere API

**Feature**: Replace Gemini with Cohere API
**Branch**: `010-replace-gemini-cohere`
**Date**: 2025-12-25

## Overview

This feature is a **provider replacement** with **no data model changes**. The migration replaces the AI service provider layer while preserving all existing data structures, API contracts, and database schemas.

---

## Existing Data Models (Unchanged)

### 1. ChatRequest (Request Model)

**File**: `backend/src/backend/models.py`

**Purpose**: Represents incoming chat requests from the frontend.

**Schema**:
```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
```

**Fields**:
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `message` | `str` | Yes | Non-empty | Student's question or prompt |

**Constraints**:
- `message` must be non-empty (enforced by Pydantic)
- No maximum length constraint (FastAPI handles payload size limits)

**Usage**:
```python
# Frontend sends:
{
    "message": "What is physical AI?"
}

# Backend parses into ChatRequest object:
chat_request = ChatRequest(message="What is physical AI?")
```

**No Changes Required**: This model remains identical before and after Cohere migration.

---

### 2. ChatResponse (Response Model)

**File**: `backend/src/backend/models.py`

**Purpose**: Represents chat responses returned to the frontend.

**Schema**:
```python
from pydantic import BaseModel

class ChatResponse(BaseModel):
    response: str
    agent_name: str
```

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `response` | `str` | Yes | AI-generated educational response text |
| `agent_name` | `str` | Yes | Name of the AI agent (e.g., "AI Tutor") |

**Constraints**:
- `response` should be non-empty (validated in agent logic)
- `agent_name` defaults to "AI Tutor" or extracted from agent configuration

**Usage**:
```python
# Backend returns:
{
    "response": "Physical AI combines artificial intelligence with physical embodiment...",
    "agent_name": "AI Tutor"
}

# Frontend receives ChatResponse object
```

**No Changes Required**: This model remains identical before and after Cohere migration.

---

### 3. ErrorResponse (Error Model)

**File**: `backend/src/backend/models.py`

**Purpose**: Represents error responses for validation and service failures.

**Schema**:
```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str
```

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `detail` | `str` | Yes | Error message describing the failure |

**Usage**:
```python
# On error, FastAPI returns:
{
    "detail": "The tutor service is temporarily unavailable. Please try again later."
}
```

**No Changes Required**: Error response format unchanged.

---

## Internal Models (Implementation-Only)

### 4. AITutor Class

**File**: `backend/src/backend/agent.py`

**Purpose**: Encapsulates the AI service client and provides the `generate_response()` method.

**Current State (Gemini)**:
```python
class AITutor:
    def __init__(self):
        self.client: AsyncOpenAI  # Gemini-compatible OpenAI client
        self.agent: Agent  # agents-sdk Agent wrapper
        self.constitution: str  # Loaded from filesystem
```

**Target State (Cohere)**:
```python
class AITutor:
    def __init__(self):
        self.client: cohere.AsyncClientV2  # Native Cohere async client
        self.constitution: str  # Loaded from filesystem
        self.model: str  # Cohere model name (e.g., "command-r-plus-08-2024")
```

**Fields After Migration**:
| Field | Type | Description |
|-------|------|-------------|
| `client` | `cohere.AsyncClientV2` | Cohere API client instance |
| `constitution` | `str` | Global Constitution text loaded from filesystem |
| `model` | `str` | Cohere model identifier (from settings) |

**Key Changes**:
- **Remove**: `self.agent` (agents-sdk Agent wrapper)
- **Replace**: `AsyncOpenAI` → `cohere.AsyncClientV2`
- **Add**: `self.model` to store model name explicitly

**Rationale**:
- Simpler architecture without Agent wrapper
- Direct access to Cohere client for error handling and configuration

---

### 5. Settings Class

**File**: `backend/src/config/settings.py` and `backend/src/backend/config.py`

**Purpose**: Application configuration loaded from environment variables.

**Current State (Gemini)**:
```python
class Settings(BaseSettings):
    # Gemini Configuration
    gemini_api_key: str
    gemini_model_name: str = "models/text-embedding-004"
    gemini_model: str = "gemini-2.0-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    # Other settings...
    constitution_path: Path = Path("../.specify/memory/constitution.md")
    request_timeout_seconds: int = 30
    rate_limit_per_minute: int = 10
```

**Target State (Cohere)**:
```python
class Settings(BaseSettings):
    # Cohere Configuration
    cohere_api_key: str
    cohere_model: str = "command-r-plus-08-2024"

    # Other settings (unchanged)...
    constitution_path: Path = Path("../.specify/memory/constitution.md")
    request_timeout_seconds: int = 30
    rate_limit_per_minute: int = 10

    # Qdrant, auth, database settings remain unchanged...
```

**Fields Changed**:
| Old Field | New Field | Type | Default | Description |
|-----------|-----------|------|---------|-------------|
| `gemini_api_key` | `cohere_api_key` | `str` | Required | API key for Cohere |
| `gemini_model` | `cohere_model` | `str` | `"command-r-plus-08-2024"` | Cohere model identifier |
| ~~`gemini_model_name`~~ | *(removed)* | - | - | Embedding model (not used for chat) |
| ~~`gemini_base_url`~~ | *(removed)* | - | - | OpenAI-compatible endpoint (not needed for native SDK) |

**Rationale**:
- `gemini_model_name` not used in current chat flow (RAG embeddings use separate config)
- `gemini_base_url` not needed with native Cohere SDK
- Minimal configuration surface area (2 fields: API key + model)

---

## Database Schema (No Changes)

This migration **does not affect database schemas**. All database models remain unchanged:

### User Model
**File**: `backend/src/auth/models/user.py`

**No Changes**: Authentication and user management unaffected.

**Schema**:
```python
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Rationale**: Per spec requirement: "Do not change routes, database, auth, or frontend."

---

## State Transitions

### AITutor Lifecycle (Before Migration)

```
1. [Application Startup]
   ↓
2. initialize_agent() called
   ↓
3. AITutor.__init__()
   - Load constitution from filesystem
   - Create AsyncOpenAI client (Gemini endpoint)
   - Wrap in OpenAIChatCompletionsModel
   - Create Agent with instructions and model
   ↓
4. [Agent Ready]
   ↓
5. On /chat request → generate_response(message)
   - Call Runner.run(agent, input=message)
   - Extract result.final_output
   - Return response
```

### AITutor Lifecycle (After Migration)

```
1. [Application Startup]
   ↓
2. initialize_agent() called
   ↓
3. AITutor.__init__()
   - Validate COHERE_API_KEY is set
   - Load constitution from filesystem
   - Create AsyncClientV2 (Cohere native client)
   ↓
4. [Agent Ready]
   ↓
5. On /chat request → generate_response(message)
   - Call client.chat(messages=[{developer: constitution}, {user: message}])
   - Extract response.message.content[0].text
   - Return response
```

**Key Differences**:
- **Removed**: Agent wrapper, Runner, OpenAIChatCompletionsModel
- **Simplified**: Direct client.chat() call instead of Runner.run()
- **Messages format**: Constitution passed as `developer` role message instead of Agent instructions

---

## Validation Rules

### Input Validation (Unchanged)

**ChatRequest.message**:
- Must be non-empty string (Pydantic validation)
- No explicit max length (FastAPI request size limits apply)

### Output Validation (Enhanced)

**AITutor.generate_response() checks**:
```python
# After Cohere API call
if not response.message or not response.message.content:
    raise EmptyAIResponse("Cohere returned empty response")

content = response.message.content[0].text
if not content or not content.strip():
    raise EmptyAIResponse("Cohere response content is empty")

return content.strip()
```

**Rationale**: Explicit validation ensures frontend always receives non-empty responses.

---

## Error States

### Exception Hierarchy (Unchanged)

**File**: `backend/src/backend/exceptions.py`

```python
class AIServiceError(Exception):
    """Base exception for AI service failures."""
    pass

class EmptyAIResponse(AIServiceError):
    """Raised when AI returns empty or unusable response."""
    pass
```

**Usage in agent.py**:
- Catch Cohere-specific exceptions (UnauthorizedError, RateLimitError, etc.)
- Map to `AIServiceError` or `EmptyAIResponse`
- Re-raise for FastAPI exception handler to return HTTP 500

**No Changes Required**: Exception classes unchanged; only the mapping logic in agent.py is updated.

---

## Dependencies Between Models

```
Settings (configuration)
    ↓ provides cohere_api_key, cohere_model, constitution_path
AITutor (service layer)
    ↓ generates response from user message
FastAPI /chat endpoint
    ↓ receives ChatRequest, returns ChatResponse
Frontend (external)
```

**Dependency Flow**:
1. **Settings** loaded from `.env` at app startup
2. **AITutor** initialized with Settings values
3. **FastAPI endpoint** receives `ChatRequest`, calls `AITutor.generate_response()`
4. **AITutor** calls Cohere API and returns string
5. **FastAPI endpoint** wraps response in `ChatResponse` model
6. **Frontend** receives JSON response

**No Changes to Flow**: The dependency chain remains identical; only the implementation inside `AITutor.generate_response()` changes.

---

## Migration Impact Summary

| Model/Class | Status | Changes |
|-------------|--------|---------|
| `ChatRequest` | ✅ Unchanged | No changes |
| `ChatResponse` | ✅ Unchanged | No changes |
| `ErrorResponse` | ✅ Unchanged | No changes |
| `User` (database) | ✅ Unchanged | No changes |
| `Settings` | ⚠️ Modified | Replace `gemini_*` fields with `cohere_*` |
| `AITutor` | 🔄 Refactored | Remove Agent wrapper, use native Cohere client |
| `AIServiceError` | ✅ Unchanged | No changes |
| `EmptyAIResponse` | ✅ Unchanged | No changes |

**Legend**:
- ✅ **Unchanged**: No modifications required
- ⚠️ **Modified**: Configuration updates only (no logic changes)
- 🔄 **Refactored**: Implementation rewritten (interface preserved)

---

## Conclusion

This feature has **minimal data model impact** because it is a **provider replacement**, not a feature addition. The migration maintains API contract stability by:

1. **Preserving all request/response models** (ChatRequest, ChatResponse, ErrorResponse)
2. **Maintaining database schema** (no migrations needed)
3. **Keeping exception hierarchy** (AIServiceError, EmptyAIResponse)
4. **Updating only configuration** (Settings class field renaming)
5. **Refactoring implementation** (AITutor internals) while preserving public interface

**No frontend changes required** because the API contract remains identical.
