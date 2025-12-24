# Research: Connect Frontend Authentication and Chat to Backend APIs

**Date**: 2025-12-23
**Feature**: 001-connect-frontend-backend-apis
**Purpose**: Resolve technical unknowns and document best practices for integrating React frontend with FastAPI backend

## Research Questions & Findings

### 1. React Context Integration with FastAPI Authentication

**Question**: What is the best practice for integrating React Context API with FastAPI JWT authentication in a Docusaurus application?

**Research Findings**:
- **Existing Implementation Analysis**: The codebase already has a well-structured `AuthContext.tsx` that implements:
  - Token storage in localStorage with key `authToken`
  - User object storage with key `user` containing `{id, email}`
  - Automatic token restoration on component mount via `useEffect`
  - Login, register, and logout methods that manage both state and localStorage
  - `isAuthenticated` computed property based on token existence

**Decision**: Use the existing `AuthContext` implementation without modifications. It already follows React best practices:
- Single source of truth for auth state
- Automatic persistence and restoration
- Clean separation of concerns (state management in context, API calls in methods)

**Rationale**: The existing implementation is production-ready and follows industry standards. No need to introduce new patterns.

**Alternatives Considered**:
- Redux for state management: Rejected - overkill for 2 contexts, adds unnecessary complexity
- TanStack Query (React Query): Rejected - existing pattern works well, no need for cache management
- Zustand: Rejected - team is already familiar with Context API

---

### 2. Error Handling Strategy for Authentication Failures

**Question**: How should we handle and display various authentication error types (401, 500, network errors) to users?

**Research Findings**:
- **Current AuthContext Implementation**: Already handles errors by:
  - Catching response errors and parsing `response.json()` for `detail` field
  - Throwing errors with user-friendly messages
  - Falling back to generic messages if parsing fails

**Decision**: Enhance error handling with specific error types per spec requirements (FR-003):
- 401 Unauthorized → "Invalid email or password. Please try again."
- 500 Internal Server Error → "The service is temporarily unavailable. Please try again later."
- Network errors (timeout, offline) → "Network error. Please check your connection."
- Unknown errors → "An unexpected error occurred. Please try again."

**Rationale**: Users need clear, actionable feedback. Technical error messages (stack traces, API error codes) should be logged client-side but not displayed to users (per FR-016).

**Implementation Pattern**:
```typescript
try {
  await login(email, password);
} catch (error) {
  if (error.message.includes('401') || error.message.includes('Invalid')) {
    setErrorMessage('Invalid email or password. Please try again.');
  } else if (error.message.includes('500')) {
    setErrorMessage('The service is temporarily unavailable. Please try again later.');
  } else if (error.message.includes('Network') || error.message.includes('timeout')) {
    setErrorMessage('Network error. Please check your connection.');
  } else {
    setErrorMessage('An unexpected error occurred. Please try again.');
  }
  console.error('[Auth Error]', { timestamp: new Date().toISOString(), error }); // FR-016 client-side logging
}
```

---

### 3. Chat Widget Conditional Rendering Based on Auth State

**Question**: How should the chat widget handle unauthenticated users per FR-014 (visible but disabled with "Sign in to chat" message)?

**Research Findings**:
- **Current ChatWidget Implementation**: Uses `ChatContext.isChatVisible` to control visibility entirely (returns `null` if not visible)
- **Spec Requirement (FR-014)**: Widget must be visible to unauthenticated users but disabled, showing "Sign in to chat" message when clicked

**Decision**: Modify `ChatWidget.tsx` to check `AuthContext.isAuthenticated`:
```typescript
const { isAuthenticated } = useAuth();
const { isChatVisible, openChat } = useChat();

// Widget button always visible
// Click handler: if authenticated, open chat; else show sign-in prompt
const handleClick = () => {
  if (isAuthenticated) {
    toggleChat();
  } else {
    // Show inline message or redirect to sign-in
    alert('Sign in to chat'); // Replace with better UI (modal or redirect)
  }
};
```

**Rationale**: Makes the feature discoverable to unauthenticated users (better UX) while maintaining security. Aligns with clarification answer from spec session 2025-12-23.

**Alternatives Considered**:
- Hide widget entirely for unauthenticated users: Rejected - poor discoverability
- Allow unauthenticated chat with limited features: Rejected - security risk, not in spec

---

### 4. Chat Message State Management and History Persistence

**Question**: How should chat message history be managed, and when should it be cleared per FR-012?

**Research Findings**:
- **Current Implementation**: No chat history persistence mechanism found in `ChatWidget` or `ChatWindow` components
- **Spec Requirement (FR-012, SC-010)**: Chat history preserved during active session, cleared on sign-out or session expiry

**Decision**: Implement chat history management in `ChatContext` or `ChatService`:
```typescript
interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string;
  status: 'sending' | 'delivered' | 'failed';
}

// Store in localStorage with key 'chatHistory'
// Clear on logout in AuthContext.logout():
localStorage.removeItem('chatHistory');
localStorage.removeItem('chatRateLimit'); // Also clear rate limit state
```

**Rationale**:
- localStorage enables session persistence across page reloads (SC-010)
- Clearing on logout ensures privacy on shared devices (clarification from spec)
- Message status tracking enables retry mechanisms (FR-007)

**Alternatives Considered**:
- Backend-persisted chat history: Rejected - out of scope, frontend-only changes
- sessionStorage instead of localStorage: Rejected - doesn't survive browser restarts (conflicts with SC-006)

---

### 5. Rate Limiting Implementation (Client-Side vs Backend)

**Question**: Should rate limiting be enforced client-side only, or should we handle backend 429 errors?

**Research Findings**:
- **Current chat-service.ts Implementation**: Already implements client-side rate limiting:
  - Tracks request timestamps in `rateLimit.requests` array
  - Limits: 3 requests per 30 seconds
  - Throws error if limit exceeded
- **Backend Implementation**: Backend already has slowapi rate limiting (FR-015)

**Decision**: Keep both client-side and backend rate limiting (defense in depth):
1. Client-side: Prevent requests before they're sent (better UX, reduces backend load)
2. Backend: Protect against abuse from malicious clients or multiple tabs
3. Handle 429 responses gracefully with countdown timer if backend includes retry-after header

**Rationale**: Client-side prevents unnecessary requests. Backend prevents abuse. Both are necessary.

**Implementation Enhancement**:
```typescript
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  const message = retryAfter
    ? `Rate limit exceeded. Please wait ${retryAfter} seconds.`
    : 'You\'ve sent too many messages. Please wait before trying again.';
  throw new Error(message);
}
```

---

### 6. TypeScript Type Safety for API Requests and Responses

**Question**: How should we ensure type safety between frontend TypeScript and backend Pydantic models?

**Research Findings**:
- **Backend Models**:
  - `UserLoginRequest`: `{email: str, password: str}`
  - `UserLoginResponse`: `{access_token: str, user_id: str, token_type: str}`
  - `ChatRequest`: `{message: str}`
  - `ChatResponse`: `{response: str, agent_name: str, timestamp: str (auto-generated)}`

**Decision**: Define matching TypeScript interfaces in frontend:
```typescript
// auth-service.ts (NEW FILE)
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  user_id: string;
  token_type: string;
}

// chat-service.ts (ALREADY EXISTS)
export interface ChatRequest {
  message: string;
  sessionId?: string; // Optional, not used by backend
}

export interface ChatResponse {
  response: string;
  agent_name: string;
  timestamp: string;
}
```

**Rationale**: Compile-time type checking prevents runtime errors. If backend contracts change, TypeScript will catch mismatches during build.

**Best Practice**: Consider code generation tools for future (openapi-typescript) but manual typing is sufficient for 2 endpoints.

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Auth Integration** | Use existing `AuthContext` as-is | Already production-ready, follows best practices |
| **Error Handling** | User-friendly messages, client-side logging | Per FR-003, FR-016; don't expose technical details |
| **Chat Widget Auth** | Visible but disabled for unauthenticated users | Better discoverability, per clarification |
| **Chat History** | localStorage, cleared on logout | Privacy (shared devices), persistence (SC-006, SC-010) |
| **Rate Limiting** | Client-side + backend (defense in depth) | Better UX + security |
| **Type Safety** | Manual TypeScript interfaces matching backend | Compile-time safety without tooling overhead |

---

## Risks Identified

1. **localStorage XSS Vulnerability**: Tokens in localStorage vulnerable to XSS attacks
   - **Mitigation**: Acceptable for MVP, document upgrade to HttpOnly cookies in future ADR
   - **Priority**: P3 (deferred)

2. **No Token Expiry Handling**: Frontend doesn't check JWT expiry before API calls
   - **Mitigation**: Backend returns 401 for expired tokens; frontend handles via error flow
   - **Priority**: P2 (handled by existing error handling pattern)

3. **Concurrent Auth Requests**: Multiple rapid sign-in submissions could create race conditions
   - **Mitigation**: Add loading state to sign-in button (disable during request)
   - **Priority**: P2 (add to tasks)

---

## Open Questions (Resolved)

All research questions resolved. No blockers identified. Ready to proceed to Phase 1 (data model and contracts).
