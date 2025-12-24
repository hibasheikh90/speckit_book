# Implementation Plan: Connect Frontend Authentication and Chat to Backend APIs

**Branch**: `001-connect-frontend-backend-apis` | **Date**: 2025-12-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-connect-frontend-backend-apis/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Connect the Docusaurus-based frontend sign-in form and chatbot UI to existing FastAPI backend authentication (`/auth/login`) and chat (`/chat`) endpoints. The implementation will integrate the existing `AuthContext` and `ChatContext` React contexts with backend APIs, enabling authenticated users to sign in and interact with the RAG-powered AI tutor. The chat endpoint no longer requires authentication (auth was removed from backend per spec assumptions), simplifying the integration. All changes are frontend-only—no backend API contracts will be modified.

## Technical Context

**Language/Version**:
- Frontend: TypeScript with React 19.0.0, Node.js >=20.0
- Backend: Python 3.11+ (FastAPI 0.104.1)

**Primary Dependencies**:
- Frontend: Docusaurus 3.9.2, React 19.0.0, @emotion/react 11.14.0, @mui/material 7.3.6, @chatscope/chat-ui-kit-react 2.1.1
- Backend: FastAPI 0.104.1, Pydantic 2.5.0, SQLAlchemy 2.0.23, python-jose 3.3.0, passlib 1.7.4, slowapi 0.1.9

**Storage**:
- PostgreSQL (Neon Serverless Postgres) via SQLAlchemy ORM
- Browser localStorage for auth tokens and chat history (client-side only)

**Testing**:
- Frontend: TypeScript type checking (tsc), manual integration testing
- Backend: pytest (existing tests for auth and chat endpoints)

**Target Platform**:
- Frontend: Modern web browsers (production: >0.5%, not dead, not op_mini all)
- Backend: Linux server with Uvicorn ASGI server

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- Sign-in authentication response: <3 seconds under normal network conditions (SC-001)
- Chat message round-trip: <5 seconds for 90% of requests under normal load (SC-003)
- Error feedback display: <2 seconds when requests fail (SC-004)
- Auth state restoration on load: <1 second for 95% of users (SC-007)

**Constraints**:
- Frontend-only changes (no backend API contract modifications)
- 30-second timeout for all API requests (authentication and chat)
- Rate limiting: 3 chat messages per 30 seconds (enforced client-side and backend)
- Message validation: 3-10,000 characters
- localStorage availability required for token persistence

**Scale/Scope**:
- Target: 100+ simultaneous users (per constitution VI)
- Integration scope: 2 existing React contexts (AuthContext, ChatContext), 2 backend endpoints (/auth/login, /chat)
- UI components: Sign-in form, chatbot widget with message history
- Error scenarios: 6 HTTP status codes (200, 401, 422, 429, 500, 504)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Educational-First Design ✅
**Status**: PASS
**Rationale**: Authentication and chat integration directly serve learning goals by enabling students to access the RAG-powered AI tutor. The chatbot is the primary interface for dynamic learning (Constitution III), and authentication ensures personalized content and preference persistence (Constitution IV). No complexity added that doesn't enhance learning.

### II. AI-Native Content Creation ✅
**Status**: PASS
**Rationale**: This planning document (`plan.md`) follows spec-driven development principles. Spec already created (`spec.md`), this plan documents architectural decisions, and tasks will be broken down in `tasks.md`. PHRs are being captured for AI collaboration transparency.

### III. RAG-First Information Architecture ✅
**Status**: PASS
**Rationale**: This feature directly enables the RAG chatbot functionality by connecting the frontend chat UI to the `/chat` endpoint. Without authentication and chat integration, students cannot access the RAG system. This is a prerequisite feature, not a deviation.

### IV. Personalization & Accessibility ✅
**Status**: PASS
**Rationale**: Authentication is mandatory for personalization features. The login flow enables user preference persistence, onboarding questionnaire data, and personalized content adjustments. This feature doesn't implement all personalization features but provides the foundation.

### V. Security & Privacy by Design ✅
**Status**: PASS
**Rationale**:
- Authentication uses existing Better-Auth implementation with JWT tokens (python-jose)
- Passwords hashed with passlib[bcrypt] (backend already implemented)
- Tokens stored in localStorage with HttpOnly cookies consideration for future enhancement
- No PII exposed in error messages (user-friendly messages only per FR-003)
- Rate limiting implemented client-side and backend (slowapi) to prevent abuse
- Client-side error logging includes no sensitive data (FR-016)
- 30-second timeouts prevent hanging requests

**Note**: localStorage for token storage is acceptable for MVP but should be upgraded to HttpOnly cookies in future for enhanced XSS protection (deferred to future ADR).

### VI. Performance & Scalability Standards ✅
**Status**: PASS
**Rationale**:
- Auth endpoint responds <3s (SC-001), chat <5s (SC-003) - within constitution's <200ms backend target applies to backend processing only
- Frontend uses React contexts for efficient state management (no unnecessary re-renders)
- Chat service implements client-side rate limiting to prevent backend overload
- Message validation prevents oversized payloads (3-10,000 chars)
- localStorage reduces backend calls for auth state restoration
- Target of 100+ simultaneous users achievable with stateless JWT auth

### VII. Open Source & Reproducibility ✅
**Status**: PASS
**Rationale**:
- All dependencies already versioned in package.json and requirements.txt
- Backend URL configurable via REACT_APP_BACKEND_URL environment variable
- No secrets hardcoded (environment variable pattern)
- Frontend-only changes mean no new backend deployment complexity
- Integration testable locally with existing Docker Compose setup

**OVERALL GATE STATUS**: ✅ PASS - No constitutional violations. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                                    # FastAPI backend (existing, no modifications needed)
├── src/
│   ├── backend/
│   │   ├── main.py                        # Main FastAPI app with /chat endpoint (auth already removed)
│   │   ├── models.py                      # ChatRequest, ChatResponse models
│   │   └── agent.py                       # AI agent implementation
│   ├── auth/
│   │   ├── routes/
│   │   │   └── login.py                   # /auth/login endpoint (existing)
│   │   ├── services/
│   │   │   └── login_service.py           # Authentication service
│   │   ├── models/
│   │   │   └── request.py                 # UserLoginRequest, UserLoginResponse
│   │   └── middleware/
│   │       └── rate_limiter.py            # Rate limiting middleware
│   └── config/
│       ├── database.py                    # Database connection
│       └── settings.py                    # App settings
└── tests/                                  # Existing backend tests

frontend/                                   # Docusaurus frontend (modification target)
├── src/
│   ├── components/
│   │   └── ChatWidget/                    # Chat widget components (existing, needs updates)
│   │       ├── ChatWidget.tsx             # Main widget component
│   │       ├── ChatWindow.tsx             # Chat window UI
│   │       ├── chat-service.ts            # Chat API service (already partially implemented)
│   │       ├── models.ts                  # TypeScript models
│   │       └── chat-widget.css            # Styles
│   ├── contexts/                          # React contexts (existing, already functional)
│   │   ├── AuthContext.tsx                # Authentication state management (already implemented!)
│   │   └── ChatContext.tsx                # Chat visibility state
│   ├── pages/                             # Docusaurus pages
│   │   └── auth/
│   │       └── signin.tsx                 # Sign-in form page (NEEDS CREATION or UPDATE)
│   └── theme/                             # Docusaurus theme customizations
└── package.json                            # Dependencies (React 19, Docusaurus 3.9.2)
```

**Structure Decision**: Web application (Option 2) with separate `backend/` and `frontend/` directories. The backend is already complete with functional `/auth/login` and `/chat` endpoints. Frontend has `AuthContext` already implemented with login/register/logout methods and localStorage token persistence. The primary work is:
1. Creating or updating the sign-in UI page to use the existing `AuthContext.login()` method
2. Ensuring `ChatWidget` components properly use `ChatContext` and conditionally render based on `AuthContext.isAuthenticated`
3. Verifying `chat-service.ts` integrates with the `/chat` endpoint correctly (already partially done)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: No violations detected. This section intentionally left empty.
