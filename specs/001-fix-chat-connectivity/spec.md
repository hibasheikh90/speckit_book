# Feature Specification: Fix Chat Frontend-Backend Connectivity

**Feature Branch**: `001-fix-chat-connectivity`
**Created**: 2025-12-25
**Status**: Draft
**Input**: User description: "Fix chatbot frontend: UI is visible but messages are not sending/receiving. Properly connect the frontend chat widget to the backend /chat POST endpoint (Cohere API) so real responses appear. Do not change backend."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Send Message and Receive AI Response (Priority: P1)

Students can type questions in the chat widget and receive educational responses from the AI tutor powered by Cohere, enabling real-time learning assistance while reading the textbook.

**Why this priority**: This is the core functionality of the chat feature - without it, the chat widget is non-functional. This represents the minimum viable product (MVP) that delivers actual value to users.

**Independent Test**: Open the textbook website, type "How does a humanoid robot balance?" in the chat widget, send it, and verify an educational response appears from the AI tutor within a few seconds.

**Acceptance Scenarios**:

1. **Given** the student has the textbook open with the chat widget visible, **When** they type a valid question (3-10,000 characters) and click Send, **Then** the message appears immediately in the chat history and a typing indicator shows while waiting for the AI response
2. **Given** a message has been successfully sent to the backend, **When** the Cohere API returns a response, **Then** the AI tutor's response appears in the chat history with proper formatting and the typing indicator disappears
3. **Given** the student sends a message, **When** the backend /chat endpoint processes the request, **Then** the frontend displays the complete response text returned from Cohere in the chat conversation

---

### User Story 2 - Handle Connection Errors Gracefully (Priority: P2)

When the backend service is unavailable or network issues occur, students see clear error messages explaining the problem and can retry, preventing confusion and frustration.

**Why this priority**: While not core functionality, good error handling is essential for user experience and helps users understand when technical issues occur versus content issues.

**Independent Test**: Stop the backend service, attempt to send a chat message, and verify a user-friendly error message appears (e.g., "Unable to connect. Please check your connection.") instead of the app crashing or hanging indefinitely.

**Acceptance Scenarios**:

1. **Given** the backend service is not running or unreachable, **When** the student attempts to send a message, **Then** an error message displays in the chat explaining the connection issue and the message is not lost
2. **Given** the request to the backend times out after 30 seconds, **When** no response is received, **Then** a timeout error message appears and the student can retry sending the message
3. **Given** the backend returns a 500 Internal Server Error, **When** processing the response, **Then** the frontend displays "Service temporarily unavailable. Please try again." instead of technical error details

---

### User Story 3 - Respect Rate Limits (Priority: P2)

The chat widget enforces rate limiting (3 messages per 30 seconds) to prevent abuse and ensure fair usage, while clearly communicating when students need to wait before sending another message.

**Why this priority**: Protects the backend infrastructure and Cohere API costs while ensuring fair access. Important for production but not needed for basic functionality testing.

**Independent Test**: Send 3 messages rapidly in succession, then attempt a 4th message immediately - verify it's blocked with a clear countdown message like "Rate limit reached. Please wait 15 seconds before sending another message."

**Acceptance Scenarios**:

1. **Given** the student has sent 3 messages within the last 30 seconds, **When** they attempt to send a 4th message, **Then** the send button is disabled and a countdown timer shows how many seconds remain until they can send again
2. **Given** the rate limit window has expired (30 seconds passed since the oldest of the 3 messages), **When** the timer reaches zero, **Then** the send button re-enables and the student can send new messages
3. **Given** rate limit information is tracked locally, **When** the student refreshes the page, **Then** the rate limit state persists via localStorage and continues enforcing the remaining wait time

---

### Edge Cases

- What happens when the network connection drops mid-request (e.g., user switches to airplane mode)?
  - The fetch request will fail with a network error, triggering the catch block that displays "Unable to connect. Please check your connection."
- How does the system handle very long AI responses (>10,000 characters) from Cohere?
  - The backend doesn't enforce maximum response length - the frontend will display the full response regardless of length. (Future enhancement could truncate or paginate extremely long responses.)
- What happens if the user sends a message containing special characters or emojis?
  - The backend accepts UTF-8 encoded JSON, so special characters and emojis are supported. The message is JSON.stringify'd which properly escapes special characters.
- How does the chat behave when the user has multiple browser tabs open?
  - Each tab maintains its own chat session with independent state in memory, but shares localStorage for persistence. Rate limiting is per-tab, not global across tabs.
- What happens if the REACT_APP_BACKEND_URL environment variable is not set or points to an invalid URL?
  - The chat service defaults to 'http://localhost:8000'. If this is invalid, all requests will fail with connection errors shown to the user.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chat widget MUST successfully send user messages to the backend `/chat` POST endpoint at the URL specified in `REACT_APP_BACKEND_URL` environment variable (defaults to http://localhost:8000)
- **FR-002**: The frontend MUST include the `Content-Type: application/json` and `Accept: application/json` headers in the POST request to match the backend's expected format
- **FR-003**: The request payload MUST contain a JSON object with a `message` property containing the user's trimmed message text (e.g., `{"message": "How do robots work?"}`)
- **FR-004**: The frontend MUST handle the backend's response format which includes `response` (the AI text), `agent_name` (agent identifier), and `timestamp` (ISO 8601 datetime) fields
- **FR-005**: When a successful response (HTTP 200) is received, the system MUST extract the `response` field and display it as a new message from the 'tutor' sender in the chat history
- **FR-006**: The chat widget MUST display a typing indicator while waiting for the backend response to provide visual feedback that processing is occurring
- **FR-007**: The system MUST validate that messages are between 3 and 10,000 characters before sending, matching the backend's validation rules
- **FR-008**: The system MUST prevent sending messages that contain only whitespace (after trimming) to avoid wasting API calls
- **FR-009**: When the backend returns error responses (422 validation error, 429 rate limit, 500 server error, 504 timeout), the frontend MUST display appropriate user-friendly error messages in the chat
- **FR-010**: The frontend MUST enforce client-side rate limiting (3 requests per 30-second window) to complement the backend's rate limiting and prevent unnecessary failed requests
- **FR-011**: The chat service MUST handle network errors (connection refused, DNS failure, network timeout) gracefully by displaying "Unable to connect. Please check your connection."
- **FR-012**: The environment variable `REACT_APP_BACKEND_URL` MUST be properly loaded at build time for the chat service to connect to the correct backend URL
- **FR-013**: The frontend build process (Docusaurus) MUST be restarted when `.env` file changes to pick up new environment variable values
- **FR-014**: CORS headers on the backend MUST allow requests from the frontend origin (typically http://localhost:3000 for development) to prevent CORS-related connection failures
- **FR-015**: User messages and AI responses MUST persist in localStorage under the `chatSession` key so conversations survive page refreshes

### Key Entities

- **ChatRequest**: Represents an outgoing message to the backend containing the user's question or statement as a text string between 3-10,000 characters
- **ChatResponse**: Represents the backend's reply containing the AI tutor's response text, the agent name, and a timestamp of when the response was generated
- **ChatMessage**: A single message in the conversation history containing id, content, sender type (student/tutor/system), timestamp, status (sent/received/pending/error), and typing indicator flag
- **ChatSession**: The complete conversation state including all messages, connection status, last activity time, rate limit tracking, and a unique session identifier
- **RateLimitInfo**: Tracking information for client-side rate limiting including request timestamps, maximum allowed requests, and time window duration

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can send a message and receive an AI response within 5 seconds under normal network conditions (95th percentile)
- **SC-002**: The chat widget successfully connects to the backend on first message send with 100% success rate when backend service is running
- **SC-003**: Error messages appear within 1 second when connection failures occur, providing immediate feedback to users
- **SC-004**: Rate limiting prevents more than 3 messages being sent in a 30-second window, with 100% enforcement accuracy
- **SC-005**: Chat conversations persist across page refreshes with 100% message retention using localStorage
- **SC-006**: The typing indicator appears immediately when sending a message and disappears within 1 second of receiving the response

## Assumptions

- The backend `/chat` endpoint is already implemented and functional (confirmed in backend/src/backend/main.py)
- The backend accepts JSON payloads with a `message` field and returns JSON responses with `response`, `agent_name`, and `timestamp` fields
- The backend has CORS configured to accept requests from the frontend development server (http://localhost:3000) and production domains
- The Cohere API integration on the backend is working correctly and returning valid responses
- The `REACT_APP_BACKEND_URL` environment variable is the standard way to configure the backend URL in Docusaurus/React apps
- Environment variables in React apps require a rebuild to take effect (standard Create React App / Docusaurus behavior)
- The chat-service.ts implementation is correct and the issue is environmental (configuration, CORS, or backend availability)
- Students will primarily use the chat on desktop browsers (Chrome, Firefox, Safari, Edge) with modern JavaScript support
- The backend is hosted on localhost:8000 for development and will use a production URL when deployed
- Rate limiting on the frontend (3 requests/30 seconds) is more restrictive than backend limits (10 requests/minute) to provide better UX

## Dependencies

- **Backend Service**: The FastAPI backend service must be running and accessible at the URL specified in `REACT_APP_BACKEND_URL`
- **Cohere API**: The backend depends on Cohere's API being available and the API key being valid (configured in backend/.env)
- **Environment Variables**: The frontend depends on `.env` file containing `REACT_APP_BACKEND_URL` being present before build
- **CORS Configuration**: The backend must have CORS middleware properly configured to allow the frontend origin
- **Browser APIs**: The chat depends on fetch API, localStorage, and standard ES6+ JavaScript features available in modern browsers
- **Docusaurus Build**: Changes to environment variables require stopping and restarting the Docusaurus development server (npm start)

## Out of Scope

- Implementing server-sent events (SSE) or WebSocket streaming for real-time response tokens (frontend has streaming code but backend doesn't support it yet)
- Adding authentication/authorization to the chat endpoint (explicitly removed from backend per recent changes)
- Modifying the backend API contract, response format, or validation rules
- Implementing chat history storage on the backend (only client-side localStorage is in scope)
- Adding file upload, image sharing, or rich media features to the chat
- Implementing multi-user chat or conversation sharing between students
- Adding conversation export or download features
- Modifying the visual design or UI layout of the chat widget (only functionality fixes)
- Implementing read receipts, message reactions, or other social features
- Adding analytics or tracking for chat usage patterns
- Optimizing the Cohere prompt engineering or AI response quality (backend concern)

## Security Considerations

- All communication with the backend uses HTTPS in production to encrypt sensitive educational questions and responses
- The chat does not require authentication (per backend design), but this means any user can access the AI tutor
- Rate limiting (3 requests/30 seconds client-side, 10 requests/minute backend-side) prevents abuse and excessive API costs
- User messages are validated for length (3-10,000 characters) to prevent oversized requests
- No personally identifiable information (PII) should be included in chat messages as conversations are not tied to user accounts
- The Cohere API key is stored server-side and never exposed to the frontend
- CORS restrictions ensure only authorized frontend origins can call the backend API
- XSS attacks are mitigated by React's automatic escaping of user content in the chat display
- localStorage data is domain-scoped and not shared across different websites

## Performance Requirements

- Chat messages must send and receive responses within 5 seconds (95th percentile) under normal network conditions
- The typing indicator must appear within 100ms of clicking Send to provide immediate feedback
- The chat widget must load and be interactive within 1 second of page load
- localStorage operations (save/load session) must complete within 50ms to avoid blocking the UI
- The rate limit countdown timer must update every second with no noticeable lag or jank
- The chat widget must support up to 100 messages in a session without performance degradation
- Network requests must timeout after 30 seconds maximum to prevent indefinite hanging

## Validation & Testing Strategy

### Functional Testing

1. **Basic Connectivity Test**: Start backend, send message "Hello", verify AI response appears
2. **Environment Variable Test**: Modify `REACT_APP_BACKEND_URL`, rebuild, verify connection uses new URL
3. **Error Handling Test**: Stop backend, send message, verify error message appears
4. **Rate Limit Test**: Send 4 messages rapidly, verify 4th is blocked with countdown
5. **Persistence Test**: Send messages, refresh page, verify messages still visible
6. **Validation Test**: Try sending 2-character message, verify blocked with validation error
7. **Validation Test**: Try sending whitespace-only message, verify blocked

### Integration Testing

1. **End-to-End Flow**: User types → sends → sees typing indicator → receives AI response → response displayed correctly
2. **CORS Test**: Frontend on localhost:3000, backend on localhost:8000, verify no CORS errors
3. **Backend Response Format Test**: Verify frontend correctly parses `response`, `agent_name`, and `timestamp` fields
4. **Timeout Test**: Artificially delay backend response, verify frontend handles timeouts gracefully

### Error Scenario Testing

1. **Network Failure**: Disconnect network mid-request, verify error handling
2. **500 Server Error**: Mock backend returning 500, verify user-friendly error
3. **422 Validation Error**: Send invalid payload format, verify error handling
4. **429 Rate Limit**: Trigger backend rate limit, verify error message
5. **504 Timeout**: Backend takes >30 seconds, verify timeout error

### Performance Testing

1. **Response Time**: Measure time from send to response displayed (target: <5s p95)
2. **Multiple Messages**: Send 50 messages in a session, verify no slowdown
3. **Large Responses**: Backend returns 5000-character response, verify renders smoothly

## Documentation Requirements

- Update the project README with instructions for configuring `REACT_APP_BACKEND_URL`
- Document the requirement to rebuild/restart Docusaurus when changing environment variables
- Create troubleshooting guide covering common issues (CORS errors, backend not running, wrong URL)
- Document the rate limiting behavior (3 messages/30 seconds) for users
- Include example .env file (`frontend/.env.example`) with required environment variables
- Add developer documentation explaining the chat service architecture and API contract

## Rollback Plan

If the fixes introduce regressions or new issues:

1. **Revert Environment Changes**: Restore previous `.env` file values
2. **Rebuild Frontend**: Run `npm run build` to revert to previous environment configuration
3. **Revert Code Changes**: Git revert any code modifications to chat-service.ts, ChatWindow.tsx, or environment files
4. **Clear localStorage**: Instruct users to clear `chatSession` from localStorage if corrupt session state is causing issues
5. **Fallback Message**: Display static message in chat: "Chat temporarily unavailable. Please try again later."

The risk is low since we're not modifying the backend and the frontend changes are isolated to environment configuration and potentially minor bug fixes in the existing chat service code.
