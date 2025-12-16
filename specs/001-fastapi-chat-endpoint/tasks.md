# Tasks: Backend Chat Communication Service with OpenAIChatCompletionsModel

**Feature**: 001-fastapi-chat-endpoint
**Generated**: 2025-12-14
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)
**Status**: Ready for Implementation

## Overview

This task breakdown implements a FastAPI chat endpoint using OpenAI Agent SDK with OpenAIChatCompletionsModel and Gemini 2.0 Flash. The system enables the frontend Chatbot UI to communicate with an AI agent providing educational responses about Physical AI and Humanoid Robotics, guided by the project's Global Constitution principles. The migration from AsyncOpenAI to OpenAIChatCompletionsModel maintains 100% backward compatibility in API behavior, error handling, and configuration.

## Implementation Strategy

MVP-first approach: Implement User Story 1 (Basic Question-Answer Interaction) first, then add supporting features incrementally. Each user story is designed to be independently testable and deliver value.

---

## Phase 1: Setup Tasks

**Goal**: Prepare environment and migrate dependencies from openai to openai-agents

- [ ] T001 Update pyproject.toml: Remove openai dependency and add openai-agents>=0.6.0
- [ ] T002 [P] Install new dependencies with `uv sync` and verify successful installation
- [ ] T003 [P] Verify no version conflicts with existing FastAPI, Pydantic, Uvicorn dependencies
- [ ] T004 Create directory structure: `backend/src/backend/`, `backend/tests/`

---

## Phase 2: Foundational Tasks

**Goal**: Implement core infrastructure needed by all user stories (validation, error handling, configuration)

- [ ] T005 Create backend/src/backend/config.py with Pydantic Settings for GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL, REQUEST_TIMEOUT_SECONDS
- [ ] T006 Create backend/src/backend/exceptions.py with EmptyAIResponse and AIServiceError classes
- [ ] T007 Create backend/src/backend/models.py with ChatRequest, ChatResponse, and ErrorResponse Pydantic models
- [ ] T008 [P] Implement input validation (3-10000 character limits) in ChatRequest model
- [ ] T009 [P] Add rate limiting setup using slowapi with 10 requests per minute limit
- [ ] T010 Create basic FastAPI app structure in backend/src/backend/main.py

---

## Phase 3: User Story 1 - Basic Question-Answer Interaction (Priority: P1)

**Goal**: Students can ask questions about course content and receive intelligent, educationally-focused responses

**Independent Test**: Submit "What is Physical AI?" and verify educational response is returned

- [ ] T011 [US1] Create AITutor class in backend/src/backend/agent.py with basic structure
- [ ] T012 [US1] [P] Implement OpenAIChatCompletionsModel configuration with Gemini client
- [ ] T013 [US1] [P] Load Global Constitution from .specify/memory/constitution.md and inject as agent instructions
- [ ] T014 [US1] Implement generate_response method using Runner.run() with timeout handling
- [ ] T015 [US1] [P] Create initialize_agent() and get_agent() functions for FastAPI dependency injection
- [ ] T016 [US1] [P] Implement POST /chat endpoint that accepts StudentQuestion and returns TutorResponse
- [ ] T017 [US1] [P] Connect endpoint to AITutor agent for response generation
- [ ] T018 [US1] Test basic functionality: POST /chat with "What is Physical AI?" returns 200 OK with educational response
- [ ] T019 [US1] Verify response includes agent_name and timestamp as specified

---

## Phase 4: User Story 2 - Input Quality Feedback (Priority: P2)

**Goal**: Frontend developers receive clear feedback when user input doesn't meet requirements

**Independent Test**: Submit various invalid inputs and verify clear error feedback

- [ ] T020 [US2] [P] Add validation error handling for messages under 3 characters in ChatRequest model
- [ ] T021 [US2] [P] Add validation error handling for messages over 10,000 characters in ChatRequest model
- [ ] T022 [US2] [P] Add validation for whitespace-only messages in ChatRequest model
- [ ] T023 [US2] Test validation: Submit "Hi" and verify 422 validation error with clear message
- [ ] T024 [US2] Test validation: Submit 10,001 character message and verify 422 error
- [ ] T025 [US2] Test validation: Submit whitespace-only message and verify 422 error

---

## Phase 5: User Story 3 - Service Availability Transparency (Priority: P3)

**Goal**: Students and developers understand when AI tutor service is experiencing issues

**Independent Test**: Simulate service failures and verify informative error messages

- [ ] T026 [US3] [P] Implement timeout handling (30 seconds) in AITutor.generate_response
- [ ] T027 [US3] [P] Handle EmptyAIResponse when AI returns empty content
- [ ] T028 [US3] [P] Handle AIServiceError for API connectivity issues
- [ ] T029 [US3] [P] Return appropriate error responses with error_type enum (timeout, service, etc.)
- [ ] T030 [US3] [P] Test timeout scenario: Verify 504 response when request exceeds 30 seconds
- [ ] T031 [US3] [P] Test empty response scenario: Verify 500 response when AI returns empty content
- [ ] T032 [US3] Test service error scenario: Verify 500 response when API is unavailable

---

## Phase 6: User Story 4 - Transparent Model Migration (Priority: P1)

**Goal**: Migrate from AsyncOpenAI client to OpenAIChatCompletionsModel while maintaining identical behavior

**Independent Test**: Run existing test suite and verify all tests pass without modification

- [ ] T033 [US4] [P] Replace AsyncOpenAI client with OpenAIChatCompletionsModel in AITutor.__init__()
- [ ] T034 [US4] [P] Migrate from client.chat.completions.create() to Runner.run() execution pattern
- [ ] T035 [US4] [P] Move system prompt from per-request messages to agent instructions parameter
- [ ] T036 [US4] [P] Update response extraction from response.choices[0].message.content to result.final_output
- [ ] T037 [US4] [P] Maintain identical exception handling (EmptyAIResponse, AIServiceError)
- [ ] T038 [US4] [P] Preserve identical timeout behavior using asyncio.wait_for()
- [ ] T039 [US4] [P] Verify identical response format and structure
- [ ] T040 [US4] Run existing test suite to confirm 100% compatibility

---

## Phase 7: User Story 5 - Configuration Compatibility (Priority: P2)

**Goal**: Maintain backward compatibility with existing environment configuration

**Independent Test**: Use existing .env configuration and verify service starts successfully

- [ ] T041 [US5] [P] Verify GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL are loaded from environment
- [ ] T042 [US5] [P] Verify REQUEST_TIMEOUT_SECONDS configuration is respected
- [ ] T043 [US5] [P] Verify Global Constitution path (../.specify/memory/constitution.md) is loaded correctly
- [ ] T044 [US5] [P] Test service startup with existing .env file configuration
- [ ] T045 [US5] [P] Verify configuration validation and error handling

---

## Phase 8: Testing & Validation Tasks

**Goal**: Ensure all functionality works as specified and meets success criteria

- [ ] T046 [P] Create comprehensive unit tests for AITutor class with mocked Runner.run()
- [ ] T047 [P] Create integration tests for POST /chat endpoint with various scenarios
- [ ] T048 [P] Test concurrent request handling (10 simultaneous requests)
- [ ] T049 [P] Verify service startup time is under 5 seconds
- [ ] T050 [P] Verify response time for valid questions is under 10 seconds (p95)
- [ ] T051 [P] Test rate limiting: Verify 429 response after 11 requests in 1 minute
- [ ] T052 [P] Test health endpoint: GET /health returns constitution_loaded: true
- [ ] T053 [P] Manual testing: Verify "What is Physical AI?" returns educational response

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Complete implementation with documentation, error handling, and production readiness

- [ ] T054 [P] Update backend/README.md with new dependency (openai-agents) and installation instructions
- [ ] T055 [P] Add migration notes to documentation explaining OpenAIChatCompletionsModel transition
- [ ] T056 [P] Add comprehensive error logging for debugging and monitoring
- [ ] T057 [P] Implement proper startup/shutdown lifecycle handling
- [ ] T058 [P] Add type hints throughout the codebase for better maintainability
- [ ] T059 [P] Add docstrings to all public functions and classes
- [ ] T060 [P] Create API documentation with examples for frontend integration
- [ ] T061 [P] Verify all existing tests pass with new implementation
- [ ] T062 [P] Perform final integration testing with all features enabled

---

## Dependencies

**User Story Completion Order**:
1. User Story 4 (Model Migration) must be completed before User Story 1 (Basic Interaction)
2. Foundational Phase (Phase 2) must be completed before any User Stories
3. User Story 1 provides foundation for User Stories 2 and 3

**Parallel Execution Opportunities**:
- T005-T010 (Foundational tasks) can be done in parallel with T033-T038 (Migration tasks)
- T011-T019 (User Story 1) can be done in parallel with T020-T025 (User Story 2) and T026-T032 (User Story 3)
- T046-T053 (Testing tasks) can be done in parallel after core functionality is implemented

**MVP Scope**: Complete Phase 1, Phase 2, and User Story 1 tasks (T001-T019) for minimum viable product that enables basic question-answer interaction.

## Implementation Notes

- All error handling must preserve existing exception types (EmptyAIResponse, AIServiceError) for backward compatibility
- The OpenAIChatCompletionsModel should be configured with the same timeout and API key as the previous AsyncOpenAI implementation
- Rate limiting should use slowapi with in-memory storage for MVP, with Redis support planned for production
- The Global Constitution should be loaded once during agent initialization and injected as agent instructions
- All existing API contracts (request/response formats) must remain identical from the client perspective