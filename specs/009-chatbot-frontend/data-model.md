# Data Model: Chatbot Frontend UI and API Integration

## Entities

### ChatMessage
**Description**: Represents an individual message in the chat conversation

**Fields**:
- `id: string` - Unique identifier for the message
- `content: string` - The text content of the message (3-10,000 characters)
- `sender: 'user' | 'ai'` - Indicates whether the message was sent by user or AI
- `timestamp: Date` - When the message was created/sent
- `status: 'sending' | 'sent' | 'error'` - Current status of the message
- `error?: string` - Error message if status is 'error'

**Validation Rules**:
- Content must be between 3 and 10,000 characters
- Content cannot be only whitespace
- Sender must be either 'user' or 'ai'

### ChatSession
**Description**: Represents a chat session containing message history and rate limiting state

**Fields**:
- `id: string` - Unique identifier for the session
- `messages: ChatMessage[]` - Array of messages in the conversation
- `rateLimit: { requests: number[], maxRequests: number, windowMs: number }` - Rate limiting state
- `createdAt: Date` - When the session was created
- `lastActive: Date` - When the last message was sent

**Validation Rules**:
- Messages array cannot exceed 1000 messages (to prevent memory issues)
- Rate limit must have maxRequests > 0 and windowMs > 0

### ChatWidgetState
**Description**: Represents the state of the chat widget UI

**Fields**:
- `isVisible: boolean` - Whether the chat widget is visible
- `isExpanded: boolean` - Whether the chat window is expanded
- `position: { x: number, y: number }` - Position of the chat widget on screen
- `minimized: boolean` - Whether the chat window is minimized
- `lastMessageId?: string` - ID of the last message displayed

**Validation Rules**:
- Position coordinates must be non-negative
- If minimized is true, isExpanded must be false

## State Transitions

### ChatMessage Status Transitions
- `sending` → `sent` (successful message delivery)
- `sending` → `error` (failed message delivery)

### ChatWidget Visibility Transitions
- `hidden` ↔ `visible` (widget can be toggled)
- `minimized` ↔ `expanded` (chat window can be toggled)

## Relationships
- A `ChatSession` contains multiple `ChatMessage` entities
- A `ChatWidgetState` references a specific `ChatSession` (via session ID)