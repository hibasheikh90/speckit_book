---
id: 13
title: chatbot-homepage-redesign-plan
stage: plan
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: chatbot-homepage-redesign
branch: 001-chatbot-homepage-redesign
user: hibas
command: /sp.plan
labels: ["planning", "architecture", "chatbot", "frontend", "ui-design", "contracts"]
links:
  spec: specs/001-chatbot-homepage-redesign/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-chatbot-homepage-redesign/plan.md
  - specs/001-chatbot-homepage-redesign/research.md
  - specs/001-chatbot-homepage-redesign/data-model.md
  - specs/001-chatbot-homepage-redesign/quickstart.md
  - specs/001-chatbot-homepage-redesign/contracts/api-contract.md
  - specs/001-chatbot-homepage-redesign/contracts/component-contract.md
  - CLAUDE.md (updated with TypeScript context)
tests:
  - Constitution check (6 full passes, 1 partial - approved)
  - Spec quality validation (all 14 items passed)
---

## Prompt

/sp.plan

## Response snapshot

Generated comprehensive implementation plan for chatbot homepage integration and UI redesign feature with complete architectural documentation.

**Phase 0: Research** (research.md):
- Analyzed existing frontend stack (Docusaurus 3.9.2, React 19, TypeScript 5.6.2)
- Identified runtime error in ChatWidget.tsx (closeChat undefined reference)
- Researched UI/UX design patterns for modern chat interfaces
- Selected @chatscope/chat-ui-kit-react (already installed) for UI components
- Defined responsive breakpoints (320px, 768px, 1024px)
- Planned mobile-first CSS approach with gradients and animations
- Confirmed backend API contract (no changes required)

**Phase 1: Design & Contracts** (data-model.md, contracts/):
- Defined 5 core data entities (ChatMessage, ChatSession, ChatWidgetState, ChatRequest, ChatResponse)
- Documented validation rules (message length 3-10,000 chars, rate limit 3/30s)
- Created API contract with all request/response formats and error handling
- Mapped 9 React components with props, state, and event contracts
- Defined component hierarchy and data flow
- Specified TypeScript interfaces for all entities

**Technical Context Summary**:
- Language: TypeScript 5.6.2 / JavaScript ES6+
- Stack: Docusaurus 3.9.2 + React 19.0.0
- Storage: localStorage for session persistence
- Testing: TypeScript typecheck + manual console testing
- Performance goals: <2s open, <5s round-trip, 0 errors
- Constraints: No backend changes, zero runtime errors mandatory
- Scope: ~10 files, 500-1000 LOC, 4-6 hours estimated

**Constitution Check Results**:
- ✅ I. Educational-First Design: PASS (enhances learning interface)
- ✅ II. AI-Native Content Creation: PASS (follows SDD with full docs)
- ✅ III. RAG-First Architecture: PASS (elevates chatbot to primary interface)
- ⚠️ IV. Personalization & Accessibility: PARTIAL (basic accessibility met, personalization out of scope)
- ✅ V. Security & Privacy: PASS (no vulnerabilities, env vars used)
- ✅ VI. Performance Standards: PASS (targets met/exceeded)
- ✅ VII. Open Source & Reproducibility: PASS (follows repo patterns)
- **Overall: PASS** - Ready to proceed

**ADR Candidates Identified** (3 decisions):
1. Use @chatscope UI library vs build custom
2. Frontend + backend rate limiting vs backend only
3. localStorage vs sessionStorage for persistence

**Files to Modify** (5 total):
1. ChatWidget.tsx - Fix closeChat() error
2. chat-widget.css - Redesign UI with modern styles
3. index.tsx - Add ChatWidget to homepage
4. .env - Add REACT_APP_BACKEND_URL
5. .env.example - Document environment variables

**Quickstart Guide**: Complete developer setup with step-by-step implementation tasks, testing checklists, accessibility verification, and troubleshooting guide.

## Outcome

- ✅ Impact: Complete implementation plan with research, data model, API contracts, component contracts, and quickstart guide
- 🧪 Tests: Constitution check passed (6/7 full), spec quality validated (all items passed)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, api-contract.md, component-contract.md
- 🔁 Next prompts: Run `/sp.tasks` to generate testable task breakdown; optionally `/sp.adr` for architectural decisions
- 🧠 Reflection: Planning phase uncovered existing runtime error (closeChat reference) that must be fixed. Three architecturally significant decisions documented for potential ADR creation.

## Evaluation notes (flywheel)

- Failure modes observed: None - existing spec was clear and complete
- Graders run and results (PASS/FAIL): Constitution check - PASS (6 full + 1 partial acceptable)
- Prompt variant (if applicable): Standard /sp.plan workflow following template
- Next experiment (smallest change to try): Consider whether constitution check could auto-identify ADR candidates during evaluation to streamline planning phase
