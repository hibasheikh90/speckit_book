---
id: 1
title: rag-qdrant-sync-spec
stage: spec
date: 2025-12-15
surface: agent
model: Claude Sonnet 4.5
feature: rag-qdrant-sync
branch: 005-rag-qdrant-sync
user: claude-code
command: /sp.specify
labels: [spec,rag,qdrant,vector-db,textbook]
links:
  spec: specs/005-rag-qdrant-sync/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-rag-qdrant-sync/spec.md
 - specs/005-rag-qdrant-sync/checklists/requirements.md
 - history/prompts/005-rag-qdrant-sync/
tests:
 - specs/005-rag-qdrant-sync/checklists/requirements.md
---

## Prompt

```
# Specification: Phase 5 - RAG Tool & Vector Sync (Qdrant)

## Overview
Implement the "Long-term Memory" and "Knowledge Retrieval" capabilities for the AI Tutor. This phase involves setting up Qdrant Cloud as the vector database, creating an ingestion pipeline to sync the "Physical AI & Humanoid Robotics" textbook content, and building a specific Tool that the OpenAI Agent can use to retrieve context before answering student questions.

## Scope
* **In-Scope:**
    * **Vector Database:** Setup connection to Qdrant Cloud (Free Tier) using `qdrant-client`.
    * **Ingestion Pipeline:** Create a script/function to parse Docusaurus Markdown (`.md`/`.mdx`) files, chunk the text, generate embeddings, and upsert them to Qdrant.
    * **Embedding Model:** Use **Gemini API** for generating text embeddings (as per project constraints).
    * **Agent Tool:** Create a Python function (Tool) named `search_textbook` that the OpenAI Agent can invoke to query Qdrant.
    * **Backend Update:** Update the FastAPI `/chat` endpoint to register this new tool with the Agent.
* **Out-of-Scope:**
    * Frontend UI changes (The existing chat widget from Phase 3 will automatically benefit from smarter answers).
    * Authentication (Reserved for Phase 6).

## User Stories
* **As a student**, I want the chatbot to answer specific questions about "ROS 2 nodes" or "Gazebo simulation" by citing the actual textbook content, not just general internet knowledge.
* **As a developer**, I want a script I can run (`uv run sync_db`) to update the vector database whenever I add ne*Verification:** A test query about a specific course module (e.g., "What hardware is required for the Digital Twin?") returns an accurate answer based on the `Hackathon_Physical_AI_Textbook.md` content.
* ✅ **Constitution Compliance:** Code uses Type hints, proper error handling for API failures, and follows the global project structure.
```

## Response snapshot

Created feature specification for RAG Tool & Vector Sync (Qdrant) feature. The specification includes:

- User stories for students asking textbook-specific questions, developers syncing content, and agent context retrieval
- Functional requirements covering Qdrant connection, content parsing, embedding generation, search tool creation, and integration
- Success criteria with measurable outcomes for accuracy, performance, and user satisfaction
- Edge cases for error handling and system behavior
- A quality checklist to validate the specification

The feature branch 005-rag-qdrant-sync was created, and the spec file was written to specs/005-rag-qdrant-sync/spec.md with supporting files.

## Outcome

- ✅ Impact: Feature specification created for RAG vector database integration
- 🧪 Tests: Specification quality checklist created and validated
- 📁 Files: spec.md, requirements checklist, and directory structure created
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification addresses all key requirements from user stories

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase