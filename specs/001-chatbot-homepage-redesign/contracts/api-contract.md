# API Contract: Backend Chat Endpoint

**Feature**: 001-chatbot-homepage-redesign
**Date**: 2025-12-24
**Version**: 1.0

## Overview

This document defines the contract between the frontend chatbot and the existing backend `/chat` API endpoint. The contract is derived from backend analysis and must not be modified (per user constraint: "do not change backend").

## Base URL

The backend URL is configurable via environment variable:

```typescript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
```

**Production**: Set `REACT_APP_BACKEND_URL` in `.env` file
**Development**: Defaults to `http://localhost:8000`

## Endpoint: Send Chat Message

### Request

**Method**: `POST`

**URL**: `{BACKEND_URL}/chat`

**Headers**:
```http
Content-Type: application/json
Accept: application/json
```

**Request Body**:
```json
{
  "message": "string"
}
```

**TypeScript Interface**:
```typescript
interface ChatRequest {
  message: string;    // User's question/message (3-10,000 chars)
}
```

**Validation** (Frontend):
- `message` field is required
- `message` must be a string
- `message.trim().length` must be >= 3
- `message.trim().length` must be <= 10,000
- Request sent only if rate limit not exceeded (3 requests per 30 seconds)

**Example Request**:
```http
POST http://localhost:8000/chat HTTP/1.1
Content-Type: application/json
Accept: application/json

{
  "message": "What is ROS 2 and how does it differ from ROS 1?"
}
```

### Successful Response

**Status Code**: `200 OK`

**Response Body**:
```json
{
  "response": "string",
  "agent_name": "string",
  "timestamp": "string"
}
```

**TypeScript Interface**:
```typescript
interface ChatResponse {
  response: string;      // AI tutor's response text
  agent_name: string;    // Name of the AI agent (e.g., "AI Tutor")
  timestamp: string;     // ISO 8601 timestamp (e.g., "2025-12-24T10:30:00.000Z")
}
```

**Example Response**:
```json
{
  "response": "ROS 2 (Robot Operating System 2) is the next generation of ROS, designed to address limitations of ROS 1...",
  "agent_name": "AI Tutor",
  "timestamp": "2025-12-24T10:30:00.123Z"
}
```

**Response Handling** (Frontend):
```typescript
async function sendMessage(message: string): Promise<ChatResponse> {
  const response = await fetch(`${BACKEND_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({ message: message.trim() })
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data: ChatResponse = await response.json();
  return data;
}
```

### Error Responses

#### 422 Unprocessable Entity - Validation Error

**Status Code**: `422`

**Response Body**:
```json
{
  "detail": "string"
}
```

**Example**:
```json
{
  "detail": "Message validation failed: message too short"
}
```

**Frontend Handling**:
```typescript
if (response.status === 422) {
  // Show user-friendly validation error
  showError('Please check your message and try again');
}
```

#### 429 Too Many Requests - Rate Limit Exceeded

**Status Code**: `429`

**Response Body**:
```json
{
  "detail": "string"
}
```

**Example**:
```json
{
  "detail": "Rate limit exceeded: 3 requests per minute"
}
```

**Frontend Handling**:
```typescript
if (response.status === 429) {
  // Show rate limit error
  showError('Too many requests. Please wait before sending another message');
}
```

**Note**: Frontend implements its own rate limiting (3 requests per 30 seconds) to prevent hitting backend limit. This error should rarely occur.

#### 500 Internal Server Error - Backend Failure

**Status Code**: `500`

**Response Body**:
```json
{
  "detail": "string"
}
```

**Example**:
```json
{
  "detail": "The tutor service is temporarily unavailable. Please try again later."
}
```

**Frontend Handling**:
```typescript
if (response.status === 500) {
  // Show generic error (don't expose backend details)
  showError('The AI tutor is temporarily unavailable. Please try again later');
}
```

#### 504 Gateway Timeout - Request Timeout

**Status Code**: `504`

**Response Body**:
```json
{
  "detail": "string"
}
```

**Example**:
```json
{
  "detail": "Request timed out after 60 seconds"
}
```

**Frontend Handling**:
```typescript
if (response.status === 504) {
  // Show timeout error
  showError('Request timed out. Please try again');
}
```

#### Network Error - Connection Failed

**No HTTP Response** (fetch throws exception)

**Frontend Handling**:
```typescript
try {
  const response = await fetch(...);
} catch (error) {
  // Network error (offline, CORS, DNS failure, etc.)
  showError('Unable to connect to server. Please check your internet connection');
}
```

## Error Response Mapping

| HTTP Status | Error Code | User-Friendly Message | Action |
|-------------|------------|----------------------|--------|
| 422 | Validation | "Please check your message and try again" | Show error in chat |
| 429 | Rate Limit | "Too many requests. Please wait 30 seconds" | Show error + disable send |
| 500 | Server Error | "AI tutor temporarily unavailable" | Show error + allow retry |
| 504 | Timeout | "Request timed out. Please try again" | Show error + allow retry |
| Network | Connection | "Unable to connect. Check your connection" | Show error + allow retry |

## Rate Limiting

### Backend Rate Limit

- **Limit**: 3 requests per minute (per IP address)
- **Enforced by**: Backend (using slowapi with get_remote_address)
- **Response**: HTTP 429 when exceeded

### Frontend Rate Limit (Proactive)

- **Limit**: 3 requests per 30 seconds (per browser session)
- **Enforced by**: Frontend (ChatService class)
- **Response**: Error message shown before attempting request

**Implementation**:
```typescript
class ChatService {
  private rateLimit = {
    requests: [] as number[],
    maxRequests: 3,
    windowMs: 30000 // 30 seconds
  };

  private isRateLimited(): boolean {
    const now = Date.now();

    // Remove old requests outside window
    this.rateLimit.requests = this.rateLimit.requests.filter(
      timestamp => now - timestamp < this.rateLimit.windowMs
    );

    // Check limit
    if (this.rateLimit.requests.length >= this.rateLimit.maxRequests) {
      return true; // Rate limited
    }

    // Add current request
    this.rateLimit.requests.push(now);
    return false; // OK to proceed
  }

  async sendMessage(message: string): Promise<ChatResponse> {
    // Check rate limit before sending
    if (this.isRateLimited()) {
      throw new Error('Rate limit exceeded. Please wait before sending another message.');
    }

    // Proceed with request...
  }
}
```

## CORS Configuration

**Assumption**: Backend has CORS configured to accept requests from frontend origin

**Required CORS Headers** (Backend):
```
Access-Control-Allow-Origin: <frontend-origin>
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Accept
```

**Frontend**: No special CORS handling required (handled by backend)

## Authentication

**Current State**: No authentication required for `/chat` endpoint

**Rationale**: User requirement states "do not change backend". Analysis of backend code shows `/chat` endpoint has no authentication middleware.

**Future Consideration**: If authentication is added to backend in the future, frontend will need to:
1. Include auth token in request headers
2. Handle 401 Unauthorized responses
3. Redirect to login if needed

## Response Time Expectations

**Frontend Timeout**: 30 seconds (configurable)

**Implementation**:
```typescript
async function sendMessageWithTimeout(message: string, timeoutMs = 30000): Promise<ChatResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ message }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);
    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timed out after 30 seconds');
    }
    throw error;
  }
}
```

**Success Criteria** (from spec SC-002):
- Message round-trip completes in under 5 seconds (excluding backend processing time)
- Frontend displays loading indicator during request
- Timeout after 30 seconds with user-friendly error

## Data Flow Sequence

```
User: Types message
  ↓
Frontend: Validates message length (3-10,000 chars)
  ↓
Frontend: Checks rate limit (3/30s)
  ↓
Frontend: POST /chat { message: "..." }
  ↓
Backend: Validates request
  ↓
Backend: Processes with AI agent
  ↓
Backend: Returns ChatResponse { response, agent_name, timestamp }
  ↓
Frontend: Parses response
  ↓
Frontend: Creates AI ChatMessage
  ↓
Frontend: Updates UI with message
  ↓
User: Sees AI response
```

## Testing Contract Compliance

### Manual Testing Checklist

- [ ] Send valid message (3-1000 chars) → Expect 200 + ChatResponse
- [ ] Send empty message → Frontend validation prevents send
- [ ] Send message <3 chars → Frontend validation prevents send
- [ ] Send message >10,000 chars → Frontend validation prevents send
- [ ] Send 4 messages in 30s → 4th shows rate limit error
- [ ] Backend returns 500 → User sees friendly error
- [ ] Backend returns 504 → User sees timeout error
- [ ] Disconnect network → User sees connection error
- [ ] Response includes response, agent_name, timestamp fields
- [ ] Timestamp is valid ISO 8601 format

### Network Tab Verification

**Expected Request**:
```
POST http://localhost:8000/chat
Content-Type: application/json
Request Payload: {"message":"test message"}
```

**Expected Response**:
```
Status: 200 OK
Content-Type: application/json
Response: {"response":"...","agent_name":"AI Tutor","timestamp":"2025-..."}
```

## Contract Version Control

**Version**: 1.0 (Initial)
**Last Updated**: 2025-12-24
**Breaking Changes**: None
**Backward Compatibility**: N/A (initial version)

**Future Changes**:
- Any backend changes to `/chat` endpoint require updating this contract
- Frontend must handle both old and new response formats during transition
- Version negotiation may be needed if breaking changes occur

## Summary

This contract defines:
- ✅ Exact request/response formats for `/chat` endpoint
- ✅ All error responses and frontend handling
- ✅ Rate limiting (frontend: 3/30s, backend: 3/min)
- ✅ Validation rules for message content
- ✅ Timeout handling (30 seconds)
- ✅ Error message mapping for user-friendly display
- ✅ Network error handling
- ✅ Testing checklist for contract compliance

**Constraints Verified**:
- No backend changes required ✅
- Uses existing API contract ✅
- All error scenarios handled gracefully ✅
