# Quickstart Guide: Connect Frontend Authentication and Chat to Backend APIs

**Feature**: 001-connect-frontend-backend-apis
**Date**: 2025-12-23
**Audience**: Developers implementing this feature

---

## Overview

This guide provides a step-by-step implementation path for connecting the Docusaurus frontend sign-in form and chatbot UI to the existing FastAPI backend authentication (`/auth/login`) and chat (`/chat`) endpoints.

**Good News**: Most of the heavy lifting is already done! The backend is complete, and `AuthContext` already implements authentication logic. Your main tasks are:
1. Create/update the sign-in UI page
2. Integrate auth state with the chat widget
3. Add error handling and user feedback

**Time Estimate**: 4-6 hours for an experienced React developer

---

## Prerequisites

### 1. Development Environment Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install  # Installs React 19, Docusaurus 3.9.2, MUI, etc.
```

### 2. Environment Variables

Create `.env` files in backend and frontend:

**backend/.env**:
```env
# Database (Neon Serverless Postgres)
DATABASE_URL=postgresql://user:password@hostname/database

# JWT Secret (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here

# AI Service (Google Gemini or OpenAI)
GEMINI_API_KEY=your-gemini-api-key  # Or OpenAI key

# App Settings
HOST=0.0.0.0
PORT=8000
RATE_LIMIT_PER_MINUTE=3
REQUEST_TIMEOUT_SECONDS=30
CONSTITUTION_PATH=.specify/memory/constitution.md
```

**frontend/.env**:
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### 3. Verify Backend is Running

```bash
cd backend
python -m backend.src.backend.main
# Or: uvicorn backend.src.backend.main:app --reload
```

Visit http://localhost:8000/docs to see Swagger API documentation.

**Test authentication endpoint**:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'
```

### 4. Verify Frontend is Running

```bash
cd frontend
npm start
```

Visit http://localhost:3000 to see Docusaurus site.

---

## Implementation Path

### Phase 1: Create Sign-In UI Page (30-45 minutes)

#### 1.1 Create Sign-In Page Component

**File**: `frontend/src/pages/auth/signin.tsx`

```typescript
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from '@docusaurus/router';

export default function SignIn() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/'); // Redirect to home on success
    } catch (err) {
      // Error handling per research.md decision 2
      const errorMessage = err.message || 'An unexpected error occurred';

      if (errorMessage.includes('401') || errorMessage.includes('Invalid')) {
        setError('Invalid email or password. Please try again.');
      } else if (errorMessage.includes('500')) {
        setError('The service is temporarily unavailable. Please try again later.');
      } else if (errorMessage.includes('Network') || errorMessage.includes('timeout')) {
        setError('Network error. Please check your connection.');
      } else {
        setError('An unexpected error occurred. Please try again.');
      }

      // Client-side logging (FR-016)
      console.error('[Auth Error]', {
        timestamp: new Date().toISOString(),
        email, // OK to log email (not PII in logs)
        error: err.message
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
      <h1>Sign In</h1>
      <form onSubmit={handleSubmit}>
        {error && (
          <div style={{ color: 'red', marginBottom: '15px', padding: '10px', background: '#ffebee', borderRadius: '4px' }}>
            {error}
          </div>
        )}

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
            style={{ width: '100%', padding: '8px', fontSize: '16px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            style={{ width: '100%', padding: '8px', fontSize: '16px' }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <p style={{ marginTop: '15px', textAlign: 'center' }}>
        Don't have an account? <a href="/auth/signup">Sign up</a>
      </p>
    </div>
  );
}
```

**Test**: Navigate to http://localhost:3000/auth/signin and try logging in with test credentials.

---

### Phase 2: Integrate Auth with Chat Widget (45-60 minutes)

#### 2.1 Update ChatWidget to Check Auth State

**File**: `frontend/src/components/ChatWidget/ChatWidget.tsx`

**Changes**:
1. Import `useAuth` hook
2. Check `isAuthenticated` before opening chat
3. Show "Sign in to chat" message for unauthenticated users

```typescript
import { useAuth } from '../../contexts/AuthContext';

export const ChatWidget: React.FC<ChatWidgetProps> = () => {
  const { isChatVisible, closeChat: closeGlobalChat } = useChat();
  const { isAuthenticated } = useAuth(); // Add this line

  // ... existing state ...

  const toggleChat = () => {
    // Check auth before opening chat (FR-014)
    if (!isAuthenticated) {
      alert('Please sign in to use the chatbot.');
      // Or redirect: window.location.href = '/auth/signin';
      return;
    }

    // Existing toggle logic...
    setWidgetState(prevState => {
      // ... existing code ...
    });

    if (!showChatWindow) {
      setShowChatWindow(true);
    }
  };

  // ... rest of component ...
};
```

**Better UX**: Replace `alert()` with a modal or inline message:

```typescript
const [showAuthPrompt, setShowAuthPrompt] = useState(false);

const toggleChat = () => {
  if (!isAuthenticated) {
    setShowAuthPrompt(true);
    return;
  }
  // ... existing code ...
};

// In JSX:
{showAuthPrompt && (
  <div style={{ position: 'fixed', bottom: '80px', right: '20px', background: 'white', padding: '15px', border: '1px solid #ccc', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
    <p>Sign in to chat with the AI tutor</p>
    <button onClick={() => window.location.href = '/auth/signin'}>Sign In</button>
    <button onClick={() => setShowAuthPrompt(false)}>Cancel</button>
  </div>
)}
```

#### 2.2 Clear Chat History on Logout

**File**: `frontend/src/contexts/AuthContext.tsx`

**Changes**: Add chat history clearing to `logout()` method (FR-012):

```typescript
const logout = () => {
  setUser(null);
  setToken(null);
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');

  // Clear chat-related data (FR-012)
  localStorage.removeItem('chatHistory');
  localStorage.removeItem('chatRateLimit');

  console.log('[Auth] User logged out, chat history cleared');
};
```

---

### Phase 3: Add Chat Message History Management (60-90 minutes)

#### 3.1 Enhance ChatWindow to Persist Messages

**File**: `frontend/src/components/ChatWidget/ChatWindow.tsx`

**Changes**:
1. Load chat history from localStorage on mount
2. Save chat history to localStorage on each message
3. Clear history on component unmount if user logged out

```typescript
import { useState, useEffect } from 'react';
import { ChatMessage } from './models'; // Assume this interface exists

const CHAT_HISTORY_KEY = 'chatHistory';

export const ChatWindow: React.FC<ChatWindowProps> = ({ onClose }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Load chat history on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem(CHAT_HISTORY_KEY);
    if (savedHistory) {
      try {
        const parsed = JSON.parse(savedHistory);
        setMessages(parsed);
      } catch (e) {
        console.warn('Failed to load chat history:', e);
      }
    }
  }, []);

  // Save chat history on messages change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(messages));
    }
  }, [messages]);

  const handleSendMessage = async (messageText: string) => {
    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}-${Math.random()}`,
      content: messageText,
      sender: 'user',
      timestamp: new Date().toISOString(),
      status: 'sending'
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Call chat service
      const response = await chatService.sendMessage(messageText);

      // Update user message status
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'delivered' } : msg
        )
      );

      // Add AI response
      const aiMessage: ChatMessage = {
        id: `msg-${Date.now()}-${Math.random()}`,
        content: response.response,
        sender: 'ai',
        timestamp: response.timestamp || new Date().toISOString(),
        status: 'delivered',
        agentName: response.agent_name
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      // Update user message status to failed
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id ? { ...msg, status: 'failed' } : msg
        )
      );

      // Show error message
      console.error('[Chat Error]', error);
      alert(error.message || 'Failed to send message');
    }
  };

  return (
    <div className="chat-window">
      {/* Render messages */}
      {messages.map(msg => (
        <div key={msg.id} className={`message ${msg.sender}`}>
          <div className="content">{msg.content}</div>
          {msg.status === 'sending' && <span>Sending...</span>}
          {msg.status === 'failed' && (
            <button onClick={() => handleRetry(msg)}>Retry</button>
          )}
        </div>
      ))}
      {/* ... message input ... */}
    </div>
  );
};
```

---

### Phase 4: Error Handling and UX Polish (30-45 minutes)

#### 4.1 Add Message Validation with Character Counter

**File**: `frontend/src/components/ChatWidget/ChatWindow.tsx`

```typescript
const [inputValue, setInputValue] = useState('');
const [validationError, setValidationError] = useState('');

const handleInputChange = (value: string) => {
  setInputValue(value);

  // Validate length (FR-008)
  if (value.trim().length < 3 && value.trim().length > 0) {
    setValidationError('Message must be at least 3 characters');
  } else if (value.length > 10000) {
    setValidationError('Message must be under 10,000 characters');
  } else {
    setValidationError('');
  }
};

// In JSX:
<div>
  <textarea
    value={inputValue}
    onChange={(e) => handleInputChange(e.target.value)}
    placeholder="Type your message..."
  />
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <span style={{ color: validationError ? 'red' : 'gray' }}>
      {validationError || `${10000 - inputValue.length} characters remaining`}
    </span>
    <button
      onClick={() => handleSendMessage(inputValue)}
      disabled={!!validationError || inputValue.trim().length < 3}
    >
      Send
    </button>
  </div>
</div>
```

#### 4.2 Add Rate Limit Countdown Timer

**File**: `frontend/src/components/ChatWidget/ChatWindow.tsx`

```typescript
const [rateLimitCountdown, setRateLimitCountdown] = useState(0);

const handleRateLimitError = (retryAfterSeconds: number = 30) => {
  setRateLimitCountdown(retryAfterSeconds);

  const interval = setInterval(() => {
    setRateLimitCountdown(prev => {
      if (prev <= 1) {
        clearInterval(interval);
        return 0;
      }
      return prev - 1;
    });
  }, 1000);
};

// In error handling:
if (error.message.includes('Rate limit')) {
  handleRateLimitError(30);
}

// In JSX:
{rateLimitCountdown > 0 && (
  <div style={{ color: 'orange', marginBottom: '10px' }}>
    Rate limit exceeded. Try again in {rateLimitCountdown} seconds.
  </div>
)}
```

---

## Testing Checklist

### Authentication Flow
- [ ] Sign-in page renders at `/auth/signin`
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
- [ ] Logout clears token, user, chatHistory, chatRateLimit from localStorage
- [ ] 401 error triggers logout and redirect to sign-in
- [ ] Expired token detected and user logged out

---

## Common Issues and Solutions

### Issue: "CORS Error" when calling backend

**Solution**: Add CORS middleware to FastAPI backend:

```python
# backend/src/backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: "Module not found" errors in TypeScript

**Solution**: Ensure `tsconfig.json` has correct paths:

```json
{
  "extends": "@docusaurus/tsconfig",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

### Issue: localStorage not persisting across page reloads

**Solution**: Check browser privacy settings. In Incognito/Private mode, localStorage may be disabled. Test in normal browser window.

### Issue: Chat widget not showing for authenticated users

**Solution**: Verify `ChatContext.openChat()` is called after login:

```typescript
// In signin.tsx after successful login:
const { openChat } = useChat();
await login(email, password);
openChat(); // Auto-open chat after login
navigate('/');
```

---

## Next Steps

After completing this quickstart:

1. **Run `/sp.tasks`** to generate detailed TDD tasks
2. **Review `contracts/`** for API contract details
3. **Read `data-model.md`** for entity definitions
4. **Check `research.md`** for architectural decisions

**Questions?** Refer to the feature spec at `specs/001-connect-frontend-backend-apis/spec.md` or ask your team lead.

---

## Performance Optimization Tips

- Use React.memo() for message components to prevent unnecessary re-renders
- Debounce character counter updates (currently updates on every keystroke)
- Consider virtualization for long chat histories (react-window or react-virtuoso)
- Lazy-load ChatWindow component (React.lazy + Suspense)
- Implement request cancellation for rapid consecutive sends

---

## Security Reminders

- **Never log passwords** (not even in development)
- **Sanitize AI responses** before rendering (use DOMPurify)
- **Validate all user input** client-side before sending
- **Consider migrating from localStorage to HttpOnly cookies** (see ADR placeholder in research.md)
- **Implement Content Security Policy (CSP)** for production deployment

---

**Happy coding!** 🚀
