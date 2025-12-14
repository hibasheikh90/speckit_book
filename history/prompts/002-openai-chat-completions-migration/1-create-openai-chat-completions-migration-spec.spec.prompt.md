---
id: 1
title: Create OpenAI Chat Completions Migration Spec
stage: spec
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5
feature: 002-openai-chat-completions-migration
branch: 001-fastapi-chat-endpoint
user: hibas
command: /sp.specify
labels: ["specification", "migration", "openai-chat-completions", "agents-sdk", "gemini"]
links:
  spec: specs/002-openai-chat-completions-migration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-openai-chat-completions-migration/spec.md
tests:
  - null
---

## Prompt

/sp.specify i have already created 001-fastapi-chat-endpoint and wanted to change a minor. Instead of litellm i want to use OpenAIChatCompletionsModel configured with gemini (gemini-2.0-flash). Rest things should be same.

## Response snapshot

Created feature specification for migrating from AsyncOpenAI client to OpenAIChatCompletionsModel while maintaining identical behavior and backward compatibility.

**Specification Summary:**

**Feature**: 002-openai-chat-completions-migration
**Branch**: 002-openai-chat-completions-migration
**Status**: Draft

**User Stories (Prioritized):**
1. **P1 - Transparent Model Migration**: Replace AsyncOpenAI with OpenAIChatCompletionsModel without changing external behavior
2. **P2 - Configuration Compatibility**: Maintain backward compatibility with existing environment configuration
3. **P3 - Dependency Simplification**: Replace openai package with agents-sdk to enable future agent orchestration

**Key Requirements:**
- FR-001: Replace AsyncOpenAI client with OpenAIChatCompletionsModel
- FR-002: Maintain identical request/response behavior
- FR-003: Preserve all error handling (EmptyAIResponse, AIServiceError, timeouts)
- FR-004-006: Keep same environment configuration (GEMINI_API_KEY, etc.)
- FR-008: Pass all existing tests without modification
- FR-009: Replace openai dependency with agents-sdk in pyproject.toml

**Success Criteria:**
- SC-001: 100% test compatibility (all existing tests pass unmodified)
- SC-002: Identical response structure from POST /chat
- SC-003-004: Performance maintained (startup <5s, responses <10s)
- SC-007: agents-sdk replaces openai in dependencies

**Migration Approach:**
- Localized changes to backend/src/backend/agent.py and pyproject.toml
- No frontend, API contract, or infrastructure changes
- Maintain AITutor class interface
- Preserve Global Constitution loading and system prompt injection

**Risks Identified:**
1. OpenAIChatCompletionsModel API differences from AsyncOpenAI
2. Dependency conflicts with agents-sdk
3. System prompt injection pattern differences
4. Error response handling variations

**Out of Scope:**
- Adding new agent orchestration features (Runner, Swarm)
- Changing configuration variable names
- Modifying rate limiting, validation, or endpoint logic
- Frontend or API contract updates

**Acceptance Criteria:** 8 checkpoints defined, including dependency updates, test compatibility, and behavioral equivalence.

**Next Steps:**
1. Run `/sp.plan` to create implementation plan
2. Run `/sp.tasks` to generate TDD task breakdown
3. Execute migration with red-green-refactor cycle

## Outcome

- ✅ Impact: Created comprehensive migration specification for OpenAIChatCompletionsModel adoption, maintaining backward compatibility while enabling future agent SDK features
- 🧪 Tests: Specification emphasizes 100% test compatibility requirement - all existing tests must pass without modification
- 📁 Files: Created specs/002-openai-chat-completions-migration/spec.md
- 🔁 Next prompts: `/sp.plan` to create architectural plan, then `/sp.tasks` for implementation breakdown
- 🧠 Reflection: Successfully captured user's requirement to replace LiteLLM/AsyncOpenAI with OpenAIChatCompletionsModel while keeping behavior identical. Specification prioritizes backward compatibility and test preservation as P1 concerns.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification created successfully with clear user stories, requirements, and acceptance criteria
- Graders run and results (PASS/FAIL): N/A - this is specification stage (no implementation to test yet)
- Prompt variant (if applicable): N/A - standard /sp.specify command
- Next experiment (smallest change to try): Run /sp.plan to validate feasibility of OpenAIChatCompletionsModel with Gemini configuration and confirm agents-sdk API compatibility
