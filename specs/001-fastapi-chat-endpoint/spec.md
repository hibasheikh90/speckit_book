# Feature Specification: Backend Chat Communication Service with OpenAIChatCompletionsModel

**Feature Branch**: `001-fastapi-chat-endpoint`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "Create a backend service that enables the frontend Chatbot UI to communicate with an AI agent. The agent must provide educational responses about Physical AI and Humanoid Robotics, guided by the project's Global Constitution principles. Instead of litellm i want to use OpenAIChatCompletionsModel configured with gemini (gemini-2.0-flash). Rest things should be same."

## Clarifications

### Session 2025-12-14

- Q: What should the system do when the AI service returns an empty or unusable response to a valid student question? → A: Return a friendly error message and suggest rephrasing or trying again later
- Q: What is the minimum character length for a valid question? → A: 3 characters minimum
- Q: What is the maximum wait time before a student request times out? → A: 30 seconds total timeout
- Q: How should the system handle the order of concurrent requests from the same student? → A: Process independently, responses may arrive out of order
- Q: Should the system enforce rate limiting to prevent abuse? → A: Yes, 10 requests per minute per student
- Q: Should the API behavior (request/response format) remain exactly the same from the client's perspective? → A: Yes, this is an internal implementation change only
- Q: Should we keep the same error handling behavior (EmptyAIResponse, AIServiceError, timeout handling)? → A: Yes, all error handling must remain identical
- Q: Should configuration (GEMINI_API_KEY, model name, timeout) use the same environment variables? → A: Yes, maintain backward compatibility with existing configuration
- Q: Do we need to maintain the same constitution loading mechanism? → A: Yes, system prompt injection must work identically

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Question-Answer Interaction (Priority: P1)

Students using the Physical AI textbook need to ask questions about course content and receive intelligent, educationally-focused responses that align with their learning journey.

**Why this priority**: This is the fundamental capability that enables interactive learning. Without this working, students cannot engage with the AI tutor, which is a core value proposition of the textbook platform. It represents the minimum viable product (MVP) for the chat service.

**Independent Test**: Can be fully tested by submitting a learning question (e.g., "What is Physical AI?") and verifying that a relevant, educational response is returned. Delivers immediate value by enabling students to get answers to questions about robotics and AI concepts.

**Acceptance Scenarios**:

1. **Given** the chat service is available, **When** a student submits the question "What is Physical AI?", **Then** an educational response is provided that explains the concept clearly
2. **Given** the chat service is available, **When** a student asks about a specific topic like "Explain ROS 2 nodes", **Then** the response demonstrates educational-first design (accessible language, progressive difficulty, practical examples)
3. **Given** the AI tutor is initialized with educational principles, **When** any learning question is submitted, **Then** the response reflects core pedagogical values (clarity, accessibility, practical context)

---

### User Story 2 - Input Quality Feedback (Priority: P2)

Frontend developers integrating the chat UI need clear feedback when user input doesn't meet requirements, so they can guide students to submit valid questions.

**Why this priority**: Proper input handling ensures good user experience and prevents system errors. It's essential for production but doesn't block initial learning interaction testing.

**Independent Test**: Can be fully tested by submitting various invalid inputs (empty questions, excessively long text) and verifying clear error feedback is provided. Delivers value by ensuring students understand input requirements.

**Acceptance Scenarios**:

1. **Given** the chat service is available, **When** an empty question is submitted, **Then** clear validation feedback is provided explaining that a question is required
2. **Given** the chat service is available, **When** a question with fewer than 3 characters is submitted, **Then** validation feedback indicates the question is too short and must be at least 3 characters
3. **Given** the chat service is available, **When** an excessively long question (over 10,000 characters) is submitted, **Then** feedback indicates the question exceeds the maximum length and suggests summarizing

---

### User Story 3 - Service Availability Transparency (Priority: P3)

Students and frontend developers need to understand when the AI tutor service is experiencing issues, so they can either retry later or understand the service status.

**Why this priority**: Graceful error handling is essential for production quality but can be implemented after core functionality is proven. It ensures professional service quality but doesn't block initial integration.

**Independent Test**: Can be fully tested by simulating various service failures (AI service unavailable, configuration errors) and verifying that informative error messages are provided instead of silent failures. Delivers value by maintaining user trust through transparency.

**Acceptance Scenarios**:

1. **Given** the AI service credentials are missing or invalid, **When** a student submits a question, **Then** an error message explains that the tutor service is temporarily unavailable and suggests trying again later
2. **Given** the AI service is experiencing high load, **When** a question is submitted, **Then** an appropriate error message indicates the service is busy and to retry shortly
3. **Given** the service cannot connect to the AI provider, **When** a question is submitted, **Then** an error is returned within 30 seconds rather than hanging indefinitely

---

### User Story 4 - Transparent Model Migration (Priority: P1)

Backend developers need to migrate from direct AsyncOpenAI client usage to OpenAIChatCompletionsModel abstraction for better SDK integration and future flexibility, without changing any external API behavior or breaking existing clients.

**Why this priority**: This is the core requirement - replacing the underlying AI client implementation while maintaining identical behavior. It's the foundation for future SDK-based features and agent orchestration capabilities.

**Independent Test**: Can be fully tested by running the existing test suite (backend/tests/) and verifying all tests pass without modification. Send the same POST /chat requests and verify identical response format and behavior.

**Acceptance Scenarios**:

1. **Given** the chat service is running with OpenAIChatCompletionsModel, **When** a student submits "What is Physical AI?", **Then** the response format and content quality are identical to the previous AsyncOpenAI implementation
2. **Given** the migration is complete, **When** the existing test suite (test_agent.py, test_chat_endpoint.py) runs, **Then** all tests pass without any modifications
3. **Given** the new implementation, **When** error scenarios occur (timeout, empty response, API errors), **Then** the same exceptions (EmptyAIResponse, AIServiceError) are raised with identical messages

---

### User Story 5 - Configuration Compatibility (Priority: P2)

DevOps engineers and developers need the migration to maintain backward compatibility with existing environment configuration, so deployment scripts and documentation don't need updates.

**Why this priority**: Ensures smooth deployment and operations continuity. No infrastructure changes or documentation updates required, reducing migration risk.

**Independent Test**: Can be fully tested by using the existing .env configuration file and verifying the service starts successfully and processes requests using the same environment variables (GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL, REQUEST_TIMEOUT_SECONDS).

**Acceptance Scenarios**:

1. **Given** an existing .env file with GEMINI_API_KEY, GEMINI_BASE_URL, and GEMINI_MODEL, **When** the service starts with OpenAIChatCompletionsModel, **Then** it reads configuration from the same environment variables
2. **Given** the migrated implementation, **When** the service initializes, **Then** the Global Constitution is loaded from the same path (../.specify/memory/constitution.md) and used as the system prompt
3. **Given** existing timeout settings (REQUEST_TIMEOUT_SECONDS=30), **When** requests are processed, **Then** the same timeout behavior is enforced

---

### Edge Cases

- What happens when the question contains multiple languages or special characters?
- When the same student submits multiple questions concurrently, the system processes them independently and responses may arrive out of order
- What happens if the educational principles document is unavailable during initialization?
- How does the system respond to questions that are exactly at the character limit?
- When the AI service returns an empty or unusable response, the system returns a friendly error message suggesting the student rephrase the question or try again later
- What happens when OpenAIChatCompletionsModel initialization fails due to invalid API key?
- How does the system handle Gemini API rate limiting or quota exceeded errors?
- What happens if the agents-sdk package version conflicts with other dependencies?
- How does error message formatting differ between AsyncOpenAI and OpenAIChatCompletionsModel (if at all)?
- What happens when the model name format differs between direct OpenAI client and Gemini configuration?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept student questions in text format via a backend service interface
- **FR-002**: System MUST validate that submitted questions meet basic quality requirements (minimum 3 characters, maximum 10,000 characters)
- **FR-003**: System MUST initialize an AI tutor that uses the project's Global Constitution principles to guide all responses
- **FR-004**: System MUST send validated questions to the AI tutor and retrieve educational responses
- **FR-005**: System MUST return the AI tutor's response to the requesting frontend
- **FR-006**: System MUST provide clear validation feedback when questions don't meet quality requirements
- **FR-007**: System MUST provide informative error messages when the AI tutor service is unavailable or experiencing issues
- **FR-008**: System MUST enforce a 30-second maximum timeout for all student requests and return an error message if the AI service does not respond within this timeframe
- **FR-009**: System MUST detect when the AI service returns an empty or unusable response and provide a friendly error message suggesting the student rephrase the question or try again later
- **FR-010**: System MUST maintain educational quality by ensuring all AI responses are guided by the Global Constitution principles
- **FR-011**: System MUST be ready to accept questions within 5 seconds of startup
- **FR-012**: System MUST handle multiple concurrent students asking questions simultaneously, processing requests independently without ordering guarantees (responses may arrive out of order)
- **FR-013**: System MUST enforce rate limiting of 10 requests per minute per student and return clear feedback when the limit is exceeded
- **FR-014**: System MUST replace AsyncOpenAI client with OpenAIChatCompletionsModel configured for Gemini 2.0 Flash (gemini-2.0-flash)
- **FR-015**: System MUST maintain identical request/response behavior - POST /chat endpoints return the same JSON structure
- **FR-016**: System MUST preserve all error handling - EmptyAIResponse, AIServiceError, timeout errors must raise in identical scenarios
- **FR-017**: System MUST continue reading GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL, and REQUEST_TIMEOUT_SECONDS from environment variables
- **FR-018**: System MUST load the Global Constitution from ../.specify/memory/constitution.md and inject it as the system prompt
- **FR-019**: System MUST apply the same 30-second timeout to AI requests using the new model
- **FR-020**: System MUST detect empty/whitespace-only responses and raise EmptyAIResponse
- **FR-021**: System MUST pass all existing unit tests (test_agent.py, test_chat_endpoint.py, test_validation.py, test_config.py) without modification
- **FR-022**: System MUST replace the openai package dependency with agents-sdk in pyproject.toml
- **FR-023**: System MUST maintain the same initialization pattern - initialize_agent() and get_agent() for FastAPI dependency injection
- **FR-024**: System MUST preserve the AITutor class interface - generate_response(message: str) returns str

### Key Entities

- **StudentQuestion**: Represents incoming questions from students with quality validation constraints
- **TutorResponse**: Represents educational responses generated by the AI tutor
- **ValidationFeedback**: Represents feedback provided when input doesn't meet requirements
- **ServiceError**: Represents error conditions with informative messages for users
- **EducationalPrinciples**: Represents the Global Constitution that guides all AI tutor responses
- **OpenAIChatCompletionsModel**: Replaces AsyncOpenAI client; configured with Gemini base_url, api_key, and model name
- **AITutor**: Maintains same interface; internally uses OpenAIChatCompletionsModel instead of AsyncOpenAI
- **SystemPrompt**: Global Constitution content; injected into model configuration or passed with each request

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The chat service becomes available within 5 seconds of startup
- **SC-002**: Students receive responses to valid questions within 10 seconds under normal conditions
- **SC-003**: 100% of invalid inputs (empty, too long) receive clear validation feedback rather than being processed
- **SC-004**: AI tutor responses demonstrate adherence to at least 3 core educational principles from the Global Constitution (educational-first design, accessibility, progressive difficulty)
- **SC-005**: System successfully handles at least 10 students asking questions concurrently without errors or delays
- **SC-006**: 100% of service failures result in informative error messages rather than silent failures or crashes
- **SC-007**: Students can complete a basic learning interaction (submit question, receive answer) successfully on first attempt 95% of the time
- **SC-008**: Rate limiting successfully prevents students from exceeding 10 requests per minute, with clear feedback provided when limit is reached
- **SC-009**: All existing tests pass without modification (100% test compatibility)
- **SC-010**: POST /chat endpoint returns identical response structure (ChatResponse with "response" field)
- **SC-011**: Service startup time remains under 5 seconds with new model
- **SC-012**: Response generation time for valid questions remains under 10 seconds
- **SC-013**: Error handling behavior is identical - same exception types, same error messages for equivalent scenarios
- **SC-014**: Configuration loading succeeds using existing .env files without changes
- **SC-015**: pyproject.toml contains agents-sdk dependency instead of openai package
- **SC-016**: Manual testing with "What is Physical AI?" returns educationally appropriate response (quality unchanged)

### Assumptions

- The OpenAIChatCompletionsModel from agents-sdk supports Gemini 2.0 Flash via base_url configuration
- The agents-sdk package provides OpenAI-compatible completion interfaces
- Gemini API errors map cleanly to exceptions that can be caught and wrapped in AIServiceError
- The system prompt can be injected into OpenAIChatCompletionsModel (either via model config or per-request messages)
- The agents-sdk package is compatible with Python 3.13 and FastAPI async patterns
- Existing rate limiting, validation, and FastAPI endpoint logic remain unchanged (only agent.py changes)
- The migration does not require changes to frontend or API contracts
- Documentation for OpenAIChatCompletionsModel is available via Context7 MCP server or agents-sdk repository
- The Gemini API key will be provided through environment configuration (GEMINI_API_KEY)
- The Global Constitution educational principles document is available to the backend service
- The OpenAI Agent SDK will be used for agent orchestration, configured with Gemini 2.0 Flash via OpenAIChatCompletionsModel
- The AI agent will use Gemini 2.0 Flash (gemini-2.0-flash) as the underlying language model
- Student authentication is not required for this phase (to be added later)
- Integration with textbook content retrieval (RAG) is out of scope for this phase
- The backend service infrastructure is already initialized and ready for development
- Students will primarily ask questions in English, though Unicode support is needed for names and technical terms
- The OpenAI Agent SDK supports instructions-based agent configuration to inject educational principles
- The OpenAI Agent SDK provides both streaming (Runner.run) and non-streaming (Runner.run_sync) capabilities
- Context7 MCP server provides access to the latest OpenAI Agent SDK documentation

## Non-Functional Requirements

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