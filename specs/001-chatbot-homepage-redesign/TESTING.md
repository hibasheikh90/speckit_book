# Testing Guide: Chatbot Homepage Redesign

**Feature**: Chatbot Homepage Integration and UI Redesign
**Branch**: `001-chatbot-homepage-redesign`
**Date**: 2025-12-24

## Quick Start Testing

### Prerequisites
1. Node.js and npm installed
2. Python 3.8+ installed
3. Backend dependencies installed: `cd backend && pip install -r requirements.txt`
4. Frontend dependencies installed: `cd frontend && npm install`

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Access**: Open http://localhost:3000 in your browser

---

## Test Scenarios

### Test Scenario 1: First-Time User on Homepage ✅

**Objective**: Verify chat button is visible and welcome message displays correctly

**Steps**:
1. Navigate to http://localhost:3000
2. Verify chat button (💬) appears in bottom-right corner
3. Click the chat button
4. Verify chat window opens with:
   - Header showing "AI Tutor"
   - Close button (✕) in top-right
   - Welcome message with waving hand icon (👋)
   - Text: "I'm your AI tutor for Physical AI and Humanoid Robotics"
   - Three suggested topics

**Expected Result**:
- Chat button visible and accessible
- Chat window opens smoothly without page refresh
- Welcome message displays with animation
- No console errors

**Acceptance Criteria**:
- [ ] Chat button visible in bottom-right
- [ ] Chat window opens on click
- [ ] Welcome message displays correctly
- [ ] No JavaScript errors in console

---

### Test Scenario 2: Send Message and Receive Response ✅

**Objective**: Verify end-to-end message flow from frontend to backend

**Steps**:
1. Open chat window
2. Type message: "What is Physical AI?"
3. Verify character counter shows "19 / 10000"
4. Click send button (➤) or press Enter
5. Verify user message appears immediately (blue gradient, right-aligned)
6. Verify "AI Tutor is typing..." indicator appears
7. Wait for backend response
8. Verify AI response appears (dark background, left-aligned)
9. Open DevTools Network tab and verify:
   - POST request to http://localhost:8000/chat
   - Request body: `{"message": "What is Physical AI?"}`
   - Response status: 200 OK
   - Response body contains: `response`, `agent_name`, `timestamp`

**Expected Result**:
- Message sent successfully
- Backend returns response
- UI updates correctly
- No errors in console or network

**Acceptance Criteria**:
- [ ] Message appears in chat immediately after sending
- [ ] Typing indicator shows while waiting
- [ ] Backend response displays correctly
- [ ] Network request succeeds (200 OK)
- [ ] No console errors

---

### Test Scenario 3: Input Validation ✅

**Objective**: Verify input validation prevents invalid messages

**Test 3a: Empty Message**
1. Open chat
2. Try to send empty message (just spaces)
3. Verify send button is disabled
4. Expected: Button grayed out, no request sent

**Test 3b: Message Too Short (< 3 characters)**
1. Type "Hi"
2. Click send
3. Verify validation error: "Message must be at least 3 characters"
4. Expected: Error message appears in red, no request sent

**Test 3c: Message Too Long (> 10,000 characters)**
1. Paste text longer than 10,000 characters
2. Verify character counter turns orange/warning color
3. Verify send button is disabled
4. Expected: Counter shows "10001 / 10000" in warning color, button disabled

**Test 3d: Valid Message (3-10,000 characters)**
1. Type "Tell me about robotics"
2. Verify character counter shows "23 / 10000"
3. Verify send button is enabled
4. Click send
5. Expected: Message sent successfully

**Acceptance Criteria**:
- [ ] Empty messages blocked
- [ ] Messages < 3 chars blocked with error
- [ ] Messages > 10,000 chars blocked with warning
- [ ] Valid messages (3-10,000 chars) send successfully
- [ ] Character counter updates in real-time

---

### Test Scenario 4: Rate Limiting ✅

**Objective**: Verify frontend rate limiting (3 requests per 30 seconds)

**Steps**:
1. Open chat
2. Send message 1: "Question 1" (succeeds)
3. Send message 2: "Question 2" (succeeds)
4. Send message 3: "Question 3" (succeeds)
5. Try to send message 4: "Question 4" immediately
6. Verify error message: "Rate limit exceeded. Try again in Xs"
7. Verify countdown timer displays (e.g., "Try again in 27s")
8. Verify send button is disabled
9. Wait for countdown to reach 0
10. Verify send button re-enables
11. Send message 4 successfully

**Expected Result**:
- First 3 messages succeed within 30 seconds
- 4th message blocked with rate limit error
- Countdown timer displays and decrements every second
- After 30 seconds, rate limit resets
- User can send messages again

**Acceptance Criteria**:
- [ ] 3 messages succeed within 30 seconds
- [ ] 4th message blocked with clear error
- [ ] Countdown timer displays and updates
- [ ] Send button disabled during rate limit
- [ ] Rate limit resets after 30 seconds

---

### Test Scenario 5: Error Handling ✅

**Objective**: Verify graceful error handling for various failure scenarios

**Test 5a: Backend Unreachable**
1. Stop backend server (Ctrl+C in backend terminal)
2. Try to send message
3. Verify error: "Unable to connect. Please check your connection."
4. Expected: User-friendly error in chat, no technical details

**Test 5b: Backend Returns 500 Error**
1. Backend running but encounters error
2. Send message that triggers 500 response
3. Verify error: "Service temporarily unavailable. Please try again."
4. Expected: Friendly error message, no stack trace

**Test 5c: Network Timeout**
1. Simulate slow network (>30 seconds)
2. Send message
3. After 30 seconds, verify timeout error
4. Expected: "Request timed out. Please try again."

**Acceptance Criteria**:
- [ ] Network errors show friendly message
- [ ] 500 errors show friendly message
- [ ] Timeouts handled gracefully
- [ ] No technical details exposed to user
- [ ] All errors displayed as system messages in chat

---

### Test Scenario 6: Responsive Design ✅

**Objective**: Verify chat works on all screen sizes

**Screen Sizes to Test**:
- Mobile small: 320x568 (iPhone SE)
- Mobile large: 414x896 (iPhone 11)
- Tablet: 768x1024 (iPad)
- Desktop: 1920x1080

**Steps for Each Size**:
1. Open Chrome DevTools (F12)
2. Click responsive mode icon
3. Select device or enter custom dimensions
4. Reload page
5. Verify chat button visible and clickable (≥44px touch target)
6. Open chat
7. Verify window scales appropriately:
   - Mobile (<480px): Full screen
   - Tablet (480-768px): 350px wide
   - Desktop (>768px): 400px wide
8. Send a message
9. Verify input field is usable
10. Verify no horizontal scrolling
11. Verify all text is readable (≥14px)

**Acceptance Criteria**:
- [ ] Chat button visible on all screen sizes
- [ ] Touch targets ≥44px on mobile
- [ ] Chat window scales appropriately
- [ ] No horizontal scrolling
- [ ] Text readable (≥14px font)
- [ ] Input usable on all devices

---

### Test Scenario 7: Accessibility ✅

**Objective**: Verify keyboard navigation and screen reader support

**Keyboard Navigation**:
1. Tab to chat button → verify focus visible
2. Press Enter → chat opens
3. Tab to input field → verify focus visible
4. Type message
5. Press Enter → message sends
6. Tab to close button → verify focus visible
7. Press Enter → chat closes
8. Press Escape (in chat) → chat closes

**Screen Reader**:
1. Enable screen reader (NVDA/JAWS/VoiceOver)
2. Tab to chat button
3. Verify announces: "Open chat, button"
4. Open chat
5. Verify header announces: "AI Tutor, dialog"
6. Tab to input
7. Verify announces: "Message input"
8. Type and send message
9. Verify new messages are announced

**Acceptance Criteria**:
- [ ] All elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Tab order logical
- [ ] Enter/Escape keys work correctly
- [ ] Aria labels present and accurate
- [ ] Screen reader announces content correctly

---

## Console Error Check ⚠️ CRITICAL

**Objective**: Zero console errors during all operations

**Steps**:
1. Open Chrome DevTools Console (F12)
2. Filter to "Errors" only
3. Perform all operations:
   - Open chat
   - Send 5 messages
   - Trigger validation error
   - Trigger rate limit
   - Close chat
   - Reopen chat
4. Scroll through messages
5. Close and reopen multiple times
6. Check console for:
   - Red errors ❌
   - Yellow warnings ⚠️
   - React warnings
   - Memory leaks

**Expected Result**: **ZERO errors or warnings**

**Common Issues to Watch For**:
- "Can't perform a React state update on an unmounted component"
- "Each child in a list should have a unique key prop"
- "findDOMNode is deprecated"
- "Warning: validateDOMNesting"
- CORS errors
- Network errors (should be handled gracefully)

**Acceptance Criteria**:
- [ ] **ZERO console errors when opening chat**
- [ ] **ZERO console errors when sending messages**
- [ ] **ZERO console errors when closing chat**
- [ ] **ZERO React warnings**
- [ ] **NO memory leak warnings**

---

## Performance Metrics

**Objective**: Verify performance targets from spec

**Metrics to Measure**:

1. **Chat Open Time**: < 2 seconds
   - Start: Click chat button
   - End: Chat window fully rendered
   - Measure: Chrome DevTools Performance tab

2. **Message Round-Trip**: < 5 seconds (excluding backend processing)
   - Start: Click send button
   - End: AI response displayed
   - Measure: Network tab timestamps

3. **Smooth Scrolling**: 60fps
   - Send 20+ messages
   - Scroll through message list
   - Measure: DevTools Performance → FPS meter

4. **Bundle Size Impact**:
   - Run: `npm run build`
   - Check: `build/static/js/*.js` sizes
   - Document: Total bundle size increase

**Acceptance Criteria**:
- [ ] Chat opens in < 2 seconds
- [ ] Message round-trip < 5 seconds total
- [ ] Scrolling maintains 60fps
- [ ] Bundle size documented

---

## Browser Compatibility

**Browsers to Test**:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**Test Matrix**:
| Browser | Open Chat | Send Message | Validation | Rate Limit | Errors | Responsive |
|---------|-----------|--------------|------------|------------|---------|------------|
| Chrome  | [ ]       | [ ]          | [ ]        | [ ]        | [ ]     | [ ]        |
| Firefox | [ ]       | [ ]          | [ ]        | [ ]        | [ ]     | [ ]        |
| Safari  | [ ]       | [ ]          | [ ]        | [ ]        | [ ]     | [ ]        |
| Edge    | [ ]       | [ ]          | [ ]        | [ ]        | [ ]     | [ ]        |

---

## Regression Testing

**Existing Features to Verify Still Work**:

1. **Homepage**:
   - [ ] Homepage loads correctly
   - [ ] Hero section displays
   - [ ] "Sign in to Read" button works
   - [ ] Navigation menu works

2. **Docusaurus Site**:
   - [ ] Docs pages load
   - [ ] Sidebar navigation works
   - [ ] Search works (if enabled)
   - [ ] Dark mode toggle works

3. **Layout**:
   - [ ] Footer displays correctly
   - [ ] Navbar displays correctly
   - [ ] Chat widget doesn't overlap content

---

## Manual Testing Checklist

Complete this checklist before marking testing as done:

### Setup
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser DevTools open (Console + Network tabs)

### Basic Functionality
- [ ] Chat button visible on homepage
- [ ] Chat button clickable
- [ ] Chat window opens/closes
- [ ] Welcome message displays
- [ ] Can type in input field
- [ ] Can send message
- [ ] Backend receives message
- [ ] AI response displays

### Validation
- [ ] Empty message blocked
- [ ] Short message (<3 chars) blocked
- [ ] Long message (>10,000 chars) blocked
- [ ] Character counter updates
- [ ] Valid message sends

### Rate Limiting
- [ ] 3 messages succeed in 30s
- [ ] 4th message blocked
- [ ] Countdown timer works
- [ ] Rate limit resets after 30s

### Error Handling
- [ ] Network error handled
- [ ] 500 error handled
- [ ] Timeout handled
- [ ] Errors displayed as system messages

### UI/UX
- [ ] Loading indicator shows
- [ ] Typing indicator shows
- [ ] Messages auto-scroll
- [ ] Send button disabled when invalid
- [ ] Visual feedback on all actions

### Responsive
- [ ] Works on mobile (320px)
- [ ] Works on tablet (768px)
- [ ] Works on desktop (1920px)
- [ ] No horizontal scroll
- [ ] Touch targets ≥44px

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Screen reader compatible
- [ ] Proper ARIA labels

### Performance
- [ ] Chat opens < 2s
- [ ] Message round-trip < 5s
- [ ] Smooth scrolling (60fps)
- [ ] No memory leaks

### Console
- [ ] ✅ **ZERO console errors**
- [ ] ✅ **ZERO React warnings**
- [ ] ✅ **NO deprecation warnings**

---

## Known Issues

*Document any known issues or limitations discovered during testing*

1. **Issue**: [Description]
   - **Severity**: Critical/High/Medium/Low
   - **Steps to Reproduce**: [Steps]
   - **Workaround**: [If any]
   - **Status**: Open/In Progress/Fixed

---

## Test Results Summary

**Date Tested**: YYYY-MM-DD
**Tester**: [Name]
**Browser**: [Browser + Version]
**OS**: [Operating System]

**Overall Status**: ✅ PASS / ⚠️ PASS WITH ISSUES / ❌ FAIL

**Test Summary**:
- Scenarios Passed: X/7
- Console Errors: 0 ✅
- Performance: Within Targets ✅
- Responsive: All Sizes ✅
- Accessibility: Keyboard + Screen Reader ✅

**Notes**:
[Any additional observations or comments]

---

## Next Steps After Testing

1. **If All Tests Pass**:
   - Create pull request
   - Request code review
   - Schedule deployment

2. **If Issues Found**:
   - Document issues in Known Issues section
   - Create GitHub issues for critical bugs
   - Fix issues and re-test
   - Update test results

3. **Documentation**:
   - Update README with chat widget usage
   - Document environment variables
   - Add troubleshooting guide

---

**Last Updated**: 2025-12-24
**Test Spec Version**: 1.0
