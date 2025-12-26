# Quickstart Guide: Chat Connectivity Fix

**Feature**: Fix Chat Frontend-Backend Connectivity
**Branch**: `001-fix-chat-connectivity`
**Purpose**: Step-by-step guide to diagnose, fix, and verify chat connectivity

## Prerequisites

Before starting, ensure you have:

- **Node.js**: v20.0.0 or higher
  ```bash
  node --version  # Should show v20.x.x or higher
  ```

- **Python**: 3.11 or higher
  ```bash
  python --version  # Should show Python 3.11.x or higher
  ```

- **Package Managers**: npm (comes with Node) and pip (comes with Python)

- **Git**: Repository cloned and on correct branch
  ```bash
  git branch  # Should show * 001-fix-chat-connectivity
  ```

## Quick Diagnosis (5 minutes)

Run these checks to identify the issue:

### Step 1: Check Backend Service

```bash
# Windows PowerShell
netstat -an | findstr 8000

# Unix/Mac/Linux
netstat -an | grep 8000
```

**Expected**: Line showing `LISTENING` on port 8000
**If Empty**: Backend not running → Go to "Start Backend" section

### Step 2: Check Frontend Service

```bash
# Windows PowerShell
netstat -an | findstr 3000

# Unix/Mac/Linux
netstat -an | grep 3000
```

**Expected**: Line showing `LISTENING` on port 3000
**If Empty**: Frontend not running → Go to "Start Frontend" section

### Step 3: Check CORS Configuration

```bash
grep -n "CORSMiddleware" backend/src/backend/main.py
```

**Expected**: Lines showing CORS middleware import and configuration
**If Empty**: CORS not configured → **This is likely the issue!**

## Fix: Add CORS Middleware (PRIMARY SOLUTION)

### Step 1: Edit Backend Main File

**File**: `backend/src/backend/main.py`

**Location**: After line 2 (imports section), add:
```python
from fastapi.middleware.cors import CORSMiddleware
```

**Location**: After line 21 (`app = FastAPI(...)`), add:
```python
# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Docusaurus dev server
        "http://127.0.0.1:3000",     # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

**Full Context (How it should look)**:
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ← ADD THIS
from slowapi import Limiter, _rate_limit_exceeded_handler
# ... other imports ...

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Educational AI Tutor API", version="1.0.0")

# Configure CORS for frontend communication  # ← ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(registration.router)
# ... rest of file ...
```

### Step 2: Restart Backend Service

If backend is running, stop it (Ctrl+C) and restart:

```bash
cd backend
uvicorn src.backend.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
Starting up AI tutor service...
AI tutor service ready!
INFO:     Application startup complete.
```

**If Error "ModuleNotFoundError"**: Install dependencies first:
```bash
pip install -r requirements.txt
```

**If Error "Port 8000 already in use"**:
```bash
# Windows: Find and kill process
netstat -ano | findstr 8000
taskkill /PID <process_id> /F

# Unix/Mac: Find and kill process
lsof -ti:8000 | xargs kill -9
```

## Start Backend (If Not Running)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Expected**: List of packages installing (FastAPI, Cohere SDK, etc.)

### Step 2: Verify Environment Variables

```bash
# Check if .env file exists
ls .env  # Should show backend/.env

# Verify Cohere API key is set
cat .env | grep COHERE_API_KEY
```

**Expected**: `COHERE_API_KEY=vI1pNLILAXVcEw5xS9V1zQDEDWofStxmc87UepOn`

**If Missing**: Copy from `.env.example` and add your Cohere API key

### Step 3: Start Backend Server

```bash
uvicorn src.backend.main:app --reload
```

**Keep this terminal open** - backend must stay running for chat to work.

## Start Frontend (If Not Running)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

**Expected**: Installation of React, Docusaurus, and other packages

### Step 2: Verify Environment Variables

```bash
# Check if .env file exists
ls .env  # Should show frontend/.env

# Verify backend URL is set
cat .env
```

**Expected**:
```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8000
```

**If Missing or Wrong**:
```bash
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env
```

### Step 3: Start Frontend Server

```bash
npm start
```

**Expected Output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

**Keep this terminal open** - frontend must stay running.

**Browser Auto-Opens**: Should automatically open `http://localhost:3000`
**If Not**: Manually open browser to `http://localhost:3000`

## Test Chat Connectivity (2 minutes)

### Step 1: Open Chat Widget

1. Browser should be on `http://localhost:3000`
2. Look for chat widget icon (usually bottom-right corner)
3. Click to open chat interface

### Step 2: Send Test Message

1. Type: `Hello`
2. Click **Send** button or press **Enter**
3. **Expected**: Message appears immediately, typing indicator shows

### Step 3: Verify AI Response

1. Wait 2-5 seconds
2. **Expected**: AI tutor response appears in chat
3. **Example Response**: "Hello! I'm your educational AI tutor for Physical AI and Humanoid Robotics. How can I help you today?"

### Step 4: Check Browser Console (If Failed)

1. Press **F12** to open Developer Tools
2. Click **Console** tab
3. **Look for errors**:

**If CORS Error** (red text):
```
Access to fetch at 'http://localhost:8000/chat' from origin 'http://localhost:3000'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header
```
**Solution**: CORS middleware not added or backend not restarted → Go back to "Fix: Add CORS Middleware"

**If Connection Error**:
```
Failed to fetch
TypeError: NetworkError when attempting to fetch resource
```
**Solution**: Backend not running → Go to "Start Backend"

**If 404 Error**:
```
POST http://localhost:8000/chat 404 (Not Found)
```
**Solution**: Wrong backend URL or endpoint path incorrect → Verify backend is running and `/chat` endpoint exists

## Verify Success Criteria

After chat is working, test these scenarios from the spec:

### ✅ Test 1: Basic Send/Receive (SC-001)
- **Action**: Send "How does a robot balance?"
- **Expected**: Receive educational response within 5 seconds
- **Pass Criteria**: Response appears with tutor's answer

### ✅ Test 2: Error Handling (User Story 2)
- **Action**: Stop backend (Ctrl+C in backend terminal), try sending message
- **Expected**: Error message "Unable to connect. Please check your connection." appears
- **Pass Criteria**: User-friendly error (not technical crash)
- **Cleanup**: Restart backend after test

### ✅ Test 3: Rate Limiting (User Story 3)
- **Action**: Send 3 messages rapidly, then try a 4th immediately
- **Expected**: 4th message blocked, countdown timer shows
- **Pass Criteria**: "Rate limit reached. Please wait X seconds" message

### ✅ Test 4: Message Persistence (SC-005)
- **Action**: Send 2 messages, refresh page (F5)
- **Expected**: Messages still visible in chat history
- **Pass Criteria**: localStorage maintains session across refreshes

## Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Cause**: Backend dependencies not installed
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "Error: Cannot find module 'react'"

**Cause**: Frontend dependencies not installed
**Solution**:
```bash
cd frontend
npm install
```

### Issue: Chat widget not visible

**Cause**: Frontend not fully loaded or widget component not rendering
**Solution**:
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Check browser console for React errors

### Issue: "Address already in use" (Port 8000 or 3000)

**Cause**: Another process using the port
**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Unix/Mac
lsof -ti:8000 | xargs kill -9
```

### Issue: Environment variable not loading in Docusaurus

**Cause**: `.env` changed but Docusaurus not restarted
**Solution**:
1. Stop frontend (Ctrl+C)
2. Restart: `npm start`
3. **Note**: Docusaurus only loads .env on startup, not during hot reload

### Issue: CORS error after adding middleware

**Cause**: Backend not restarted after code change
**Solution**:
1. Stop backend (Ctrl+C)
2. Restart: `uvicorn src.backend.main:app --reload`
3. Verify "Application startup complete" message

### Issue: "Cohere API error" in backend logs

**Cause**: Invalid Cohere API key or quota exceeded
**Solution**:
1. Check `backend/.env` has valid `COHERE_API_KEY`
2. Test API key at https://dashboard.cohere.com/
3. Check API usage/quota limits

## Development Workflow

For daily development, follow this startup sequence:

### Terminal 1: Backend
```bash
cd backend
uvicorn src.backend.main:app --reload
# Leave running
```

### Terminal 2: Frontend
```bash
cd frontend
npm start
# Leave running
```

### Browser
```
Open: http://localhost:3000
Test: Click chat widget → Send message → Verify response
```

**Keep both terminals open** while developing. Services auto-reload on code changes:
- Backend: `--reload` flag auto-restarts on Python file changes
- Frontend: Docusaurus hot-reloads on React/TypeScript changes

## Next Steps

After connectivity is working:

1. **Run `/sp.tasks`**: Generate detailed implementation tasks
2. **Implement CORS fix**: Add middleware code to backend
3. **Test thoroughly**: Run all acceptance scenarios from spec
4. **Document**: Update README with CORS configuration notes
5. **Commit**: Create git commit with fix
6. **PR**: Create pull request for review

## Success Checklist

Before marking this feature complete, verify:

- [ ] Backend running on port 8000 with CORS middleware
- [ ] Frontend running on port 3000
- [ ] Chat widget visible and clickable
- [ ] Test message sent successfully
- [ ] AI response received within 5 seconds
- [ ] Error handling works (backend stopped test)
- [ ] Rate limiting works (4 messages test)
- [ ] Message persistence works (page refresh test)
- [ ] No CORS errors in browser console
- [ ] No connection errors in browser console

**All checked?** ✅ Chat connectivity is FIXED!
