# Chat API Contract

**Endpoint**: `/chat`
**Method**: POST
**Purpose**: Send user message to AI tutor and receive educational response
**Backend Implementation**: `backend/src/backend/main.py:chat()`
**Rate Limit**: 3 requests per 30 seconds (per IP address)
**Authentication**: **None** (auth removed from backend endpoint per spec)

---

## Request

### Headers
```http
Content-Type: application/json
Accept: application/json
```

**Note**: No `Authorization` header required (backend authentication removed)

### Body Schema
```json
{
  "message": "string (required, 3-10,000 characters)"
}
```

**TypeScript Interface**:
```typescript
interface ChatRequest {
  message: string;     // User's question or input (trimmed, 3-10,000 chars)
  sessionId?: string;  // Optional, not used by backend (reserved for future)
}
```

### Validation Rules (Frontend)
- `message`: Required, trimmed whitespace, minimum 3 characters, maximum 10,000 characters
- Validate before sending to prevent unnecessary 422 errors

### Validation Rules (Backend)
- `message`: Required, Pydantic model validates presence
- **Length validation**: Backend may return 422 if message is too short or too long

### Example Request
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ROS 2 and how does it differ from ROS 1?"
  }'
```

---

## Successful Response (200 OK)

### Body Schema
```json
{
  "response": "string (AI-generated response)",
  "agent_name": "string (AI agent name, e.g., 'AI Tutor')",
  "timestamp": "string (ISO 8601 timestamp, optional in practice)"
}
```

**TypeScript Interface**:
```typescript
interface ChatResponse {
  response: string;      // AI tutor's educational response
  agent_name: string;    // Name of the AI agent
  timestamp: string;     // Server-generated timestamp (may not always be present)
}
```

### Example Response
```json
{
  "response": "ROS 2 (Robot Operating System 2) is a complete rewrite of ROS 1 designed for production robotics. Key differences include:\n\n1. **Communication**: Uses DDS (Data Distribution Service) instead of custom middleware\n2. **Real-time Support**: Better support for real-time systems\n3. **Security**: Built-in security features with DDS Security\n4. **Cross-platform**: Improved support for Windows and macOS\n5. **Node Composition**: Allows multiple nodes in a single process\n\nWould you like me to elaborate on any of these differences?",
  "agent_name": "AI Tutor",
  "timestamp": "2025-12-23T14:30:15Z"
}
```

### Frontend Handling
```typescript
const response = await fetch('/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: trimmedMessage })
});

if (response.ok) {
  const data: ChatResponse = await response.json();
  // Append AI message to chat history
  addMessage({
    id: `msg-${Date.now()}`,
    content: data.response,
    sender: 'ai',
    timestamp: data.timestamp || new Date().toISOString(),
    status: 'delivered',
    agentName: data.agent_name
  });
}
```

---

## Error Responses

### 422 Unprocessable Entity (Validation Error)

**Trigger**: Invalid message format (empty, too short, too long, or missing field)

**Body**:
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Frontend Handling**:
```typescript
if (response.status === 422) {
  setErrorMessage('Invalid message format. Message must be between 3 and 10,000 characters.');
  console.error('[Chat Validation Error]', {
    timestamp: new Date().toISOString(),
    status: 422,
    message: trimmedMessage,
    length: trimmedMessage.length
  });
}
```

---

### 429 Too Many Requests (Rate Limit Exceeded)

**Trigger**: More than 3 chat requests within 30 seconds

**Body**:
```json
{
  "detail": "Rate limit exceeded: 3 per 30 second"
}
```

**Headers**:
```http
Retry-After: 30  # Seconds until rate limit resets (may not always be present)
```

**Frontend Handling**:
```typescript
if (response.status === 429) {
  const retryAfter = response.headers.get('Retry-After');
  const seconds = retryAfter ? parseInt(retryAfter) : 30;
  setErrorMessage(`You've sent too many messages. Please wait ${seconds} seconds before trying again.`);

  // Optional: Show countdown timer
  startCountdown(seconds, (remaining) => {
    setErrorMessage(`Rate limit exceeded. Try again in ${remaining}s.`);
  });
}
```

---

### 500 Internal Server Error (AI Service Failure)

**Trigger**: AI service exception (API quota exceeded, model error, unexpected error)

**Body**:
```json
{
  "detail": "The tutor service is temporarily unavailable. Please try again later."
}
```

**Note**: Backend may return a mock response instead of 500 during development/testing:
```json
{
  "response": "[Mock Response] Regarding '<message>': This is a test response. Authentication has been removed from this endpoint. (AI service temporarily unavailable due to API quota.)",
  "agent_name": "AI Tutor"
}
```

**Frontend Handling**:
```typescript
if (response.status === 500) {
  setErrorMessage('The AI tutor service is temporarily unavailable. Please try again later.');
  console.error('[AI Service Error]', {
    timestamp: new Date().toISOString(),
    status: 500
  });

  // Update message status to 'failed' with retry option
  updateMessageStatus(messageId, 'failed');
}
```

---

### 504 Gateway Timeout (Request Timeout)

**Trigger**: AI agent takes longer than configured timeout (default: 30 seconds per spec)

**Body**:
```json
{
  "detail": "Request timed out after 30 seconds"
}
```

**Frontend Handling**:
```typescript
if (response.status === 504) {
  setErrorMessage('Request timeout. The AI is taking too long to respond. Please try again.');
  console.error('[Timeout Error]', {
    timestamp: new Date().toISOString(),
    status: 504,
    message: trimmedMessage
  });

  updateMessageStatus(messageId, 'failed');
}
```

---

### Network Errors (Offline, DNS Failure, Connection Refused)

**Trigger**: Client cannot reach backend (offline, server down, network issue)

**Frontend Handling**:
```typescript
try {
  const response = await Promise.race([
    fetch('/chat', { method: 'POST', body: ... }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), 30000)
    )
  ]);
} catch (error) {
  if (error.message === 'Failed to fetch' || error.message.includes('NetworkError')) {
    setErrorMessage('Network error. Please check your internet connection.');
  } else if (error.message === 'Request timeout') {
    setErrorMessage('Request timeout. Please try again later.');
  } else {
    setErrorMessage('An unexpected error occurred. Please try again.');
  }
  console.error('[Network Error]', {
    timestamp: new Date().toISOString(),
    error: error.message
  });
}
```

---

## Rate Limiting (Client-Side + Backend)

### Client-Side Implementation (ChatService)
```typescript
class ChatService {
  private rateLimit = {
    requests: [] as number[],
    maxRequests: 3,
    windowMs: 30000
  };

  private isRateLimited(): boolean {
    const now = Date.now();
    this.rateLimit.requests = this.rateLimit.requests.filter(
      t => now - t < this.rateLimit.windowMs
    );

    if (this.rateLimit.requests.length >= this.rateLimit.maxRequests) {
      return true; // Block request before sending
    }

    this.rateLimit.requests.push(now);
    return false;
  }

  async sendMessage(message: string): Promise<string> {
    if (this.isRateLimited()) {
      throw new Error('Rate limit exceeded. Please wait before sending another message.');
    }
    // Proceed with fetch...
  }
}
```

### Backend Rate Limiting (slowapi)
- Enforced per IP address
- 3 requests per 30-second window
- Returns 429 if exceeded
- Independent of client-side rate limiting (defense in depth)

---

## Message Validation (Frontend)

**Validation before API call** (per FR-008):
```typescript
function validateMessage(message: string): { valid: boolean; error?: string } {
  const trimmed = message.trim();

  if (trimmed.length < 3) {
    return { valid: false, error: 'Message is too short. Please enter at least 3 characters.' };
  }

  if (trimmed.length > 10000) {
    return { valid: false, error: 'Message is too long. Please keep your message under 10,000 characters.' };
  }

  return { valid: true };
}

// Usage
const validation = validateMessage(userInput);
if (!validation.valid) {
  setErrorMessage(validation.error);
  return; // Don't send request
}
```

**Character Counter UI** (recommended):
```typescript
const remaining = 10000 - userInput.length;
const color = remaining < 100 ? 'red' : remaining < 500 ? 'orange' : 'gray';
<span style={{ color }}>{remaining} characters remaining</span>
```

---

## Response Processing

### Streaming Support (Future Enhancement)
- Current implementation: Non-streaming (complete response in one payload)
- **Reserved for future**: `/chat` endpoint may support Server-Sent Events (SSE) for streaming responses
- `chat-service.ts` already has `sendStreamingMessage()` method stub

### HTML Sanitization
- AI responses may contain markdown or special characters
- **Frontend responsibility**: Sanitize HTML to prevent XSS
- Use library like `DOMPurify` or escape HTML entities before rendering

```typescript
import DOMPurify from 'dompurify';

function renderAIResponse(response: string): string {
  return DOMPurify.sanitize(response, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li', 'code', 'pre'],
    ALLOWED_ATTR: []
  });
}
```

---

## Contract Invariants

1. **No Authentication Required**: Endpoint is public (authentication removed)
2. **Response Format**: Always returns JSON (never HTML)
3. **Message Length**: Backend enforces 3-10,000 character limit
4. **Rate Limit**: Always 3 requests per 30 seconds (backend enforced)
5. **Timeout**: Backend request timeout is 30 seconds (per spec)
6. **Backward Compatibility**: No breaking changes to request/response schema without versioning

---

## Testing Checklist

- [ ] Valid message (3+ chars) returns 200 with AI response
- [ ] Empty message returns 422
- [ ] Message < 3 characters returns 422 (or handled client-side)
- [ ] Message > 10,000 characters returns 422 (or handled client-side)
- [ ] 4th request within 30 seconds returns 429
- [ ] Retry-After header present in 429 response (if backend provides)
- [ ] AI service error returns 500 or mock response
- [ ] Request exceeding 30s returns 504
- [ ] Network timeout handled gracefully (client-side)
- [ ] Special characters in message handled correctly (no injection)
- [ ] Response HTML sanitized before rendering
- [ ] Rate limit state persists across component remounts
- [ ] Rate limit state cleared on logout
