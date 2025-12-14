---
description: "Implementation tasks for Backend Chat Communication Service"
---

# Tasks: Backend Chat Communication Service

**Input**: Design documents from `/specs/001-fastapi-chat-endpoint/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: This feature includes comprehensive test tasks following TDD principles as specified in the plan.md Phase 3 testing requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/backend/` for implementation, `backend/tests/` for tests
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 Update backend/pyproject.toml with FastAPI, Uvicorn, Pydantic, OpenAI SDK, python-dotenv dependencies per plan.md Phase 2.1
- [x] T002 [P] Create backend/.env.example with GEMINI_API_KEY, GEMINI_BASE_URL, GEMINI_MODEL, REQUEST_TIMEOUT_SECONDS, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS, HOST, PORT per plan.md Phase 2.1
- [x] T003 [P] Add pytest, pytest-asyncio, httpx to dev dependencies in backend/pyproject.toml per plan.md Phase 2.1
- [x] T004 Run `uv sync --dev` in backend directory to install all dependencies
- [x] T005 [P] Create backend/tests/__init__.py as test package marker
- [x] T006 [P] Verify Global Constitution file exists at ../.specify/memory/constitution.md from backend directory per ADR-002

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 [P] Create backend/src/backend/config.py with Settings class using pydantic-settings per plan.md Phase 2.2
- [x] T008 [P] Create backend/src/backend/exceptions.py with RateLimitExceeded, EmptyAIResponse, AIServiceError classes per plan.md Phase 2.6
- [x] T009 [P] Create backend/src/backend/models.py with ChatRequest, ChatResponse, ErrorResponse Pydantic models per plan.md Phase 2.3
- [x] T010 Create backend/tests/conftest.py with pytest fixtures (app, client, mock agent) per plan.md Phase 2.7
- [x] T011 Verify constitution loading: read ../.specify/memory/constitution.md and confirm ~6KB content loads successfully

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Question-Answer Interaction (Priority: P1) 🎯 MVP

**Goal**: Enable students to submit questions and receive AI-generated educational responses guided by the Global Constitution

**Independent Test**: Submit "What is Physical AI?" to POST /chat and verify a relevant educational response is returned with 200 OK status

### Tests for User Story 1 (TDD - Write First, Ensure FAIL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Create backend/tests/test_config.py with tests for config loading from .env and defaults per plan.md Phase 2.2
- [x] T013 [P] [US1] Create backend/tests/test_validation.py with tests for ChatRequest validation (valid message, too short, too long, whitespace-only) per plan.md Phase 2.3
- [x] T014 [P] [US1] Create backend/tests/test_agent.py with tests for AITutor initialization, constitution loading, and response generation (mocked) per plan.md Phase 2.5
- [x] T015 [P] [US1] Create backend/tests/test_chat_endpoint.py with test_chat_endpoint_success for valid message returning 200 OK per plan.md Phase 2.7

### Implementation for User Story 1

- [x] T016 [P] [US1] Implement backend/src/backend/config.py Settings class with all configuration fields, defaults, and .env loading per plan.md Phase 1.3
- [x] T017 [P] [US1] Implement backend/src/backend/models.py ChatRequest with Field validation (min_length=3, max_length=10000) and whitespace validator per plan.md Phase 1.2
- [x] T018 [P] [US1] Implement backend/src/backend/models.py ChatResponse and ErrorResponse models per plan.md Phase 1.2
- [x] T019 [US1] Implement backend/src/backend/agent.py AITutor class with _load_constitution() method reading from settings.constitution_path per plan.md Phase 2.5 and ADR-002
- [x] T020 [US1] Implement backend/src/backend/agent.py AITutor.generate_response() with AsyncOpenAI client configured for Gemini per ADR-001, including asyncio.wait_for timeout per ADR-005
- [x] T021 [US1] Implement backend/src/backend/agent.py initialize_agent() and get_agent() for FastAPI dependency injection per plan.md Phase 2.5
- [x] T022 [US1] Create backend/src/backend/main.py with FastAPI app, lifespan context manager calling initialize_agent() per plan.md Phase 2.7
- [x] T023 [US1] Implement backend/src/backend/main.py POST /chat endpoint with ChatRequest validation, agent.generate_response() call, ChatResponse return per plan.md Phase 2.7
- [x] T024 [US1] Add empty response detection in agent.py generate_response(): check if content is None/empty/whitespace, raise EmptyAIResponse per ADR-007
- [x] T025 [US1] Add timeout error handling in /chat endpoint: catch asyncio.TimeoutError from agent, return 500 with "request took too long" message per FR-008
- [x] T026 [US1] Add AI service error handling in /chat endpoint: catch AIServiceError, return 500 with appropriate message per FR-007
- [x] T027 [US1] Add empty response error handling in /chat endpoint: catch EmptyAIResponse, return 500 with "unable to generate response, try rephrasing" per clarification Q1 answer
- [x] T028 [P] [US1] Create backend/src/backend/main.py GET /health endpoint returning status and constitution_loaded flag per plan.md Phase 2.7
- [x] T029 [US1] Run pytest backend/tests/test_config.py backend/tests/test_validation.py backend/tests/test_agent.py backend/tests/test_chat_endpoint.py and verify all tests pass
- [ ] T030 [US1] Manual test: Start server with `uv run uvicorn backend.main:app --reload`, POST to /chat with `{"message": "What is Physical AI?"}`, verify 200 OK with educational response

**Checkpoint**: At this point, User Story 1 should be fully functional - students can ask questions and receive AI responses

---

## Phase 4: User Story 2 - Input Quality Feedback (Priority: P2)

**Goal**: Provide clear validation feedback when student input doesn't meet quality requirements (too short, too long, empty)

**Independent Test**: Submit {"message": "Hi"} (2 chars) to /chat and verify 422 status with "at least 3 characters" error; submit 10,001 char message and verify 422 with "at most 10000 characters" error

### Tests for User Story 2 (TDD - Write First, Ensure FAIL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T031 [P] [US2] Add backend/tests/test_validation.py test_message_too_short: ChatRequest with 2-char message raises ValidationError
- [ ] T032 [P] [US2] Add backend/tests/test_validation.py test_message_too_long: ChatRequest with 10,001-char message raises ValidationError
- [ ] T033 [P] [US2] Add backend/tests/test_validation.py test_message_whitespace_only: ChatRequest with "   " raises ValidationError with "cannot be only whitespace"
- [ ] T034 [P] [US2] Add backend/tests/test_chat_endpoint.py test_chat_endpoint_validation_too_short: POST /chat with 2-char message returns 422
- [ ] T035 [P] [US2] Add backend/tests/test_chat_endpoint.py test_chat_endpoint_validation_too_long: POST /chat with 10,001-char message returns 422
- [ ] T036 [P] [US2] Add backend/tests/test_chat_endpoint.py test_chat_endpoint_validation_missing_field: POST /chat without message field returns 422

### Implementation for User Story 2

- [ ] T037 [US2] Verify backend/src/backend/models.py ChatRequest has Field(min_length=3, max_length=10000) - already implemented in T017, no changes needed
- [ ] T038 [US2] Verify backend/src/backend/models.py ChatRequest has @field_validator for whitespace-only check - already implemented in T017, no changes needed
- [ ] T039 [US2] Verify backend/src/backend/main.py POST /chat uses ChatRequest for validation - FastAPI auto-validates, returns 422 on error (no code changes)
- [ ] T040 [US2] Run pytest backend/tests/test_validation.py backend/tests/test_chat_endpoint.py and verify all US2 tests pass
- [ ] T041 [US2] Manual test: POST /chat with {"message": "Hi"}, verify 422 with validation detail; POST with 10,001 chars, verify 422; POST without message field, verify 422

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - students get helpful feedback for invalid input

---

## Phase 5: User Story 3 - Service Availability Transparency (Priority: P3)

**Goal**: Provide informative error messages when AI service is unavailable, times out, or returns empty responses (instead of silent failures)

**Independent Test**: Mock AI service to return empty response, verify 500 with "unable to generate response, try rephrasing"; mock 31-second timeout, verify 500 with "request took too long" message

### Tests for User Story 3 (TDD - Write First, Ensure FAIL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T042 [P] [US3] Add backend/tests/test_agent.py test_agent_raises_empty_response_error: mock AI client returning empty content, verify EmptyAIResponse raised
- [ ] T043 [P] [US3] Add backend/tests/test_agent.py test_agent_raises_timeout_error: mock AI client with asyncio.TimeoutError, verify AIServiceError with "timed out" raised
- [ ] T044 [P] [US3] Add backend/tests/test_agent.py test_agent_raises_ai_service_error: mock AI client with generic exception, verify AIServiceError raised
- [ ] T045 [P] [US3] Add backend/tests/test_chat_endpoint.py test_chat_endpoint_empty_response: mock agent.generate_response raising EmptyAIResponse, verify 500 with "unable to generate response" message
- [ ] T046 [P] [US3] Add backend/tests/test_chat_endpoint.py test_chat_endpoint_timeout: mock agent.generate_response raising AIServiceError("timed out"), verify 500 with "took too long" message
- [ ] T047 [P] [US3] Add backend/tests/test_chat_endpoint.py test_chat_endpoint_service_unavailable: mock agent.generate_response raising AIServiceError (generic), verify 500 with "temporarily unavailable" message

### Implementation for User Story 3

- [ ] T048 [US3] Verify backend/src/backend/agent.py generate_response() checks for empty/None/whitespace content and raises EmptyAIResponse - already implemented in T024, no changes needed
- [ ] T049 [US3] Verify backend/src/backend/agent.py generate_response() wraps API call with asyncio.wait_for(timeout=30) - already implemented in T020, no changes needed
- [ ] T050 [US3] Verify backend/src/backend/agent.py generate_response() catches asyncio.TimeoutError and raises AIServiceError("timed out") - already implemented in T020/T025, no changes needed
- [ ] T051 [US3] Verify backend/src/backend/agent.py generate_response() catches generic exceptions and raises AIServiceError - already implemented in T020/T026, no changes needed
- [ ] T052 [US3] Verify backend/src/backend/main.py /chat endpoint has EmptyAIResponse handler returning 500 with "unable to generate response, try rephrasing" - already implemented in T027, no changes needed
- [ ] T053 [US3] Verify backend/src/backend/main.py /chat endpoint has AIServiceError handler checking for "timed out" and returning appropriate message - already implemented in T025/T026, no changes needed
- [ ] T054 [US3] Run pytest backend/tests/test_agent.py backend/tests/test_chat_endpoint.py and verify all US3 tests pass
- [ ] T055 [US3] Manual test: Mock Gemini API to return empty response, verify graceful error; simulate timeout, verify timeout message

**Checkpoint**: All user stories (US1, US2, US3) should now be independently functional with comprehensive error handling

---

## Phase 6: Rate Limiting (Cross-Cutting - Affects All Stories)

**Goal**: Enforce 10 requests per minute per student (IP-based) to prevent abuse

**Independent Test**: Submit 10 valid requests rapidly, verify all return 200; submit 11th request, verify 429 with rate limit error message

### Tests for Rate Limiting (TDD - Write First, Ensure FAIL)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T056 [P] Create backend/tests/test_rate_limiter.py with test_allows_requests_under_limit: InMemoryRateLimiter allows 10 requests for same client per plan.md Phase 2.4
- [ ] T057 [P] Add backend/tests/test_rate_limiter.py test_blocks_requests_over_limit: 11th request for same client is blocked per plan.md Phase 2.4
- [ ] T058 [P] Add backend/tests/test_rate_limiter.py test_allows_after_window_expires: after 60s window, client can make requests again per plan.md Phase 2.4
- [ ] T059 Add backend/tests/test_chat_endpoint.py test_chat_endpoint_rate_limit: make 10 requests to /chat, all succeed; 11th returns 429 per plan.md Phase 2.7

### Implementation for Rate Limiting

- [ ] T060 Create backend/src/backend/rate_limiter.py with InMemoryRateLimiter class (max_requests, window_seconds, _requests dict) per plan.md Phase 2.4 and ADR-003
- [ ] T061 Implement backend/src/backend/rate_limiter.py InMemoryRateLimiter.is_allowed(client_id) with timestamp deque, cutoff logic, limit check per plan.md Phase 2.4
- [ ] T062 Add backend/src/backend/rate_limiter.py InMemoryRateLimiter.reset(client_id) for testing per plan.md Phase 2.4
- [ ] T063 Instantiate rate_limiter in backend/src/backend/main.py with settings.rate_limit_requests and settings.rate_limit_window per plan.md Phase 2.7
- [ ] T064 Create backend/src/backend/main.py get_client_identifier(request) extracting request.client.host per plan.md Phase 2.7 and ADR-003
- [ ] T065 Add rate limiting to backend/src/backend/main.py POST /chat: call rate_limiter.is_allowed(client_id), raise HTTPException(429) if exceeded per plan.md Phase 2.7
- [ ] T066 Run pytest backend/tests/test_rate_limiter.py backend/tests/test_chat_endpoint.py and verify all rate limit tests pass
- [ ] T067 Manual test: Use curl or httpx to send 11 rapid requests to /chat, verify 10 succeed and 11th returns 429 with clear error message

**Checkpoint**: Rate limiting successfully enforced across all user stories

---

## Phase 7: Integration Testing & End-to-End Validation

**Purpose**: Verify complete system behavior across all user stories

- [ ] T068 [P] Create backend/tests/test_integration.py with test_end_to_end_chat_flow: POST valid message → verify 200, response length >50, contains relevant keywords per plan.md Phase 3.2
- [ ] T069 [P] Add backend/tests/test_integration.py test_constitution_adherence: submit "Explain ROS 2 nodes" → verify response has educational tone, accessible language
- [ ] T070 [P] Add backend/tests/test_integration.py test_concurrent_requests: launch 10 concurrent /chat requests with asyncio.gather, verify all succeed per SC-005
- [ ] T071 Run pytest --cov=backend --cov-report=term-missing backend/tests/ and verify >90% coverage per plan.md Phase 3.1
- [ ] T072 Validate acceptance criteria: AC.1 (server launches <5s), AC.2 (valid request returns 200), AC.3 (response has "response" key), AC.4 (adheres to constitution), AC.5 (invalid request returns 422) per spec.md Section 4

---

## Phase 8: Documentation & Deployment Preparation

**Purpose**: Finalize documentation and prepare for deployment

- [ ] T073 [P] Update backend/README.md with Quick Start, Prerequisites, Setup instructions, API documentation links, Testing section per plan.md Phase 2.8
- [ ] T074 [P] Verify backend/.env.example has all required variables with example values per plan.md Phase 4.1
- [ ] T075 [P] Add comment to backend/.env.example explaining each configuration variable
- [ ] T076 [P] Create production startup instructions in backend/README.md: `uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000` per plan.md Phase 4.2
- [ ] T077 Measure startup time with `time uv run uvicorn backend.main:app` and verify <5 seconds per SC-001
- [ ] T078 Test health check endpoint: curl http://localhost:8000/health, verify {"status": "healthy", "constitution_loaded": true} per plan.md Phase 4.3
- [ ] T079 [P] Document known limitations in README.md: IP-based rate limiting (NAT users share limit), no persistence (restart clears limits) per ADR-003

---

## Phase 9: Polish & Final Validation

**Purpose**: Code quality, security, and final checks

- [ ] T080 [P] Run linter/formatter on all backend/src/backend/ files if configured
- [ ] T081 [P] Security review: verify no hardcoded secrets, API key only via .env, input validation present per Principle V (Constitution)
- [ ] T082 [P] Review all error messages for clarity and user-friendliness per spec.md clarifications
- [ ] T083 Verify Global Constitution integration: submit varied questions, manually check responses adhere to educational-first design, accessibility, progressive difficulty per SC-004
- [ ] T084 Load test: use httpx AsyncClient to send 10 concurrent requests, verify all complete successfully and response times <10s per SC-002 and SC-005
- [ ] T085 Final smoke test: Fresh .env setup → uv sync → uvicorn server start → POST /chat → verify end-to-end success
- [ ] T086 Create list of next phase items (Phase 6 auth, Phase 5 RAG) for future reference

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - MVP priority
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) - Can run parallel with US1 if staffed
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) - Can run parallel with US1/US2 if staffed
- **Rate Limiting (Phase 6)**: Depends on US1 core /chat endpoint (T023) being implemented
- **Integration Testing (Phase 7)**: Depends on all user stories (US1, US2, US3) and rate limiting being complete
- **Documentation (Phase 8)**: Can start after US1 complete; finalize after all phases
- **Polish (Phase 9)**: Depends on all previous phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - **No dependencies on other stories**
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - **No dependencies on other stories** (validation is independent)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - **No dependencies on other stories** (error handling is independent)

**Key Insight**: All user stories are independently implementable after Phase 2!

### Within Each User Story

1. **Tests FIRST** (TDD): All test tasks must be written and FAIL before implementation
2. **Models before services**: Pydantic models (T017-T018) before AI agent (T019-T021)
3. **Services before endpoints**: AI agent (T019-T021) before /chat endpoint (T022-T023)
4. **Core before error handling**: Basic /chat implementation (T023) before error handlers (T024-T027)
5. **Implementation before validation**: Code tasks before pytest runs (T029, T040, T054)

### Parallel Opportunities

**Phase 1 (Setup) - All [P] tasks can run in parallel:**
- T002 (.env.example), T003 (dev dependencies), T005 (tests/__init__.py), T006 (verify constitution)

**Phase 2 (Foundational) - All [P] tasks can run in parallel:**
- T007 (config.py), T008 (exceptions.py), T009 (models.py)

**User Story 1 - Tests [P] tasks:**
- T012 (test_config.py), T013 (test_validation.py), T014 (test_agent.py), T015 (test_chat_endpoint.py) - all different files

**User Story 1 - Implementation [P] tasks:**
- T016 (config.py impl), T017 (ChatRequest impl), T018 (ChatResponse/ErrorResponse impl) - all different modules within models.py or config.py

**User Story 2 - All test tasks [P]:**
- T031-T036 (different test functions, can be written in parallel)

**User Story 3 - All test tasks [P]:**
- T042-T047 (different test functions, can be written in parallel)

**Rate Limiting - Test tasks [P]:**
- T056, T057, T058 (test_rate_limiter.py different functions)

**Integration Testing - All [P]:**
- T068, T069, T070 (different test functions)

**Documentation - All [P]:**
- T073 (README.md), T074-T075 (.env.example), T076 (startup instructions), T079 (limitations)

**Polish - Quality tasks [P]:**
- T080 (linting), T081 (security review), T082 (error message review)

---

## Parallel Example: User Story 1

```bash
# STEP 1: Launch all US1 tests together (TDD - write tests first):
Task T012: "Create backend/tests/test_config.py..."
Task T013: "Create backend/tests/test_validation.py..."
Task T014: "Create backend/tests/test_agent.py..."
Task T015: "Create backend/tests/test_chat_endpoint.py..."

# STEP 2: Launch all US1 implementation foundation tasks together:
Task T016: "Implement backend/src/backend/config.py Settings class..."
Task T017: "Implement backend/src/backend/models.py ChatRequest..."
Task T018: "Implement backend/src/backend/models.py ChatResponse and ErrorResponse..."

# STEP 3: Sequential agent implementation (depends on config/models):
Task T019: "Implement backend/src/backend/agent.py AITutor class..."
Task T020: "Implement backend/src/backend/agent.py AITutor.generate_response()..."
Task T021: "Implement backend/src/backend/agent.py initialize_agent() and get_agent()..."

# STEP 4: FastAPI app (depends on agent):
Task T022: "Create backend/src/backend/main.py with FastAPI app..."
Task T023: "Implement backend/src/backend/main.py POST /chat endpoint..."
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - RECOMMENDED

1. **Complete Phase 1: Setup** (T001-T006) - ~30 minutes
2. **Complete Phase 2: Foundational** (T007-T011) - CRITICAL blocker - ~45 minutes
3. **Complete Phase 3: User Story 1** (T012-T030) - MVP core - ~3 hours
4. **STOP and VALIDATE**:
   - Run pytest, verify all US1 tests pass
   - Manual test: Start server, POST valid question, verify response
   - Check response adheres to Global Constitution principles
5. **Deploy/Demo if ready** - You now have a working AI tutor chat service!

**Total MVP Time**: ~4.25 hours

### Incremental Delivery (Add User Stories Sequentially)

1. **Foundation** (Phases 1-2) → ~1.25 hours → Foundation ready
2. **Add User Story 1** (Phase 3) → ~3 hours → Test independently → **Deploy/Demo (MVP!)**
3. **Add User Story 2** (Phase 4) → ~1 hour → Test independently → Deploy/Demo (now with better validation)
4. **Add User Story 3** (Phase 5) → ~1.5 hours → Test independently → Deploy/Demo (now with robust error handling)
5. **Add Rate Limiting** (Phase 6) → ~1 hour → Test independently → Deploy/Demo (now production-ready)
6. **Integration & Polish** (Phases 7-9) → ~2.5 hours → Final validation → Production deploy

**Total Complete Time**: ~11.5 hours (matches plan.md estimate)

### Parallel Team Strategy (3 Developers)

With multiple developers:

1. **All team members**: Complete Setup + Foundational together (~1.25 hours)
2. **Once Foundational is done, split user stories**:
   - **Developer A**: User Story 1 (Phase 3) - T012-T030
   - **Developer B**: User Story 2 (Phase 4) - T031-T041
   - **Developer C**: User Story 3 (Phase 5) - T042-T055
3. **All team members**: Complete Rate Limiting together (Phase 6) - T056-T067
4. **All team members**: Integration Testing & Polish (Phases 7-9) - T068-T086

**Total Parallel Time**: ~6 hours (with 3 developers)

---

## Task Summary

**Total Tasks**: 86 tasks

**Tasks per User Story**:
- Setup (Phase 1): 6 tasks
- Foundational (Phase 2): 5 tasks (CRITICAL blocker)
- User Story 1 - MVP (Phase 3): 19 tasks (Tests: 4, Implementation: 15)
- User Story 2 (Phase 4): 11 tasks (Tests: 6, Implementation: 5)
- User Story 3 (Phase 5): 14 tasks (Tests: 6, Implementation: 8)
- Rate Limiting (Phase 6): 12 tasks (Tests: 4, Implementation: 8)
- Integration Testing (Phase 7): 5 tasks
- Documentation (Phase 8): 7 tasks
- Polish (Phase 9): 7 tasks

**Parallel Opportunities**: 42 tasks marked [P] can run in parallel (49% of total tasks)

**MVP Scope** (Phases 1-3): 30 tasks → ~4.25 hours → Working AI tutor chat service

**Independent Test Criteria**:
- ✅ **US1**: POST {"message": "What is Physical AI?"} → 200 OK with educational response
- ✅ **US2**: POST {"message": "Hi"} → 422 with validation error
- ✅ **US3**: Mock empty AI response → 500 with "try rephrasing" message
- ✅ **Rate Limiting**: 11 rapid requests → 10 succeed, 11th returns 429

**Format Validation**: ✅ All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`

---

## Notes

- **[P] tasks** = different files or independent test functions, no dependencies
- **[Story] label** maps task to specific user story (US1, US2, US3) for traceability
- **Each user story is independently completable and testable** after Phase 2 foundation
- **TDD Approach**: All test tasks must be written FIRST and FAIL before implementation tasks
- **Verify tests fail before implementing**: Critical for true TDD workflow
- **Commit after each task or logical group**: Enables easy rollback and progress tracking
- **Stop at any checkpoint to validate story independently**: Each phase ends with validation
- **File paths are exact**: Every task specifies the exact file to create/modify
- **ADR references included**: Tasks reference specific ADRs (e.g., ADR-001, ADR-003) for context
- **Avoid**: Vague tasks, same-file conflicts, cross-story dependencies that break independence

---

## Next Steps

1. **Start with MVP**: Complete Phases 1-3 (Setup → Foundational → User Story 1)
2. **Validate MVP**: Run tests, manual validation, check constitution adherence
3. **Demo/Deploy**: You have a working AI tutor chat service!
4. **Iterate**: Add User Stories 2 and 3 incrementally
5. **Production-Ready**: Complete Rate Limiting and Polish phases

**Recommended first task**: T001 - Update backend/pyproject.toml with dependencies
