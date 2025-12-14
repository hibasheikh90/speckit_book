---
id: 3
title: Generate Implementation Plan
stage: plan
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5
feature: 001-fastapi-chat-endpoint
branch: 001-fastapi-chat-endpoint
user: system
command: /sp.plan
labels: ["planning", "architecture", "adr", "backend", "fastapi", "gemini-api"]
links:
  spec: specs/001-fastapi-chat-endpoint/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fastapi-chat-endpoint/plan.md
tests:
  - 7 ADRs identified and documented
  - Constitution compliance check performed
---

## Prompt

```text
/sp.plan

Generate a detailed, step-by-step implementation plan and identify all Architecturally Significant Decisions (ADRs) required for **Phase 2: Minimalist FastAPI Backend with OpenAI Agents SDK**.

The implementation must strictly adhere to the following specification and project constraints, and must be executed within the pre-initialized `backend` directory using the `uv` environment.

[Full user specification provided...]
```

## Response snapshot

Created comprehensive implementation plan with 4 major phases and 7 Architectural Decision Records:

**Plan Structure:**
1. **Phase 0: Research & Validation** - Validate Gemini API + OpenAI SDK compatibility, verify constitution file location
2. **Phase 1: Core Architecture & Design** - API contracts, data models (Pydantic), configuration management, module boundaries
3. **Phase 2: Implementation Sequence** - 8 sub-phases covering setup, config, models, rate limiter, agent, exceptions, FastAPI app, README
4. **Phase 3: Testing & Validation** - Unit tests (100% coverage targets), integration tests, acceptance criteria validation, performance testing
5. **Phase 4: Deployment Preparation** - Environment configuration, startup commands, health checks

**Architecture Decision Records (ADRs) Documented:**

1. **ADR-001: Gemini API Integration via OpenAI SDK**
   - Decision: Use OpenAI Python SDK with base_url override to target Gemini's OpenAI-compatible endpoint
   - Rationale: Constitution mandate, compatibility, migration path
   - Alternative: google-generativeai SDK (rejected - violates constitution)

2. **ADR-002: Global Constitution as System Prompt**
   - Decision: Load entire `.specify/memory/constitution.md` as system prompt (~6KB, 1,500 tokens)
   - Rationale: Specification requirement, Gemini's 1M token context window, maximum educational alignment
   - Alternative: Summarized constitution (rejected - premature optimization)

3. **ADR-003: IP-Based Rate Limiting (Pre-Authentication)**
   - Decision: In-memory dict-based rate limiter using client IP from `request.client.host`
   - Rationale: No authentication this phase, simplicity, zero external dependencies
   - Limitations: NAT users share limit, server restart clears state
   - Migration Path: Phase 6 replaces with user ID-based + Redis for distributed

4. **ADR-004: Error Response Structure**
   - Decision: Pydantic default for 422, custom `{"error": "..."}` for 429/500
   - Rationale: Detailed validation errors vs. user-friendly service errors
   - Consequence: Frontend handles two formats

5. **ADR-005: Async FastAPI with 30-Second Timeout**
   - Decision: Native FastAPI async routes + `asyncio.wait_for()` for timeout enforcement
   - Rationale: Meets FR-008 (30s timeout) and SC-005 (10 concurrent requests)
   - Alternative: Sync + threading (rejected - poor concurrency)

6. **ADR-006: Constitution Loading Strategy**
   - Decision: Synchronous load during `AITutor.__init__()`, fail-fast if missing
   - Rationale: Agent cannot function without constitution (FR-003)
   - Consequence: Constitution updates require restart (acceptable for MVP)

7. **ADR-007: Empty Response Detection**
   - Decision: Check for None/empty/whitespace content, raise `EmptyAIResponse` exception
   - Rationale: Clarification Q1 mandates specific error message ("rephrase")
   - Error Message: "Unable to generate a response. Please try rephrasing your question or try again later."

**Technical Stack Finalized:**
- FastAPI 0.115+ (async/await for concurrency)
- Uvicorn (ASGI server)
- Pydantic 2.x (validation: 3-10,000 chars)
- OpenAI SDK 1.x (configured for Gemini API)
- python-dotenv (environment variables)
- pytest + pytest-asyncio + httpx (testing)

**Project Structure:**
- Backend-only (Option 2: Web application structure)
- Flat module structure: main.py, models.py, agent.py, config.py, rate_limiter.py, exceptions.py
- Test coverage targets: 90-100% per module

**Constitution Compliance:**
- ✅ All 7 core principles addressed
- ✅ API keys via `.env` (Principle V: Security)
- ✅ FastAPI mandated by constitution (§ Technical Architecture)
- ✅ OpenAI SDK mandated (§ Backend Dependencies)
- ⏭️ RAG, auth, personalization deferred to future phases (as specified)

**Timeline Estimate:** 11.5 hours (single developer, sequential work)

## Outcome

- ✅ Impact: Complete implementation plan with 7 ADRs, ready for task generation
- 🧪 Tests: Constitution compliance check passed, all success criteria mapped to implementation
- 📁 Files: plan.md (800+ lines, comprehensive architecture documentation)
- 🔁 Next prompts: `/sp.tasks` (generate TDD-style implementation tasks), Create standalone ADR files in `history/adr/`
- 🧠 Reflection: ADR-driven planning approach successfully balanced specification requirements, user's detailed input, and Global Constitution mandates. IP-based rate limiting (ADR-003) is pragmatic compromise for pre-auth MVP with clear migration path. Constitution-as-system-prompt (ADR-002) leverages Gemini's large context window for maximum educational alignment.

## Evaluation notes (flywheel)

- Failure modes observed: None; plan integrates spec, clarifications, user input, and constitution without conflicts
- Graders run and results (PASS/FAIL): Constitution compliance check PASS (7/7 principles addressed or deferred appropriately)
- Prompt variant (if applicable): Combined user's detailed specification with /sp.plan command context
- Next experiment (smallest change to try): Test whether ADR-first planning (write ADRs before detailed implementation steps) improves downstream task clarity vs. ADRs-last approach
