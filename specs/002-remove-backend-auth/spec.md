# Feature Specification: Remove Backend Authentication

**Feature ID**: 002-remove-backend-auth
**Date**: 2025-12-22
**Status**: Planning
**Related PHR**: history/prompts/002-remove-backend-auth/001-remove-backend-authentication-spec.spec.prompt.md

## Overview

Remove all authentication and authorization components from the FastAPI backend, making all endpoints publicly accessible. This is a destructive refactoring that eliminates security barriers while preserving all other functionality.

## Requirements

### Functional Requirements

**FR1: Remove JWT Authentication**
- Delete all JWT token creation, validation, and decoding logic
- Remove `backend/src/auth/utils/jwt.py` module entirely
- Remove JWT-related configuration from settings

**FR2: Remove HTTPBearer Security**
- Remove all `HTTPBearer` instances and `HTTPAuthorizationCredentials` imports
- Delete `backend/src/auth/middleware/jwt.py` containing auth middleware

**FR3: Remove Auth Dependencies from Routes**
- Remove `Depends(get_current_user)` from the `/chat` endpoint
- Remove `Depends(validate_token_only)` from `/auth/verify` endpoint
- Remove all user authentication checks from protected endpoints

**FR4: Remove Auth Routes**
- Delete `/auth/login` endpoint and associated service logic
- Delete `/auth/register` endpoint and associated service logic
- Delete `/auth/verify` endpoint
- Remove auth router registration from main.py

**FR5: Remove Supporting Infrastructure**
- Delete password hashing utilities (`backend/src/auth/utils/password.py`)
- Delete validation utilities (`backend/src/auth/utils/validation.py`)
- Delete user model (`backend/src/auth/models/user.py`)
- Delete auth exceptions (`backend/src/auth/exceptions.py`)
- Delete auth request/response models (`backend/src/auth/models/request.py`, `response.py`)
- Delete auth services (`backend/src/auth/services/`)

**FR6: Remove Rate Limiting Middleware**
- Delete `backend/src/auth/middleware/rate_limiter.py`
- Remove slowapi dependency and rate limiting decorators

**FR7: Preserve Non-Auth Functionality**
- Keep `/health` endpoint unchanged
- Keep `/chat` endpoint logic (remove only auth dependency)
- Keep database configuration (may be needed for other features)
- Keep core application structure and FastAPI setup

### Non-Functional Requirements

**NFR1: Zero Breaking Changes to Public Endpoints**
- `/chat` endpoint must accept the same request/response format (minus auth headers)
- `/health` endpoint remains unchanged

**NFR2: Clean Removal**
- No orphaned imports or unused code
- No commented-out auth code
- Remove auth-related dependencies from requirements.txt/pyproject.toml

**NFR3: Documentation Updates**
- Update API documentation to reflect public endpoints
- Remove auth setup instructions from README if present

## Scope

### In Scope
- Complete removal of authentication and authorization system
- Removal of 14 auth-related Python files (~900 lines)
- Cleanup of auth dependencies and imports
- Making all endpoints publicly accessible

### Out of Scope
- Adding new features or endpoints
- Modifying database schema (keep users table if it exists, just unused)
- Changing non-auth business logic
- Adding alternative security mechanisms
- Modifying frontend or client code

## Technical Context

**Current State**: FastAPI backend with comprehensive JWT-based authentication system including:
- JWT token generation and validation (HS256)
- HTTPBearer security scheme
- User registration and login flows
- Password hashing with bcrypt
- Rate limiting on auth endpoints
- Database-backed user management

**Target State**: FastAPI backend with no authentication requirements:
- All endpoints publicly accessible
- No JWT validation or token requirements
- No user authentication or authorization checks
- Simplified route handlers without auth dependencies

## Acceptance Criteria

1. **AC1**: All auth-related files deleted from `backend/src/auth/` directory
2. **AC2**: `/chat` endpoint accepts requests without Authorization header
3. **AC3**: `/auth/*` routes return 404 (endpoints removed)
4. **AC4**: Backend starts successfully with no auth imports
5. **AC5**: `pytest` runs with no auth-related test failures
6. **AC6**: No references to `get_current_user`, `validate_token_only`, `HTTPBearer` in codebase
7. **AC7**: `requirements.txt` cleaned of auth-only dependencies (PyJWT, bcrypt, slowapi)

## Dependencies

**Files to be Modified/Deleted** (from exploration):
1. `backend/src/auth/utils/jwt.py` - DELETE
2. `backend/src/auth/middleware/jwt.py` - DELETE
3. `backend/src/auth/middleware/rate_limiter.py` - DELETE
4. `backend/src/auth/routes/login.py` - DELETE
5. `backend/src/auth/routes/registration.py` - DELETE
6. `backend/src/auth/routes/verify.py` - DELETE
7. `backend/src/auth/utils/password.py` - DELETE
8. `backend/src/auth/utils/validation.py` - DELETE
9. `backend/src/auth/models/user.py` - DELETE
10. `backend/src/auth/models/request.py` - DELETE
11. `backend/src/auth/models/response.py` - DELETE (if exists)
12. `backend/src/auth/exceptions.py` - DELETE
13. `backend/src/auth/services/` - DELETE (all service files)
14. `backend/src/backend/main.py` - MODIFY (remove auth imports and dependencies)
15. `backend/src/config/settings.py` - MODIFY (remove JWT settings)
16. `backend/requirements.txt` or `backend/pyproject.toml` - MODIFY (remove auth deps)

## Risks & Mitigation

**Risk 1: Breaking existing clients**
- Mitigation: Document API changes; ensure endpoint URLs remain the same

**Risk 2: Orphaned database tables**
- Mitigation: Document that users table remains but is unused; provide migration script if needed

**Risk 3: Incomplete removal leaving security holes**
- Mitigation: Use comprehensive search for auth-related imports; run security scan after removal

**Risk 4: Test failures from removed fixtures**
- Mitigation: Delete auth-related test files; update integration tests to not use auth

## Success Metrics

- ✅ Backend starts without errors
- ✅ All tests pass (after removing auth tests)
- ✅ `/chat` endpoint accessible without auth headers
- ✅ No auth-related imports in codebase
- ✅ Reduced codebase size by ~900 lines
