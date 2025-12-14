# Feature Specification: Migrate to OpenAIChatCompletionsModel

**Feature Branch**: `002-openai-chat-completions-migration`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "Instead of litellm i want to use OpenAIChatCompletionsModel configured with gemini (gemini-2.0-flash). Rest things should be same."

## Clarifications

### Session 2025-12-14

- Q: Should the API behavior (request/response format) remain exactly the same from the client's perspective? → A: Yes, this is an internal implementation change only
- Q: Should we keep the same error handling behavior (EmptyAIResponse, AIServiceError, timeout handling)? → A: Yes, all error handling must remain identical
- Q: Should configuration (GEMINI_API_KEY, model name, timeout) use the same environment variables? → A: Yes, maintain backward compatibility with existing configuration
- Q: Do we need to maintain the same constitution loading mechanism? → A: Yes, system prompt injection must work identically

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Transparent Model Migration (Priority: P1)

Backend developers need to migrate from direct AsyncOpenAI client usage to OpenAIChatCompletionsModel abstraction for better SDK integration and future flexibility, without changing any external API behavior or breaking existing clients.

**Why this priority**: This is the core requirement - replacing the underlying AI client implementation while maintaining identical behavior. It's the foundation for future SDK-based features and agent orchestration capabilities.

**Independent Test**: Can be fully tested by running the existing test suite (backend/tests/) and verifying all tests pass without modification. Send the same POST /chat requests and verify identical response format and behavior.

**Acceptance Scenarios**:

1. **Given** the chat service is running with OpenAIChatCompletionsModel, **When** a student submits "What is Physical AI?", **Then** the response format and content quality are identical to the previous AsyncOpenAI implementation
2. **Given** the migration is complete, **When** the existing test suite (test_agent.py, test_chat_endpoint.py) runs, **Then** all tests pass without any modifications
3. **Given** the new implementation, **When** error scenarios occur (timeout, empty response, API errors), **Then** the same exceptions (EmptyAIResponse, AIServiceError) are raised with identical messages

---

### User Story 2 - Configuration Compatibility (Priority: P2)

DevOps engineers and developers need the migration to maintain backward compatibility with existing environment configuration, so deployment scripts and documentation don't need updates.

**Why this priority**: Ensures smooth deployment and operations continuity. No infrastructure changes or documentation updates required, reducing migration risk.

**Independent Test**: Can be fully tested by using the existing .env configuration file and verifying the service starts successfully and processes requests using the same environment variables (GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL, REQUEST_TIMEOUT_SECONDS).

**Acceptance Scenarios**:

1. **Given** an existing .env file with GEMINI_API_KEY, GEMINI_BASE_URL, and GEMINI_MODEL, **When** the service starts with OpenAIChatCompletionsModel, **Then** it reads configuration from the same environment variables
2. **Given** the migrated implementation, **When** the service initializes, **Then** the Global Constitution is loaded from the same path (../.specify/memory/constitution.md) and used as the system prompt
3. **Given** existing timeout settings (REQUEST_TIMEOUT_SECONDS=30), **When** requests are processed, **Then** the same timeout behavior is enforced

---

### User Story 3 - Dependency Simplification (Priority: P3)

Backend developers need to replace the openai package dependency with the agents-sdk package, enabling future agent orchestration features while reducing dependency footprint.

**Why this priority**: Sets the foundation for future agent-based features. While important for long-term architecture, it's not blocking core functionality.

**Independent Test**: Can be fully tested by verifying pyproject.toml dependencies (openai removed, agents-sdk added) and running `uv sync` successfully, followed by the full test suite passing.

**Acceptance Scenarios**:

1. **Given** the migrated codebase, **When** reviewing pyproject.toml dependencies, **Then** the openai package is removed and agents-sdk is added
2. **Given** the new dependencies, **When** running `uv sync`, **Then** all dependencies install successfully without conflicts
3. **Given** the agents-sdk integration, **When** future agent features are needed, **Then** the foundation is in place to use Runner, Swarm, and other SDK capabilities

---

### Edge Cases

- What happens when OpenAIChatCompletionsModel initialization fails due to invalid API key?
- How does the system handle Gemini API rate limiting or quota exceeded errors?
- What happens if the agents-sdk package version conflicts with other dependencies?
- How does error message formatting differ between AsyncOpenAI and OpenAIChatCompletionsModel (if at all)?
- What happens when the model name format differs between direct OpenAI client and Gemini configuration?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace AsyncOpenAI client with OpenAIChatCompletionsModel configured for Gemini 2.0 Flash (gemini-2.0-flash)
- **FR-002**: System MUST maintain identical request/response behavior - POST /chat endpoints return the same JSON structure
- **FR-003**: System MUST preserve all error handling - EmptyAIResponse, AIServiceError, timeout errors must raise in identical scenarios
- **FR-004**: System MUST continue reading GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL, and REQUEST_TIMEOUT_SECONDS from environment variables
- **FR-005**: System MUST load the Global Constitution from ../.specify/memory/constitution.md and inject it as the system prompt
- **FR-006**: System MUST apply the same 30-second timeout to AI requests using the new model
- **FR-007**: System MUST detect empty/whitespace-only responses and raise EmptyAIResponse
- **FR-008**: System MUST pass all existing unit tests (test_agent.py, test_chat_endpoint.py, test_validation.py, test_config.py) without modification
- **FR-009**: System MUST replace the openai package dependency with agents-sdk in pyproject.toml
- **FR-010**: System MUST maintain the same initialization pattern - initialize_agent() and get_agent() for FastAPI dependency injection
- **FR-011**: System MUST preserve the AITutor class interface - generate_response(message: str) returns str
- **FR-012**: System MUST handle OpenAI-compatible error formats from Gemini API

### Key Entities

- **OpenAIChatCompletionsModel**: Replaces AsyncOpenAI client; configured with Gemini base_url, api_key, and model name
- **AITutor**: Maintains same interface; internally uses OpenAIChatCompletionsModel instead of AsyncOpenAI
- **SystemPrompt**: Global Constitution content; injected into model configuration or passed with each request

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All existing tests pass without modification (100% test compatibility)
- **SC-002**: POST /chat endpoint returns identical response structure (ChatResponse with "response" field)
- **SC-003**: Service startup time remains under 5 seconds with new model
- **SC-004**: Response generation time for valid questions remains under 10 seconds
- **SC-005**: Error handling behavior is identical - same exception types, same error messages for equivalent scenarios
- **SC-006**: Configuration loading succeeds using existing .env files without changes
- **SC-007**: pyproject.toml contains agents-sdk dependency instead of openai package
- **SC-008**: Manual testing with "What is Physical AI?" returns educationally appropriate response (quality unchanged)

### Assumptions

- The OpenAIChatCompletionsModel from agents-sdk supports Gemini 2.0 Flash via base_url configuration
- The agents-sdk package provides OpenAI-compatible completion interfaces
- Gemini API errors map cleanly to exceptions that can be caught and wrapped in AIServiceError
- The system prompt can be injected into OpenAIChatCompletionsModel (either via model config or per-request messages)
- The agents-sdk package is compatible with Python 3.13 and FastAPI async patterns
- Existing rate limiting, validation, and FastAPI endpoint logic remain unchanged (only agent.py changes)
- The migration does not require changes to frontend or API contracts
- Documentation for OpenAIChatCompletionsModel is available via Context7 MCP server or agents-sdk repository

### Non-Functional Requirements

- **NFR-001**: Migration must not introduce performance degradation (response times within 10% of baseline)
- **NFR-002**: Code changes should be minimal - ideally localized to backend/src/backend/agent.py and pyproject.toml
- **NFR-003**: Error messages must remain clear and user-friendly (maintain existing error message quality)
- **NFR-004**: The migration should not require database schema changes, API version bumps, or frontend updates

## Out of Scope

- Adding new agent orchestration features (Runner, Swarm) - this migration only replaces the model client
- Changing the Global Constitution loading mechanism or content
- Modifying rate limiting, validation, or endpoint routing logic
- Updating frontend chatbot UI or API contracts
- Adding new error types or changing error handling patterns beyond what's needed for compatibility
- Implementing streaming responses (maintain existing non-streaming behavior)
- Changing configuration variable names or structure
- Adding observability/logging beyond existing patterns

## Migration Risks

- **Risk 1**: OpenAIChatCompletionsModel API differs from AsyncOpenAI in subtle ways (e.g., error formats, response structure)
  - **Mitigation**: Thorough testing with existing test suite; add compatibility layer if needed
- **Risk 2**: agents-sdk dependency conflicts with existing packages (FastAPI, Pydantic)
  - **Mitigation**: Test `uv sync` early; check version compatibility before full implementation
- **Risk 3**: System prompt injection pattern differs between AsyncOpenAI and OpenAIChatCompletionsModel
  - **Mitigation**: Research agents-sdk documentation; verify system message handling in tests
- **Risk 4**: Gemini API error responses may not be handled identically by the new client
  - **Mitigation**: Test error scenarios explicitly (timeout, empty response, API errors)

## Acceptance Criteria

**The migration is complete when:**

1. ✅ pyproject.toml lists agents-sdk instead of openai in dependencies
2. ✅ backend/src/backend/agent.py uses OpenAIChatCompletionsModel instead of AsyncOpenAI
3. ✅ All existing tests pass: `pytest backend/tests/` shows 100% pass rate
4. ✅ Manual test: POST /chat with "What is Physical AI?" returns 200 OK with educational response
5. ✅ Error scenarios work: Empty response raises EmptyAIResponse, timeout raises AIServiceError
6. ✅ Configuration loads from existing .env file without changes
7. ✅ Service starts within 5 seconds and /health endpoint returns constitution_loaded: true
8. ✅ Code review confirms: minimal changes, only agent.py and pyproject.toml modified (plus any necessary test adjustments for mock compatibility)

---

**Next Steps After Approval:**

1. Run `/sp.plan` to create implementation plan with architectural decisions
2. Run `/sp.tasks` to generate TDD task breakdown
3. Execute migration following red-green-refactor cycle
4. Validate with full test suite and manual testing
5. Create Prompt History Record (PHR) documenting the migration
