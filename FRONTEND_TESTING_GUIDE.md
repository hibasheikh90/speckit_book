# Frontend Testing Guide - Login & Authentication UI

**Date:** 2025-12-17
**Frontend URL:** http://localhost:3000
**Backend URL:** http://localhost:8000
**Status:** ✅ Both servers running

---

## 🎯 Testing Checklist

### Server Status:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ API endpoints functional
- ✅ Authentication system working

---

## 📋 Manual Testing Steps

### 1. Homepage Verification
**URL:** http://localhost:3000

**What to Check:**
- [ ] Page loads without errors
- [ ] Navigation bar displays correctly
- [ ] All links work
- [ ] Footer displays properly
- [ ] No console errors in browser DevTools

---

### 2. Login Page Testing
**URL:** http://localhost:3000/signin

**Test Cases:**

#### Test 2.1: Page Load
- [ ] Login form displays correctly
- [ ] Email input field visible
- [ ] Password input field visible
- [ ] Submit button present
- [ ] "Sign up" link present

#### Test 2.2: Valid Login
**Steps:**
1. Enter email: `chattest@example.com`
2. Enter password: `TestPassword123!`
3. Click "Login" button

**Expected:**
- [ ] Form submits without errors
- [ ] JWT token saved to localStorage
- [ ] Redirect to homepage or dashboard
- [ ] Success message or user menu appears
- [ ] User is logged in (check localStorage for 'authToken')

**Browser Console Check:**
```javascript
localStorage.getItem('authToken')
// Should return a JWT token
```

#### Test 2.3: Invalid Login - Wrong Password
**Steps:**
1. Enter email: `chattest@example.com`
2. Enter password: `WrongPassword123!`
3. Click "Login" button

**Expected:**
- [ ] Error message displayed: "Incorrect email or password"
- [ ] No token saved to localStorage
- [ ] User remains on login page
- [ ] Form doesn't clear (user can retry)

#### Test 2.4: Invalid Login - Nonexistent User
**Steps:**
1. Enter email: `nonexistent@example.com`
2. Enter password: `TestPassword123!`
3. Click "Login" button

**Expected:**
- [ ] Error message displayed: "Incorrect email or password"
- [ ] No token saved
- [ ] User remains on login page

#### Test 2.5: Form Validation
**Steps:**
1. Try submitting with empty email
2. Try submitting with invalid email format
3. Try submitting with empty password

**Expected:**
- [ ] Form validation prevents submission
- [ ] Clear error messages shown
- [ ] No API request made

---

### 3. Signup Page Testing
**URL:** http://localhost:3000/signup

**Test Cases:**

#### Test 3.1: Page Load
- [ ] Signup form displays correctly
- [ ] Email input field visible
- [ ] Password input field visible
- [ ] Confirm password field visible (if present)
- [ ] Submit button present
- [ ] "Sign in" link present

#### Test 3.2: Valid Registration
**Steps:**
1. Enter email: `newuser@example.com`
2. Enter password: `SecurePass123!`
3. Confirm password (if required)
4. Click "Sign Up" button

**Expected:**
- [ ] Form submits without errors
- [ ] Success message displayed
- [ ] Automatic login OR redirect to login page
- [ ] User can log in immediately

#### Test 3.3: Duplicate Email
**Steps:**
1. Enter email: `chattest@example.com` (already registered)
2. Enter password: `TestPassword123!`
3. Click "Sign Up" button

**Expected:**
- [ ] Error message: "Email already registered"
- [ ] User remains on signup page
- [ ] Can try with different email

#### Test 3.4: Weak Password
**Steps:**
1. Enter email: `weakpass@example.com`
2. Enter password: `weak` (too short, no uppercase, no number)
3. Click "Sign Up" button

**Expected:**
- [ ] Error message about password requirements
- [ ] Clear instructions: "8+ chars, uppercase, lowercase, number"
- [ ] Form doesn't submit
- [ ] User can fix and retry

#### Test 3.5: Invalid Email Format
**Steps:**
1. Enter email: `notanemail` (no @ or domain)
2. Enter password: `TestPassword123!`
3. Click "Sign Up" button

**Expected:**
- [ ] Email validation error
- [ ] Form doesn't submit
- [ ] Clear error message

---

### 4. Authentication Flow Testing

#### Test 4.1: Protected Route Access
**Steps:**
1. Without logging in, try to access a protected page
2. Check if redirected to login

**Expected:**
- [ ] Redirect to /signin
- [ ] Clear message: "Please log in to continue"

#### Test 4.2: Token Persistence
**Steps:**
1. Log in successfully
2. Refresh the page (F5)
3. Check if still logged in

**Expected:**
- [ ] User remains logged in after refresh
- [ ] Token persists in localStorage
- [ ] User info restored

#### Test 4.3: Logout
**Steps:**
1. Log in successfully
2. Click logout button (if present)
3. Check localStorage

**Expected:**
- [ ] Token removed from localStorage
- [ ] Redirect to homepage or login
- [ ] User menu disappears
- [ ] Protected routes now blocked

---

### 5. Chat Widget Testing
**URL:** http://localhost:3000 (after login)

**Test Cases:**

#### Test 5.1: Chat Widget Visibility
**Steps:**
1. Log in successfully
2. Look for chat widget/button on page

**Expected:**
- [ ] Chat button/widget visible
- [ ] Icon or label clearly visible
- [ ] Positioned in corner (typically bottom-right)

#### Test 5.2: Open Chat Window
**Steps:**
1. Click on chat widget button
2. Observe chat window

**Expected:**
- [ ] Chat window opens/expands
- [ ] Message input field visible
- [ ] Send button present
- [ ] Chat history area visible
- [ ] Close/minimize button present

#### Test 5.3: Send Message (Authenticated)
**Steps:**
1. Ensure logged in
2. Open chat widget
3. Type message: "What is ROS 2?"
4. Click send

**Expected:**
- [ ] Message appears in chat (user bubble)
- [ ] Loading indicator shows
- [ ] Response appears (bot bubble)
- [ ] Response text is readable
- [ ] No errors in console

**Note:** Due to Gemini API quota, might get mock response:
```
[Mock Response] Regarding 'What is ROS 2?':
This is a test response. The authentication system is
working correctly. (AI service temporarily unavailable
due to API quota.)
```

#### Test 5.4: Send Message (Not Authenticated)
**Steps:**
1. Log out
2. Try to open chat widget

**Expected:**
- [ ] Chat widget prompts to log in
- [ ] OR redirects to login page
- [ ] Clear message about authentication requirement

#### Test 5.5: Chat Persistence
**Steps:**
1. Send a few messages
2. Close chat widget
3. Reopen chat widget

**Expected:**
- [ ] Previous messages still visible
- [ ] Chat history persists
- [ ] Can continue conversation

---

## 🔍 Browser DevTools Checks

### Console (F12 → Console)
**Check for:**
- [ ] No JavaScript errors
- [ ] No failed API requests (check Network tab)
- [ ] No CORS errors
- [ ] API calls to http://localhost:8000

### Network Tab (F12 → Network)
**During Login:**
- [ ] POST request to `/auth/login`
- [ ] Status: 200 OK
- [ ] Response contains `access_token`

**During Registration:**
- [ ] POST request to `/auth/register`
- [ ] Status: 201 Created
- [ ] Response contains user `id` and `email`

**During Chat:**
- [ ] POST request to `/chat`
- [ ] Authorization header present: `Bearer <token>`
- [ ] Status: 200 OK (or 500 if API quota exceeded)

### Application Tab (F12 → Application)
**LocalStorage:**
```javascript
// After login, should see:
{
  "authToken": "eyJhbGciOiJIUzI1NiIs...",
  "user": '{"id":"...","email":"..."}',
  "chatWidgetState": "{...}"
}
```

---

## 🎨 UI/UX Checks

### Design & Layout:
- [ ] Responsive design (try different window sizes)
- [ ] Mobile-friendly (test on mobile or use DevTools device mode)
- [ ] Forms are well-aligned
- [ ] Buttons are clickable and styled
- [ ] Colors match the futuristic/robotics theme
- [ ] Typography is readable

### User Experience:
- [ ] Clear labels on all inputs
- [ ] Helpful error messages
- [ ] Loading states during API calls
- [ ] Success messages after actions
- [ ] Smooth transitions/animations
- [ ] No jarring page reloads

### Accessibility:
- [ ] Tab navigation works
- [ ] Form inputs have labels
- [ ] Buttons have proper aria labels
- [ ] Error messages are announced
- [ ] Color contrast is sufficient

---

## 🐛 Common Issues & Fixes

### Issue 1: CORS Error
**Symptom:** Console shows CORS policy error
**Check:** Backend CORS configuration
**Fix:** Ensure backend allows http://localhost:3000

### Issue 2: 401 Unauthorized
**Symptom:** All API calls return 401
**Check:**
- Token in localStorage
- Authorization header format: `Bearer <token>`
**Fix:** Log in again to get fresh token

### Issue 3: Chat Not Working
**Symptom:** Chat returns 500 error
**Reason:** Gemini API quota exceeded
**Expected:** This is normal - mock response should appear
**Verify:** Check server logs for "AI service error: Error code: 429"

### Issue 4: Frontend Not Loading
**Symptom:** Page shows blank or loading forever
**Check:**
- Frontend server running: `netstat -ano | findstr :3000`
- Check console for errors
**Fix:** Restart dev server: `npm run start`

### Issue 5: Backend Not Responding
**Symptom:** All API calls timeout
**Check:** Backend server running: `curl http://localhost:8000/health`
**Fix:** Restart backend: `python start_test_server.py`

---

## ✅ Success Criteria

**All tests pass if:**
1. ✅ Login page loads and looks good
2. ✅ Can register new user successfully
3. ✅ Can log in with registered credentials
4. ✅ JWT token saved in localStorage
5. ✅ Invalid credentials show appropriate errors
6. ✅ Chat widget appears after login
7. ✅ Can send messages (even if mock response)
8. ✅ Logout works and clears token
9. ✅ No console errors (except expected ones)
10. ✅ UI is responsive and looks professional

---

## 📊 Testing Results Template

```markdown
## Frontend Testing Results

**Date:** 2025-12-17
**Tester:** [Your Name]
**Browser:** [Chrome/Firefox/Safari/Edge]
**Status:** [Pass/Fail]

### Test Results:
- [ ] Homepage: Pass/Fail
- [ ] Login Page: Pass/Fail
- [ ] Signup Page: Pass/Fail
- [ ] Authentication Flow: Pass/Fail
- [ ] Chat Widget: Pass/Fail
- [ ] Error Handling: Pass/Fail
- [ ] UI/UX: Pass/Fail

### Issues Found:
1. [Issue description]
2. [Issue description]

### Notes:
[Any additional observations]
```

---

## 🚀 Quick Test Script

**For rapid verification, test these core flows:**

1. **Happy Path:**
   ```
   1. Go to /signup
   2. Register: test{timestamp}@example.com / TestPass123!
   3. Should redirect or auto-login
   4. Open chat widget
   5. Send message
   6. Verify response
   ```

2. **Error Path:**
   ```
   1. Go to /signin
   2. Try login with wrong password
   3. Verify error message
   4. Try with correct credentials
   5. Verify success
   ```

3. **Protected Route:**
   ```
   1. Log out
   2. Try to access chat
   3. Should redirect to login
   4. Log back in
   5. Chat should work
   ```

---

## 📞 URLs Reference

**Frontend:**
- Homepage: http://localhost:3000
- Login: http://localhost:3000/signin
- Signup: http://localhost:3000/signup
- Docs: http://localhost:3000/docs/intro

**Backend:**
- Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- Register: http://localhost:8000/auth/register
- Login: http://localhost:8000/auth/login
- Chat: http://localhost:8000/chat

---

## 🎯 Next Steps After Testing

**If All Tests Pass:**
1. Document any issues found
2. Create production build: `npm run build`
3. Test production build: `npm run serve`
4. Prepare for deployment

**If Issues Found:**
1. Document each issue with screenshots
2. Prioritize: Critical → High → Medium → Low
3. Fix issues one by one
4. Retest after fixes

---

**Happy Testing!** 🧪✨

If you encounter any issues, check:
1. Server logs (backend terminal)
2. Browser console (F12)
3. Network tab (F12 → Network)
4. This guide's "Common Issues" section
