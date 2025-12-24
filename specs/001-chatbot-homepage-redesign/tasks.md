# Tasks: Chatbot Homepage Integration and UI Redesign

**Feature Branch**: `001-chatbot-homepage-redesign`
**Created**: 2025-12-24
**Status**: In Progress
**Spec**: [spec.md](./spec.md)

## Task Completion Status

- [ ] Phase 1: Backend Integration & Auth Cleanup (3 tasks)
- [ ] Phase 2: Homepage Integration (2 tasks)
- [ ] Phase 3: Modern UI Redesign (4 tasks)
- [ ] Phase 4: Input Validation & Rate Limiting (3 tasks)
- [ ] Phase 5: Error Handling & User Feedback (3 tasks)
- [ ] Phase 6: Testing & Quality Assurance (4 tasks)

---

## Phase 1: Backend Integration & Auth Cleanup

### Task 1.1: Complete Frontend Auth Removal ✅ IN PROGRESS

**Priority**: P1 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Remove all authentication-related code from the frontend chat service to align with the backend's current auth-free implementation.

**Files to Modify**:
- `frontend/src/components/ChatWidget/chat-service.ts` (already modified)
- `frontend/src/components/ChatWidget/ChatWidget.tsx` (fix variable reference)

**Changes Already Staged**:
- ✅ Removed `Authorization` header from chat service
- ✅ Removed 401 authentication error handling
- ✅ Fixed `closeGlobalChat()` → `closeChat()` reference

**Acceptance Criteria**:
- [ ] No references to `authToken` in chat-service.ts
- [ ] No 401 error handling in chat methods
- [ ] ChatWidget uses correct `closeChat()` reference from context
- [ ] No console errors when opening/closing chat
- [ ] Chat requests succeed without auth headers

**Test Cases**:
```typescript
// Test: sendMessage without auth token
expect(localStorage.getItem('authToken')).toBeNull();
const response = await chatService.sendMessage("Test message");
expect(response.response).toBeDefined();

// Test: No Authorization header in request
// Verify in DevTools Network tab that POST /chat has no Authorization header
```

**Verification**:
1. Open browser DevTools → Network tab
2. Send a chat message
3. Inspect POST request to `/chat` endpoint
4. Verify NO `Authorization` header is present
5. Verify response is successful (200 OK)

---

### Task 1.2: Verify Backend API Contract Compatibility

**Priority**: P1 | **Estimated Complexity**: Small | **Stage**: red

**Description**: Test that the frontend chat service correctly communicates with the backend `/chat` API using the expected request/response format.

**Files to Inspect**:
- `backend/src/backend/main.py:60-117` (chat endpoint)
- `backend/src/backend/models.py` (ChatRequest, ChatResponse models)
- `frontend/src/components/ChatWidget/chat-service.ts:70-95`

**Acceptance Criteria**:
- [ ] Frontend sends POST to `/chat` with `{ message: string }` body
- [ ] Backend returns `{ response: string, agent_name: string, timestamp?: string }`
- [ ] Frontend correctly extracts `response` field from backend response
- [ ] Rate limiting (3 req/30s) matches backend constraint
- [ ] Error responses are handled gracefully

**Test Cases**:
```bash
# Manual API test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?"}'

# Expected response format:
# { "response": "...", "agent_name": "AI Tutor", "timestamp": "..." }
```

**Verification**:
1. Start backend server: `cd backend && uvicorn src.backend.main:app --reload`
2. Open frontend in browser
3. Send test message through chat UI
4. Verify in Network tab: request body matches `ChatRequest` model
5. Verify response matches `ChatResponse` model
6. Check browser console for any errors

---

### Task 1.3: Add Environment Variable for Backend URL

**Priority**: P1 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Ensure the backend URL is configurable via environment variable with sensible defaults for local development and production.

**Files to Modify**:
- `frontend/src/components/ChatWidget/chat-service.ts:1-20`
- `frontend/.env.example` (create if missing)
- `frontend/.env.local` (for local development)

**Current Implementation**:
```typescript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
```

**Acceptance Criteria**:
- [ ] `REACT_APP_BACKEND_URL` environment variable is documented
- [ ] Default to `http://localhost:8000` for local development
- [ ] `.env.example` file exists with template
- [ ] Chat service uses environment variable correctly
- [ ] No hardcoded URLs in chat-service.ts

**Files to Create**:
```bash
# frontend/.env.example
REACT_APP_BACKEND_URL=http://localhost:8000

# frontend/.env.local (for development, git-ignored)
REACT_APP_BACKEND_URL=http://localhost:8000
```

**Verification**:
1. Check `chat-service.ts:BACKEND_URL` uses environment variable
2. Verify `.env.example` exists and is committed
3. Test with different backend URLs
4. Confirm chat works with default URL

---

## Phase 2: Homepage Integration

### Task 2.1: Integrate ChatWidget into Homepage

**Priority**: P1 | **Estimated Complexity**: Medium | **Stage**: green

**Description**: Add the ChatWidget component to the homepage so users can access the chatbot immediately upon landing on the site.

**Files to Modify**:
- Find homepage component (likely `frontend/src/pages/index.tsx` or similar Docusaurus page)
- Import and render `ChatWidgetWithProvider` or `ChatWidget`

**Dependencies**:
- Requires ChatContext provider to be available
- May need to wrap homepage in ChatProvider if not already done

**Acceptance Criteria**:
- [ ] ChatWidget button is visible on homepage
- [ ] Button is positioned in bottom-right corner (or specified location)
- [ ] Button is accessible and clickable
- [ ] Clicking button opens chat window
- [ ] Chat widget doesn't interfere with homepage content
- [ ] Widget persists when scrolling page

**Investigation Required**:
1. Locate homepage component file
2. Check if ChatProvider is already available
3. Determine best integration point for widget
4. Test on Docusaurus site structure

**Test Cases**:
```typescript
// Visual test
1. Navigate to homepage (/)
2. Verify chat button is visible in bottom-right
3. Button should show 💬 icon
4. Click button → chat window opens
5. Send message → verify it works
6. Close chat → button reappears
```

**Verification**:
1. Run `npm start` in frontend directory
2. Open http://localhost:3000
3. Verify chat button appears on homepage
4. Test open/close functionality
5. Check browser console for errors

---

### Task 2.2: Ensure Chat Widget Positioning and Styling

**Priority**: P2 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Style the chat button and window to be visually appealing, properly positioned, and non-intrusive to homepage content.

**Files to Modify**:
- `frontend/src/components/ChatWidget/chat-widget.css`
- Possibly add z-index management

**Current State**: Check existing styles in chat-widget.css

**Acceptance Criteria**:
- [ ] Chat button fixed to bottom-right corner (20px margins)
- [ ] Button has appropriate z-index to stay above content
- [ ] Chat window opens smoothly without layout shift
- [ ] Widget is responsive on mobile (320px+) and desktop (1920px)
- [ ] No horizontal scrolling introduced
- [ ] Accessible on all screen sizes

**CSS Requirements**:
```css
.chat-widget-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  /* Additional styling for modern appearance */
}

.chat-widget-container {
  /* Ensure proper positioning */
}
```

**Test Cases**:
- Desktop (1920x1080): button visible, doesn't overlap content
- Tablet (768x1024): button properly positioned, touch-friendly
- Mobile (320x568): button accessible, chat window fills screen appropriately

**Verification**:
1. Test on multiple screen sizes using DevTools responsive mode
2. Verify button is always visible and accessible
3. Check z-index doesn't conflict with other elements
4. Ensure smooth animations when opening/closing

---

## Phase 3: Modern UI Redesign

### Task 3.1: Design and Implement Modern Chat Window Layout

**Priority**: P2 | **Estimated Complexity**: Medium | **Stage**: green

**Description**: Redesign the chat window with a modern, clean interface featuring clear visual hierarchy, proper spacing, and contemporary design patterns.

**Files to Modify**:
- `frontend/src/components/ChatWidget/ChatWindow.tsx`
- `frontend/src/components/ChatWidget/chat-widget.css`

**Design Requirements** (per spec FR-009):
- Clean header with title and close button
- Message area with clear user/AI distinction
- Modern input field with send button
- Smooth transitions and animations
- Professional color scheme
- Readable typography (font-size ≥ 14px)

**UI Components to Implement**:
```
┌─────────────────────────────┐
│ AI Tutor            [X]     │ ← Header
├─────────────────────────────┤
│                             │
│  [AI] Hello! How can...     │ ← Messages
│  [You] What is Physical AI? │
│  [AI] Physical AI refers... │
│                             │
│                        ↓    │ ← Scroll
├─────────────────────────────┤
│ [Type message...    ] [>]   │ ← Input
└─────────────────────────────┘
```

**Acceptance Criteria**:
- [ ] Header shows "AI Tutor" title and close button (X)
- [ ] Messages display in conversation format with timestamps
- [ ] User messages aligned right with distinct color
- [ ] AI messages aligned left with distinct color
- [ ] Message bubbles have rounded corners and proper padding
- [ ] Input area is fixed at bottom with send button
- [ ] Smooth scroll behavior in message area
- [ ] Modern color palette (suggest: blue/gray theme)

**Test Cases**:
1. Visual regression test: compare before/after screenshots
2. Message rendering: send 10 messages, verify layout
3. Scroll test: send 20+ messages, verify smooth scrolling
4. Accessibility: keyboard navigation works

**Verification**:
1. Open chat window
2. Send multiple messages
3. Verify visual design matches modern chat apps (Slack, Discord, etc.)
4. Get user feedback on design

---

### Task 3.2: Implement Message Bubble Components

**Priority**: P2 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Create reusable message bubble components with clear visual distinction between user and AI messages.

**Files to Create/Modify**:
- `frontend/src/components/ChatWidget/MessageBubble.tsx` (new component)
- `frontend/src/components/ChatWidget/chat-widget.css`

**Component Interface**:
```typescript
interface MessageBubbleProps {
  message: string;
  sender: 'user' | 'ai';
  timestamp?: string;
  agentName?: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  sender,
  timestamp,
  agentName
}) => {
  // Render message bubble with appropriate styling
};
```

**Acceptance Criteria**:
- [ ] Component accepts message, sender, timestamp props
- [ ] User messages: right-aligned, blue background, white text
- [ ] AI messages: left-aligned, gray background, dark text
- [ ] Timestamps displayed in small gray text below message
- [ ] Agent name shown for AI messages
- [ ] Message text wraps properly for long content
- [ ] Code blocks/markdown rendering (if needed)

**Styling Requirements**:
```css
.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  margin-bottom: 8px;
  word-wrap: break-word;
}

.message-bubble--user {
  background: #007bff;
  color: white;
  align-self: flex-end;
}

.message-bubble--ai {
  background: #f1f3f4;
  color: #202124;
  align-self: flex-start;
}
```

**Test Cases**:
- Render user message: verify styling
- Render AI message: verify styling
- Long message (500 chars): verify wrapping
- Multiple messages: verify proper spacing

---

### Task 3.3: Add Loading States and Typing Indicators

**Priority**: P2 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Implement visual feedback to show when a message is being sent or the AI is generating a response.

**Files to Modify**:
- `frontend/src/components/ChatWidget/ChatWindow.tsx`
- `frontend/src/components/ChatWidget/chat-widget.css`

**UI Elements to Add**:
1. Loading spinner when sending message
2. "AI is typing..." indicator while waiting for response
3. Disable input field during processing
4. Visual feedback on send button

**Acceptance Criteria**:
- [ ] Spinner/loader appears when message is being sent
- [ ] "AI is typing..." indicator shows while waiting for backend response
- [ ] Input field and send button disabled during processing
- [ ] Loading states clear when response received
- [ ] Error states display if request fails
- [ ] Smooth transitions between states

**Component State Management**:
```typescript
const [isLoading, setIsLoading] = useState(false);
const [isAITyping, setIsAITyping] = useState(false);

const handleSendMessage = async (message: string) => {
  setIsLoading(true);
  try {
    // Send message
    setIsAITyping(true);
    const response = await chatService.sendMessage(message);
    // Display response
  } finally {
    setIsLoading(false);
    setIsAITyping(false);
  }
};
```

**Test Cases**:
1. Send message → verify spinner appears
2. Wait for response → verify "typing" indicator
3. Response received → verify loaders disappear
4. Network error → verify error state displays

---

### Task 3.4: Improve Typography and Readability

**Priority**: P2 | **Estimated Complexity**: Small | **Stage**: refactor

**Description**: Enhance text readability with appropriate font sizes, line heights, and spacing throughout the chat interface.

**Files to Modify**:
- `frontend/src/components/ChatWidget/chat-widget.css`

**Typography Standards**:
- Body text: 14-16px
- Headers: 18-20px
- Timestamps: 12px
- Line height: 1.5
- Font family: System fonts (SF Pro, Segoe UI, Roboto)

**Acceptance Criteria**:
- [ ] All text is readable at minimum 14px font size
- [ ] Line height provides comfortable reading (1.4-1.6)
- [ ] Consistent font family across all chat components
- [ ] Proper contrast ratios (WCAG AA minimum)
- [ ] Text doesn't overflow or get cut off
- [ ] Mobile text sizes are appropriate (no tiny text)

**CSS Updates**:
```css
:root {
  --chat-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  --chat-font-size-base: 15px;
  --chat-font-size-small: 13px;
  --chat-line-height: 1.5;
}

.chat-window {
  font-family: var(--chat-font-family);
  font-size: var(--chat-font-size-base);
  line-height: var(--chat-line-height);
}
```

**Verification**:
1. Test readability on various devices
2. Check contrast with accessibility tools
3. Verify text scales properly
4. Get user feedback on readability

---

## Phase 4: Input Validation & Rate Limiting

### Task 4.1: Implement Frontend Input Validation

**Priority**: P1 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Add validation to ensure user messages meet requirements before sending to the backend (3-10,000 characters).

**Files to Modify**:
- `frontend/src/components/ChatWidget/ChatWindow.tsx`
- `frontend/src/components/ChatWidget/chat-service.ts:28-50`

**Validation Rules** (per spec FR-005):
- Minimum length: 3 characters (trimmed)
- Maximum length: 10,000 characters
- Must not be empty/whitespace only
- Sanitize potentially malicious input

**Current Implementation**: Check existing validation in chat-service.ts

**Acceptance Criteria**:
- [ ] Empty messages blocked with user-friendly error
- [ ] Messages < 3 chars show "Message too short" error
- [ ] Messages > 10,000 chars show "Message too long" error
- [ ] Whitespace-only messages rejected
- [ ] Error messages display in UI (not just console)
- [ ] Send button disabled for invalid input
- [ ] Character counter shows remaining characters

**UI Enhancements**:
```typescript
// Add character counter below input
<span className="character-count">
  {messageLength}/10000
</span>

// Show validation errors
{validationError && (
  <div className="validation-error">{validationError}</div>
)}
```

**Test Cases**:
```typescript
// Test: Empty message
expect(validateMessage("")).toThrow("Message cannot be empty");

// Test: Too short
expect(validateMessage("Hi")).toThrow("Message must be at least 3 characters");

// Test: Too long
const longMessage = "a".repeat(10001);
expect(validateMessage(longMessage)).toThrow("Message must be less than 10,000 characters");

// Test: Valid message
expect(validateMessage("What is Physical AI?")).toBe(true);
```

---

### Task 4.2: Enhance Rate Limiting with User Feedback

**Priority**: P1 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Improve the existing rate limiting implementation to provide clear visual feedback when rate limits are reached.

**Files to Modify**:
- `frontend/src/components/ChatWidget/chat-service.ts:102-120` (RateLimiter class)
- `frontend/src/components/ChatWidget/ChatWindow.tsx`

**Current Implementation**: Review existing RateLimiter in chat-service.ts

**Requirements** (per spec FR-006):
- 3 requests per 30 seconds (matches backend)
- Clear error message when limit exceeded
- Visual countdown/timer showing when user can send next message
- Disable send button when rate limited

**Acceptance Criteria**:
- [ ] Rate limiter prevents >3 requests in 30 seconds
- [ ] User sees countdown timer when rate limited
- [ ] Error message: "Rate limit exceeded. You can send another message in X seconds."
- [ ] Send button disabled when rate limited
- [ ] Timer updates every second
- [ ] Rate limit resets after 30 seconds

**UI Enhancement**:
```typescript
const [rateLimitRemaining, setRateLimitRemaining] = useState<number | null>(null);

// When rate limited:
{rateLimitRemaining && (
  <div className="rate-limit-notice">
    Rate limit exceeded. Try again in {rateLimitRemaining}s
  </div>
)}
```

**Test Cases**:
1. Send 3 messages quickly → 4th should be blocked
2. Wait 30 seconds → should be able to send again
3. Verify countdown timer displays correctly
4. Check send button is disabled when limited

---

### Task 4.3: Add Message Length Counter in Input Field

**Priority**: P2 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Display a real-time character counter to help users stay within the 10,000 character limit.

**Files to Modify**:
- `frontend/src/components/ChatWidget/ChatWindow.tsx`
- `frontend/src/components/ChatWidget/chat-widget.css`

**UI Design**:
```
┌─────────────────────────────────┐
│ Type your message...            │
│                                 │
│                     125 / 10000 │ ← Counter
└─────────────────────────────────┘
```

**Acceptance Criteria**:
- [ ] Character counter displays current length
- [ ] Counter updates in real-time as user types
- [ ] Counter turns red when approaching limit (>9,500 chars)
- [ ] Counter turns red when limit exceeded
- [ ] Counter positioned in bottom-right of input area
- [ ] Counter is non-intrusive and readable

**Implementation**:
```typescript
const [messageLength, setMessageLength] = useState(0);

const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
  const message = e.target.value;
  setMessageLength(message.length);
  setCurrentMessage(message);
};

// Render:
<span className={`char-counter ${messageLength > 9500 ? 'warning' : ''}`}>
  {messageLength} / 10000
</span>
```

**Test Cases**:
- Type message → counter updates
- Paste long text → counter shows correct length
- Delete text → counter decreases
- Exceed limit → counter turns red

---

## Phase 5: Error Handling & User Feedback

### Task 5.1: Implement Comprehensive Error Handling

**Priority**: P1 | **Estimated Complexity**: Medium | **Stage**: green

**Description**: Add robust error handling for all failure scenarios with user-friendly error messages that don't expose technical details.

**Files to Modify**:
- `frontend/src/components/ChatWidget/ChatWindow.tsx`
- `frontend/src/components/ChatWidget/chat-service.ts:70-95`

**Error Scenarios to Handle** (per spec edge cases):
1. Backend unreachable (network error)
2. Backend returns 500 error
3. Request timeout (>30 seconds)
4. Rate limit exceeded (429)
5. Invalid response format
6. Empty response from backend
7. CORS errors

**Acceptance Criteria**:
- [ ] Network errors show: "Unable to connect. Please check your connection."
- [ ] 500 errors show: "Service temporarily unavailable. Please try again."
- [ ] Timeout shows: "Request timed out. Please try again."
- [ ] Rate limit shows: "Too many requests. Wait X seconds."
- [ ] All errors display in chat UI (not just console)
- [ ] Error messages are friendly and actionable
- [ ] Retry mechanism for transient failures
- [ ] No technical stack traces shown to users

**Error Display UI**:
```typescript
interface ErrorMessageProps {
  error: string;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ error, onRetry }) => (
  <div className="error-message">
    <span className="error-icon">⚠️</span>
    <span className="error-text">{error}</span>
    {onRetry && (
      <button onClick={onRetry} className="retry-button">
        Retry
      </button>
    )}
  </div>
);
```

**Test Cases**:
```typescript
// Test: Network error
mockFetch.mockRejectedValue(new Error('Network error'));
await sendMessage("test");
expect(screen.getByText(/Unable to connect/)).toBeInTheDocument();

// Test: 500 error
mockFetch.mockResolvedValue({ ok: false, status: 500 });
await sendMessage("test");
expect(screen.getByText(/temporarily unavailable/)).toBeInTheDocument();
```

---

### Task 5.2: Add Request Timeout Handling

**Priority**: P1 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Implement timeout for chat requests to prevent indefinite waiting when backend is slow or unresponsive.

**Files to Modify**:
- `frontend/src/components/ChatWidget/chat-service.ts:70-95`

**Requirements**:
- Timeout after 30 seconds (configurable)
- Show user-friendly timeout message
- Cancel ongoing request when timeout occurs
- Allow user to retry

**Implementation**:
```typescript
const TIMEOUT_MS = 30000; // 30 seconds

async sendMessage(message: string): Promise<ChatMessage> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      signal: controller.signal,
      // ... other options
    });

    clearTimeout(timeoutId);
    // ... process response
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    }
    throw error;
  }
}
```

**Acceptance Criteria**:
- [ ] Requests timeout after 30 seconds
- [ ] Timeout error shows user-friendly message
- [ ] Ongoing request is cancelled on timeout
- [ ] User can retry after timeout
- [ ] Loading indicator clears on timeout

**Test Cases**:
- Mock slow backend (35 seconds) → verify timeout
- Mock normal response (<5 seconds) → verify no timeout
- Verify AbortController cancels request

---

### Task 5.3: Add Empty State and Welcome Message

**Priority**: P2 | **Estimated Complexity**: Small | **Stage**: green

**Description**: Display a friendly welcome message when the chat is first opened with no message history.

**Files to Modify**:
- `frontend/src/components/ChatWidget/ChatWindow.tsx`

**Welcome Message Design**:
```
┌─────────────────────────────────┐
│ AI Tutor                   [X]  │
├─────────────────────────────────┤
│                                 │
│     👋 Welcome!                 │
│                                 │
│  I'm your AI tutor for Physical │
│  AI and Humanoid Robotics.      │
│                                 │
│  Ask me anything about:         │
│  • Physical AI concepts         │
│  • Robotics fundamentals        │
│  • Course materials             │
│                                 │
│                                 │
├─────────────────────────────────┤
│ Type your question...      [>]  │
└─────────────────────────────────┘
```

**Acceptance Criteria**:
- [ ] Welcome message displays when chat is empty
- [ ] Message is friendly and informative
- [ ] Suggests topics users can ask about
- [ ] Welcome message disappears after first user message
- [ ] Styled consistently with chat theme

**Implementation**:
```typescript
{messages.length === 0 && (
  <div className="welcome-message">
    <h3>👋 Welcome!</h3>
    <p>I'm your AI tutor for Physical AI and Humanoid Robotics.</p>
    <p>Ask me anything about:</p>
    <ul>
      <li>Physical AI concepts</li>
      <li>Robotics fundamentals</li>
      <li>Course materials</li>
    </ul>
  </div>
)}
```

**Test Cases**:
- Open fresh chat → welcome message appears
- Send first message → welcome message disappears
- Close and reopen → messages preserved, no welcome

---

## Phase 6: Testing & Quality Assurance

### Task 6.1: Fix All Console Errors and Warnings

**Priority**: P1 | **Estimated Complexity**: Medium | **Stage**: red

**Description**: Identify and resolve all JavaScript runtime errors, React warnings, and console errors in the chat widget.

**Investigation Required**:
1. Open chat in browser with DevTools console
2. Perform all chat operations
3. Document all errors/warnings
4. Fix each issue systematically

**Common Issues to Check**:
- React key props on list items
- Uncontrolled → controlled component warnings
- Memory leaks from useEffect
- State updates on unmounted components
- PropTypes warnings
- Deprecated API usage

**Acceptance Criteria**:
- [ ] Zero console errors when opening chat
- [ ] Zero console errors when sending messages
- [ ] Zero console errors when closing chat
- [ ] Zero React warnings in development mode
- [ ] No memory leaks detected
- [ ] All useEffect cleanup functions present
- [ ] No "Cannot update component while rendering" warnings

**Testing Procedure**:
1. Open browser console (F12)
2. Filter to Errors and Warnings only
3. Perform complete chat workflow:
   - Open chat widget
   - Send 5 messages
   - Scroll message history
   - Test error scenarios
   - Close chat
   - Reopen chat
4. Document each error with screenshot
5. Fix systematically
6. Retest until clean

**Verification**:
```bash
# Run in development mode
cd frontend
npm start

# Open http://localhost:3000
# Open DevTools console
# Perform all chat operations
# Console should be clean (no red errors, no yellow warnings)
```

---

### Task 6.2: Add Responsive Design Testing

**Priority**: P1 | **Estimated Complexity**: Medium | **Stage**: red

**Description**: Test and fix the chat widget on all screen sizes to ensure responsive, functional design from mobile to desktop.

**Screen Sizes to Test** (per spec SC-005):
- Mobile small: 320x568 (iPhone SE)
- Mobile large: 414x896 (iPhone 11)
- Tablet portrait: 768x1024 (iPad)
- Tablet landscape: 1024x768 (iPad rotated)
- Desktop small: 1366x768
- Desktop large: 1920x1080

**Acceptance Criteria**:
- [ ] Chat button visible and accessible on all screen sizes
- [ ] Chat window scales appropriately on mobile (<500px width)
- [ ] No horizontal scrolling on any device
- [ ] Touch targets ≥44px on mobile (send button, close button)
- [ ] Input field usable on mobile keyboards
- [ ] Message bubbles wrap properly on narrow screens
- [ ] Font sizes readable on all devices (≥14px)
- [ ] Spacing/padding appropriate for touch interfaces

**Responsive Behavior**:
```css
/* Mobile first approach */
.chat-window {
  width: 100%;
  height: 100%;
  max-width: 100vw;
  max-height: 100vh;
}

/* Tablet and up */
@media (min-width: 768px) {
  .chat-window {
    width: 400px;
    height: 600px;
    max-height: 80vh;
    border-radius: 12px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .chat-window {
    width: 450px;
    height: 650px;
  }
}
```

**Test Cases**:
For each screen size:
1. Open chat button → verify size and position
2. Click to open → verify window size
3. Send message → verify input usability
4. Scroll messages → verify smooth scrolling
5. Close chat → verify button returns

**Verification**:
- Use Chrome DevTools responsive mode
- Test on real devices if possible
- Screenshot each screen size
- Document any issues found

---

### Task 6.3: Conduct Integration Testing

**Priority**: P1 | **Estimated Complexity**: Large | **Stage**: red

**Description**: Perform end-to-end testing of the complete chat workflow from homepage to backend response.

**Test Scenarios** (based on spec user stories):

**Scenario 1: First-Time User on Homepage**
```
Given: User visits homepage for first time
When: Page loads
Then: Chat button visible in bottom-right corner

When: User clicks chat button
Then: Chat window opens smoothly
  And: Welcome message displays
  And: Input field is focused and ready

When: User types "What is Physical AI?"
Then: Character counter shows 19/10000
  And: Send button is enabled

When: User clicks send
Then: Message appears in chat as user message
  And: Loading indicator shows "AI is typing..."
  And: Input field is disabled

When: Backend responds
Then: AI response appears in chat
  And: Loading indicator disappears
  And: Input field is re-enabled
  And: No console errors appear
```

**Scenario 2: Rate Limit Testing**
```
Given: Chat is open
When: User sends 3 messages in quick succession
Then: All 3 messages succeed

When: User attempts 4th message within 30 seconds
Then: Error message displays "Rate limit exceeded..."
  And: Send button is disabled
  And: Countdown timer shows seconds remaining

When: 30 seconds elapse
Then: Send button re-enables
  And: User can send messages again
```

**Scenario 3: Error Handling**
```
Given: Backend is unreachable
When: User sends message
Then: Error displays "Unable to connect..."
  And: Retry button appears

When: User clicks retry
Then: Request attempts again

Given: Backend returns 500 error
When: User sends message
Then: Friendly error displays (not technical details)
```

**Scenario 4: Mobile Experience**
```
Given: User on mobile device (iPhone SE, 320px width)
When: User opens homepage
Then: Chat button visible and touch-friendly (≥44px)

When: User taps chat button
Then: Chat fills screen appropriately
  And: Keyboard appears when input focused
  And: Input field remains visible above keyboard
```

**Acceptance Criteria**:
- [ ] All 4 scenarios pass without errors
- [ ] No console errors in any scenario
- [ ] All user interactions work as expected
- [ ] Error recovery works correctly
- [ ] Mobile experience is smooth
- [ ] Performance is acceptable (<5s for message round-trip)

**Documentation**:
- Create test report with pass/fail for each scenario
- Screenshot critical steps
- Note any issues or edge cases discovered
- Document browser/device tested

---

### Task 6.4: Performance and Accessibility Audit

**Priority**: P2 | **Estimated Complexity**: Medium | **Stage**: red

**Description**: Audit the chat widget for performance issues and accessibility compliance.

**Performance Checks**:
- [ ] Initial render time <2 seconds
- [ ] Message send/receive <5 seconds (excluding backend processing)
- [ ] Smooth scrolling (60fps)
- [ ] No memory leaks after 50+ messages
- [ ] Bundle size impact documented
- [ ] No unnecessary re-renders

**Accessibility Checks** (WCAG 2.1 Level AA):
- [ ] Keyboard navigation works (Tab, Enter, Esc)
- [ ] Screen reader support (aria-labels)
- [ ] Focus indicators visible
- [ ] Color contrast ≥4.5:1 for normal text
- [ ] Color contrast ≥3:1 for large text
- [ ] Focus trapped in chat when open
- [ ] Escape key closes chat
- [ ] All interactive elements keyboard-accessible

**Tools to Use**:
```bash
# Lighthouse audit
npm run build
# Run Lighthouse in Chrome DevTools

# axe DevTools for accessibility
# Install axe extension
# Run automated scan

# React DevTools Profiler
# Profile component renders
# Identify unnecessary re-renders
```

**Acceptance Criteria**:
- [ ] Lighthouse Performance score ≥90
- [ ] Lighthouse Accessibility score ≥90
- [ ] No axe violations (errors)
- [ ] Keyboard navigation fully functional
- [ ] Screen reader announces messages correctly
- [ ] Focus management works properly

**Documentation**:
- Lighthouse report screenshots
- axe scan results
- List of accessibility improvements made
- Performance metrics before/after optimization

---

## Next Steps After Completion

1. **Manual Testing**: Perform full manual test on all browsers (Chrome, Firefox, Safari, Edge)
2. **User Acceptance Testing**: Have stakeholders test the chat widget
3. **Create Pull Request**: Submit PR with all changes
4. **Documentation**: Update README with chat widget usage
5. **Deployment**: Coordinate production deployment

---

## Notes

- **Constraint Reminder**: NO backend changes allowed
- **Full File Return**: All modified files must be returned complete
- **Test Coverage**: Aim for >80% component test coverage
- **Browser Support**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

---

## Task Dependencies Graph

```
Phase 1 (Backend Integration)
  ├─ 1.1 → 1.2 → 1.3
  └─ Required before Phase 2

Phase 2 (Homepage Integration)
  ├─ 2.1 → 2.2
  └─ Required before Phase 6

Phase 3 (UI Redesign)
  ├─ 3.1 → 3.2 → 3.3 → 3.4
  └─ Can run parallel to Phase 4

Phase 4 (Validation)
  ├─ 4.1 → 4.2 → 4.3
  └─ Can run parallel to Phase 3

Phase 5 (Error Handling)
  ├─ 5.1 → 5.2 → 5.3
  └─ Depends on Phase 1

Phase 6 (Testing)
  ├─ 6.1 → 6.2 → 6.3 → 6.4
  └─ Requires all previous phases
```

---

**Created**: 2025-12-24
**Last Updated**: 2025-12-24
**Total Tasks**: 19
