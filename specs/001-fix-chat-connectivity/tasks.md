# Tasks: Fix Chat Frontend-Backend Connectivity

**Input**: Design documents from `/specs/001-fix-chat-connectivity/`
**Prerequisites**: plan.md, spec.md, research.md, quickstart.md

**Tests**: Manual integration testing only (no automated test tasks required for configuration fix)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/backend/`, `frontend/src/`
- All paths use absolute references from repository root

## Phase 1: Setup (Environment Verification)

**Purpose**: Verify environment configuration and service prerequisites before implementing fix

- [ ] T001 Verify Node.js 20+ installed by running `node --version`
- [ ] T002 Verify Python 3.11+ installed by running `python --version`
- [ ] T003 [P] Verify backend dependencies installed by checking `backend/requirements.txt` existence
- [ ] T004 [P] Verify frontend dependencies installed by checking `frontend/package.json` existence
- [ ] T005 Verify Cohere API key exists in `backend/.env` (COHERE_API_KEY variable)
- [ ] T006 Verify frontend environment variable in `frontend/.env` (REACT_APP_BACKEND_URL=http://localhost:8000)

---

## Phase 2: Foundational (CORS Fix - Blocks User Story 1)

**Purpose**: Fix root cause (missing CORS middleware) that prevents ALL chat functionality

**⚠️ CRITICAL**: User Story 1 cannot work until CORS is configured

- [ ] T007 Add CORS middleware import to `backend/src/backend/main.py` after line 2: `from fastapi.middleware.cors import CORSMiddleware`
- [ ] T008 Add CORS middleware configuration to `backend/src/backend/main.py` after line 21 (after `app = FastAPI(...)`): Configure allow_origins with ["http://localhost:3000", "http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["*"]
- [ ] T009 Restart backend service to apply CORS changes: Stop existing uvicorn process and run `cd backend && uvicorn src.backend.main:app --reload`
- [ ] T010 Verify backend startup shows "Application startup complete" message
- [ ] T011 Restart frontend service to ensure environment variables loaded: Stop existing npm process and run `cd frontend && npm start`
- [ ] T012 Verify frontend startup shows "Docusaurus website is running at: http://localhost:3000/"

**Checkpoint**: CORS configured - chat connectivity should now work, ready for User Story 1 testing

---

## Phase 3: User Story 1 - Send Message and Receive AI Response (Priority: P1) 🎯 MVP

**Goal**: Enable students to send chat messages and receive AI tutor responses from Cohere

**Independent Test**: Open chat widget at http://localhost:3000, type "How does a humanoid robot balance?", send message, and verify AI response appears within 5 seconds

### Implementation for User Story 1

- [ ] T013 [US1] Open browser to http://localhost:3000 and locate chat widget icon (bottom-right corner)
- [ ] T014 [US1] Click chat widget to expand interface
- [ ] T015 [US1] Type test message "Hello" in chat input field
- [ ] T016 [US1] Click Send button or press Enter to send message
- [ ] T017 [US1] Verify user message appears immediately in chat history
- [ ] T018 [US1] Verify typing indicator appears while waiting for backend response
- [ ] T019 [US1] Wait up to 5 seconds for AI response
- [ ] T020 [US1] Verify AI tutor response appears in chat with proper formatting (response from Cohere)
- [ ] T021 [US1] Verify typing indicator disappears after response received
- [ ] T022 [US1] Open browser DevTools (F12) → Console tab and verify NO CORS errors present
- [ ] T023 [US1] Open browser DevTools → Network tab and verify POST request to http://localhost:8000/chat shows status 200 OK

**Checkpoint**: User Story 1 complete - Basic send/receive functionality working

---

## Phase 4: User Story 2 - Handle Connection Errors Gracefully (Priority: P2)

**Goal**: Display user-friendly error messages when backend is unavailable or network issues occur

**Independent Test**: Stop backend service, send chat message, verify error message "Unable to connect. Please check your connection." appears instead of crash

### Implementation for User Story 2

- [ ] T024 [US2] Stop backend service by pressing Ctrl+C in backend terminal (kill uvicorn process)
- [ ] T025 [US2] Return to browser at http://localhost:3000 with chat widget open
- [ ] T026 [US2] Type test message "Test error handling" in chat input
- [ ] T027 [US2] Click Send button
- [ ] T028 [US2] Verify error message appears in chat: "Unable to connect. Please check your connection."
- [ ] T029 [US2] Verify message was NOT lost (still in input field or recoverable)
- [ ] T030 [US2] Verify chat widget doesn't crash or freeze
- [ ] T031 [US2] Restart backend service: Run `cd backend && uvicorn src.backend.main:app --reload`
- [ ] T032 [US2] Send another test message and verify it works (confirms recovery from error state)
- [ ] T033 [US2] Test timeout handling by modifying backend to delay 35 seconds (optional verification of timeout error message)

**Checkpoint**: User Story 2 complete - Error handling works gracefully

---

## Phase 5: User Story 3 - Respect Rate Limits (Priority: P2)

**Goal**: Enforce 3 messages per 30 seconds client-side rate limiting with countdown timer

**Independent Test**: Send 3 messages rapidly, attempt 4th message immediately, verify it's blocked with "Rate limit reached. Please wait X seconds" countdown

### Implementation for User Story 3

- [ ] T034 [US3] Ensure both backend and frontend services are running
- [ ] T035 [US3] Open browser to http://localhost:3000 with chat widget open
- [ ] T036 [US3] Send first message "Message 1" and wait for response
- [ ] T037 [US3] Immediately send second message "Message 2" without waiting
- [ ] T038 [US3] Immediately send third message "Message 3" without waiting
- [ ] T039 [US3] Immediately attempt to send fourth message "Message 4"
- [ ] T040 [US3] Verify Send button is disabled (cannot click)
- [ ] T041 [US3] Verify rate limit message appears: "Rate limit reached. Please wait X seconds before sending another message"
- [ ] T042 [US3] Verify countdown timer decrements every second
- [ ] T043 [US3] Wait for countdown to reach 0
- [ ] T044 [US3] Verify Send button re-enables when timer expires
- [ ] T045 [US3] Send another message to confirm rate limit reset
- [ ] T046 [US3] Refresh page (F5) and verify rate limit state persists via localStorage
- [ ] T047 [US3] If rate limit active before refresh, verify countdown continues correctly after refresh

**Checkpoint**: User Story 3 complete - Rate limiting enforced correctly

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and verification across all user stories

- [ ] T048 [P] Update `frontend/.env.example` (if missing) to document REACT_APP_BACKEND_URL requirement
- [ ] T049 [P] Create troubleshooting section in project README documenting CORS configuration requirement
- [ ] T050 [P] Document CORS middleware configuration in README for future contributors
- [ ] T051 Verify all success criteria from spec.md:
  - SC-001: Response time <5 seconds (p95) ✅
  - SC-002: 100% connection success when backend running ✅
  - SC-003: Error messages within 1 second ✅
  - SC-004: Rate limiting 100% accurate ✅
  - SC-005: Message persistence across refreshes ✅
  - SC-006: Typing indicator immediate ✅
- [ ] T052 Run through quickstart.md verification steps end-to-end
- [ ] T053 Test edge case: Network disconnection mid-request (optional - turn off WiFi, send message, verify error)
- [ ] T054 Test edge case: Multiple browser tabs (send messages in 2 tabs, verify rate limiting per-tab)
- [ ] T055 Clear browser localStorage and verify fresh session starts correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - Can proceed in priority order: US1 (P1) → US2 (P2) → US3 (P2)
  - US2 and US3 can be tested in parallel after US1 works
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (T007-T012) - CORS must be configured
  - **CRITICAL MVP**: This is the minimum viable product - chat must work
- **User Story 2 (P2)**: Depends on US1 being functional (need working chat to test errors)
  - Can start after US1 checkpoint
  - Independent test: Stop backend and verify error handling
- **User Story 3 (P2)**: Depends on US1 being functional (need working chat to test rate limits)
  - Can start after US1 checkpoint
  - Can run in parallel with US2 (different test scenarios)
  - Independent test: Send 4 rapid messages

### Within Each User Story

**User Story 1** (Sequential execution - must follow order):
1. T013-T014: Open and expand chat widget
2. T015-T016: Send test message
3. T017-T021: Verify message flow (user message → typing indicator → AI response)
4. T022-T023: Verify no errors in DevTools

**User Story 2** (Sequential execution):
1. T024: Stop backend
2. T025-T030: Test error handling
3. T031-T032: Restart and verify recovery

**User Story 3** (Sequential execution):
1. T034-T035: Prepare test environment
2. T036-T038: Send 3 messages
3. T039-T045: Test rate limiting
4. T046-T047: Test persistence

### Parallel Opportunities

- **Setup Phase**: T003 (backend check) and T004 (frontend check) can run in parallel
- **Foundational Phase**:
  - T007-T008 (edit main.py) are sequential
  - T009-T010 (restart backend) and T011-T012 (restart frontend) can run in parallel AFTER T008
- **User Stories**: US2 and US3 can be tested in parallel after US1 works (different team members or sequential)
- **Polish Phase**: T048, T049, T050 (documentation) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Edit CORS configuration (sequential):
Task T007: Add import
Task T008: Add middleware config

# Restart services (parallel after T008):
Terminal 1: Task T009-T010: Restart backend
Terminal 2: Task T011-T012: Restart frontend
```

---

## Parallel Example: User Story 2 and 3

```bash
# After User Story 1 works, two developers can work in parallel:

Developer A (User Story 2):
Task T024-T033: Test error handling scenarios

Developer B (User Story 3):
Task T034-T047: Test rate limiting scenarios
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006) - ~2 minutes
2. Complete Phase 2: Foundational (T007-T012) - ~5 minutes
   - **CRITICAL**: CORS fix that enables connectivity
3. Complete Phase 3: User Story 1 (T013-T023) - ~5 minutes
4. **STOP and VALIDATE**: Chat send/receive working
5. **Deploy/Demo**: MVP is ready - students can use chat

**Total MVP Time**: ~12 minutes

### Incremental Delivery

1. **Foundation** (Setup + Foundational) → CORS configured, services running
2. **MVP** (+ User Story 1) → Chat send/receive working ✅ **DELIVERABLE**
3. **Error Handling** (+ User Story 2) → Graceful error messages ✅ **DELIVERABLE**
4. **Rate Limiting** (+ User Story 3) → Abuse prevention ✅ **DELIVERABLE**
5. **Polish** (+ Phase 6) → Documentation complete ✅ **FINAL DELIVERABLE**

Each increment adds value without breaking previous functionality.

### Sequential Execution (Single Developer)

**Day 1: MVP** (~15 minutes)
- Complete Setup, Foundational, User Story 1
- Verify chat works end-to-end
- Commit and push

**Day 2: Enhanced UX** (~20 minutes)
- Complete User Story 2 (error handling)
- Complete User Story 3 (rate limiting)
- Test edge cases
- Commit and push

**Day 3: Documentation** (~10 minutes)
- Complete Polish phase
- Update README and troubleshooting docs
- Final verification
- Create PR

**Total**: ~45 minutes spread over 3 sessions

---

## Notes

- **No automated tests**: This is a configuration fix with manual integration testing per spec
- **[P] tasks**: Indicate tasks that can run in parallel (different files or independent verification)
- **[Story] labels**: Map tasks to user stories for traceability
- **MVP = User Story 1**: Core chat functionality is the minimum viable product
- **Fast iteration**: Entire fix can be completed in 15-45 minutes depending on testing thoroughness
- **Low risk**: Configuration change only, no code logic modifications
- **Rollback**: Simple - revert CORS middleware, restart backend
- **Commit strategy**: Commit after each phase checkpoint for easy rollback
- **Browser DevTools**: Essential for verifying CORS errors are gone (F12 → Console/Network)
- **Service restarts**: Required after code changes (backend) and env changes (frontend)

---

## Success Checklist

Before marking feature complete, verify:

- [x] Phase 1: Setup verified (Node, Python, dependencies, env vars)
- [ ] Phase 2: CORS middleware added and services restarted
- [ ] Phase 3: User Story 1 working (send message → receive AI response)
- [ ] Phase 4: User Story 2 working (error handling when backend down)
- [ ] Phase 5: User Story 3 working (rate limiting enforced)
- [ ] Phase 6: Documentation updated (README, .env.example)
- [ ] No CORS errors in browser console
- [ ] All 6 success criteria from spec.md verified
- [ ] Quickstart.md verification steps pass

**All checked?** ✅ Chat connectivity is FIXED and READY FOR PRODUCTION!
