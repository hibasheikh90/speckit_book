# Research Report: Cohere API Integration

**Feature**: Replace Gemini with Cohere API
**Branch**: `010-replace-gemini-cohere`
**Date**: 2025-12-25

## Executive Summary

This research resolves all technical unknowns for migrating from Google Gemini to Cohere API in the FastAPI backend. The recommendation is to use **native Cohere SDK** (`cohere` Python package) with direct API integration, removing the `openai-agents` framework wrapper.

---

## 1. Cohere Python SDK

### Decision
Use **`cohere` package** (official Cohere Python SDK) with `AsyncClientV2` for async FastAPI integration.

### Installation
```bash
pip install cohere
```

### Requirements
- Python >=3.9, <4.0
- Async support via `cohere.AsyncClientV2`

### Key Imports
```python
import cohere
from cohere import AsyncClientV2
```

### Rationale
- Official SDK with full Cohere feature support
- Native async/await support for FastAPI
- Well-documented with active maintenance
- Direct API access (no compatibility layers)

### Alternatives Considered
- **OpenAI SDK with Cohere compatibility endpoint**: Adds unnecessary abstraction layer, limits access to Cohere-specific features
- **HTTP requests library (httpx/aiohttp)**: Requires manual request/response handling, error parsing, and maintenance

---

## 2. Chat Completions API Pattern

### Decision
Use **non-streaming async chat** with system instructions via `developer` role.

### Implementation Pattern
```python
import cohere

client = cohere.AsyncClientV2(
    api_key=settings.cohere_api_key,
    timeout=float(settings.request_timeout_seconds)
)

response = await client.chat(
    model="command-r-plus-08-2024",
    messages=[
        {"role": "developer", "content": constitution_text},  # System prompt
        {"role": "user", "content": user_message}
    ],
    temperature=0.7,
    max_tokens=2000,
)

# Extract response
content = response.message.content[0].text
```

### Key Parameters
- **model**: Model identifier (e.g., `command-r-plus-08-2024`)
- **messages**: List of dicts with `role` (`developer`, `user`, `assistant`) and `content`
- **temperature**: 0.0-2.0 (recommended 0.7 for educational content)
- **max_tokens**: Response length limit (2000 sufficient for tutoring)
- **timeout**: Configured at client level

### Rationale
- Matches existing synchronous response pattern
- `developer` role replaces OpenAI's `system` for instructions
- Simpler than streaming for current use case
- Timeout handling via `asyncio.wait_for()`

### Alternatives Considered
- **Streaming responses**: Adds complexity; frontend expects complete responses
- **Batch API**: Not needed for single-turn chat interactions

---

## 3. Error Handling Strategy

### Decision
Catch specific Cohere exceptions and map to custom `AIServiceError` and `EmptyAIResponse`.

### Error Mapping Table

| Cohere Exception | HTTP Status | Custom Exception | User Message |
|-----------------|-------------|------------------|--------------|
| `UnauthorizedError` | 401 | `AIServiceError` | "Invalid Cohere API key - check configuration" |
| `RateLimitError` | 429 | `AIServiceError` | "Rate limit exceeded - please try again later" |
| `BadRequestError` | 400 | `AIServiceError` | "Invalid request to Cohere API: {details}" |
| `ServiceUnavailableError` | 500 | `AIServiceError` | "Cohere service temporarily unavailable" |
| `asyncio.TimeoutError` | 504 | `AIServiceError` | "Request timed out after {N} seconds" |
| Empty response | 500 | `EmptyAIResponse` | "AI service returned empty response" |

### Implementation Pattern
```python
from cohere.errors import (
    UnauthorizedError,
    RateLimitError,
    BadRequestError,
    ServiceUnavailableError
)

try:
    response = await asyncio.wait_for(
        client.chat(...),
        timeout=settings.request_timeout_seconds
    )

    if not response.message or not response.message.content:
        raise EmptyAIResponse("Cohere returned empty response")

    return response.message.content[0].text.strip()

except asyncio.TimeoutError:
    raise AIServiceError(f"Request timed out after {settings.request_timeout_seconds} seconds")
except UnauthorizedError:
    raise AIServiceError("Invalid Cohere API key - check configuration")
except RateLimitError:
    raise AIServiceError("Rate limit exceeded - please try again later")
except BadRequestError as e:
    raise AIServiceError(f"Invalid request to Cohere API: {str(e)}")
except ServiceUnavailableError:
    raise AIServiceError("Cohere service temporarily unavailable")
except EmptyAIResponse:
    raise
except Exception as e:
    raise AIServiceError(f"AI service error: {str(e)}")
```

### Rationale
- Preserves existing error handling contract (`AIServiceError`, `EmptyAIResponse`)
- Provides specific error messages for debugging
- Maintains backward compatibility with frontend error handling
- Graceful degradation for unexpected errors

### Alternatives Considered
- **Generic exception handling**: Loses valuable error context for debugging
- **Retry logic with exponential backoff**: Adds complexity; current rate limits (10 req/min) well below Cohere's limits (500 req/min production)

---

## 4. Agent Framework Compatibility

### Decision
**Remove `openai-agents` framework** and use **native Cohere SDK directly**.

### Migration Path

**Current Architecture** (Gemini via agents framework):
```
User Request → FastAPI → AITutor → openai-agents (Agent, Runner) → AsyncOpenAI (Gemini endpoint) → Gemini API
```

**Target Architecture** (Native Cohere):
```
User Request → FastAPI → AITutor → AsyncClientV2 → Cohere API
```

### Implementation Changes

**Remove**:
- `openai-agents>=0.6.0` dependency
- `Agent`, `Runner`, `AsyncOpenAI`, `OpenAIChatCompletionsModel` imports
- Agent framework initialization logic

**Add**:
- `cohere` dependency
- `AsyncClientV2` client initialization
- Direct `client.chat()` calls

### Code Comparison

**Before (agent.py with agents framework)**:
```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

gemini_client = AsyncOpenAI(
    api_key=settings.gemini_api_key,
    base_url=settings.gemini_base_url,
)

model = OpenAIChatCompletionsModel(
    model=settings.gemini_model,
    openai_client=gemini_client
)

self.agent = Agent(
    name="Educational Tutor",
    instructions=constitution,
    model=model
)

result = await Runner.run(
    starting_agent=self.agent,
    input=message
)
content = result.final_output
```

**After (agent.py with native Cohere)**:
```python
import cohere

self.client = cohere.AsyncClientV2(
    api_key=settings.cohere_api_key,
    timeout=float(settings.request_timeout_seconds)
)

response = await self.client.chat(
    model=settings.cohere_model,
    messages=[
        {"role": "developer", "content": self.constitution},
        {"role": "user", "content": message}
    ],
    temperature=0.7,
)

content = response.message.content[0].text
```

### Rationale
- **Simpler architecture**: Removes 2 abstraction layers (Agent, Runner, OpenAIChatCompletionsModel)
- **Better performance**: Direct API calls without wrapper overhead
- **Full feature access**: No limitations from OpenAI compatibility layer
- **Easier maintenance**: Fewer dependencies, clearer error paths
- **Aligns with spec**: "Remove Gemini completely" includes removing Gemini-specific wrappers

### Alternatives Considered
- **Cohere's OpenAI Compatibility API** (`base_url="https://api.cohere.ai/compatibility/v1"`): Keeps unnecessary abstraction; limits access to Cohere-specific features; indirect API access

---

## 5. Model Selection

### Decision
Use **`command-r-plus-08-2024`** as the default model for educational tutoring.

### Model Comparison

| Model | Use Case | Context Length | Performance | Cost |
|-------|----------|----------------|-------------|------|
| `command-r-plus-08-2024` | **General tutoring, conversational AI** | 128k tokens | Fast, high quality | Standard |
| `command-a-03-2025` | Advanced reasoning, complex questions | 256k tokens | Slower, highest quality | Premium |
| `command-r` | Multilingual, coding tasks | 128k tokens | Fast, good quality | Standard |

### Rationale for `command-r-plus-08-2024`
- **Strong conversational capabilities**: Excellent for educational dialogue
- **Balanced speed/quality**: Suitable for real-time chat responses
- **Sufficient context**: 128k tokens handles large constitution + user query
- **Cost-effective**: Standard pricing tier
- **Well-tested**: Stable production model

### When to Upgrade to `command-a-03-2025`
- Advanced physics/robotics reasoning required
- Need to process entire textbook chapters in context
- Tool use integration for textbook search (future enhancement)

### Alternatives Considered
- **`command-r`**: Less conversational quality than `command-r-plus`
- **`command-a-03-2025`**: Overkill for current needs; higher latency and cost

---

## 6. Configuration Management

### Decision
Replace all `gemini_*` settings with `cohere_*` equivalents using Pydantic Settings.

### Configuration Changes

**Remove from settings.py**:
```python
gemini_api_key: str
gemini_model_name: str = "models/text-embedding-004"
gemini_model: str = "gemini-2.0-flash"
gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
```

**Add to settings.py**:
```python
cohere_api_key: str
cohere_model: str = "command-r-plus-08-2024"
```

### Environment Variables

**Remove from .env**:
```bash
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash
GEMINI_BASE_URL=...
```

**Add to .env**:
```bash
COHERE_API_KEY=your_cohere_api_key_here
COHERE_MODEL=command-r-plus-08-2024
```

### Validation Strategy
```python
# In AITutor.__init__()
if not settings.cohere_api_key:
    raise RuntimeError("COHERE_API_KEY environment variable is required")
```

### Rationale
- **Consistent naming**: `cohere_*` prefix matches existing pattern
- **Minimal surface area**: Only 2 settings needed (API key + model)
- **Type safety**: Pydantic validates at startup
- **Secure**: API key from environment, never hardcoded

### Alternatives Considered
- **Keep `gemini_*` names for compatibility**: Confusing; violates "remove completely" requirement
- **Generic names (`ai_api_key`)**: Less explicit; harder to debug

---

## 7. Rate Limiting & Quotas

### Decision
**Keep existing rate limiting** (10 req/min via `slowapi`); no changes needed.

### Cohere API Limits

| Tier | Chat API Limit | Embedding API Limit | Total Calls |
|------|----------------|---------------------|-------------|
| **Trial Keys** | 20 req/min | 1,000 req/min | 1,000 calls/month |
| **Production Keys** | 500 req/min | 10,000 req/min | Pay-as-you-go |

### Current Implementation
```python
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, chat_request: ChatRequest):
    # ... existing code ...
```

### Rationale
- **Well below limits**: 10 req/min << 20 req/min (trial) or 500 req/min (production)
- **User experience**: Prevents abuse without impacting legitimate users
- **No changes needed**: Existing `slowapi` middleware continues working
- **Cohere handles burst**: API-level rate limiting as safety net

### Alternatives Considered
- **Increase to 50 req/min**: Unnecessary; current limit sufficient for testing and initial deployment
- **Remove rate limiting**: Opens up to abuse; contradicts security best practices

---

## 8. Timeout Handling

### Decision
Configure timeout at **client level** and use `asyncio.wait_for()` for request-level timeout.

### Implementation Pattern
```python
import asyncio
import cohere

# Client-level timeout (default for all requests)
client = cohere.AsyncClientV2(
    api_key=settings.cohere_api_key,
    timeout=float(settings.request_timeout_seconds)  # 30 seconds
)

# Request-level timeout (additional safety)
response = await asyncio.wait_for(
    client.chat(...),
    timeout=settings.request_timeout_seconds
)
```

### Timeout Hierarchy
1. **Cohere client timeout** (30s): Network/read timeout for HTTP requests
2. **asyncio.wait_for timeout** (30s): Overall request timeout including processing
3. **FastAPI request timeout**: Default (no limit, handled by client/asyncio)

### Error Handling
```python
try:
    response = await asyncio.wait_for(client.chat(...), timeout=30)
except asyncio.TimeoutError:
    raise AIServiceError("Request timed out after 30 seconds")
```

### Rationale
- **Defense in depth**: Two timeout layers prevent hung requests
- **User experience**: 30-second timeout reasonable for educational chat
- **Consistency**: Matches existing Gemini timeout behavior
- **Error clarity**: Specific timeout exception for debugging

### Alternatives Considered
- **Only client timeout**: Misses edge cases where Cohere returns slowly
- **Only asyncio timeout**: Doesn't handle network-level hangs
- **Custom httpx client with granular timeouts**: Over-engineered for current needs

---

## 9. Dependencies Update

### Decision
Remove `openai-agents` and `google-generativeai`; add `cohere`.

### Dependency Changes

**Remove from pyproject.toml**:
```toml
"openai-agents>=0.6.0",
"google-generativeai>=0.8.0",
```

**Add to pyproject.toml**:
```toml
"cohere>=5.0.0",
```

**Keep unchanged**:
```toml
"fastapi>=0.115.0",
"uvicorn[standard]>=0.32.0",
"pydantic>=2.10.0",
"pydantic-settings>=2.6.0",
"slowapi>=0.1.9",
"python-dotenv>=1.0.0",
"qdrant-client>=1.12.0",  # For RAG - not affected by this change
"langchain-text-splitters>=0.3.0",  # For RAG - not affected
"tiktoken>=0.8.0",  # For RAG - not affected
```

### Installation Command
```bash
pip uninstall openai-agents google-generativeai -y
pip install cohere
```

### Rationale
- **Minimal dependencies**: Removes 2 unused packages, adds 1 needed package
- **Security**: Fewer dependencies = smaller attack surface
- **Maintenance**: Less dependency conflicts and version pinning
- **RAG preserved**: Qdrant and related packages untouched

### Alternatives Considered
- **Keep `openai-agents` for future OpenAI integration**: YAGNI (You Aren't Gonna Need It); add when needed
- **Use `cohere>=5.11.0` (latest)**: Pin to major version for stability; let minor versions auto-update

---

## 10. Backward Compatibility

### Decision
**Maintain identical request/response format** for frontend compatibility.

### API Contract (Unchanged)

**Request Model** (`models.py`):
```python
class ChatRequest(BaseModel):
    message: str
```

**Response Model** (`models.py`):
```python
class ChatResponse(BaseModel):
    response: str
    agent_name: str
```

**Endpoint Signature** (`main.py`):
```python
@app.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, chat_request: ChatRequest):
    # ... implementation changes internally ...
    return ChatResponse(
        response=response_text,
        agent_name="AI Tutor"  # Or from tutor_agent
    )
```

### No Changes Required
- **Routes**: `/chat` endpoint unchanged
- **HTTP methods**: POST request unchanged
- **Headers**: Content-Type: application/json unchanged
- **Status codes**: 200 (success), 429 (rate limit), 500 (error) unchanged
- **Frontend code**: No modifications needed

### Rationale
- **Spec requirement**: "Do not change routes, database, auth, or frontend"
- **Principle of Least Surprise**: Users expect same interface
- **Testing**: Existing frontend tests continue passing
- **Deployment**: Zero-downtime migration possible

### Alternatives Considered
- **Add `model` field to response**: Breaking change for frontend; unnecessary
- **Change endpoint to `/chat/cohere`**: Violates spec; confuses users

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **SDK** | Native Cohere Python SDK (`cohere` package) | Simpler, full feature access, better performance |
| **Client** | `AsyncClientV2` with async/await | Native FastAPI async support |
| **Architecture** | Remove `openai-agents` framework | Eliminates unnecessary abstraction layers |
| **Model** | `command-r-plus-08-2024` | Balanced speed/quality for educational tutoring |
| **API Pattern** | Non-streaming async chat | Matches existing synchronous response pattern |
| **System Prompt** | `developer` role in messages | Cohere's equivalent to OpenAI's `system` role |
| **Error Handling** | Catch specific Cohere exceptions | Detailed error context for debugging |
| **Timeout** | Client-level (30s) + asyncio.wait_for (30s) | Defense in depth, matches existing behavior |
| **Rate Limiting** | Keep existing 10 req/min | Well below Cohere limits, prevents abuse |
| **Configuration** | Replace `gemini_*` with `cohere_*` | Clear naming, minimal settings |
| **Dependencies** | Remove 2, add 1 | Fewer dependencies, smaller attack surface |
| **API Contract** | Identical request/response format | Backend-only change, zero frontend impact |

---

## Files Requiring Changes

1. **`backend/pyproject.toml`** - Update dependencies
2. **`backend/src/config/settings.py`** - Replace Gemini config with Cohere
3. **`backend/src/backend/config.py`** - Replace Gemini config with Cohere
4. **`backend/src/backend/agent.py`** - Rewrite with native Cohere SDK
5. **`backend/src/backend/main.py`** - Update health check to report Cohere model
6. **`.env`** - Update environment variables

---

## Files NOT Requiring Changes

- **`backend/src/backend/models.py`** - ChatRequest/ChatResponse unchanged
- **`backend/src/backend/exceptions.py`** - AIServiceError/EmptyAIResponse unchanged
- **`backend/src/auth/*`** - Authentication untouched
- **`backend/src/config/database.py`** - Database unchanged
- **`backend/src/tools/*`** - Textbook search tool unchanged (temporarily disabled anyway)
- **Frontend files** - Zero frontend changes
- **Database schema** - No migrations needed

---

## Testing Strategy

### Unit Tests
- Test `AITutor.generate_response()` with mock Cohere client
- Test error handling for each Cohere exception type
- Test empty response handling

### Integration Tests
- End-to-end chat flow: user query → backend → Cohere → response
- Health check endpoint returns Cohere model info
- Rate limiting still enforced (10 req/min)

### Manual Testing
```bash
# 1. Start backend
cd backend/src
uvicorn backend.main:app --reload

# 2. Test health check
curl http://localhost:8000/health

# Expected: {"status":"healthy","constitution_loaded":true,"model":"command-r-plus-08-2024","rate_limit":"10/minute"}

# 3. Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is physical AI?"}'

# Expected: {"response":"Physical AI refers to...","agent_name":"AI Tutor"}

# 4. Test error handling (invalid API key)
# Modify .env to use invalid key, restart server, send chat request
# Expected: 500 error with "AI service temporarily unavailable"
```

### Performance Validation
- Response time <30 seconds (timeout threshold)
- Comparable or faster than Gemini (baseline: measure existing response times first)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Cohere API key invalid/missing | Service fails at startup | Add validation in `AITutor.__init__()`; fail fast with clear error |
| Cohere rate limits too restrictive | Service degraded for high traffic | Current 10 req/min well below limits; monitor usage |
| Response quality different from Gemini | User experience changes | Test with sample questions; tune temperature/max_tokens if needed |
| Constitution too long for context | Request fails | Constitution <5k tokens; Cohere supports 128k context |
| Cohere service downtime | Chat unavailable | Implement fallback message (already exists in current code) |
| Breaking changes in Cohere SDK | Future upgrades break code | Pin to major version (`cohere>=5.0.0`); test before upgrading |

---

## Next Steps

1. ✅ **Research complete** - All unknowns resolved
2. ⏭️ **Phase 1: Design** - Create data-model.md and contracts
3. ⏭️ **Phase 2: Tasks** - Generate testable implementation tasks
4. ⏭️ **Implementation** - Execute migration following tasks.md
5. ⏭️ **Testing** - Validate all scenarios from spec.md
6. ⏭️ **Deployment** - Update .env, restart service, monitor

---

**Research Status**: ✅ Complete
**All NEEDS CLARIFICATION resolved**: Yes
**Ready for Phase 1**: Yes
