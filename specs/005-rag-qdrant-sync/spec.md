# Feature Specification: RAG Tool & Vector Sync (Qdrant)

**Feature Branch**: `005-rag-qdrant-sync`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "Phase 5 - RAG Tool & Vector Sync (Qdrant) - Implement the \"Long-term Memory\" and \"Knowledge Retrieval\" capabilities for the AI Tutor. This phase involves setting up Qdrant Cloud as the vector database, creating an ingestion pipeline to sync the \"Physical AI & Humanoid Robotics\" textbook content, and building a specific Tool that the OpenAI Agent can use to retrieve context before answering student questions."

## Clarifications

### Session 2025-12-15

- Q: Which Qdrant deployment option should be used for production? → A: Use Qdrant Cloud Free Tier for production deployment

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Student asks textbook-specific questions (Priority: P1)

As a student, I want the chatbot to answer specific questions about "ROS 2 nodes" or "Gazebo simulation" by citing the actual textbook content, not just general internet knowledge.

**Why this priority**: This is the core value proposition of the feature - providing accurate, textbook-based answers to students' specific questions.

**Independent Test**: Students can ask specific textbook-related questions and receive answers that cite the actual textbook content, demonstrating the RAG system is working.

**Acceptance Scenarios**:

1. **Given** a student asks a specific question about textbook content, **When** they submit the query to the chatbot, **Then** the chatbot responds with an answer that includes citations from the textbook content.

2. **Given** a student asks a question about "ROS 2 nodes" from the Physical AI & Humanoid Robotics textbook, **When** they submit the query, **Then** the chatbot provides an answer based on the actual textbook content about ROS 2 nodes.

---

### User Story 2 - Developer syncs textbook content to vector database (Priority: P2)

As a developer, I want a script I can run (`uv run sync_db`) to update the vector database whenever I add new textbook content.

**Why this priority**: This enables maintainability and keeps the knowledge base up-to-date with new content.

**Independent Test**: A developer can run the sync script and verify that new textbook content is properly indexed in the vector database.

**Acceptance Scenarios**:

1. **Given** new textbook content has been added to the repository, **When** a developer runs the sync script, **Then** the vector database is updated with embeddings of the new content.

---

### User Story 3 - Agent retrieves context before answering (Priority: P3)

As a developer, I want the OpenAI Agent to automatically retrieve relevant textbook context before answering student questions.

**Why this priority**: This ensures the AI Tutor leverages the knowledge base without requiring manual intervention.

**Independent Test**: The AI Agent can be observed to retrieve relevant textbook content before formulating responses to student questions.

**Acceptance Scenarios**:

1. **Given** a student asks a question, **When** the AI Agent processes the query, **Then** it retrieves relevant textbook content using the search tool before generating a response.

---

### Edge Cases

- What happens when the Qdrant vector database is temporarily unavailable?
- How does the system handle very long textbook content that exceeds embedding limits?
- What if no relevant textbook content is found for a student's question?
- How does the system handle concurrent requests to the vector database?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST connect to Qdrant Cloud using the qdrant-client library
- **FR-002**: System MUST parse Docusaurus Markdown (.md/.mdx) files from the textbook content
- **FR-003**: System MUST chunk the textbook text content into 150-token segments for embedding
- **FR-004**: System MUST generate embeddings using the Gemini API for all textbook content
- **FR-005**: System MUST upsert the embeddings and content to Qdrant vector database
- **FR-006**: System MUST provide a `search_textbook` function that the OpenAI Agent can invoke to query Qdrant
- **FR-007**: System MUST register the `search_textbook` tool with the OpenAI Agent in the FastAPI `/chat` endpoint
- **FR-008**: System MUST return up to 5 relevant textbook content results when students ask questions related to the textbook
- **FR-010**: System MUST handle API failures gracefully with appropriate error handling
- **FR-011**: System MUST provide a script (e.g., `uv run sync_db`) to sync textbook content to the vector database
- **FR-012**: System MUST support concurrent access with rate limiting to ensure stability under load

### Key Entities *(include if feature involves data)*

- **Textbook Content**: Represents the "Physical AI & Humanoid Robotics" textbook content in Docusaurus Markdown format
- **Vector Embeddings**: Numerical representations of textbook content chunks stored in Qdrant for semantic search
- **Search Tool**: A Python function that allows the OpenAI Agent to query the vector database for relevant textbook content
- **Qdrant Collection**: A named container in Qdrant storing the textbook embeddings and associated metadata

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Students receive textbook-specific answers when asking questions about "ROS 2 nodes" or "Gazebo simulation" with 90% accuracy
- **SC-002**: The system can sync textbook content to the vector database in under 5 minutes for a typical textbook
- **SC-003**: Students report 80% satisfaction with the accuracy and relevance of textbook-based answers
- **SC-004**: The search functionality returns relevant textbook content within 2 seconds for 95% of queries
- **SC-005**: A test query about a specific course module (e.g., "What hardware is required for the Digital Twin?") returns an accurate answer based on the textbook content