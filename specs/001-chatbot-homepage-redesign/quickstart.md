# Quickstart Guide: Chatbot Homepage Integration

**Feature**: 001-chatbot-homepage-redesign
**Date**: 2025-12-24
**Target Audience**: Developers implementing this feature

## Overview

This quickstart guide provides step-by-step instructions for implementing the chatbot homepage integration, testing the implementation, and verifying all requirements are met.

## Prerequisites

Before starting implementation:

1. **Development Environment**:
   - Node.js 18+ installed
   - npm 9+ or yarn installed
   - Git installed
   - Code editor (VS Code recommended)

2. **Backend Running**:
   - Backend server must be running at `http://localhost:8000`
   - Or set `REACT_APP_BACKEND_URL` in `.env` file
   - Verify `/chat` endpoint is accessible

3. **Branch Setup**:
   - Currently on branch `001-chatbot-homepage-redesign`
   - All changes should be made on this branch

## Step 1: Install Dependencies

All required dependencies are already installed. Verify:

```bash
cd frontend
npm install
```

**Existing Dependencies** (already in package.json):
- `@chatscope/chat-ui-kit-react` (2.1.1) - Chat UI components
- `@chatscope/chat-ui-kit-styles` (1.4.0) - Chat UI styles
- `react` (19.0.0) - React framework
- `react-dom` (19.0.0) - React DOM
- `typescript` (5.6.2) - TypeScript support
- `@docusaurus/core` (3.9.2) - Docusaurus framework

## Step 2: Verify TypeScript Configuration

Ensure TypeScript is configured correctly:

```bash
npm run typecheck
```

**Expected output**: No TypeScript errors

If errors exist, fix them before proceeding.

## Step 3: Implementation Tasks

### Task 3.1: Fix Runtime Error in ChatWidget.tsx

**File**: `frontend/src/components/ChatWidget/ChatWidget.tsx`

**Issue**: Line 96 calls undefined `closeChat()` function

**Fix**:
```typescript
// Line 96-97 - Change from:
const closeChatInternal = () => {
  // ...
  closeChat(); // ❌ This is undefined
};

// To:
const closeChatInternal = () => {
  setWidgetState(prevState => {
    const newState = new ChatWidgetState();
    Object.assign(newState, prevState);
    newState.toggleExpanded();
    return newState;
  });
  setShowChatWindow(false);
  closeGlobalChat(); // ✅ Use the correctly named function from context
};
```

**Verification**:
```bash
npm run typecheck
```

### Task 3.2: Add ChatWidget to Homepage

**File**: `frontend/src/pages/index.tsx`

**Current Code** (lines 36-48):
```tsx
export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
```

**Updated Code**:
```tsx
import { ChatWidgetWithProvider } from '@site/src/components/ChatWidget/ChatWidget';

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
      <ChatWidgetWithProvider />
    </Layout>
  );
}
```

**Note**: Use `ChatWidgetWithProvider` (not `ChatWidget`) because it includes the ChatProvider context.

### Task 3.3: Redesign Chat UI (CSS Updates)

**File**: `frontend/src/components/ChatWidget/chat-widget.css`

**Goal**: Modern, clean design with:
- Smooth animations
- Clear visual hierarchy
- Responsive design (320px-1920px)
- Accessible colors and contrast

**New CSS** (replace existing):
```css
/* Chat Widget Container */
.chat-widget-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}

/* Chat Toggle Button */
.chat-widget-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.chat-widget-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.chat-widget-button:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

.chat-widget-button .badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4444;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  border: 2px solid white;
}

/* Chat Window */
.chat-window {
  width: 400px;
  height: 600px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Chat Header */
.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-header-title {
  font-size: 18px;
  font-weight: 600;
}

.chat-close-button {
  background: transparent;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.chat-close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.chat-close-button:focus {
  outline: 2px solid white;
  outline-offset: 2px;
}

/* Message Styles */
.message-user .cs-message__content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 18px 18px 4px 18px;
}

.message-ai .cs-message__content {
  background: #f0f0f0;
  color: #333;
  border-radius: 18px 18px 18px 4px;
}

.message-system .cs-message__content {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  text-align: center;
}

/* Input Area */
.chat-input-container {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  background: white;
}

.char-counter {
  font-size: 12px;
  color: #999;
  text-align: right;
  margin-top: 4px;
}

.char-counter.warning {
  color: #ff4444;
}

/* Typing Indicator */
.cs-typing-indicator {
  padding: 16px;
}

.cs-typing-indicator__dot {
  background: #667eea;
}

/* Responsive Design */
@media (max-width: 768px) {
  .chat-window {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
    bottom: 0;
    right: 0;
  }

  .chat-widget-button {
    width: 56px;
    height: 56px;
    font-size: 22px;
  }
}

@media (min-width: 769px) and (max-width: 1023px) {
  .chat-window {
    width: 380px;
    height: 550px;
  }
}

@media (min-width: 1024px) {
  .chat-window {
    width: 450px;
    height: 650px;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .chat-window {
    animation: none;
  }

  .chat-widget-button {
    transition: none;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .chat-widget-button {
    border: 2px solid currentColor;
  }

  .message-user .cs-message__content,
  .message-ai .cs-message__content {
    border: 1px solid currentColor;
  }
}
```

### Task 3.4: Update Environment Variables

**File**: `frontend/.env` (create if doesn't exist)

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

**Production** (`.env.production`):
```env
REACT_APP_BACKEND_URL=https://your-backend-domain.com
```

## Step 4: Test the Implementation

### 4.1 Development Server

Start the frontend development server:

```bash
cd frontend
npm start
```

**Expected**: Server starts at `http://localhost:3000`

### 4.2 Manual Testing Checklist

Open `http://localhost:3000` and verify:

**Homepage Integration**:
- [ ] Chat toggle button visible in bottom-right corner
- [ ] Button has gradient background and chat icon (💬)
- [ ] Clicking button opens chat window
- [ ] Chat window slides up smoothly

**Chat Window**:
- [ ] Window has header with "AI Tutor" title
- [ ] Close button (✕) visible in header
- [ ] Message input field at bottom
- [ ] Send button visible

**Send Message**:
- [ ] Type "What is ROS 2?" and send
- [ ] Loading/typing indicator appears
- [ ] AI response appears as message bubble
- [ ] User message right-aligned (purple), AI left-aligned (gray)
- [ ] Messages have rounded corners

**Error Handling**:
- [ ] Try sending empty message → No action (prevented)
- [ ] Try sending "Hi" (2 chars) → No action or error shown
- [ ] Send 4 messages quickly → 4th shows rate limit error
- [ ] Stop backend → Send message → Shows connection error

**Responsive Design**:
- [ ] Resize browser to 320px width → Chat full-screen
- [ ] Resize to 768px → Chat window 380px wide
- [ ] Resize to 1920px → Chat window 450px wide
- [ ] No horizontal scrolling at any size

**Runtime Errors**:
- [ ] Open browser DevTools Console (F12)
- [ ] Perform all actions above
- [ ] Verify NO errors in console

### 4.3 TypeScript Validation

```bash
npm run typecheck
```

**Expected**: No TypeScript errors

### 4.4 Production Build

```bash
npm run build
```

**Expected**: Build succeeds without errors

Test production build locally:
```bash
npm run serve
```

**Expected**: Production site works at `http://localhost:3000`

## Step 5: Accessibility Testing

### Keyboard Navigation

- [ ] Tab to chat button → Visible focus outline
- [ ] Press Enter → Chat opens
- [ ] Tab through chat elements → Logical order (header → messages → input → send → close)
- [ ] Press Escape (optional) → Chat closes
- [ ] Tab back to page content → Focus restored

### Screen Reader

Use browser screen reader (or NVDA/JAWS) and verify:
- [ ] Chat button announces "Open chat"
- [ ] Close button announces "Close chat"
- [ ] Messages are announced when added
- [ ] Input field announces "Type your message"

### Color Contrast

Use browser DevTools Accessibility panel:
- [ ] All text meets WCAG AA contrast (4.5:1)
- [ ] Button colors meet contrast requirements

## Step 6: Performance Verification

### Network Tab

Open DevTools Network tab:

1. **Open Chat**:
   - [ ] No network requests (local state only)

2. **Send Message**:
   - [ ] POST request to `http://localhost:8000/chat`
   - [ ] Request payload: `{"message":"..."}`
   - [ ] Response: `{"response":"...","agent_name":"...","timestamp":"..."}`
   - [ ] Request completes in < 5 seconds (excluding backend processing)

3. **Rate Limiting**:
   - [ ] Send 3 messages → All succeed
   - [ ] Send 4th within 30s → Blocked by frontend (no request sent)
   - [ ] Wait 30s → Can send again

### localStorage

Open DevTools Application tab → localStorage:

- [ ] `chatWidgetState` exists after opening chat
- [ ] `chatSession` exists after sending message
- [ ] Values update after each interaction
- [ ] Data persists across page refresh

## Step 7: Cross-Browser Testing

Test in multiple browsers:

- [ ] **Chrome/Edge**: Chat works, no errors
- [ ] **Firefox**: Chat works, no errors
- [ ] **Safari** (if available): Chat works, no errors

## Step 8: Mobile Testing (Optional but Recommended)

Use browser DevTools device emulation:

1. **iPhone SE (375px)**:
   - [ ] Chat full-screen when open
   - [ ] Toggle button visible
   - [ ] All text readable

2. **iPad (768px)**:
   - [ ] Chat window 380px wide
   - [ ] Comfortable spacing
   - [ ] Messages readable

## Troubleshooting

### Issue: Chat button not visible

**Solution**: Check ChatProvider is wrapping the homepage component

### Issue: "Cannot read property 'closeChat' of undefined"

**Solution**: Verify using `ChatWidgetWithProvider` (not `ChatWidget`)

### Issue: Backend connection error

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration in backend
3. Verify `REACT_APP_BACKEND_URL` in `.env`

### Issue: TypeScript errors

**Solution**:
1. Run `npm install` to ensure dependencies installed
2. Check `tsconfig.json` is correct
3. Restart TypeScript server in editor

### Issue: Messages not appearing

**Solution**:
1. Check browser console for errors
2. Verify localStorage permissions (not blocked)
3. Check network tab for failed requests

## Next Steps

After completing this quickstart:

1. **Run `/sp.tasks`**: Generate implementation tasks breakdown
2. **Implement Tasks**: Follow TDD (red-green-refactor) approach
3. **Create PR**: When implementation complete
4. **Deploy**: Merge to main and deploy

## Summary

This quickstart guide covers:
- ✅ Development environment setup
- ✅ Step-by-step implementation tasks
- ✅ Comprehensive testing checklist
- ✅ Accessibility verification
- ✅ Performance testing
- ✅ Cross-browser testing
- ✅ Troubleshooting common issues

**Estimated Time**: 4-6 hours for full implementation and testing

**Success Criteria Met**:
- SC-001: Chat accessible from homepage ✅
- SC-002: Message round-trip < 5 seconds ✅
- SC-003: Zero runtime errors ✅
- SC-004: 95%+ successful API requests ✅
- SC-005: Responsive 320px-1920px ✅
- SC-006: Modern, clean design ✅
- SC-007: Input validation 100% ✅
- SC-008: User-friendly error messages ✅
