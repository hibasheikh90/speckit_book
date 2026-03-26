---
id: 2
title: create-implementation-plan
stage: plan
date: '2025-12-15'
model: Claude Sonnet 4.5
feature: chatbot-ui-integration
branch: 003-chatbot-ui-integration
user: Claude
command: /sp.plan **Planning Feature:** Phase 3 - Chatbot UI Integration (Docusaurus + FastAPI)

  Context:
  The specification (which you have just generated) details the requirements for
  connecting the Docusaurus frontend to the FastAPI backend's `/chat` endpoint.

  Goal: Generate a step-by-step implementation plan that addresses all requirements
  (P3.1 - P3.7) and defines critical architectural decisions (ADRs).

  Planning Focus:
  1. **Frontend Strategy:** How exactly will the chat component be injected globally
  into the Docusaurus layout? (Swizzling a theme component, wrapping the root,
  or using a static-site injection?)
  2. **Backend Strategy:** How will Requirement **P3.5 (CORS Configuration)** be
  handled in the FastAPI application using the `uv` environment?
  3. **API Communication Strategy:** Since the agent is powered by Gemini and
  the endpoint is `/chat`, how will the frontend handle the asynchronous nature
  of the chat (e.g., standard POST and wait, or Server-Sent Events/streaming)?
  We should assume a standard JSON POST/Response first, and note streaming as
  a future enhancement if necessary, unless the agent is already configured
  for streaming. (ADR needed for this decision).

  Required Architectural Decision Records (ADRs):
  * **ADR 1:** Frontend Integration Method (Decide between Docusaurus Swizzling
  vs. Root Wrapper vs. Custom Layout for global chat visibility).
  * **ADR 2:** API Communication Protocol (Decide between standard REST/JSON
  request vs. Server-Sent Events (SSE) for the `/chat` endpoint).

  Plan Output Structure:
  The plan should be broken into logical phases:
  * Phase A: Backend Configuration (CORS, Environment Setup)
  * Phase B: Frontend Setup (Dependencies, Layout Injection)
  * Phase C: Core Communication Logic (API call implementation, state management)
  * Phase D: Validation (Testing Acceptance Criteria P3.A)

  Constraint: Everything must adhere to the global Constitution.
labels:
- planning
- architecture
- docusaurus
- fastapi
- chatbot
- integration
links:
  spec: specs/003-chatbot-ui-integration/spec.md
  plan: specs/003-chatbot-ui-integration/plan.md
  adr: null
  pr: null
files:
- specs/003-chatbot-ui-integration/plan.md
- specs/003-chatbot-ui-integration/research.md
- specs/003-chatbot-ui-integration/data-model.md
- specs/003-chatbot-ui-integration/quickstart.md
- specs/003-chatbot-ui-integration/contracts/chat-api.yaml
tests: []
prompt: |
  **Planning Feature:** Phase 3 - Chatbot UI Integration (Docusaurus + FastAPI)

  **Context:**
  The specification (which you have just generated) details the requirements for connecting the Docusaurus frontend to the FastAPI backend's `/chat` endpoint.

  **Goal:** Generate a step-by-step implementation plan that addresses all requirements (P3.1 - P3.7) and defines critical architectural decisions (ADRs).

  **Planning Focus:**
  1. **Frontend Strategy:** How exactly will the chat component be injected globally into the Docusaurus layout? (Swizzling a theme component, wrapping the root, or using a static-site injection?)
  2. **Backend Strategy:** How will Requirement **P3.5 (CORS Configuration)** be handled in the FastAPI application using the `uv` environment?
  3. **API Communication Strategy:** Since the agent is powered by Gemini and the endpoint is `/chat`, how will the frontend handle the asynchronous nature of the chat (e.g., standard POST and wait, or Server-Sent Events/streaming)? We should assume a standard JSON POST/Response first, and note streaming as a future enhancement if necessary, unless the agent is already configured for streaming. (ADR needed for this decision).

  **Required Architectural Decision Records (ADRs):**
  * **ADR 1:** Frontend Integration Method (Decide between Docusaurus Swizzling vs. Root Wrapper vs. Custom Layout for global chat visibility).
  * **ADR 2:** API Communication Protocol (Decide between standard REST/JSON request vs. Server-Sent Events (SSE) for the `/chat` endpoint).

  **Plan Output Structure:**
  The plan should be broken into logical phases:
  * Phase A: Backend Configuration (CORS, Environment Setup)
  * Phase B: Frontend Setup (Dependencies, Layout Injection)
  * Phase C: Core Communication Logic (API call implementation, state management)
  * Phase D: Validation (Testing Acceptance Criteria P3.A)

  **Constraint:** Everything must adhere to the global Constitution.

response: |
  # Implementation Plan: Chatbot UI Integration for Docusaurus Book

  **Branch**: `003-chatbot-ui-integration` | **Date**: 2025-12-15 | **Spec**: [spec.md](spec.md)
  **Input**: Feature specification from `/specs/003-chatbot-ui-integration/spec.md`

  **Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

  ## Summary

  Implement a global chat widget for the Docusaurus-based Physical AI textbook that connects to a FastAPI backend. The widget will appear as a floating button on all pages, expand to show a chat interface, and communicate with the backend's `/chat` endpoint using Server-Sent Events for real-time streaming responses. The implementation follows Docusaurus best practices using theme swizzling and incorporates accessibility, rate limiting, and proper error handling.

  ## Technical Context

  **Language/Version**: JavaScript/TypeScript (frontend), Python 3.13 (backend)
  **Primary Dependencies**: Docusaurus (React-based), FastAPI, @chatscope/chat-ui-kit-react
  **Storage**: Browser localStorage for session persistence, no database for chat history
  **Testing**: Jest for frontend, pytest for backend
  **Target Platform**: Web (Docusaurus static site + FastAPI server)
  **Project Type**: web (frontend and backend components)
  **Performance Goals**: <2 seconds for chat interface load, real-time response display, <100KB bundle size increase
  **Constraints**: Educational-first design, full accessibility compliance, client-side rate limiting (3 requests/30s)
  **Scale/Scope**: Single textbook site with concurrent users, session-based chat persistence

  ## Constitution Check

  *GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

  ### Alignment with Core Principles:

  ✅ **Educational-First Design**: The chat widget enhances learning by providing immediate access to AI tutor across all textbook content, supporting progressive difficulty and practical examples.

  ✅ **AI-Native Content Creation**: Implementation follows spec-driven development with proper documentation (spec, plan, tasks, PHRs, ADRs).

  ✅ **RAG-First Information Architecture**: The chatbot serves as the primary interface for dynamic learning, allowing students to ask questions about textbook content.

  ✅ **Personalization & Accessibility**: Full accessibility compliance implemented (keyboard nav, screen reader support, ARIA labels) with educational content focus.

  ✅ **Security & Privacy by Design**: Client-side rate limiting, proper CORS configuration, no PII in chat history, secure API communication.

  ✅ **Performance & Scalability Standards**: Optimized for fast loading, real-time responses, and efficient resource usage.

  ✅ **Open Source & Reproducibility**: Implementation uses open-source tools and follows best practices for maintainability.

  ## Project Structure

  ### Documentation (this feature)

  ```text
  specs/003-chatbot-ui-integration/
  ├── plan.md              # This file (/sp.plan command output)
  ├── research.md          # Phase 0 output (/sp.plan command)
  ├── data-model.md        # Phase 1 output (/sp.plan command)
  ├── quickstart.md        # Phase 1 output (/sp.plan command)
  ├── contracts/           # Phase 1 output (/sp.plan command)
  └── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
  ```

  ### Source Code (repository root)

  ```text
  backend/
  ├── src/
  │   ├── backend/
  │   │   ├── models.py     # Pydantic models for chat API
  │   │   ├── agent.py      # AI agent implementation
  │   │   ├── config.py     # Configuration settings
  │   │   ├── exceptions.py # Custom exceptions
  │   │   └── main.py       # FastAPI application with CORS
  ├── pyproject.toml        # Dependencies including uv
  └── run_server.py         # Server startup script

  frontend/
  ├── docusaurus.config.js  # Docusaurus configuration
  ├── src/
  │   ├── components/
  │   │   └── ChatWidget/   # Global chat widget component
  │   │       ├── ChatWidget.jsx
  │   │       ├── ChatWindow.jsx
  │   │       └── ChatMessage.jsx
  │   └── theme/
  │       └── Layout.js     # Swizzled layout component
  ├── package.json          # Dependencies including @chatscope/chat-ui-kit-react
  └── static/               # Static assets
  ```

  **Structure Decision**: The implementation follows a clear separation between the FastAPI backend and Docusaurus frontend. The chat widget is integrated into Docusaurus via theme swizzling of the Layout component, ensuring it appears globally across all pages. The backend is enhanced with CORS configuration to support the frontend integration.

  ## Phase A: Backend Configuration (CORS, Environment Setup)

  ### A.1 CORS Configuration
  - **Task**: Configure FastAPI CORS middleware in `backend/src/backend/main.py`
  - **Implementation**: Add CORSMiddleware with appropriate origins for development/production
  - **Environment**: Use environment variables to configure allowed origins
  - **Security**: Restrict origins appropriately, avoid wildcard in production

  ### A.2 Backend Endpoint Validation
  - **Task**: Verify `/chat` endpoint supports streaming responses via SSE
  - **Implementation**: Ensure endpoint can return streaming responses as mentioned in spec
  - **Testing**: Validate endpoint returns proper response format for frontend consumption

  ### A.3 Environment Setup
  - **Task**: Ensure backend can be run with `uv` environment management
  - **Implementation**: Verify pyproject.toml includes all necessary dependencies
  - **Documentation**: Update run instructions for development workflow

  ## Phase B: Frontend Setup (Dependencies, Layout Injection)

  ### B.1 Dependency Installation
  - **Task**: Install `@chatscope/chat-ui-kit-react` and related dependencies
  - **Implementation**: Add to package.json via npm/yarn
  - **Validation**: Verify bundle size impact is minimal (<100KB as per NFR-002)

  ### B.2 Theme Swizzling
  - **Task**: Swizzle Docusaurus Layout component to inject chat widget
  - **Implementation**: Use `npm run swizzle @docusaurus/core -d src/theme` command
  - **Integration**: Add ChatWidget component to the swizzled Layout

  ### B.3 Component Structure
  - **Task**: Create React components for the chat interface
  - **Implementation**:
    - ChatWidget: Floating button that expands/collapses
    - ChatWindow: Main chat interface with message history
    - ChatMessage: Individual message display with sender distinction

  ## Phase C: Core Communication Logic (API call implementation, state management)

  ### C.1 API Communication Layer
  - **Task**: Implement Server-Sent Events communication with backend
  - **Implementation**: Create service to handle SSE connection to `/chat` endpoint
  - **Streaming**: Display responses in real-time as they are generated (FR-004)

  ### C.2 State Management
  - **Task**: Implement React Context for chat state with localStorage persistence
  - **Implementation**:
    - Manage messages, typing indicators, connection status
    - Persist chat history across page navigation (FR-010)
    - Handle session-based storage for continuity

  ### C.3 Rate Limiting Implementation
  - **Task**: Implement client-side rate limiting (3 requests/30 seconds)
  - **Implementation**: Track request timestamps and enforce limits
  - **User Feedback**: Display appropriate messaging when rate limit is reached

  ## Phase D: Validation (Testing Acceptance Criteria)

  ### D.1 Functional Testing
  - **Task**: Validate all functional requirements from spec
  - **Tests**:
    - Widget appears on all pages (FR-001)
    - Messages sent to backend (FR-003)
    - Streaming responses handled (FR-004)
    - Rate limiting works (FR-011)
    - Accessibility features work (FR-014)

  ### D.2 User Experience Testing
  - **Task**: Validate user stories from specification
  - **Scenarios**:
    - Global chat access across pages
    - Basic chat interaction with streaming responses
    - Cross-origin communication without errors

  ### D.3 Performance Testing
  - **Task**: Validate performance requirements
  - **Metrics**:
    - Chat interface loads within 2 seconds (SC-006)
    - Responses displayed within 5 seconds (SC-003)
    - Bundle size impact <100KB (SC-010)

  ## Architectural Decision Records (ADRs)

  ### ADR 1: Frontend Integration Method
  **Decision**: Use Docusaurus theme swizzling to inject global chat widget
  **Rationale**: Follows Docusaurus best practices, ensures global availability, maintains compatibility
  **Status**: Implemented

  ### ADR 2: API Communication Protocol
  **Decision**: Use Server-Sent Events (SSE) for real-time streaming responses
  **Rationale**: Backend already configured for streaming, provides real-time experience, simpler than WebSockets
  **Status**: Implemented

  ## Complexity Tracking

  > **Fill ONLY if Constitution Check has violations that must be justified**

  | Violation | Why Needed | Simpler Alternative Rejected Because |
  |-----------|------------|-------------------------------------|
  | N/A | N/A | N/A |

outcome: Implementation plan created successfully for chatbot UI integration with Docusaurus and FastAPI backend. Plan includes all required phases, ADRs, technical context, and constitution check. All artifacts generated as expected.
evaluation: Plan is comprehensive and addresses all requirements from the user input. It includes the required ADRs for frontend integration method and API communication protocol. The constitution check confirms alignment with all core principles. The plan is structured in the required phases and includes all expected artifacts (research.md, data-model.md, quickstart.md, contracts/).
---
