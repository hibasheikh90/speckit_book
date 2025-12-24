# Tasks: Connect Frontend Authentication and Chat to Backend APIs

**Feature Branch**: `001-connect-frontend-backend-apis`
**Date**: 2025-12-23
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

---

## Task Summary

**Total Tasks**: 28
**MVP Scope**: User Story 1 + User Story 2 (P1 tasks only) = 15 tasks
**Estimated Effort**: 6-8 hours for MVP, 10-12 hours for full feature

**User Story Distribution**:
- Setup (Phase 1): 2 tasks
- Foundational (Phase 2): 3 tasks
- User Story 1 (P1): 7 tasks
- User Story 2 (P1): 5 tasks
- User Story 3 (P2): 4 tasks
- User Story 4 (P2): 4 tasks
- User Story 5 (P3): 2 tasks
- Polish (Final): 1 task

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 only)
Complete US1 (authentication) and US2 (chat messaging) for a working end-to-end flow. This delivers core value: users can sign in and chat with the AI tutor.

### Incremental Delivery
- **Phase 1**: Setup environment and verify backend connectivity (2 tasks)
- **Phase 2**: Foundational work for all stories (3 tasks)
- **Phase 3**: US1 - Sign-in flow (7 tasks) → **First deliverable checkpoint**
- **Phase 4**: US2 - Chat messaging (5 tasks) → **MVP complete**
- **Phase 5**: US3 - Auth error handling (4 tasks)
- **Phase 6**: US4 - Chat error handling (4 tasks)
- **Phase 7**: US5 - Session persistence (2 tasks)
- **Phase 8**: Polish & cross-cutting concerns (1 task)

### Parallel Execution Opportunities
Tasks marked with **[P]** can be executed in parallel within their phase (different files, no blocking dependencies).

---

## Dependencies & Execution Order

### User Story Dependency Graph
```
Setup Phase (Phase 1)
  ↓
Foundational Phase (Phase 2)
  ↓
┌─────────────────────┬─────────────────────┐
│                     │                     │
User Story 1 (P1) ← User Story 2 (P1)   User Story 5 (P3)
Sign-In Flow         Chat Messaging        Session Persistence
  ↓                     ↓                     ↓
  └──────┬──────────────┘                     │
         ↓                                    │
  ┌──────┴──────────┐                        │
  │                 │                        │
User Story 3 (P2) User Story 4 (P2)         │
Auth Errors       Chat Errors               │
  │                 │                        │
  └────────┬────────┘                        │
           ↓                                 │
           └─────────────┬───────────────────┘
                         ↓
                    Polish Phase
```

**Key Dependencies**:
- **US2 depends on US1**: Chat requires authentication context (checking `isAuthenticated`)
- **US3 depends on US1**: Auth error handling builds on auth flow
- **US4 depends on US2**: Chat error handling builds on chat messaging
- **US5 is independent**: Can be developed in parallel with US3/US4 after US1 complete

**Recommended Order**: Phase 1 → Phase 2 → US1 → US2 (MVP) → US3 → US4 → US5 → Polish

---

## Phase 1: Setup (Environment & Prerequisites)

**Goal**: Verify development environment and backend API connectivity

**Tasks**:

- [ ] T001 Verify backend is running and accessible at http://localhost:8000/docs (Swagger UI should load)
- [ ] T002 Verify frontend environment variables - confirm REACT_APP_BACKEND_URL is set in frontend/.env (default: http://localhost:8000)

**Acceptance**:
- Backend Swagger UI accessible at /docs
- Frontend can reach backend (no CORS errors on test fetch)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create shared types and utilities needed by all user stories

**Tasks**:

- [ ] T003 [P] Create TypeScript interface for LoginRequest in frontend/src/types/auth.ts matching backend contract (email: string, password: string)
- [ ] T004 [P] Create TypeScript interface for LoginResponse in frontend/src/types/auth.ts matching backend contract (access_token: string, user_id: string, token_type: string)
- [ ] T005 [P] Create TypeScript interface for ChatMessage in frontend/src/types/chat.ts (id: string, content: string, sender: 'user'|'ai', timestamp: string, status: 'sending'|'delivered'|'failed', agentName?: string)

**Acceptance**:
- All TypeScript interfaces match backend Pydantic models
- No type errors when importing interfaces

**Parallel Execution Example**:
```bash
# Run these 3 tasks in parallel (different files)
Task T003 | Task T004 | Task T005
```

---

## Phase 3: User Story 1 - Successful Sign-In and Chat Access (P1)

**Story Goal**: Enable users to sign in with valid credentials, store authentication token, and access chatbot UI

**Independent Test Criteria**:
- ✅ Sign-in page renders at /auth/signin with email and password fields
- ✅ Valid credentials trigger POST /auth/login and receive access_token
- ✅ Token and user stored in localStorage (keys: 'authToken', 'user')
- ✅ Authenticated state restored on page reload
- ✅ Chat widget visible and interactive for authenticated users
- ✅ Chat widget shows "Sign in to chat" prompt for unauthenticated users

**Tasks**:

- [ ] T006 [US1] Create sign-in page component at frontend/src/pages/auth/signin.tsx with email and password input fields, submit button, and error display area
- [ ] T007 [US1] Implement form submission handler in signin.tsx that calls AuthContext.login(email, password) on submit
- [ ] T008 [US1] Add loading state to signin.tsx - disable submit button and show "Signing in..." text while request is pending
- [ ] T009 [US1] Implement redirect to home page (/) in signin.tsx after successful login using useNavigate from @docusaurus/router
- [ ] T010 [US1] Update ChatWidget.tsx to import useAuth hook and check isAuthenticated before opening chat window
- [ ] T011 [US1] Add unauthenticated user prompt in ChatWidget.tsx - when user clicks widget and isAuthenticated is false, display "Sign in to chat" message with link to /auth/signin
- [ ] T012 [US1] Verify AuthContext.logout() clears authToken and user from localStorage (existing code in AuthContext.tsx:86-90 should already do this - just verify)

**Acceptance**:
- Sign-in page accessible at /auth/signin
- Valid credentials (from backend test data) successfully authenticate
- localStorage contains authToken and user after login
- Page reload maintains authenticated state
- Chat widget shows appropriate UI based on auth state

**Parallel Execution Example**:
```bash
# T006-T009 are sequential (same file: signin.tsx)
# T010-T011 can run after T006-T009 complete (different file: ChatWidget.tsx)
# T012 is verification only (can run anytime after Phase 2)

Sequential: T006 → T007 → T008 → T009
Then Parallel: T010 | T011 | T012
```

---

## Phase 4: User Story 2 - Send Messages and Receive Chatbot Responses (P1)

**Story Goal**: Enable authenticated users to send messages to AI tutor and receive responses

**Independent Test Criteria**:
- ✅ Authenticated user can open chat window
- ✅ User message sent triggers POST /chat with {message: "text"}
- ✅ Chat service validates message length (3-10,000 chars) before sending
- ✅ User message appears in chat with status "sending" → "delivered"
- ✅ AI response appears in chat with agent name and timestamp
- ✅ Chat history persists in localStorage during session

**Tasks**:

- [ ] T013 [P] [US2] Create ChatMessage component in frontend/src/components/ChatWidget/ChatMessage.tsx to render individual messages with sender, content, timestamp, and status indicator
- [ ] T014 [P] [US2] Implement message validation function in ChatWindow.tsx - validate message length (3-10,000 chars trimmed) before calling chat service
- [ ] T015 [US2] Update ChatWindow.tsx to manage messages state array and load initial chat history from localStorage (key: 'chatHistory') on component mount
- [ ] T016 [US2] Implement handleSendMessage function in ChatWindow.tsx that adds user message to state with status 'sending', calls chatService.sendMessage(), updates status to 'delivered' on success
- [ ] T017 [US2] Add AI response handling in ChatWindow.tsx - when chatService.sendMessage() succeeds, append AI message to messages state with content from response.response field

**Acceptance**:
- User can type and send messages
- Messages validated for length before sending
- User messages show sending status
- AI responses appear in chat
- Chat history saved to localStorage

**Parallel Execution Example**:
```bash
# T013 and T014 are independent (different concerns)
# T015-T017 are sequential (same file, build on each other)

Parallel: T013 | T014
Then Sequential: T015 → T016 → T017
```

---

## Phase 5: User Story 3 - Handle Authentication Errors (P2)

**Story Goal**: Display clear error messages for authentication failures (401, 500, network errors)

**Independent Test Criteria**:
- ✅ Invalid credentials show "Invalid email or password. Please try again."
- ✅ Backend 500 error shows "The service is temporarily unavailable. Please try again later."
- ✅ Network error shows "Network error. Please check your connection."
- ✅ Errors logged to console with timestamp (FR-016)
- ✅ Error messages clear when user tries again

**Tasks**:

- [ ] T018 [P] [US3] Add error state (useState) to signin.tsx to store and display error messages below form fields
- [ ] T019 [US3] Implement error handling in signin.tsx handleSubmit - catch errors from AuthContext.login() and map to user-friendly messages based on error type (401 → "Invalid email or password", 500 → "Service unavailable", network → "Network error")
- [ ] T020 [US3] Add client-side error logging in signin.tsx error handler - console.error with timestamp, email (not password), and error message (FR-016)
- [ ] T021 [US3] Clear error message in signin.tsx when user starts typing in email or password fields (add onChange handlers)

**Acceptance**:
- Error messages display correctly for each error type
- Errors logged to console with proper format
- UI provides clear recovery path

**Parallel Execution Example**:
```bash
# All tasks in signin.tsx (sequential)
T018 → T019 → T020 → T021
```

---

## Phase 6: User Story 4 - Handle Chat Communication Errors (P2)

**Story Goal**: Handle chat endpoint errors (422, 429, 500, 504) with clear feedback and recovery options

**Independent Test Criteria**:
- ✅ Empty message shows validation error before sending
- ✅ Message >10,000 chars shows validation error before sending
- ✅ Backend 500 error shows "Failed to send message. Please try again." with retry button
- ✅ Rate limit (429) shows "You've sent too many messages. Please wait X seconds."
- ✅ Timeout (504) shows "Request timeout. Please try again later."

**Tasks**:

- [ ] T022 [P] [US4] Add character counter UI in ChatWindow.tsx input area showing remaining characters (10000 - inputLength) with color coding (red <100, orange <500, gray otherwise)
- [ ] T023 [US4] Implement error handling in ChatWindow.tsx handleSendMessage - catch errors from chatService.sendMessage() and update message status to 'failed'
- [ ] T024 [US4] Add retry button to failed messages in ChatMessage.tsx - when status is 'failed', display "Retry" button that calls handleSendMessage again with same message content
- [ ] T025 [US4] Implement rate limit countdown timer in ChatWindow.tsx - when 429 error occurs, parse Retry-After header (default 30s), display countdown, and disable send button until timer expires

**Acceptance**:
- Message validation prevents invalid sends
- Failed messages show retry option
- Rate limit displays countdown
- All error states provide recovery path

**Parallel Execution Example**:
```bash
# T022 is UI-only (can run early)
# T023-T025 are sequential (error handling flow)

Start with: T022
Then Sequential: T023 → T024 → T025
```

---

## Phase 7: User Story 5 - Maintain Session State (P3)

**Story Goal**: Restore authentication state from localStorage and clear chat history on logout

**Independent Test Criteria**:
- ✅ Close browser, reopen → user still authenticated (within 24h token validity)
- ✅ Logout clears authToken, user, chatHistory, chatRateLimit from localStorage
- ✅ Expired token detected on page load → user logged out and redirected

**Tasks**:

- [ ] T026 [P] [US5] Update AuthContext.tsx logout() method to clear chatHistory and chatRateLimit from localStorage in addition to authToken and user (lines 86-90)
- [ ] T027 [P] [US5] Save chat messages to localStorage in ChatWindow.tsx useEffect - whenever messages state changes, save to localStorage with key 'chatHistory'

**Acceptance**:
- Authentication persists across browser sessions
- Logout clears all user data including chat history
- Session expiry handled gracefully

**Parallel Execution Example**:
```bash
# T026 and T027 are independent (different files)
T026 | T027
```

---

## Phase 8: Polish & Cross-Cutting Concerns (Final Phase)

**Goal**: Final UX polish and validation

**Tasks**:

- [ ] T028 Run TypeScript type check (npm run typecheck in frontend/) and fix any type errors in signin.tsx, ChatWidget.tsx, ChatWindow.tsx, ChatMessage.tsx

**Acceptance**:
- No TypeScript errors
- All components follow coding standards
- Performance meets spec requirements (SC-001, SC-003, SC-004)

---

## Testing Strategy

**Note**: Tests are NOT included in this task list as they were not explicitly requested in the specification. The spec focuses on manual integration testing and TypeScript type checking.

**Manual Testing Checklist** (from quickstart.md):

### Authentication Flow
- [ ] Sign-in page renders at /auth/signin
- [ ] Valid credentials trigger successful login
- [ ] Invalid credentials show error message "Invalid email or password"
- [ ] Network error shows "Network error. Please check your connection"
- [ ] Loading state disables button and shows "Signing in..."
- [ ] Successful login redirects to home page
- [ ] Already authenticated users are redirected from sign-in page
- [ ] Token and user stored in localStorage after login
- [ ] Page refresh maintains authenticated state

### Chat Integration
- [ ] Chat widget button visible to all users
- [ ] Unauthenticated users see "Sign in to chat" message when clicking widget
- [ ] Authenticated users can open chat window
- [ ] Messages sent successfully to backend
- [ ] AI responses displayed in chat window
- [ ] Chat history persists across page reloads
- [ ] Chat history cleared on logout
- [ ] Rate limit state cleared on logout

### Error Handling
- [ ] Empty message shows validation error
- [ ] Message < 3 characters shows "Message must be at least 3 characters"
- [ ] Message > 10,000 characters shows error
- [ ] Character counter updates in real-time
- [ ] 429 error shows rate limit message with countdown
- [ ] 500 error shows "Service temporarily unavailable"
- [ ] 504 error shows "Request timeout"
- [ ] Failed messages show retry button
- [ ] Network errors handled gracefully

### Session Management
- [ ] Logout clears authToken, user, chatHistory, chatRateLimit from localStorage
- [ ] 401 error triggers logout and redirect to sign-in
- [ ] Expired token detected and user logged out

---

## Implementation Notes

### Key Files to Modify

**Create New**:
- `frontend/src/pages/auth/signin.tsx` (US1: T006-T009)
- `frontend/src/types/auth.ts` (Foundational: T003-T004)
- `frontend/src/types/chat.ts` (Foundational: T005)
- `frontend/src/components/ChatWidget/ChatMessage.tsx` (US2: T013)

**Modify Existing**:
- `frontend/src/components/ChatWidget/ChatWidget.tsx` (US1: T010-T011)
- `frontend/src/components/ChatWidget/ChatWindow.tsx` (US2: T014-T017, US4: T022-T025, US5: T027)
- `frontend/src/contexts/AuthContext.tsx` (US1: T012 verify, US5: T026 update)

**Already Implemented (No Changes Needed)**:
- `frontend/src/contexts/AuthContext.tsx` - login(), register(), logout() methods
- `frontend/src/contexts/ChatContext.tsx` - chat visibility state
- `frontend/src/components/ChatWidget/chat-service.ts` - sendMessage() with rate limiting
- `backend/src/auth/routes/login.py` - /auth/login endpoint
- `backend/src/backend/main.py` - /chat endpoint

### Code References

- AuthContext login implementation: `frontend/src/contexts/AuthContext.tsx:42-66`
- AuthContext logout implementation: `frontend/src/contexts/AuthContext.tsx:86-91`
- Chat service sendMessage: `frontend/src/components/ChatWidget/chat-service.ts:57-111`
- Backend auth endpoint: `backend/src/auth/routes/login.py:19-50`
- Backend chat endpoint: `backend/src/backend/main.py:60-117`

### Performance Considerations

- **T016**: Debounce localStorage writes if chat history becomes large (>100 messages)
- **T013**: Use React.memo() for ChatMessage component to prevent unnecessary re-renders
- **T022**: Debounce character counter updates (update every 100ms instead of every keystroke)

### Security Considerations

- **T006**: Never log password values (only log email and error messages)
- **T020**: Ensure error logs don't contain sensitive user data
- **T017**: Sanitize AI response content before rendering (use DOMPurify or escape HTML)
- **T026**: Consider migrating from localStorage to HttpOnly cookies in future for XSS protection

---

## MVP Deliverable (User Stories 1 + 2)

**Tasks**: T001-T017 (17 tasks including setup)
**Estimated Effort**: 6-8 hours
**Deliverable**: Users can sign in and chat with AI tutor

**Acceptance Criteria**:
- Sign-in page functional with valid credentials
- Authentication state persisted in localStorage
- Chat widget shows based on auth state
- Users can send messages and receive AI responses
- Chat history persists during session

**To Run MVP**:
1. Complete Phase 1 (Setup): T001-T002
2. Complete Phase 2 (Foundational): T003-T005
3. Complete Phase 3 (US1): T006-T012
4. Complete Phase 4 (US2): T013-T017
5. Test end-to-end flow: Sign in → Open chat → Send message → Receive response

---

## Full Feature Deliverable (All User Stories)

**Tasks**: T001-T028 (28 tasks)
**Estimated Effort**: 10-12 hours
**Deliverable**: Complete authentication and chat integration with error handling and session persistence

**Acceptance Criteria**: All success criteria from spec.md (SC-001 through SC-010)

**To Run Full Feature**:
1. Complete MVP (T001-T017)
2. Complete Phase 5 (US3): T018-T021
3. Complete Phase 6 (US4): T022-T025
4. Complete Phase 7 (US5): T026-T027
5. Complete Phase 8 (Polish): T028
6. Run full manual testing checklist above

---

## Task Format Validation

✅ All tasks follow required format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ Task IDs sequential (T001-T028)
✅ [P] marker on parallelizable tasks (12 tasks marked)
✅ [Story] labels on user story tasks (US1-US5)
✅ File paths included in all implementation tasks
✅ Dependencies documented in phase descriptions

---

## Questions or Issues?

Refer to:
- **spec.md** for detailed requirements and acceptance scenarios
- **plan.md** for architectural decisions and technical context
- **data-model.md** for entity definitions and validation rules
- **contracts/auth-api.md** for authentication API contract
- **contracts/chat-api.md** for chat API contract
- **quickstart.md** for implementation examples and common issues

**Next Step**: Start with Phase 1 (Setup) and proceed sequentially through phases, or jump straight to MVP by completing Phases 1-4.
