# Data Model: Chatbot Homepage Integration

**Feature**: 001-chatbot-homepage-redesign
**Date**: 2025-12-24
**Phase**: 1 - Design & Contracts

## Overview

This document defines all data structures, TypeScript interfaces, and state management patterns for the chatbot homepage integration feature. All models are derived from functional requirements and existing codebase structures.

## Core Data Entities

### 1. ChatMessage

Represents a single message in the conversation.

**TypeScript Interface**:
```typescript
interface ChatMessage {
  id: string;                    // Unique identifier (UUID or timestamp-based)
  content: string;                // Message text content
  sender: MessageSender;          // Who sent the message
  timestamp: string;              // ISO 8601 timestamp
  status?: MessageStatus;         // Delivery/processing status
  typingIndicator?: boolean;      // Whether this is a typing indicator
}

type MessageSender = 'user' | 'ai' | 'system';

type MessageStatus = 'sending' | 'sent' | 'error' | 'delivered';
```

**Attributes**:
- `id` (string, required): Unique identifier for the message
  - Format: `msg-${Date.now()}-${randomSuffix}` or UUID
  - Used for React keys and message tracking

- `content` (string, required): The message text
  - Validation: 3-10,000 characters (FR-005)
  - Sanitized for XSS before display

- `sender` (MessageSender, required): Who sent the message
  - `'user'`: Message from the user
  - `'ai'`: Response from AI tutor
  - `'system'`: System messages (errors, notifications)

- `timestamp` (string, required): When the message was created
  - Format: ISO 8601 (e.g., "2025-12-24T10:30:00.000Z")
  - Used for message ordering and display

- `status` (MessageStatus, optional): Current message state
  - `'sending'`: Message being sent to backend
  - `'sent'`: Message successfully sent
  - `'delivered'`: Response received
  - `'error'`: Failed to send/receive

- `typingIndicator` (boolean, optional): Indicates typing animation
  - Used for AI "typing..." display

**Relationships**:
- Belongs to one ChatSession
- No direct relationships with other entities

**Validation Rules** (from FR-005):
```typescript
function validateMessage(content: string): { valid: boolean; error?: string } {
  const trimmed = content.trim();

  if (trimmed.length < 3) {
    return { valid: false, error: 'Message must be at least 3 characters' };
  }

  if (trimmed.length > 10000) {
    return { valid: false, error: 'Message must be under 10,000 characters' };
  }

  return { valid: true };
}
```

### 2. ChatSession

Represents the current conversation state and metadata.

**TypeScript Interface**:
```typescript
interface ChatSession {
  sessionId: string;              // Unique session identifier
  messages: ChatMessage[];        // Array of messages in chronological order
  connectionStatus: ConnectionStatus; // Current connection state
  lastActivity: string;           // ISO 8601 timestamp of last activity
  rateLimitInfo: RateLimitInfo;   // Rate limiting state
}

type ConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'error';

interface RateLimitInfo {
  requestsMade: number;           // Requests made in current window
  windowStart: string;            // ISO 8601 timestamp of window start
  remainingRequests: number;      // Requests remaining (3 max)
}
```

**Attributes**:
- `sessionId` (string, required): Unique identifier for the session
  - Format: `session-${Date.now()}`  or UUID
  - Persists across chat open/close within browser session

- `messages` (ChatMessage[], required): All messages in the conversation
  - Ordered chronologically (oldest first)
  - Persisted to localStorage (FR-014)
  - Cleared when page reloads (not persistent across sessions)

- `connectionStatus` (ConnectionStatus, required): Current backend connection state
  - `'connecting'`: Establishing connection
  - `'connected'`: Ready to send/receive
  - `'disconnected'`: Not connected (chat closed or error)
  - `'error'`: Connection failed

- `lastActivity` (string, required): Last message timestamp
  - Format: ISO 8601
  - Used for session timeout (if implemented)

- `rateLimitInfo` (RateLimitInfo, required): Rate limiting state
  - Tracks requests per 30-second window (FR-006)
  - Prevents exceeding backend limit (3/30s)

**State Transitions**:
```
disconnected → connecting → connected
connected → disconnected (on close)
connected → error (on backend failure)
error → connecting (on retry)
```

**Methods**:
```typescript
class ChatSession {
  constructor(sessionId?: string) {
    this.sessionId = sessionId || `session-${Date.now()}`;
    this.messages = [];
    this.connectionStatus = 'disconnected';
    this.lastActivity = new Date().toISOString();
    this.rateLimitInfo = {
      requestsMade: 0,
      windowStart: new Date().toISOString(),
      remainingRequests: 3
    };
  }

  // Add message to session
  addMessage(message: ChatMessage): void {
    this.messages.push(message);
    this.lastActivity = new Date().toISOString();
  }

  // Check and increment rate limit
  incrementRateLimit(): boolean {
    const now = new Date();
    const windowStart = new Date(this.rateLimitInfo.windowStart);
    const windowMs = 30000; // 30 seconds

    // Reset window if expired
    if (now.getTime() - windowStart.getTime() > windowMs) {
      this.rateLimitInfo = {
        requestsMade: 0,
        windowStart: now.toISOString(),
        remainingRequests: 3
      };
    }

    // Check limit
    if (this.rateLimitInfo.requestsMade >= 3) {
      return false; // Rate limit exceeded
    }

    // Increment
    this.rateLimitInfo.requestsMade++;
    this.rateLimitInfo.remainingRequests = 3 - this.rateLimitInfo.requestsMade;
    return true;
  }
}
```

### 3. ChatWidgetState

Tracks UI state for the chat widget (open/closed, position, visibility).

**TypeScript Interface**:
```typescript
interface ChatWidgetState {
  isExpanded: boolean;            // Whether chat window is open
  isVisible: boolean;             // Whether chat widget is visible on page
  position: WidgetPosition;       // Widget position on screen
  unreadCount: number;            // Unread message count (if minimized)
  lastMessagePreview: string;     // Preview of last message
}

interface WidgetPosition {
  x: number;                      // Horizontal position (pixels from right)
  y: number;                      // Vertical position (pixels from bottom)
}
```

**Attributes**:
- `isExpanded` (boolean, required): Whether the chat window is open
  - `true`: Chat window visible
  - `false`: Only toggle button visible

- `isVisible` (boolean, required): Whether widget appears on page
  - `true`: Widget rendered on homepage
  - `false`: Widget hidden (not on homepage)

- `position` (WidgetPosition, required): Widget screen position
  - Default: `{ x: 20, y: 20 }` (20px from bottom-right corner)
  - Adjusts based on screen size (mobile vs desktop)

- `unreadCount` (number, required): Unread messages when minimized
  - Increments when AI responds while chat is minimized
  - Resets to 0 when chat is expanded
  - Displayed as badge on toggle button

- `lastMessagePreview` (string, required): Preview of most recent message
  - Truncated to 50 characters
  - Displayed in tooltip or notification

**Persistence**:
```typescript
// Save to localStorage
localStorage.setItem('chatWidgetState', JSON.stringify(widgetState));

// Load from localStorage
const saved = localStorage.getItem('chatWidgetState');
const widgetState = saved ? JSON.parse(saved) : defaultWidgetState;
```

### 4. API Request/Response Models

Data structures for backend communication.

**Request Model** (existing):
```typescript
interface ChatRequest {
  message: string;                // User's message (3-10,000 chars)
}
```

**Response Model** (existing):
```typescript
interface ChatResponse {
  response: string;               // AI tutor's response
  agent_name: string;             // Name of AI agent
  timestamp: string;              // ISO 8601 response timestamp
}
```

**Error Response Model**:
```typescript
interface ErrorResponse {
  detail: string;                 // Human-readable error message
  status?: number;                // HTTP status code
  code?: string;                  // Error code (e.g., 'RATE_LIMIT_EXCEEDED')
}
```

**HTTP Error Mapping**:
- 422: Validation error → "Please check your message and try again"
- 429: Rate limit → "Too many requests. Please wait before sending another message"
- 500: Server error → "The tutor service is temporarily unavailable. Please try again later"
- 504: Timeout → "Request timed out. Please try again"
- Network error → "Unable to connect to server. Please check your internet connection"

## State Management Architecture

### React Context Structure

**ChatContext** (existing, in `frontend/src/contexts/ChatContext.tsx`):
```typescript
interface ChatContextValue {
  isChatVisible: boolean;         // Global chat visibility
  openChat: () => void;           // Open chat globally
  closeChat: () => void;          // Close chat globally
}

const ChatContext = React.createContext<ChatContextValue | undefined>(undefined);

export function ChatProvider({ children }: { children: React.ReactNode }) {
  const [isChatVisible, setIsChatVisible] = useState(false);

  const openChat = useCallback(() => setIsChatVisible(true), []);
  const closeChat = useCallback(() => setIsChatVisible(false), []);

  return (
    <ChatContext.Provider value={{ isChatVisible, openChat, closeChat }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }
  return context;
}
```

### Component State Management

**ChatWidget Component State**:
```typescript
// In ChatWidget.tsx
const [widgetState, setWidgetState] = useState<ChatWidgetState>({
  isExpanded: false,
  isVisible: true,
  position: { x: 20, y: 20 },
  unreadCount: 0,
  lastMessagePreview: ''
});

const [showChatWindow, setShowChatWindow] = useState(false);
```

**ChatWindow Component State**:
```typescript
// In ChatWindow.tsx
const [session, setSession] = useState<ChatSession>(() => {
  const saved = localStorage.getItem('chatSession');
  return saved ? JSON.parse(saved) : new ChatSession();
});

const [isTyping, setIsTyping] = useState(false);
const [error, setError] = useState<string | null>(null);
```

### Data Flow Diagram

```
User Interaction
      ↓
ChatWidget (toggle button)
      ↓
useChat() → ChatContext
      ↓
ChatWindow opens
      ↓
User types message
      ↓
Input validation (3-10,000 chars)
      ↓
Rate limit check (3/30s)
      ↓
ChatService.sendMessage()
      ↓
POST /chat { message }
      ↓
Backend processes
      ↓
ChatResponse { response, agent_name, timestamp }
      ↓
ChatSession.addMessage(aiMessage)
      ↓
UI updates with message
      ↓
localStorage.setItem('chatSession', session)
```

## Validation and Business Rules

### Message Validation (FR-005)

**Rule**: Messages must be 3-10,000 characters after trimming

**Implementation**:
```typescript
function validateMessageLength(message: string): ValidationResult {
  const trimmed = message.trim();

  if (trimmed.length === 0) {
    return { valid: false, error: 'Message cannot be empty' };
  }

  if (trimmed.length < 3) {
    return { valid: false, error: 'Message must be at least 3 characters' };
  }

  if (trimmed.length > 10000) {
    return {
      valid: false,
      error: 'Message is too long. Please keep under 10,000 characters'
    };
  }

  return { valid: true };
}
```

### Rate Limiting (FR-006)

**Rule**: Maximum 3 requests per 30-second window

**Implementation**:
```typescript
interface RateLimitInfo {
  requestsMade: number;           // 0-3
  windowStart: string;            // ISO 8601
  remainingRequests: number;      // 3 - requestsMade
}

function checkRateLimit(rateLimitInfo: RateLimitInfo): boolean {
  const now = new Date();
  const windowStart = new Date(rateLimitInfo.windowStart);
  const windowMs = 30000; // 30 seconds

  // Check if window expired
  if (now.getTime() - windowStart.getTime() > windowMs) {
    // Reset window
    return true; // Can proceed
  }

  // Check if limit exceeded
  if (rateLimitInfo.requestsMade >= 3) {
    return false; // Rate limited
  }

  return true; // Can proceed
}
```

### Session Persistence (FR-014)

**Rule**: Chat history preserved during current browser session

**Implementation**:
```typescript
// Save on every message update
useEffect(() => {
  const sessionData = {
    sessionId: session.sessionId,
    messages: session.messages,
    connectionStatus: session.connectionStatus,
    lastActivity: session.lastActivity,
    rateLimitInfo: session.rateLimitInfo
  };
  localStorage.setItem('chatSession', JSON.stringify(sessionData));
}, [session]);

// Load on component mount
useEffect(() => {
  const saved = localStorage.getItem('chatSession');
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      setSession(parsed);
    } catch (error) {
      console.warn('Failed to restore chat session');
    }
  }
}, []);
```

## Type Definitions Summary

**File**: `frontend/src/components/ChatWidget/models.ts`

```typescript
// Message types
export type MessageSender = 'user' | 'ai' | 'system';
export type MessageStatus = 'sending' | 'sent' | 'error' | 'delivered';
export type ConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'error';

// Core interfaces
export interface ChatMessage {
  id: string;
  content: string;
  sender: MessageSender;
  timestamp: string;
  status?: MessageStatus;
  typingIndicator?: boolean;
}

export interface RateLimitInfo {
  requestsMade: number;
  windowStart: string;
  remainingRequests: number;
}

export interface ChatSession {
  sessionId: string;
  messages: ChatMessage[];
  connectionStatus: ConnectionStatus;
  lastActivity: string;
  rateLimitInfo: RateLimitInfo;
}

export interface WidgetPosition {
  x: number;
  y: number;
}

export interface ChatWidgetState {
  isExpanded: boolean;
  isVisible: boolean;
  position: WidgetPosition;
  unreadCount: number;
  lastMessagePreview: string;
}

// API types
export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
  agent_name: string;
  timestamp: string;
}

export interface ErrorResponse {
  detail: string;
  status?: number;
  code?: string;
}

// Validation types
export interface ValidationResult {
  valid: boolean;
  error?: string;
}
```

## Data Constraints

| Entity | Field | Constraint | Validation |
|--------|-------|------------|------------|
| ChatMessage | content | 3-10,000 chars | Client-side validation before send |
| ChatMessage | timestamp | ISO 8601 format | `new Date().toISOString()` |
| ChatSession | messages | Max 1000 messages | Clear old messages if exceeded |
| ChatSession | rateLimitInfo.requestsMade | 0-3 | Reset after 30 seconds |
| ChatWidgetState | unreadCount | >= 0 | Reset to 0 when chat expanded |
| ChatRequest | message | 3-10,000 chars | Validated before API call |

## Summary

This data model provides:
- **5 core entities**: ChatMessage, ChatSession, ChatWidgetState, ChatRequest, ChatResponse
- **Type-safe interfaces**: All TypeScript types defined
- **Validation rules**: Message length, rate limiting, error handling
- **State management**: React Context + component state
- **Persistence**: localStorage for session and widget state
- **API contracts**: Request/response structures matching backend

All models align with functional requirements and support the chatbot homepage integration feature.
