# Implementation Plan: Replace Gemini with Cohere API

**Branch**: `010-replace-gemini-cohere` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-replace-gemini-cohere/spec.md`

## Summary

Migrate the FastAPI backend from Google Gemini API to Cohere API for chat response generation. This is a **backend-only change** that replaces the AI provider layer while maintaining identical API contracts for frontend compatibility. No changes to routes, database, authentication, or frontend code are required.

**Core Change**: Replace `openai-agents` framework wrapping Gemini with native Cohere Python SDK (`cohere.AsyncClientV2`) for direct API integration.

**Impact**: Backend implementation only; zero frontend changes; no database migrations; no API contract modifications.

---

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: FastAPI 0.115+, Cohere Python SDK 5.0+, Pydantic 2.10+, Pydantic Settings 2.6+
**Storage**: Neon Serverless Postgres (unchanged), Qdrant Cloud (unchanged)
**Testing**: pytest (unit tests), manual integration tests, API contract validation
**Target Platform**: Linux server (production), Windows/Mac (development)
**Project Type**: Web application (FastAPI backend + Docusaurus frontend)
**Performance Goals**: <30s response time (timeout threshold), comparable to Gemini baseline
**Constraints**: <200ms p95 for health checks, maintain 10 req/min rate limit, zero frontend changes
**Scale/Scope**: Single backend service, 6 files modified, ~200 lines of code changed

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Educational-First Design
- **Status**: PASS
- **Rationale**: Migration improves AI response quality with Cohere's `command-r-plus-08-2024` model optimized for conversational education. Constitution (system prompt) remains loaded and enforced.
- **Evidence**: Constitution loading mechanism preserved; `developer` role in Cohere messages replaces OpenAI `system` role with identical behavior.

### ✅ AI-Native Content Creation
- **Status**: PASS
- **Rationale**: Migration follows spec-driven development principles with full specification, planning, and task breakdown.
- **Evidence**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` created following SDD workflow.

### ✅ RAG-First Information Architecture
- **Status**: PASS
- **Rationale**: RAG system (Qdrant vector store) unchanged; only chat response generation layer replaced. Future: Cohere supports tool use for enhanced RAG integration.
- **Evidence**: Qdrant configuration, textbook search tool, and embedding generation untouched.

### ✅ Personalization & Accessibility
- **Status**: PASS
- **Rationale**: User preferences, onboarding, and translation features unaffected (handled separately from chat API).
- **Evidence**: Database schema unchanged; authentication and user management unchanged.

### ✅ Security & Privacy by Design
- **Status**: PASS
- **Rationale**: API key management follows same secure pattern (environment variables, never hardcoded). Error messages sanitized (no internal details leaked). Cohere SDK uses HTTPS by default.
- **Evidence**: `COHERE_API_KEY` in `.env`, validated at startup; error handling wraps Cohere exceptions in generic messages.

### ✅ Performance & Scalability Standards
- **Status**: PASS
- **Rationale**: Cohere API latency comparable to Gemini; rate limits increased (20-500 req/min vs. current 10 req/min cap). Timeout handling preserved (30s). Native SDK reduces abstraction overhead.
- **Evidence**: `request_timeout_seconds` enforced via `asyncio.wait_for()`; client-level timeout configured; rate limiting via `slowapi` unchanged.

### ✅ Open Source & Reproducibility
- **Status**: PASS
- **Rationale**: Migration documented in detail with quickstart guide, dependency updates, and rollback plan. All code changes tracked in version control.
- **Evidence**: `quickstart.md` provides step-by-step setup; `.env.example` updated; `pyproject.toml` dependencies explicit.

---

## Project Structure

### Documentation (this feature)

```text
specs/010-replace-gemini-cohere/
├── spec.md              # Feature requirements and acceptance criteria
├── plan.md              # This file (architectural plan)
├── research.md          # Cohere API research findings
├── data-model.md        # Data structures and models analysis
├── quickstart.md        # Developer setup guide
├── contracts/
│   └── chat-api.yaml    # OpenAPI contract for /chat endpoint
└── tasks.md             # NOT created by /sp.plan (created by /sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── backend/
│   │   ├── main.py               # FastAPI app (health check updated)
│   │   ├── agent.py              # AITutor class (REWRITTEN)
│   │   ├── models.py             # ChatRequest/ChatResponse (unchanged)
│   │   ├── exceptions.py         # AIServiceError/EmptyAIResponse (unchanged)
│   │   └── config.py             # Settings (Gemini → Cohere config)
│   ├── config/
│   │   ├── settings.py           # Settings (Gemini → Cohere config)
│   │   └── database.py           # Database config (unchanged)
│   ├── auth/                     # Authentication (unchanged)
│   │   ├── routes/
│   │   ├── models/
│   │   └── middleware/
│   └── tools/                    # Textbook search tool (unchanged)
│       └── textbook_search_tool.py
├── tests/                        # Tests (to be updated)
│   ├── unit/
│   └── integration/
├── pyproject.toml                # Dependencies (agents/gemini → cohere)
└── .env                          # Environment variables (GEMINI → COHERE)

frontend/                         # NO CHANGES
docs/                             # NO CHANGES
.specify/                         # NO CHANGES
```

**Structure Decision**: Web application (backend + frontend separation). This feature modifies **backend only**, specifically the AI provider layer in `backend/src/backend/agent.py`. All other components remain unchanged to maintain backward compatibility.

---

## Complexity Tracking

> **No violations detected** - all constitution gates passed without exceptions.

---

## Architecture Decisions

### ADR-001: Use Native Cohere SDK Instead of OpenAI Compatibility Layer

**Decision**: Use `cohere.AsyncClientV2` (native Cohere Python SDK) instead of Cohere's OpenAI compatibility API.

**Context**:
- Current implementation uses `openai-agents` framework with `AsyncOpenAI` client pointing to Gemini's OpenAI-compatible endpoint
- Cohere offers two integration paths:
  1. **OpenAI Compatibility API** (`base_url="https://api.cohere.ai/compatibility/v1"`)
  2. **Native Cohere SDK** (`cohere.AsyncClientV2`)

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| **OpenAI Compatibility API** | Minimal code changes; familiar OpenAI interface; works with existing `openai-agents` | Adds abstraction layer; limits access to Cohere-specific features; indirect API access |
| **Native Cohere SDK** ✅ | Direct API access; full feature support; simpler architecture; better error handling; fewer dependencies | Requires rewriting `agent.py`; removes `openai-agents` framework |

**Decision Rationale**:
1. **Spec requirement**: "Remove Gemini completely" includes removing Gemini-specific wrappers (`openai-agents`)
2. **Simpler architecture**: Eliminates 2 abstraction layers (Agent, Runner, OpenAIChatCompletionsModel)
3. **Better performance**: Direct API calls without wrapper overhead; reduced latency
4. **Full feature access**: No limitations from OpenAI compatibility layer; access to Cohere tool use, streaming, and advanced parameters
5. **Easier maintenance**: Fewer dependencies (remove 2, add 1); clearer error paths; official SDK support
6. **Future-proofing**: Native SDK gets new features first; less risk of compatibility issues

**Consequences**:
- **Positive**: Cleaner codebase, fewer dependencies, direct error handling, better performance
- **Negative**: More extensive code changes in `agent.py` (full rewrite vs. configuration change)
- **Mitigation**: Comprehensive quickstart guide and rollback plan provided

**Implementation**:
```python
# Before (Gemini via agents framework)
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

gemini_client = AsyncOpenAI(api_key=settings.gemini_api_key, base_url=settings.gemini_base_url)
model = OpenAIChatCompletionsModel(model=settings.gemini_model, openai_client=gemini_client)
self.agent = Agent(name="Educational Tutor", instructions=constitution, model=model)

result = await Runner.run(starting_agent=self.agent, input=message)
content = result.final_output

# After (Native Cohere)
import cohere

self.client = cohere.AsyncClientV2(api_key=settings.cohere_api_key, timeout=30.0)

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

---

### ADR-002: Select `command-r-plus-08-2024` as Default Model

**Decision**: Use `command-r-plus-08-2024` as the default Cohere model for educational tutoring.

**Context**:
- Cohere offers multiple chat models with different capabilities and performance characteristics
- Educational tutoring requires conversational quality, reasoning ability, and reasonable response times

**Options Considered**:

| Model | Context Length | Performance | Use Case | Cost |
|-------|----------------|-------------|----------|------|
| `command-r` | 128k tokens | Fast, good quality | Multilingual, coding | Standard |
| **`command-r-plus-08-2024`** ✅ | 128k tokens | Fast, high quality | **Conversational AI, tutoring** | Standard |
| `command-a-03-2025` | 256k tokens | Slower, highest quality | Advanced reasoning, complex questions | Premium |

**Decision Rationale**:
1. **Strong conversational capabilities**: Optimized for dialogue and educational interactions
2. **Balanced speed/quality**: Suitable for real-time chat responses (<5s typical latency)
3. **Sufficient context**: 128k tokens handles large constitution + user query + conversation history
4. **Cost-effective**: Standard pricing tier; production keys offer 500 req/min
5. **Well-tested**: Stable production model with proven reliability

**When to Upgrade to `command-a-03-2025`**:
- Advanced physics/robotics reasoning required (e.g., kinematic calculations)
- Need to process entire textbook chapters in context (>128k tokens)
- Tool use integration for textbook search (future enhancement)

**Consequences**:
- **Positive**: High-quality responses, reasonable latency, cost-effective
- **Negative**: Advanced reasoning scenarios may require upgrade; 128k context limit
- **Mitigation**: Model can be changed via `COHERE_MODEL` environment variable without code changes

**Configuration**:
```python
# settings.py
cohere_model: str = "command-r-plus-08-2024"

# .env
COHERE_MODEL=command-r-plus-08-2024

# Can be overridden without code changes:
# COHERE_MODEL=command-a-03-2025
```

---

### ADR-003: Use `developer` Role for Constitution (System Prompt)

**Decision**: Pass Global Constitution as a message with `role="developer"` instead of using a separate system/instructions field.

**Context**:
- Gemini integration used `Agent(instructions=constitution)` to set system prompt
- Cohere Chat API uses messages-based format with roles: `user`, `assistant`, `developer`
- `developer` role is Cohere's equivalent to OpenAI's `system` role for instructions

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| **`developer` role in messages** ✅ | Official Cohere pattern; behaves like system prompt; clear intent | Adds message to context (uses tokens) |
| Include constitution in first user message | Simpler message structure | Mixes user content with instructions; less semantic clarity |
| Prepend to every user message | No dedicated role needed | Wasteful (repeats constitution); increases token usage |

**Decision Rationale**:
1. **Official Cohere pattern**: `developer` role documented as system instruction mechanism
2. **Semantic clarity**: Separates instructions from user input
3. **Consistent behavior**: Mirrors OpenAI `system` role and Gemini `instructions` field
4. **Token efficiency**: Constitution sent once per request, not concatenated to every message

**Implementation**:
```python
messages = [
    {
        "role": "developer",  # System instructions
        "content": self.constitution  # Global Constitution text
    },
    {
        "role": "user",  # User input
        "content": message
    }
]

response = await self.client.chat(model=self.model, messages=messages)
```

**Consequences**:
- **Positive**: Clear separation of concerns; follows Cohere best practices
- **Negative**: Constitution counts toward context limit (typically <5k tokens, well within 128k limit)
- **Mitigation**: Constitution size optimized; 128k context sufficient for constitution + conversation

---

### ADR-004: Maintain Identical API Contract (Zero Breaking Changes)

**Decision**: Preserve exact `/chat` endpoint request/response format, status codes, and error messages.

**Context**:
- Spec requirement: "Do not change routes, database, auth, or frontend. Only replace AI provider layer."
- Frontend chat interface expects specific JSON format
- Existing tests validate current API contract

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| **Preserve exact contract** ✅ | Zero frontend changes; existing tests pass; backward compatible | Cannot add new features to response (e.g., model metadata) |
| Add `model` field to ChatResponse | Transparency (frontend knows which model) | Breaking change; requires frontend update |
| Change endpoint to `/chat/cohere` | Clear API versioning | Violates spec; requires route changes and frontend update |

**Decision Rationale**:
1. **Spec compliance**: Explicit requirement to avoid frontend changes
2. **Backward compatibility**: Existing frontend, tests, and integrations continue working
3. **Deployment simplicity**: Zero-downtime migration possible (swap backend, frontend unaware)
4. **Principle of Least Surprise**: Users expect same interface; internal changes invisible

**Contract Definition**:

**Request** (`ChatRequest`):
```json
{
  "message": "What is physical AI?"
}
```

**Response** (`ChatResponse`):
```json
{
  "response": "Physical AI combines artificial intelligence...",
  "agent_name": "AI Tutor"
}
```

**Status Codes**:
- `200`: Successful response
- `422`: Validation error (invalid request format)
- `429`: Rate limit exceeded
- `500`: Internal server error (AI service failure)
- `504`: Request timeout

**Consequences**:
- **Positive**: Zero frontend impact; seamless migration; no breaking changes
- **Negative**: Cannot expose Cohere-specific metadata without API versioning
- **Mitigation**: Future enhancements can use API versioning (e.g., `/v2/chat`) if needed

**Validation**:
```python
# Unchanged request model
class ChatRequest(BaseModel):
    message: str

# Unchanged response model
class ChatResponse(BaseModel):
    response: str
    agent_name: str

# Endpoint signature unchanged
@app.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, chat_request: ChatRequest):
    # ... implementation changes internally ...
    return ChatResponse(response=response_text, agent_name="AI Tutor")
```

---

### ADR-005: Two-Layer Timeout Strategy (Client + asyncio)

**Decision**: Configure timeout at both Cohere client level and request level using `asyncio.wait_for()`.

**Context**:
- Current implementation uses `asyncio.wait_for()` with 30-second timeout
- Cohere SDK supports client-level timeout configuration
- Need defense-in-depth against hung requests

**Options Considered**:

| Option | Pros | Cons |
|--------|------|------|
| Client timeout only | Single configuration point | Doesn't handle processing delays after API response |
| asyncio timeout only | Handles end-to-end request time | Doesn't prevent network-level hangs |
| **Both client + asyncio** ✅ | Defense in depth; handles all timeout scenarios | Redundant configuration (both set to 30s) |

**Decision Rationale**:
1. **Defense in depth**: Two independent timeout mechanisms prevent all hang scenarios
2. **Client timeout**: Prevents network-level hangs (connection, read, write)
3. **asyncio timeout**: Ensures overall request completes within expected time
4. **User experience**: Guaranteed response or error within 30 seconds
5. **Consistency**: Matches existing Gemini timeout behavior

**Implementation**:
```python
# Client-level timeout (network operations)
self.client = cohere.AsyncClientV2(
    api_key=settings.cohere_api_key,
    timeout=float(settings.request_timeout_seconds)  # 30.0 seconds
)

# Request-level timeout (overall operation)
response = await asyncio.wait_for(
    self.client.chat(...),
    timeout=settings.request_timeout_seconds  # 30 seconds
)

# Error handling
try:
    response = await asyncio.wait_for(...)
except asyncio.TimeoutError:
    raise AIServiceError(f"Request timed out after {settings.request_timeout_seconds} seconds")
```

**Timeout Hierarchy**:
1. **Cohere client timeout** (30s): Network/read timeout for HTTP requests
2. **asyncio.wait_for timeout** (30s): Overall request timeout including processing
3. **FastAPI request timeout**: No explicit limit (handled by client/asyncio layers)

**Consequences**:
- **Positive**: No hung requests; guaranteed timeout; clear error messages
- **Negative**: Redundant configuration (both timeouts set to same value)
- **Mitigation**: Settings centralized in `request_timeout_seconds`; easy to adjust

---

## Phase 0: Research Findings

**Status**: ✅ Complete

**Output**: [research.md](./research.md)

### Key Findings Summary

1. **Cohere Python SDK**: Official package `cohere>=5.0.0` with `AsyncClientV2` for async FastAPI
2. **Chat API Pattern**: Non-streaming async chat with `developer` role for system instructions
3. **Error Handling**: Specific exceptions (UnauthorizedError, RateLimitError, BadRequestError, ServiceUnavailableError) mapped to custom errors
4. **Agent Framework**: Remove `openai-agents`; use native Cohere SDK for simpler architecture
5. **Model Selection**: `command-r-plus-08-2024` recommended for educational tutoring
6. **Configuration**: Replace `gemini_*` with `cohere_*` settings (2 fields: API key + model)
7. **Rate Limiting**: Keep 10 req/min; well below Cohere limits (20-500 req/min)
8. **Timeout Strategy**: Client-level (30s) + asyncio.wait_for (30s) for defense in depth
9. **Backward Compatibility**: Maintain identical ChatRequest/ChatResponse format
10. **Dependencies**: Remove 2 packages (openai-agents, google-generativeai), add 1 (cohere)

**All unknowns resolved** - ready for implementation.

---

## Phase 1: Design Artifacts

**Status**: ✅ Complete

### Data Model

**Output**: [data-model.md](./data-model.md)

**Summary**: No data model changes required. This is a provider replacement with:
- ✅ ChatRequest, ChatResponse, ErrorResponse models unchanged
- ✅ Database schema unchanged (no migrations)
- ⚠️ Settings class updated (gemini_* → cohere_* fields)
- 🔄 AITutor class refactored (remove Agent wrapper, use AsyncClientV2)

### API Contracts

**Output**: [contracts/chat-api.yaml](./contracts/chat-api.yaml)

**Summary**: OpenAPI 3.0 specification for `/chat` and `/health` endpoints documenting:
- POST `/chat` - Request: `{message: string}`, Response: `{response: string, agent_name: string}`
- GET `/health` - Response: `{status: string, constitution_loaded: boolean, model: string, rate_limit: string}`
- Status codes: 200, 422, 429, 500, 504
- Rate limiting: 10 req/min per IP
- Timeout: 30 seconds

**Contract Stability**: No breaking changes; frontend requires zero modifications.

### Quickstart Guide

**Output**: [quickstart.md](./quickstart.md)

**Summary**: Step-by-step developer guide covering:
1. Prerequisites (Cohere API key, Python 3.9+)
2. Dependency updates (uninstall agents/gemini, install cohere)
3. Configuration changes (settings.py, config.py, .env)
4. agent.py rewrite (complete code listing)
5. Health check update (1 line in main.py)
6. Testing procedures (health, chat, error handling, rate limiting)
7. Troubleshooting (common issues and solutions)
8. Rollback plan (restore previous version)

---

## Implementation Checklist

### Dependencies & Configuration

- [ ] Update `backend/pyproject.toml`: Remove `openai-agents>=0.6.0`, `google-generativeai>=0.8.0`; Add `cohere>=5.0.0`
- [ ] Run `pip uninstall openai-agents google-generativeai -y && pip install cohere`
- [ ] Update `backend/src/config/settings.py`: Replace `gemini_*` fields with `cohere_*`
- [ ] Update `backend/src/backend/config.py`: Replace `gemini_*` fields with `cohere_*`
- [ ] Update `backend/.env`: Remove `GEMINI_*` vars, add `COHERE_API_KEY`, `COHERE_MODEL`

### Code Changes

- [ ] Backup `backend/src/backend/agent.py` to `agent.py.backup`
- [ ] Rewrite `backend/src/backend/agent.py` with native Cohere SDK
  - [ ] Replace imports: `from agents import ...` → `import cohere`
  - [ ] Replace `AsyncOpenAI` → `cohere.AsyncClientV2`
  - [ ] Remove `Agent`, `Runner`, `OpenAIChatCompletionsModel`
  - [ ] Update `generate_response()` to use `client.chat(messages=[...])`
  - [ ] Add Cohere-specific error handling (UnauthorizedError, RateLimitError, etc.)
- [ ] Update `backend/src/backend/main.py` health check: `settings.gemini_model` → `settings.cohere_model`

### Testing

- [ ] Start backend: `uvicorn backend.main:app --reload`
- [ ] Verify startup message shows "Cohere model: command-r-plus-08-2024"
- [ ] Test health check: `curl http://localhost:8000/health` → verify `model` field
- [ ] Test chat endpoint: `curl -X POST http://localhost:8000/chat -d '{"message":"What is physical AI?"}'`
- [ ] Test error handling: Invalid API key → 500 error
- [ ] Test rate limiting: 11 rapid requests → 11th returns 429 error
- [ ] Test timeout: (simulated by network delay or complex question) → 504 error

### Validation

- [ ] No Gemini references: `grep -r "gemini" backend/src/` returns only comments
- [ ] No agents imports: `grep -r "from agents import" backend/src/` returns nothing
- [ ] Cohere installed: `pip list | grep cohere` shows cohere>=5.0.0
- [ ] Frontend unchanged: No modifications to frontend files
- [ ] Database unchanged: No schema changes or migrations
- [ ] Auth unchanged: No changes to authentication system

---

## Risk Assessment & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Cohere API key invalid/missing** | Low | High | Validate at startup in `AITutor.__init__()`; fail fast with clear error |
| **Response quality different from Gemini** | Medium | Medium | Test with sample questions; tune temperature/max_tokens; use constitution for consistency |
| **Cohere rate limits too restrictive** | Low | Low | Trial keys: 20 req/min; Production: 500 req/min; Current limit: 10 req/min (well below) |
| **Constitution too long for context** | Low | Low | Constitution <5k tokens; Cohere supports 128k context; trim if needed |
| **Cohere service downtime** | Low | Medium | Implement fallback message (already exists); monitor Cohere status page |
| **Breaking changes in Cohere SDK** | Low | Medium | Pin to major version (`cohere>=5.0.0`); test before upgrading minor versions |
| **Timeout issues with complex questions** | Medium | Low | Two-layer timeout (client + asyncio); 30s sufficient; increase if needed |
| **Rollback needed due to issues** | Low | High | Backup agent.py; document rollback steps; keep Gemini credentials temporarily |

---

## Deployment Plan

### Pre-Deployment

1. **Backup current code**: `git commit -m "Pre-Cohere migration checkpoint"`
2. **Obtain Cohere API key**: Sign up at dashboard.cohere.com; generate production key
3. **Test in development**: Complete all testing checklist items
4. **Measure baseline**: Record Gemini response times for comparison

### Deployment Steps

1. **Update dependencies**: `pip install cohere && pip uninstall openai-agents google-generativeai -y`
2. **Deploy code changes**: Push to production server
3. **Update .env**: Add `COHERE_API_KEY` and `COHERE_MODEL`
4. **Restart backend**: `systemctl restart backend` or equivalent
5. **Verify health check**: `curl https://api.yourdomain.com/health` → check `model` field
6. **Monitor logs**: Watch for errors or unexpected behavior
7. **Test chat endpoint**: Send test queries, verify responses

### Post-Deployment

1. **Monitor usage**: Track Cohere API usage in dashboard
2. **Compare metrics**: Response times, error rates vs. Gemini baseline
3. **Collect feedback**: User experience with new AI provider
4. **Tune parameters**: Adjust temperature, max_tokens if needed
5. **Remove Gemini credentials**: After 1 week of stable operation

### Rollback Procedure

If critical issues arise:

1. **Restore code**: `git revert <commit>` or restore `agent.py.backup`
2. **Restore dependencies**: `pip install openai-agents google-generativeai && pip uninstall cohere -y`
3. **Restore .env**: Replace `COHERE_*` with `GEMINI_*` variables
4. **Restart backend**: Apply previous version
5. **Verify**: Health check shows `gemini-2.0-flash`

---

## Success Metrics

### Functional Metrics

- ✅ All chat requests generate responses from Cohere API (verify via logs)
- ✅ Application startup succeeds with Cohere client initialization (<5 seconds)
- ✅ Zero breaking changes to frontend (existing chat interface works without modification)
- ✅ Health check endpoint reports `command-r-plus-08-2024`
- ✅ Error handling maintains existing user experience (500 errors for AI failures)
- ✅ No Gemini-related code remains (verified by `grep -r gemini backend/src/`)
- ✅ Environment variables updated (no `GEMINI_*` references)

### Performance Metrics

- ✅ Chat response times comparable to Gemini (within 10% variance)
- ✅ Health check responds in <200ms (p95)
- ✅ No requests timeout before 30s threshold
- ✅ Rate limiting enforced (10 req/min)
- ✅ Startup time <5 seconds

### Quality Metrics

- ✅ Responses relevant to Physical AI and Humanoid Robotics
- ✅ Constitution instructions followed (educational tone, accurate content)
- ✅ Error messages clear and actionable
- ✅ No empty or malformed responses

---

## Follow-Up Tasks

### Immediate (Post-Migration)

1. Update `.env.example` with Cohere configuration template
2. Update README.md with Cohere setup instructions
3. Archive Gemini credentials securely (for rollback if needed)
4. Document any parameter tuning (temperature, max_tokens) in ADR

### Short-Term (1-2 weeks)

1. Collect user feedback on response quality
2. Compare Cohere costs vs. Gemini costs
3. Monitor error rates and timeout frequency
4. Tune temperature/max_tokens based on feedback

### Long-Term (Future Enhancements)

1. Implement Cohere tool use for textbook search integration
2. Explore `command-a-03-2025` for advanced reasoning scenarios
3. Add response caching for common questions
4. Implement streaming responses for real-time chat experience

---

## Architectural Decision Records

All significant decisions documented as ADRs above:

- **ADR-001**: Use Native Cohere SDK Instead of OpenAI Compatibility Layer
- **ADR-002**: Select `command-r-plus-08-2024` as Default Model
- **ADR-003**: Use `developer` Role for Constitution (System Prompt)
- **ADR-004**: Maintain Identical API Contract (Zero Breaking Changes)
- **ADR-005**: Two-Layer Timeout Strategy (Client + asyncio)

**Note**: Per workflow requirement, `/sp.adr` command should be run manually to create formal ADR files in `history/adr/` for any of these decisions deemed architecturally significant.

---

## Conclusion

This plan provides a comprehensive architectural blueprint for migrating from Gemini to Cohere API. The migration is **low-risk, high-value** because:

1. **Isolated scope**: Backend-only changes; no frontend, database, or auth modifications
2. **Clear architecture**: Native SDK integration simpler than agents framework
3. **Backward compatible**: API contract preserved; zero breaking changes
4. **Well-researched**: All unknowns resolved in Phase 0 research
5. **Documented**: Quickstart guide enables confident implementation
6. **Testable**: Clear testing procedures and success metrics
7. **Reversible**: Rollback plan documented for risk mitigation

**Ready for `/sp.tasks` command** to generate testable implementation tasks.

---

**Plan Status**: ✅ Complete
**Phase 0 (Research)**: ✅ Complete
**Phase 1 (Design)**: ✅ Complete
**Phase 2 (Tasks)**: ⏭️ Run `/sp.tasks` command to generate tasks.md
