# Component Contract: Chatbot UI Components

**Feature**: 001-chatbot-homepage-redesign
**Date**: 2025-12-24
**Version**: 1.0

## Overview

This document defines the contracts for all React components in the chatbot homepage integration feature, including props, state, events, and component interactions.

## Component Hierarchy

```
Homepage (index.tsx)
  └── ChatProvider (Context)
      └── ChatWidget
          ├── ChatToggleButton (when collapsed)
          └── ChatWindow (when expanded)
              ├── ChatHeader
              ├── ChatMessageList
              │   └── ChatMessage (multiple)
              └── ChatInput
```

## 1. ChatProvider Component

**Purpose**: Provides global chat visibility state to all components

**Location**: `frontend/src/contexts/ChatContext.tsx`

**Props**: None (wrapper component)

**Context Value**:
```typescript
interface ChatContextValue {
  isChatVisible: boolean;       // Whether chat is visible globally
  openChat: () => void;         // Function to show chat
  closeChat: () => void;        // Function to hide chat
}
```

**Usage**:
```tsx
// Wrap homepage with provider
<ChatProvider>
  <Homepage />
</ChatProvider>

// Consume in components
const { isChatVisible, openChat, closeChat } = useChat();
```

**State Management**:
- Maintains single boolean state: `isChatVisible`
- Initially `false` (chat hidden)
- Persists across component renders (not across page reloads)

**Contract Guarantees**:
- `isChatVisible` is always a boolean
- `openChat()` always sets `isChatVisible` to `true`
- `closeChat()` always sets `isChatVisible` to `false`
- Context never returns `undefined` (throws error if used outside provider)

---

## 2. ChatWidget Component

**Purpose**: Main chat widget container that manages toggle button and chat window

**Location**: `frontend/src/components/ChatWidget/ChatWidget.tsx`

**Props**:
```typescript
interface ChatWidgetProps {
  // No props - fully self-contained
}
```

**Internal State**:
```typescript
const [widgetState, setWidgetState] = useState<ChatWidgetState>({
  isExpanded: boolean;          // Whether chat window is open
  isVisible: boolean;           // Whether widget is on page (from ChatContext)
  position: { x: number; y: number };  // Position on screen
  unreadCount: number;          // Unread messages count
  lastMessagePreview: string;   // Last message preview
});

const [showChatWindow, setShowChatWindow] = useState<boolean>(false);
```

**Consumed Context**:
```typescript
const { isChatVisible, closeChat } = useChat();
```

**Behavior**:
1. **Mounting**: Load state from localStorage, render based on `isChatVisible`
2. **Toggle Click**: Open chat window, set `isExpanded` to `true`
3. **Close**: Collapse chat window, set `isExpanded` to `false`, call `closeChat()`
4. **Unmounting**: Save state to localStorage

**Rendering Logic**:
```typescript
if (!isChatVisible) return null;

return showChatWindow ? <ChatWindow /> : <ChatToggleButton />;
```

**Contract Guarantees**:
- Only renders when `isChatVisible` is `true`
- Mutually exclusive rendering: either toggle button OR chat window (never both)
- State persisted to localStorage on every update
- Calls `closeChat()` when user closes chat window

**Events Emitted**: None (self-contained)

**Side Effects**:
- Reads from `localStorage` on mount
- Writes to `localStorage` on state change
- Calls ChatContext `closeChat()` on close

---

## 3. ChatToggleButton Component

**Purpose**: Floating action button to open chat (shown when chat is collapsed)

**Location**: Inline in `ChatWidget.tsx` (can be extracted if needed)

**Props**:
```typescript
interface ChatToggleButtonProps {
  onClick: () => void;          // Callback when button clicked
  unreadCount: number;          // Number to show in badge (0 = no badge)
}
```

**Rendering**:
```tsx
<button
  className="chat-widget-button"
  onClick={onClick}
  aria-label="Open chat"
  data-unread={unreadCount > 0 ? unreadCount : undefined}
>
  💬
  {unreadCount > 0 && <span className="badge">{unreadCount}</span>}
</button>
```

**CSS Classes**:
- `.chat-widget-button`: Main button styles (fixed bottom-right, circular, shadow)
- `.chat-widget-button .badge`: Unread count badge (red circle, white text)

**Accessibility**:
- `aria-label="Open chat"` for screen readers
- Keyboard accessible (Tab + Enter)
- Focus visible outline

**Contract Guarantees**:
- Always renders button with chat icon (💬)
- Shows badge only when `unreadCount > 0`
- Calls `onClick` when clicked or Enter pressed
- Button is focusable and keyboard-accessible

---

## 4. ChatWindow Component

**Purpose**: Main chat interface with header, message list, and input

**Location**: `frontend/src/components/ChatWidget/ChatWindow.tsx`

**Props**:
```typescript
interface ChatWindowProps {
  onClose: () => void;                  // Callback when user closes chat
  onUnreadMessage: (message: string) => void;  // Callback for unread messages
}
```

**Internal State**:
```typescript
const [session, setSession] = useState<ChatSession>({
  sessionId: string;
  messages: ChatMessage[];
  connectionStatus: ConnectionStatus;
  lastActivity: string;
  rateLimitInfo: RateLimitInfo;
});

const [isTyping, setIsTyping] = useState<boolean>(false);
```

**Behavior**:
1. **Mounting**: Load session from localStorage
2. **Send Message**: Validate, check rate limit, call API, update session
3. **Receive Response**: Add AI message to session, scroll to bottom
4. **Error**: Display error message in chat
5. **Close**: Call `onClose()` callback
6. **Unmounting**: Save session to localStorage

**Rendering**:
```tsx
<div className="chat-window">
  <ChatHeader onClose={onClose} />
  <ChatMessageList messages={session.messages} isTyping={isTyping} />
  <ChatInput onSend={handleSend} disabled={isTyping} />
</div>
```

**Contract Guarantees**:
- Always calls `onClose()` when close button clicked
- Validates messages before sending (3-10,000 chars)
- Enforces rate limit (3 messages per 30 seconds)
- Displays all messages in chronological order
- Scrolls to latest message automatically
- Persists session to localStorage after every message
- Shows typing indicator when AI is responding
- Disables input when typing indicator is active

**Events Emitted**:
- `onClose()` - When user clicks close button
- `onUnreadMessage(message)` - When AI responds while chat is minimized (future feature)

**Side Effects**:
- Reads from `localStorage` on mount
- Writes to `localStorage` on session change
- Makes HTTP POST to `/chat` endpoint
- Scrolls message list to bottom on new message

---

## 5. ChatHeader Component

**Purpose**: Header bar with title and close button

**Location**: Inline in `ChatWindow.tsx` (using @chatscope/chat-ui-kit-react ConversationHeader)

**Props**:
```typescript
interface ChatHeaderProps {
  onClose: () => void;          // Callback when close button clicked
}
```

**Rendering** (using @chatscope components):
```tsx
<ConversationHeader>
  <ConversationHeader.Content>
    <div className="chat-header-title">AI Tutor</div>
  </ConversationHeader.Content>
  <ConversationHeader.Actions>
    <button
      className="chat-close-button"
      onClick={onClose}
      aria-label="Close chat"
    >
      ✕
    </button>
  </ConversationHeader.Actions>
</ConversationHeader>
```

**Contract Guarantees**:
- Always displays "AI Tutor" as title
- Always shows close button (✕)
- Calls `onClose()` when close button clicked
- Close button is keyboard accessible (Escape key optional)

---

## 6. ChatMessageList Component

**Purpose**: Scrollable list of chat messages

**Location**: Inline in `ChatWindow.tsx` (using @chatscope/chat-ui-kit-react MessageList)

**Props**:
```typescript
interface ChatMessageListProps {
  messages: ChatMessage[];      // Array of messages to display
  isTyping: boolean;            // Whether to show typing indicator
}
```

**Rendering**:
```tsx
<MessageList typingIndicator={isTyping ? <TypingIndicator /> : null}>
  {messages.map(msg => (
    <ChatMessage key={msg.id} message={msg} />
  ))}
</MessageList>
```

**Behavior**:
- Auto-scrolls to bottom when new message added
- Shows typing indicator at bottom when `isTyping` is true
- Handles empty state (no messages)

**Contract Guarantees**:
- Renders messages in array order (chronological)
- Each message has unique `key` prop (message.id)
- Shows typing indicator only when `isTyping` is true
- Scrolls to bottom automatically on new messages
- Supports infinite scroll (if needed in future)

---

## 7. ChatMessage Component

**Purpose**: Individual message bubble (user or AI)

**Location**: Inline in `ChatWindow.tsx` (using @chatscope/chat-ui-kit-react Message)

**Props**:
```typescript
interface ChatMessageProps {
  message: ChatMessage;         // Message data to display
}
```

**Message Data**:
```typescript
interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai' | 'system';
  timestamp: string;
  status?: 'sending' | 'sent' | 'error' | 'delivered';
}
```

**Rendering** (using @chatscope components):
```tsx
<Message
  model={{
    message: message.content,
    sender: message.sender,
    direction: message.sender === 'user' ? 'outgoing' : 'incoming',
    position: 'normal'
  }}
  className={`message-${message.sender}`}
>
  {message.status === 'error' && <Message.Footer>Failed to send</Message.Footer>}
</Message>
```

**Visual Styling**:
- **User messages**: Right-aligned, blue background, white text
- **AI messages**: Left-aligned, gray background, dark text
- **System messages**: Centered, yellow background, warning icon

**Contract Guarantees**:
- Always displays `message.content` text
- Aligns based on `sender` (user=right, ai/system=left)
- Shows error indicator if `status === 'error'`
- Sanitizes HTML to prevent XSS
- Renders markdown formatting (if needed)
- Shows timestamp on hover/tap

---

## 8. ChatInput Component

**Purpose**: Text input field with send button

**Location**: Inline in `ChatWindow.tsx` (using @chatscope/chat-ui-kit-react MessageInput)

**Props**:
```typescript
interface ChatInputProps {
  onSend: (message: string) => Promise<void>;  // Callback when send clicked
  disabled: boolean;                            // Whether input is disabled
}
```

**Internal State**:
```typescript
const [inputValue, setInputValue] = useState<string>('');
const [charCount, setCharCount] = useState<number>(0);
```

**Rendering**:
```tsx
<div className="chat-input-container">
  <MessageInput
    placeholder="Type your message..."
    value={inputValue}
    onChange={(val) => {
      setInputValue(val);
      setCharCount(val.length);
    }}
    onSend={() => {
      onSend(inputValue);
      setInputValue('');
      setCharCount(0);
    }}
    disabled={disabled}
    attachButton={false}
    sendButton={true}
  />
  <div className="char-counter">{charCount}/10,000</div>
</div>
```

**Behavior**:
1. User types message → Update `inputValue` and `charCount`
2. User presses Enter or clicks Send → Call `onSend(inputValue)`
3. `onSend` validates and sends → Clear input if successful
4. Show validation error → Keep input value

**Validation** (performed before `onSend`):
- Empty message (after trim): Don't send, no error shown
- Message < 3 chars: Don't send, show error "Message must be at least 3 characters"
- Message > 10,000 chars: Don't send, show error "Message too long"

**Contract Guarantees**:
- Clears input only after successful send
- Shows character count (0-10,000)
- Prevents send when disabled
- Calls `onSend()` on Enter key or Send button click
- Trims whitespace before sending
- Focuses input on mount
- Supports multiline (Shift+Enter for new line)

**Accessibility**:
- `aria-label="Type your message"`
- `aria-describedby="char-counter"`
- Keyboard accessible (Tab, Enter)

---

## 9. ChatService Class

**Purpose**: Handles API communication and rate limiting

**Location**: `frontend/src/components/ChatWidget/chat-service.ts`

**Public Methods**:
```typescript
class ChatService {
  // Send message and get response
  async sendMessage(
    message: string,
    onResponse: (response: string) => void
  ): Promise<void>

  // Send streaming message (SSE)
  async sendStreamingMessage(
    message: string,
    onMessage: (content: string, isPartial?: boolean) => void
  ): Promise<void>

  // Connect to service (for streaming)
  connect(): void

  // Disconnect from service
  disconnect(): void

  // Save rate limit state
  saveRateLimitState(): void

  // Load rate limit state
  loadRateLimitState(): void
}
```

**Method Contracts**:

### sendMessage()
```typescript
async sendMessage(message: string, onResponse: (response: string) => void): Promise<void>
```
- **Pre-conditions**:
  - `message.trim().length` >= 3 and <= 10,000
  - Not rate limited (< 3 requests in last 30s)
- **Post-conditions**:
  - Calls `onResponse(data.response)` with AI response
  - Increments rate limit counter
- **Throws**:
  - Error if message too short/long
  - Error if rate limited
  - Error if backend returns non-200
  - Error if network failure

### isRateLimited()
```typescript
private isRateLimited(): boolean
```
- **Returns**: `true` if rate limit exceeded, `false` otherwise
- **Side Effects**: Cleans up expired rate limit entries
- **Logic**: Max 3 requests in 30-second sliding window

**Contract Guarantees**:
- Validates message length before sending
- Enforces rate limit before sending
- Throws descriptive errors for all failure cases
- Parses JSON response correctly
- Handles network errors gracefully

---

## Component Interaction Diagram

```
User clicks toggle button
  ↓
ChatWidget.toggleChat()
  ↓
ChatWidget.setShowChatWindow(true)
  ↓
<ChatWindow> renders
  ↓
User types in <ChatInput>
  ↓
ChatInput.onChange(message)
  ↓
User presses Enter
  ↓
ChatInput.onSend(message)
  ↓
ChatWindow.handleSend(message)
  ↓
ChatService.sendMessage(message, onResponse)
  ↓
Backend POST /chat
  ↓
Backend returns ChatResponse
  ↓
onResponse(response.response)
  ↓
ChatWindow.addMessage(aiMessage)
  ↓
<ChatMessageList> re-renders with new message
  ↓
Auto-scroll to bottom
```

## Testing Component Contracts

### Unit Test Checklist

**ChatWidget**:
- [ ] Renders null when `isChatVisible` is false
- [ ] Renders toggle button when collapsed
- [ ] Renders chat window when expanded
- [ ] Saves state to localStorage on mount/unmount
- [ ] Calls `closeChat()` when user closes

**ChatWindow**:
- [ ] Loads session from localStorage on mount
- [ ] Validates message length (3-10,000)
- [ ] Enforces rate limit (3/30s)
- [ ] Calls `onClose()` when close clicked
- [ ] Displays error messages in chat
- [ ] Scrolls to bottom on new message

**ChatInput**:
- [ ] Clears input after successful send
- [ ] Shows character count
- [ ] Disables when `disabled` prop is true
- [ ] Calls `onSend()` on Enter or Send click
- [ ] Trims whitespace before sending

**ChatService**:
- [ ] Throws error for short messages (<3 chars)
- [ ] Throws error for long messages (>10,000 chars)
- [ ] Throws error when rate limited
- [ ] Handles 4xx/5xx backend errors
- [ ] Handles network errors
- [ ] Parses ChatResponse correctly

## Summary

This component contract defines:
- ✅ 9 components with props, state, and behavior
- ✅ ChatProvider context structure
- ✅ Component hierarchy and rendering logic
- ✅ Event callbacks and data flow
- ✅ ChatService API communication
- ✅ Validation rules and error handling
- ✅ Accessibility requirements
- ✅ Testing checklist

All components follow React best practices and support the chatbot homepage integration requirements.
