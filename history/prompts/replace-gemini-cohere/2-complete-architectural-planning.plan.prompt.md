---
id: 2
title: Complete architectural planning for Cohere migration
stage: plan
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: 010-replace-gemini-cohere
branch: 010-replace-gemini-cohere
user: hibas
command: /sp.plan
labels: ["architecture", "cohere", "gemini-migration", "api-integration", "planning"]
links:
  spec: specs/010-replace-gemini-cohere/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/010-replace-gemini-cohere/plan.md
  - specs/010-replace-gemini-cohere/research.md
  - specs/010-replace-gemini-cohere/data-model.md
  - specs/010-replace-gemini-cohere/quickstart.md
  - specs/010-replace-gemini-cohere/contracts/chat-api.yaml
tests:
  - Manual testing procedures documented in quickstart.md
  - API contract validation via OpenAPI spec
  - Integration test scenarios defined in plan.md
---

## Prompt

sp.plan

## Response snapshot

Successfully completed comprehensive architectural planning for replacing Gemini with Cohere API in the FastAPI backend.

**Phase 0 - Research Complete:**
- Researched Cohere Python SDK integration patterns
- Analyzed chat API usage and best practices
- Evaluated native SDK vs OpenAI compatibility layer
- Selected `command-r-plus-08-2024` as default model
- Documented error handling strategies for Cohere-specific exceptions
- Resolved all technical unknowns
- Output: research.md (10 decisions documented with rationale and alternatives)

**Phase 1 - Design Complete:**
- Created data model analysis (data-model.md)
  - Documented unchanged models (ChatRequest, ChatResponse, ErrorResponse)
  - Identified Settings class changes (gemini_* → cohere_*)
  - Detailed AITutor refactoring approach
- Generated OpenAPI contract (contracts/chat-api.yaml)
  - /chat endpoint specification
  - /health endpoint specification
  - All status codes and error responses documented
- Authored quickstart guide (quickstart.md)
  - Step-by-step migration instructions
  - Dependency updates
  - Configuration changes
  - Testing procedures
  - Troubleshooting guide
  - Rollback plan

**Phase 2 - Architecture Plan Complete:**
- Documented 5 major architectural decisions (ADR-001 through ADR-005):
  1. Use native Cohere SDK instead of OpenAI compatibility layer
  2. Select command-r-plus-08-2024 as default model
  3. Use developer role for constitution (system prompt)
  4. Maintain identical API contract (zero breaking changes)
  5. Two-layer timeout strategy (client + asyncio)
- Passed all 7 constitution gates (Educational-First, AI-Native, RAG-First, Personalization, Security, Performance, Open Source)
- Defined project structure and file changes
- Created implementation checklist with 18 items
- Documented risk assessment with mitigations
- Established deployment plan with rollback procedure
- Defined success metrics (functional, performance, quality)

**Key Decisions:**
- Remove openai-agents framework; use native cohere.AsyncClientV2
- Backend-only changes; zero frontend modifications
- Preserve exact API contract for backward compatibility
- 6 files to modify, ~200 lines of code changed
- No database migrations required

**Next Step:** Run `/sp.tasks` to generate testable implementation tasks.

## Outcome

- ✅ Impact: Comprehensive architectural plan created with research, design artifacts, and ADRs. Ready for implementation phase.
- 🧪 Tests: Testing strategy documented in plan.md; quickstart.md provides manual test procedures; contract validation via OpenAPI spec
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml); 0 code files modified (planning phase only)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks; Consider `/sp.adr` to formalize ADRs in history/adr/
- 🧠 Reflection: Planning phase successfully decomposed provider migration into clear phases. Research agent provided valuable Cohere SDK insights. Native SDK approach simplifies architecture vs compatibility layer. Zero frontend impact critical for seamless deployment.

## Evaluation notes (flywheel)

- Failure modes observed: None; all constitution gates passed; research resolved all unknowns
- Graders run and results (PASS/FAIL): Constitution Check: PASS (7/7 gates); API Contract Validation: PASS (backward compatible); Complexity Assessment: PASS (no unjustified violations)
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Execute /sp.tasks to validate plan translates to actionable, testable tasks
