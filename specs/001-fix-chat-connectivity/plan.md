# Implementation Plan: Fix Chat Frontend-Backend Connectivity

**Branch**: `001-fix-chat-connectivity` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fix-chat-connectivity/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix the chatbot frontend connectivity issue where the UI is visible but messages aren't sending/receiving. The chat widget must successfully connect to the existing backend `/chat` POST endpoint (already integrated with Cohere API) to enable students to ask questions and receive AI tutor responses. Investigation reveals the frontend code is correctly implemented - the issue is environmental (backend not running, CORS misconfiguration, or environment variable not loaded).

**Technical Approach**: Diagnose and fix the connectivity issue by ensuring:
1. Backend service is running on the correct port (8000)
2. CORS is configured to allow frontend origin (localhost:3000)
3. Environment variable `REACT_APP_BACKEND_URL` is properly loaded (requires Docusaurus rebuild)
4. Network requests reach the backend successfully

This is a **configuration/environment fix**, not a code rewrite.

## Technical Context

**Language/Version**: TypeScript 5.6.2 (frontend), Python 3.11+ (backend - existing, no changes)
**Primary Dependencies**:
- Frontend: React 19.0.0, Docusaurus 3.9.2, @chatscope/chat-ui-kit-react 2.1.1
- Backend (existing): FastAPI, Cohere SDK via OpenAI-compatible endpoint
**Storage**: localStorage (frontend session persistence), Neon Serverless Postgres (backend - existing)
**Testing**: Manual integration testing (send message → verify response appears)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge) - desktop primary
**Project Type**: Web application (existing frontend + backend architecture)
**Performance Goals**: <5 seconds p95 for send-to-response latency
**Constraints**: Cannot modify backend code or API contract, must work with existing `/chat` endpoint
**Scale/Scope**: Single chat widget component, affects all textbook pages where chat is embedded

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principle III: RAG-First Information Architecture ✅

**Requirement**: "The integrated Retrieval-Augmented Generation (RAG) chatbot is not a bonus feature—it is the primary interface for dynamic learning"

**Compliance**: This fix directly enables the RAG chatbot to function, aligning with the constitution's mandate that the chatbot is the primary learning interface. Without this fix, students cannot access the AI tutor.

**Gate**: PASS - Fix is essential for core educational mission

### Core Principle V: Security & Privacy by Design ✅

**Requirement**: "API keys and secrets MUST use environment variables (`.env`), never hardcoded"

**Compliance**: The fix uses `REACT_APP_BACKEND_URL` environment variable (already following best practice). Backend API key (Cohere) is server-side only, never exposed to frontend.

**Gate**: PASS - No security violations, follows .env pattern

### Core Principle VI: Performance & Scalability Standards ✅

**Requirement**: "Frontend: Docusaurus static site generation ensures <2s initial page load. Backend: FastAPI endpoints respond in <200ms (p95) for RAG queries"

**Compliance**:
- Frontend chat widget already exists and loads quickly
- Backend `/chat` endpoint already exists and meets performance requirements
- This fix only enables connectivity, doesn't impact performance

**Gate**: PASS - No performance degradation

### Core Principle II: AI-Native Content Creation ✅

**Requirement**: "All content creation and maintenance MUST leverage AI tooling (Claude Code, Spec-Kit Plus) following spec-driven development principles"

**Compliance**: This work follows SDD workflow (spec → plan → tasks → implementation) with proper PHR documentation.

**Gate**: PASS - Following SDD process

### Complexity Check ✅

**No new complexity added**: This is a configuration/diagnosis fix for existing code. No new frameworks, libraries, or architectural patterns introduced.

**Gate**: PASS - Minimal complexity, maximum value

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-chat-connectivity/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Diagnosis and root cause analysis
├── quickstart.md        # Phase 1: Steps to verify and test the fix
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
# Existing Web application structure (no changes to structure)
backend/
├── src/
│   ├── backend/
│   │   ├── main.py           # ✅ Existing /chat endpoint (DO NOT MODIFY)
│   │   ├── models.py         # ✅ ChatRequest/ChatResponse models
│   │   ├── agent.py          # ✅ Cohere integration
│   │   └── config.py         # ✅ Settings with COHERE_API_KEY
│   └── requirements.txt
└── tests/

frontend/
├── src/
│   ├── components/
│   │   └── ChatWidget/
│   │       ├── ChatWidget.tsx        # ✅ Chat UI component (existing)
│   │       ├── ChatWindow.tsx        # ✅ Chat conversation UI (existing)
│   │       ├── chat-service.ts       # ✅ Backend API integration (existing)
│   │       ├── models.ts             # ✅ ChatMessage/ChatSession models (existing)
│   │       └── hooks.ts              # ✅ useChatService hook (existing)
│   ├── contexts/
│   │   └── ChatContext.tsx           # ✅ Global chat state (existing)
│   ├── theme/
│   │   └── Root.tsx                  # ✅ Chat widget provider (existing)
│   └── ...
├── .env                               # 🔧 MAY NEED: Verify REACT_APP_BACKEND_URL
├── .env.example                       # 📝 MAY ADD: Document required env vars
├── package.json                       # ✅ Existing dependencies
└── docusaurus.config.js              # ✅ Docusaurus configuration
```

**Structure Decision**: Using existing web application structure (frontend + backend). No structural changes required - this is a connectivity/configuration fix affecting existing files only.

**Files to Modify/Verify**:
- `frontend/.env` - Ensure `REACT_APP_BACKEND_URL=http://localhost:8000` is set
- `frontend/.env.example` - Add documentation for required env vars (if missing)
- `backend/src/backend/main.py` - Verify CORS configuration (read-only check)

**No New Files Created**: This fix uses only existing code.

## Complexity Tracking

**No violations** - Constitution Check passed all gates. No complexity justification needed.

---

## Phase 0: Research & Diagnosis

**Status**: To be generated

**Output**: `research.md` with root cause analysis and solution approach

**Research Questions**:
1. Why aren't messages sending from frontend to backend?
2. Is the backend service running on port 8000?
3. Are CORS headers configured to allow frontend origin (localhost:3000)?
4. Is `REACT_APP_BACKEND_URL` environment variable loaded by Docusaurus?
5. What are the exact HTTP errors (if any) in browser console?

**Deliverable**: research.md documenting:
- Root cause of connectivity failure
- Verification steps to diagnose the issue
- Solution approach (environment config, service startup, or CORS fix)

---

## Phase 1: Design & Contracts

**Status**: To be generated after Phase 0

**Output**: `quickstart.md` with verification and testing steps

**Why No data-model.md**: The data models (ChatRequest, ChatResponse, ChatMessage, ChatSession) already exist and are documented in the spec. No new entities or modifications needed.

**Why No contracts/**: The API contract (`POST /chat` with `{"message": "text"}` → `{"response": "...", "agent_name": "...", "timestamp": "..."}`) already exists in the backend. No contract changes needed.

**Quickstart Content**:
1. **Prerequisites**: Node 20+, Python 3.11+, both services installed
2. **Backend Startup**: `cd backend && uvicorn src.backend.main:app --reload`
3. **Frontend Startup**: `cd frontend && npm start`
4. **Environment Check**: Verify `.env` has `REACT_APP_BACKEND_URL=http://localhost:8000`
5. **Test Procedure**: Open chat widget, send message, verify response
6. **Troubleshooting**: Common issues (CORS errors, connection refused, wrong URL)

**Deliverable**: quickstart.md with step-by-step verification guide

---

## Phase 2: Task Breakdown

**Status**: Will be created by `/sp.tasks` command (NOT part of /sp.plan)

**Expected Tasks**:
1. Diagnose connectivity issue (check backend running, CORS, env vars)
2. Fix identified issue (start backend, configure CORS, or rebuild frontend)
3. Verify message send/receive works end-to-end
4. Test error handling (stop backend, verify error messages)
5. Test rate limiting (send 4 messages rapidly)
6. Document troubleshooting steps

**Note**: Actual tasks will be generated in tasks.md by the `/sp.tasks` command based on this plan.

---

## Implementation Notes

### No Backend Changes

Per spec requirement: "Do not change backend." The backend `/chat` endpoint at `backend/src/backend/main.py` is already correctly implemented and integrated with Cohere. This fix focuses exclusively on:

1. **Environment Configuration**: Ensuring frontend knows where to find backend
2. **Service Availability**: Ensuring backend is running and accessible
3. **CORS Configuration**: Verifying backend allows frontend origin (read-only check)

### Frontend Code Status

The frontend chat implementation in `frontend/src/components/ChatWidget/` is already correct:
- `chat-service.ts`: Properly makes POST requests to `{BACKEND_URL}/chat`
- `ChatWindow.tsx`: Correctly handles send/receive flow with typing indicators
- Error handling, rate limiting, and validation all implemented

**No frontend code changes expected** - the issue is environmental, not logical.

### Diagnosis-First Approach

Phase 0 (research.md) will perform diagnostic steps to identify the exact root cause:
1. Check if backend service is running (`netstat -an | grep 8000` or similar)
2. Check if CORS is configured in `backend/src/backend/main.py` (read-only)
3. Check if `REACT_APP_BACKEND_URL` is in `frontend/.env`
4. Check if Docusaurus has been rebuilt since .env changes
5. Inspect browser console for HTTP errors (network tab)

The solution will be one of:
- **Start backend**: `cd backend && uvicorn src.backend.main:app --reload`
- **Rebuild frontend**: `cd frontend && npm start` (restart dev server)
- **Fix CORS** (read-only diagnosis, will document if this is the issue)

### Testing Strategy

**Manual Integration Test** (no automated tests needed for config fix):
1. Start backend on port 8000
2. Start frontend on port 3000
3. Open browser to localhost:3000
4. Open chat widget
5. Type "Hello" and send
6. Verify AI response appears

**Success Criteria**: SC-001 from spec - "Students can send a message and receive an AI response within 5 seconds under normal network conditions"

### Risk Assessment

**Risk**: LOW - Configuration fix with no code changes

**Rollback**: Simple - stop services, revert .env if changed

**Impact**: HIGH - Enables core RAG chatbot functionality (Constitution Principle III)

