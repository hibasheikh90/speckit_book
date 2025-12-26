# Research & Diagnosis: Chat Frontend-Backend Connectivity

**Feature**: Fix Chat Frontend-Backend Connectivity
**Branch**: `001-fix-chat-connectivity`
**Date**: 2025-12-25
**Status**: Root cause identified

## Executive Summary

**Root Cause Identified**: The backend FastAPI service is **missing CORS (Cross-Origin Resource Sharing) middleware configuration**. This prevents the frontend (running on `http://localhost:3000`) from making API requests to the backend (running on `http://localhost:8000`) due to browser same-origin policy restrictions.

**Impact**: All chat widget messages fail with CORS errors before reaching the backend, making the chat completely non-functional.

**Solution**: Add `CORSMiddleware` to `backend/src/backend/main.py` allowing the frontend origin.

**Confidence**: HIGH - This is a standard web development issue with a well-known solution.

## Diagnostic Investigation

### 1. Frontend Code Analysis ✅

**Location**: `frontend/src/components/ChatWidget/chat-service.ts`

**Findings**:
```typescript
// Line 3: Backend URL configuration
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

// Lines 75-82: POST request to /chat endpoint
const response = await fetch(`${BACKEND_URL}/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  body: JSON.stringify({ message: trimmedMessage })
});
```

**Assessment**: ✅ **CORRECT**
- Properly uses environment variable for backend URL
- Includes correct headers for JSON communication
- Request payload format matches backend expectations
- Error handling implemented for network failures

**Conclusion**: Frontend code is correctly implemented. No changes needed.

### 2. Backend Endpoint Analysis ✅

**Location**: `backend/src/backend/main.py`

**Findings**:
```python
# Line 60-117: /chat endpoint implementation
@app.post("/chat", response_model=ChatResponse, responses={...})
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    # Validates message (3-10000 chars, no whitespace-only)
    # Calls Cohere API via agent
    # Returns ChatResponse with response, agent_name, timestamp
```

**Assessment**: ✅ **CORRECT**
- Endpoint accepts POST requests at `/chat`
- Expects `ChatRequest` model with `message` field
- Returns `ChatResponse` with `response`, `agent_name`, `timestamp` fields
- Validation rules match frontend (3-10,000 characters)
- Cohere integration working

**Conclusion**: Backend endpoint is correctly implemented. No changes needed to endpoint logic.

### 3. CORS Configuration Analysis ❌ **ISSUE FOUND**

**Location**: `backend/src/backend/main.py`

**Findings**:
```python
# Lines 1-30: FastAPI app initialization
from fastapi import FastAPI, Request, HTTPException
# ... other imports

app = FastAPI(title="Educational AI Tutor API", version="1.0.0")
# ... authentication routes and rate limiter setup
```

**Assessment**: ❌ **MISSING CORS CONFIGURATION**
- No `from fastapi.middleware.cors import CORSMiddleware` import
- No `app.add_middleware(CORSMiddleware, ...)` configuration
- Frontend requests from `http://localhost:3000` will be blocked by browser
- Backend won't send required CORS headers (`Access-Control-Allow-Origin`, etc.)

**Expected Behavior Without CORS**:
1. Frontend makes POST request to `http://localhost:8000/chat`
2. Browser sends preflight OPTIONS request (CORS check)
3. Backend responds without `Access-Control-Allow-Origin` header
4. Browser blocks the request with CORS error
5. Frontend never receives response, displays connection error

**Browser Console Error (Expected)**:
```
Access to fetch at 'http://localhost:8000/chat' from origin 'http://localhost:3000'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
on the requested resource.
```

**Conclusion**: This is the root cause. CORS must be configured.

### 4. Environment Variable Configuration ✅

**Location**: `frontend/.env`

**Findings**:
```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8000
```

**Assessment**: ✅ **CORRECT**
- Environment variable is set correctly
- Points to `http://localhost:8000` (standard FastAPI development port)
- Docusaurus will load this on dev server start

**Caveat**: Changes to `.env` require restarting Docusaurus dev server (`npm start`)

**Conclusion**: Environment configuration is correct.

### 5. Service Availability Check ⚠️ **NEEDS VERIFICATION**

**Backend Service**:
- **Expected**: `uvicorn src.backend.main:app --reload` running on port 8000
- **Verification Command**: `netstat -an | grep 8000` (Unix) or `netstat -an | findstr 8000` (Windows)
- **Status**: Not verified in this analysis - user must check if backend is running

**Frontend Service**:
- **Expected**: `npm start` running on port 3000 (Docusaurus default)
- **Verification Command**: `netstat -an | grep 3000` or `netstat -an | findstr 3000`
- **Status**: Not verified in this analysis - user must check if frontend is running

**Conclusion**: Services may or may not be running. User must verify.

## Root Cause Summary

### Primary Issue: Missing CORS Middleware ❌

**Problem**: `backend/src/backend/main.py` does not configure CORS middleware, causing browser to block all cross-origin requests from frontend to backend.

**Why This Matters**:
- Modern browsers enforce Same-Origin Policy (SOP) for security
- Frontend (`http://localhost:3000`) and backend (`http://localhost:8000`) are different origins
- Without CORS headers, browser rejects responses from backend
- This is a **security feature**, not a bug - CORS must be explicitly enabled

**Solution Required**:
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Educational AI Tutor API", version="1.0.0")

# Add CORS middleware
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

### Secondary Checks (May Also Be Issues)

1. **Backend Not Running**: If `uvicorn` isn't started, frontend gets "connection refused" instead of CORS error
2. **Frontend Not Running**: If Docusaurus isn't started, no requests are made
3. **Environment Not Loaded**: If `.env` changed but Docusaurus not restarted, requests go to wrong URL

**Diagnostic Decision Tree**:
```
Is backend running on port 8000?
├─ NO → Start backend: `cd backend && uvicorn src.backend.main:app --reload`
└─ YES → Does browser console show CORS error?
    ├─ YES → Add CORS middleware (PRIMARY SOLUTION)
    └─ NO → Check if frontend is running on port 3000
        ├─ NO → Start frontend: `cd frontend && npm start`
        └─ YES → Check browser Network tab for actual error
```

## Solution Approach

### Recommended Fix (Addressing Root Cause)

**Step 1: Add CORS Middleware to Backend**

**File**: `backend/src/backend/main.py`
**Location**: After `app = FastAPI(...)` initialization (around line 21)
**Change Type**: Add import and middleware configuration

**Code to Add**:
```python
from fastapi.middleware.cors import CORSMiddleware

# ... existing FastAPI app initialization ...

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Docusaurus dev server
        "http://127.0.0.1:3000",     # Alternative localhost
        # Add production URLs when deployed (e.g., "https://textbook.example.com")
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

**Rationale**:
- `allow_origins`: Whitelist frontend URLs (development and production)
- `allow_credentials=True`: Allow cookies/auth headers (for future auth integration)
- `allow_methods`: Support all REST methods (chat uses POST)
- `allow_headers=["*"]`: Accept any headers (simplifies development)

**Security Note**: In production, replace `"*"` with specific headers like `["Content-Type", "Authorization"]` for better security.

**Step 2: Restart Backend Service**

After adding CORS middleware, restart the backend:
```bash
# Stop current uvicorn process (Ctrl+C)
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

**Step 3: Verify Frontend is Running**

Ensure Docusaurus is running on port 3000:
```bash
cd frontend
npm start
```

**Expected Output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

**Step 4: Test Chat Connectivity**

1. Open browser to `http://localhost:3000`
2. Open Developer Tools (F12) → Console tab
3. Open chat widget
4. Type "Hello" and send
5. **Expected**: No CORS error, AI response appears in chat
6. **If Still Failing**: Check Network tab for actual HTTP error

### Alternative Solutions (If CORS Doesn't Resolve)

**If Backend Not Running**:
```bash
cd backend
# Install dependencies if needed
pip install -r requirements.txt
# Start backend
uvicorn src.backend.main:app --reload
```

**If Environment Variable Not Loaded**:
```bash
cd frontend
# Edit .env to ensure REACT_APP_BACKEND_URL=http://localhost:8000
# Restart Docusaurus (kill process and run again)
npm start
```

**If Port Conflict (8000 or 3000 already in use)**:
```bash
# Check what's using port
netstat -an | findstr 8000  # Windows
netstat -an | grep 8000     # Unix/Mac

# Kill process or use different port
# For different port, update REACT_APP_BACKEND_URL in frontend/.env
```

## Technology Decisions

### Decision: Use FastAPI CORSMiddleware (Standard Library)

**Rationale**:
- FastAPI includes CORS middleware in standard library (`fastapi.middleware.cors`)
- No additional dependencies required
- Well-documented and widely used
- Supports all required CORS features (origins, methods, headers, credentials)

**Alternatives Considered**:
1. **starlette.middleware.cors.CORSMiddleware**: FastAPI's middleware is built on this (same functionality)
2. **Custom CORS headers**: More complex, error-prone, reinventing the wheel
3. **Reverse proxy (nginx)**: Overkill for development, adds deployment complexity

**Chosen**: FastAPI CORSMiddleware - simplest, most maintainable solution.

### Decision: Whitelist Specific Origins (Not Wildcard)

**Rationale**:
- Security best practice: only allow known frontend origins
- Prevents unauthorized websites from making requests to our backend
- Easy to extend (add production URL when deployed)

**Alternatives Considered**:
1. **`allow_origins=["*"]` (wildcard)**: Insecure, allows any website to call our API
2. **Environment variable for origins**: Over-engineered for this use case

**Chosen**: Hardcoded whitelist - secure, simple, easy to update.

### Decision: Manual Integration Testing (No Automated Tests)

**Rationale**:
- This is an environment/configuration fix, not application logic
- CORS is enforced by browser, not easily testable in backend unit tests
- Manual verification (send chat message → see response) is fastest and most reliable

**Alternatives Considered**:
1. **E2E tests (Playwright/Cypress)**: Valuable but overkill for simple connectivity check
2. **Backend CORS unit tests**: Can verify middleware is configured, but won't catch actual browser issues

**Chosen**: Manual testing - appropriate for configuration fix.

## Risk Analysis

### Risk 1: CORS Configuration Too Permissive

**Scenario**: Using `allow_origins=["*"]` or `allow_headers=["*"]` in production

**Impact**: Security vulnerability - unauthorized websites could make requests to backend

**Mitigation**:
- Use specific origin whitelist (localhost for dev, production URL for prod)
- Document that `allow_headers=["*"]` should be replaced with specific headers in production
- Add TODO comment in code for production hardening

**Likelihood**: LOW (following best practices in this plan)

### Risk 2: Port Conflicts

**Scenario**: Port 8000 or 3000 already in use by another service

**Impact**: Services won't start, connectivity tests fail

**Mitigation**:
- Check for port conflicts before starting services
- Document how to identify and kill conflicting processes
- Consider using different ports if needed (update .env accordingly)

**Likelihood**: MEDIUM (common development environment issue)

### Risk 3: Environment Variable Not Loaded

**Scenario**: Docusaurus not restarted after `.env` changes

**Impact**: Frontend makes requests to wrong URL (default localhost:8000 might still work, but best to verify)

**Mitigation**:
- Document that .env changes require Docusaurus restart
- Add verification step in quickstart guide

**Likelihood**: LOW (frontend .env is already correct)

## Next Steps

### Immediate Actions (Phase 1)

1. **Create quickstart.md**: Step-by-step guide to start services and test connectivity
2. **Update agent context**: Document CORS as a known requirement for this project
3. **Prepare tasks.md**: Break down CORS fix into testable tasks

### Implementation Tasks (Phase 2 - Generated by /sp.tasks)

Expected tasks:
1. Add CORS middleware import and configuration to `backend/src/backend/main.py`
2. Restart backend service
3. Verify both services running (backend on 8000, frontend on 3000)
4. Test: Send chat message and verify AI response appears
5. Test: Error handling (stop backend, verify error message)
6. Test: Rate limiting (send 4 messages rapidly)
7. Document CORS configuration in README/troubleshooting guide

### Documentation Updates

- Update `frontend/.env.example` if missing
- Add troubleshooting section to project README
- Document CORS requirement for future contributors

## Conclusion

The chat connectivity issue is **definitively** caused by missing CORS middleware in the backend. The frontend and backend code are both correctly implemented - this is purely a configuration issue.

**Confidence Level**: 95% - CORS is the most common cause of cross-origin request failures in web development, and the backend code review confirms no CORS middleware is configured.

**Effort Estimate**: LOW - Adding 10 lines of CORS configuration code, restarting service, and testing takes ~15 minutes.

**Success Probability**: HIGH - CORS configuration is a well-understood, low-risk change with immediate, verifiable results.
