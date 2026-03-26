# Tasks: RAG Tool & Vector Sync (Qdrant)

**Feature**: RAG Tool & Vector Sync (Qdrant)
**Branch**: `005-rag-qdrant-sync`
**Created**: 2025-12-15
**Status**: Draft

## Overview

Implementation of RAG (Retrieval-Augmented Generation) system for the AI Tutor using Qdrant Cloud as the vector database and Gemini API for embeddings. This includes an ingestion pipeline to parse Docusaurus Markdown files, chunk text into 150-token segments, generate embeddings, and upsert to Qdrant. Also includes a `search_textbook` tool for the OpenAI Agent and integration with the FastAPI `/chat` endpoint.

## Implementation Strategy

The implementation will follow a phased approach with user stories as the primary organization unit. We'll start with the highest priority user story (US1) to create an MVP, then add supporting functionality for US2 and US3. Each phase will be independently testable and deliver value to users.

**MVP Scope**: User Story 1 - Students can ask textbook-specific questions and receive answers with textbook citations.

## Dependencies

User stories have the following dependencies:
- US2 (Developer sync) must be completed before US1 (Student questions) can be fully functional, since the vector database needs content to search
- US3 (Agent context retrieval) depends on the search tool implementation from US1

## Parallel Execution Examples

Within each user story phase, tasks can be executed in parallel where they operate on different files/modules:
- Services can be developed in parallel: `qdrant_service.py`, `gemini_service.py`, `ingestion_service.py`
- Tests can be written in parallel with implementation
- Configuration and setup tasks can run while core services are being built

---

## Phase 1: Setup & Configuration

Goal: Establish project infrastructure and dependencies needed for all user stories.

**Independent Test**: Dependencies are installed and configuration files are set up.

- [x] T001 Create backend directory structure per plan
- [x] T002 Add new dependencies to backend/pyproject.toml: qdrant-client, google-generativeai, langchain-text-splitters, tiktoken
- [x] T003 Create backend/.env.example with QDRANT_URL, QDRANT_API_KEY, GEMINI_API_KEY placeholders
- [x] T004 Create backend/src/config/settings.py for Qdrant and Gemini configuration
- [x] T005 Create backend/src/services/__init__.py
- [x] T006 Create backend/src/tools/__init__.py
- [x] T007 Create backend/src/scripts/__init__.py

---

## Phase 2: Foundational Components

Goal: Implement core services needed by multiple user stories (Qdrant connection, Gemini API, text processing).

**Independent Test**: Core services can connect to external APIs and perform basic operations.

- [x] T008 [P] Implement backend/src/services/qdrant_service.py with collection setup and connection
- [x] T009 [P] Implement backend/src/services/gemini_service.py with embedding generation
- [x] T010 [P] Implement backend/src/services/rag_service.py with search functionality
- [ ] T011 [P] Create backend/src/models/textbook_chunk.py for data representation
- [ ] T012 [P] Implement text chunking utility using langchain TokenTextSplitter with 150-token limit

---

## Phase 3: User Story 1 - Student asks textbook-specific questions (Priority: P1)

Goal: Students can ask specific questions about textbook content and receive answers with citations from the textbook.

**Independent Test**: Students can ask specific textbook-related questions and receive answers that cite the actual textbook content, demonstrating the RAG system is working.

**Acceptance Scenarios**:
1. Given a student asks a specific question about textbook content, When they submit the query to the chatbot, Then the chatbot responds with an answer that includes citations from the textbook content.
2. Given a student asks a question about "ROS 2 nodes" from the Physical AI & Humanoid Robotics textbook, When they submit the query, Then the chatbot provides an answer based on the actual textbook content about ROS 2 nodes.

- [ ] T013 [US1] Create backend/src/tools/textbook_search_tool.py with search_textbook function per contract
- [ ] T014 [US1] Implement vector search functionality in qdrant_service.py to return up to 5 results
- [ ] T015 [US1] Update backend/src/api/chat_router.py to register the search_textbook tool with OpenAI Agent
- [ ] T016 [US1] Test integration: student query → search tool → textbook results → agent response
- [ ] T017 [US1] Implement error handling for cases when no relevant content is found

---

## Phase 4: User Story 2 - Developer syncs textbook content to vector database (Priority: P2)

Goal: Developers can run a script to update the vector database with new textbook content.

**Independent Test**: A developer can run the sync script and verify that new textbook content is properly indexed in the vector database.

**Acceptance Scenarios**:
1. Given new textbook content has been added to the repository, When a developer runs the sync script, Then the vector database is updated with embeddings of the new content.

- [ ] T018 [US2] Create backend/src/services/ingestion_service.py for Markdown parsing
- [ ] T019 [US2] Implement Docusaurus Markdown (.md/.mdx) file loader in ingestion_service.py
- [ ] T020 [US2] Create backend/src/scripts/sync_db.py as the main sync script
- [ ] T021 [US2] Implement ingestion pipeline: Markdown → chunk → embed → upsert to Qdrant
- [ ] T022 [US2] Add rate limiting to prevent API quota issues during sync
- [ ] T023 [US2] Test sync script with sample textbook content

---

## Phase 5: User Story 3 - Agent retrieves context before answering (Priority: P3)

Goal: The OpenAI Agent automatically retrieves relevant textbook context before answering student questions.

**Independent Test**: The AI Agent can be observed to retrieve relevant textbook content before formulating responses to student questions.

**Acceptance Scenarios**:
1. Given a student asks a question, When the AI Agent processes the query, Then it retrieves relevant textbook content using the search tool before generating a response.

- [ ] T024 [US3] Enhance agent integration to automatically trigger textbook search when relevant
- [ ] T025 [US3] Implement context injection logic to add retrieved content to agent prompt
- [ ] T026 [US3] Test automatic context retrieval for various textbook-related queries
- [ ] T027 [US3] Verify agent properly cites textbook sources in responses

---

## Phase 6: Validation & Cross-cutting Concerns

Goal: Validate end-to-end functionality and implement performance and error handling requirements.

**Independent Test**: All user stories work together with proper performance and error handling.

- [ ] T028 Test end-to-end RAG flow with sample textbook queries
- [ ] T029 Validate response accuracy and citation quality
- [ ] T030 Performance testing: verify search functionality returns results within 2 seconds for 95% of queries
- [ ] T031 Test concurrent access with rate limiting
- [ ] T032 Handle Qdrant unavailability gracefully
- [ ] T033 Handle very long content that exceeds embedding limits
- [ ] T034 Update pyproject.toml with any additional dependencies discovered during implementation
- [ ] T035 Update documentation with usage instructions