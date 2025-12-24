# Implementation Plan: Remove Backend Authentication

**Branch**: `002-remove-backend-auth` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-remove-backend-auth/spec.md`

## Summary

Remove all authentication and authorization components from the FastAPI backend to make all endpoints publicly accessible. This involves deleting ~900 lines of auth-specific code across 14 Python files, removing JWT validation, HTTPBearer security, auth middleware, protected route dependencies, and cleaning up auth-related package dependencies while preserving all non-auth functionality.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104.1, Pydantic 2.5.0, SQLAlchemy 2.0.23
**Storage**: Neon Serverless Postgres (preserved but users table unused)
**Testing**: pytest
**Target Platform**: Linux/Windows server (containerized with Docker)
**Project Type**: Web (backend API only)
**Performance Goals**: Maintain <200ms p95 for /chat endpoint
**Constraints**: Zero breaking changes to non-auth endpoint logic
**Scale/Scope**: 14 files to delete/modify, ~900 lines of code removal

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ PASS: Alignment with Core Principles

**Principle II: AI-Native Content Creation**
- ✅ Following SDD workflow: spec → plan → tasks → implementation
- ✅ This plan.md documents architecture decisions
- ✅ PHR-001 already created for specification phase

**Principle V: Security & Privacy by Design**
- ⚠️ **DELIBERATE VIOLATION**: Removing all authentication makes endpoints public
- **Justification**: Explicit user requirement for this feature
- **Recommendation**: Document security implications; ensure this is temporary/test environment

**Principle VI: Performance & Scalability Standards**
- ✅ Removing auth middleware may slightly improve latency
- ✅ Rate limiting removal requires monitoring to prevent abuse

**Principle VII: Open Source & Reproducibility**
- ✅ Changes are reversible via git history
- ✅ Clear documentation of what was removed

### ⚠️ WARNING: Security Implications

Removing authentication exposes the `/chat` endpoint publicly. This plan assumes:
1. This is for a development/testing environment, OR
2. Alternative security measures exist (API gateway, network isolation), OR
3. This is intentionally public for a specific use case

**Recommendation**: Create ADR to document why auth removal is necessary.

## Project Structure

### Documentation (this feature)

```text
specs/002-remove-backend-auth/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (dependency analysis)
├── data-model.md        # Phase 1 output (N/A - no data model changes)
├── contracts/           # Phase 1 output (updated API contracts)
│   └── openapi.yaml     # Updated API spec without auth
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── auth/                    # [DELETE ENTIRE DIRECTORY]
│   │   ├── middleware/
│   │   │   ├── jwt.py          # [DELETE] - get_current_user, validate_token_only
│   │   │   └── rate_limiter.py # [DELETE] - slowapi rate limiting
│   │   ├── routes/
│   │   │   ├── login.py        # [DELETE] - /auth/login endpoint
│   │   │   ├── registration.py # [DELETE] - /auth/register endpoint
│   │   │   └── verify.py       # [DELETE] - /auth/verify endpoint
│   │   ├── services/
│   │   │   ├── login.py        # [DELETE] - LoginService
│   │   │   ├── registration.py # [DELETE] - RegistrationService
│   │   │   └── user.py         # [DELETE] - UserService
│   │   ├── models/
│   │   │   ├── user.py         # [DELETE] - User SQLAlchemy model
│   │   │   ├── request.py      # [DELETE] - Auth request models
│   │   │   └── response.py     # [DELETE] - Auth response models
│   │   ├── utils/
│   │   │   ├── jwt.py          # [DELETE] - JWT creation/validation
│   │   │   ├── password.py     # [DELETE] - Bcrypt hashing
│   │   │   └── validation.py   # [DELETE] - Email/password validation
│   │   └── exceptions.py       # [DELETE] - Auth-specific exceptions
│   ├── backend/
│   │   └── main.py             # [MODIFY] - Remove auth imports and dependencies
│   ├── config/
│   │   ├── settings.py         # [MODIFY] - Remove JWT settings
│   │   └── database.py         # [KEEP] - May be needed for other features
│   ├── models/                 # [KEEP] - Non-auth models
│   ├── services/               # [KEEP] - Non-auth services
│   └── tools/                  # [KEEP] - Utilities
├── tests/
│   ├── auth/                   # [DELETE] - Auth-specific tests
│   └── integration/            # [MODIFY] - Remove auth from integration tests
├── requirements.txt            # [MODIFY] - Remove auth dependencies
├── pyproject.toml              # [CHECK] - May need updating
└── .env.example                # [MODIFY] - Remove JWT_SECRET_KEY, etc.
```

**Structure Decision**: Web application structure with backend-only modifications. The entire `/backend/src/auth/` directory will be deleted (14 files), and `/backend/src/backend/main.py` will be modified to remove auth route inclusions and dependencies.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Removing authentication (Principle V) | User explicitly requested public endpoints | Keeping auth would contradict stated requirements |

## Phase 0: Research & Dependency Analysis

### Research Objectives

1. **Identify all auth import chains**
   - Map every file that imports from `backend.src.auth`
   - Ensure no circular dependencies break during removal

2. **Catalog auth-only vs. shared dependencies**
   - `python-jose` (PyJWT) - auth-only → REMOVE
   - `passlib[bcrypt]` - auth-only → REMOVE
   - `slowapi` - auth-only (if only used for auth endpoints) → REMOVE
   - `sqlalchemy` - shared (database config remains) → KEEP
   - `psycopg2-binary` - shared → KEEP

3. **Test coverage analysis**
   - Identify tests that depend on auth fixtures
   - Determine which tests to delete vs. update

4. **API contract changes**
   - `/chat` endpoint: Remove `Authorization` header requirement
   - `/auth/*` endpoints: Return 404 after removal
   - Update OpenAPI spec to reflect public access

### Research Output

Create `research.md` with:

```markdown
# Research: Auth Removal Dependencies

## Import Chain Analysis
- **Direct importers**: main.py, integration tests
- **Transitive dependencies**: None (auth is leaf module)
- **Safe to delete**: Entire /auth directory with no side effects

## Dependency Classification
| Package | Auth-Only? | Action | Justification |
|---------|-----------|--------|---------------|
| python-jose[cryptography] | ✅ | REMOVE | JWT operations only |
| passlib[bcrypt] | ✅ | REMOVE | Password hashing only |
| slowapi | ✅ | REMOVE | Rate limiting only on auth routes |
| sqlalchemy | ❌ | KEEP | Database ORM (may be used elsewhere) |
| psycopg2-binary | ❌ | KEEP | Postgres driver (database remains) |
| pydantic | ❌ | KEEP | Validation for ChatRequest/ChatResponse |
| fastapi | ❌ | KEEP | Core framework |

## Test Impact
- Delete: `tests/auth/` directory (all auth unit tests)
- Modify: `tests/integration/test_chat.py` (remove auth headers from requests)
- Keep: `tests/integration/test_health.py` (no changes needed)

## API Contract Changes
### Before (with auth):
```http
POST /chat HTTP/1.1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{"message": "Explain ROS 2 nodes"}
```

### After (public):
```http
POST /chat HTTP/1.1
Content-Type: application/json

{"message": "Explain ROS 2 nodes"}
```

### Removed Endpoints:
- `POST /auth/register` → 404
- `POST /auth/login` → 404
- `POST /auth/verify` → 404

## Configuration Changes
- Remove from `.env`: `JWT_SECRET_KEY`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
- Remove from `settings.py`: `jwt_secret_key`, `jwt_access_token_expire_minutes`, `validate_auth_settings()`
```

## Phase 1: Design & Contracts

### Data Model Changes

**NO DATA MODEL CHANGES REQUIRED**

This feature removes code but does not modify database schema. The `users` table will remain in the database but will be unused. This preserves reversibility (auth can be re-added without data loss).

**Rationale**:
- Deleting tables is destructive and risky
- Orphaned tables are harmless
- Easier to rollback if auth removal was a mistake

### API Contracts

Generate updated OpenAPI specification in `/contracts/openapi.yaml`:

```yaml
openapi: 3.0.0
info:
  title: Educational AI Tutor API (Public - No Auth)
  version: 2.0.0
  description: Publicly accessible API for Physical AI textbook chatbot

servers:
  - url: http://localhost:8000
    description: Local development server

paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: healthy
                  constitution_loaded:
                    type: boolean
                  model:
                    type: string
                  rate_limit:
                    type: string

  /chat:
    post:
      summary: Chat with AI tutor (PUBLIC - No authentication required)
      description: Send a question about Physical AI and receive educational response
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Student's question
                  example: "What is ROS 2?"
              required:
                - message
      responses:
        '200':
          description: Successful response from AI tutor
          content:
            application/json:
              schema:
                type: object
                properties:
                  response:
                    type: string
                    description: AI tutor's answer
                  agent_name:
                    type: string
                    description: Name of the AI agent
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
        '429':
          description: Rate limit exceeded (if rate limiting is preserved)
        '500':
          description: Internal server error
        '504':
          description: Request timeout

components:
  schemas:
    ChatRequest:
      type: object
      required:
        - message
      properties:
        message:
          type: string
          minLength: 1
          maxLength: 5000

    ChatResponse:
      type: object
      properties:
        response:
          type: string
        agent_name:
          type: string

    ErrorResponse:
      type: object
      properties:
        detail:
          type: string

  # REMOVED: securitySchemes.bearerAuth (no longer applicable)
  # REMOVED: All /auth/* endpoints
```

### Quickstart Guide

Create `quickstart.md`:

```markdown
# Quickstart: Backend After Auth Removal

## Prerequisites
- Python 3.11+
- Postgres database (optional - can run without it)

## Installation

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env - no auth settings needed
   ```

3. **Run the server**:
   ```bash
   python -m src.backend.main
   ```

   Server starts at `http://localhost:8000`

## Testing the API

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "constitution_loaded": true,
  "model": "gemini-1.5-flash",
  "rate_limit": "10/minute"
}
```

### Chat Endpoint (NO AUTH REQUIRED)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?"}'
```

Expected response:
```json
{
  "response": "ROS 2 (Robot Operating System 2) is...",
  "agent_name": "AI Tutor"
}
```

## What Changed?

✅ **Removed**:
- All `/auth/*` endpoints (login, register, verify)
- JWT token validation
- `Authorization` header requirement
- Auth middleware and dependencies

✅ **Preserved**:
- `/health` endpoint
- `/chat` endpoint logic (now public)
- Database configuration
- Error handling and rate limiting

## Security Note

⚠️ **All endpoints are now public**. Deploy this version only in:
- Local development environments
- Trusted networks with external security (API gateway, VPN)
- Intentionally public use cases

For production, consider:
- Re-adding authentication, OR
- Using API gateway with rate limiting, OR
- Network-level access controls
```

### Agent Context Update

Since the constitution specifies using PowerShell scripts, let me check if that script exists:

```bash
# Would run: .specify/scripts/powershell/update-agent-context.ps1 -AgentType claude
# Not executing now as this is planning phase
```

**Note**: This step will be executed during implementation (/sp.tasks), not during planning.

## Phase 2: Implementation Order

### Execution Sequence (for /sp.tasks)

The following order ensures safe, testable removal:

1. **STEP 1: Create feature branch**
   - `git checkout -b 002-remove-backend-auth`
   - Ensures work is isolated

2. **STEP 2: Update main.py (remove auth route imports)**
   - Remove lines 15-17, 26-28 from `backend/src/backend/main.py`
   - Remove `current_user: User = Depends(get_current_user)` from `/chat` endpoint
   - Remove unused `User` and `get_current_user` imports
   - **Verification**: `python -m pytest backend/tests/integration/test_health.py` passes

3. **STEP 3: Delete auth route files**
   - Delete `backend/src/auth/routes/login.py`
   - Delete `backend/src/auth/routes/registration.py`
   - Delete `backend/src/auth/routes/verify.py`
   - **Verification**: Backend still imports successfully (no broken imports)

4. **STEP 4: Delete auth middleware**
   - Delete `backend/src/auth/middleware/jwt.py`
   - Delete `backend/src/auth/middleware/rate_limiter.py`
   - **Verification**: `python -c "from backend.src.backend.main import app"` succeeds

5. **STEP 5: Delete auth services**
   - Delete entire `backend/src/auth/services/` directory
   - **Verification**: No import errors

6. **STEP 6: Delete auth models**
   - Delete `backend/src/auth/models/user.py`
   - Delete `backend/src/auth/models/request.py`
   - Delete `backend/src/auth/models/response.py`
   - **Verification**: No import errors

7. **STEP 7: Delete auth utilities**
   - Delete `backend/src/auth/utils/jwt.py`
   - Delete `backend/src/auth/utils/password.py`
   - Delete `backend/src/auth/utils/validation.py`
   - **Verification**: No import errors

8. **STEP 8: Delete auth exceptions**
   - Delete `backend/src/auth/exceptions.py`
   - **Verification**: `python -m pytest` (all remaining tests pass)

9. **STEP 9: Remove auth directory**
   - Delete entire `backend/src/auth/` directory
   - **Verification**: `ls backend/src/` shows no `auth/` directory

10. **STEP 10: Clean up settings.py**
    - Remove JWT-related settings from `backend/src/config/settings.py`
    - Remove `validate_auth_settings()` function
    - **Verification**: `python -c "from backend.src.config.settings import settings"` succeeds

11. **STEP 11: Update requirements.txt**
    - Remove `python-jose[cryptography]==3.3.0`
    - Remove `passlib[bcrypt]==1.7.4`
    - Remove `slowapi==0.1.9`
    - **Verification**: `pip install -r backend/requirements.txt` succeeds in clean venv

12. **STEP 12: Update .env.example**
    - Remove `JWT_SECRET_KEY`
    - Remove `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
    - **Verification**: File is valid

13. **STEP 13: Delete auth tests**
    - Delete `backend/tests/auth/` directory (if exists)
    - **Verification**: `python -m pytest backend/tests/` passes

14. **STEP 14: Update integration tests**
    - Remove `Authorization` headers from chat endpoint tests
    - Update test fixtures to not require auth
    - **Verification**: `python -m pytest backend/tests/integration/` passes

15. **STEP 15: Full system test**
    - Start backend: `python -m backend.src.backend.main`
    - Test health: `curl http://localhost:8000/health`
    - Test chat: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "test"}'`
    - Verify 404 on /auth routes: `curl http://localhost:8000/auth/login`
    - **Verification**: All endpoints respond correctly, no auth required

16. **STEP 16: Update documentation**
    - Update README.md to remove auth setup instructions
    - Add note about public endpoints
    - **Verification**: Documentation is accurate

17. **STEP 17: Generate updated OpenAPI spec**
    - Visit `http://localhost:8000/docs`
    - Export updated OpenAPI spec to `specs/002-remove-backend-auth/contracts/openapi.yaml`
    - **Verification**: Spec shows no auth endpoints

18. **STEP 18: Final validation**
    - Run full test suite: `python -m pytest backend/`
    - Check for orphaned imports: `grep -r "from auth" backend/src/`
    - Check for auth references: `grep -r "get_current_user\|HTTPBearer\|JWT" backend/src/`
    - **Verification**: All searches return empty, all tests pass

## Rollback Plan

If auth removal causes issues:

1. **Immediate rollback**: `git checkout main && git branch -D 002-remove-backend-auth`
2. **Partial rollback**: Cherry-pick specific commits to restore needed auth components
3. **Data preservation**: Users table remains intact, so user data is not lost

## Risks & Mitigation

### Risk 1: Breaking existing clients
**Likelihood**: High
**Impact**: High
**Mitigation**:
- Coordinate with frontend team before deployment
- Document API changes in release notes
- Consider maintaining a deprecated auth endpoint that returns 410 Gone with migration instructions

### Risk 2: Orphaned code calling auth functions
**Likelihood**: Medium
**Impact**: Medium
**Mitigation**:
- Search entire codebase for auth imports before deletion
- Run full test suite before declaring complete
- Use grep/ripgrep to find residual references

### Risk 3: Test failures from removed fixtures
**Likelihood**: High
**Impact**: Low
**Mitigation**:
- Delete auth test directory entirely
- Update integration tests to use new public access pattern
- Mock users in tests if needed for business logic

### Risk 4: Configuration errors
**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- Test settings import after removing JWT config
- Provide updated .env.example
- Document required environment variables in README

## Success Criteria

- ✅ All auth files deleted (14 files, ~900 lines)
- ✅ `/chat` endpoint accessible without auth
- ✅ `/auth/*` routes return 404
- ✅ Backend starts without errors
- ✅ All tests pass
- ✅ No auth-related imports in codebase
- ✅ Dependencies cleaned from requirements.txt
- ✅ OpenAPI spec updated
- ✅ Documentation reflects changes

## Next Steps

1. **Review this plan** with stakeholders
2. **Create ADR** documenting decision to remove auth (see constitution requirement)
3. **Run `/sp.tasks`** to generate detailed task breakdown
4. **Execute tasks** following TDD red-green-refactor cycle
5. **Create PR** with comprehensive testing evidence

---

**Plan Status**: ✅ Ready for /sp.tasks
**Estimated Effort**: 18 tasks, ~2-3 hours of implementation
**Risk Level**: Medium (reversible via git, but requires coordination with clients)
