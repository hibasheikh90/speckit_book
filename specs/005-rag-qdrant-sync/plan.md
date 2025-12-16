# Implementation Plan: RAG Tool & Vector Sync (Qdrant)

**Branch**: `005-rag-qdrant-sync` | **Date**: 2025-12-15 | **Spec**: [link to spec](./spec.md)
**Input**: Feature specification from `/specs/005-rag-qdrant-sync/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of RAG (Retrieval-Augmented Generation) system for the AI Tutor using Qdrant Cloud as the vector database and Gemini API for embeddings. This includes an ingestion pipeline to parse Docusaurus Markdown files, chunk text into 150-token segments, generate embeddings, and upsert to Qdrant. Also includes a `search_textbook` tool for the OpenAI Agent and integration with the FastAPI `/chat` endpoint.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, qdrant-client, python-dotenv, google-generativeai, langchain-text-splitters, tiktoken
**Storage**: Qdrant Cloud (vector database), with textbook content in Markdown files
**Testing**: pytest for backend functionality
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web (backend service with API endpoints)
**Performance Goals**: <500ms retrieval for vector search (p95), <2 seconds for full RAG response
**Constraints**: <200ms p95 for API responses, support up to 100 concurrent users with rate limiting
**Scale/Scope**: Support textbook content with 100+ pages, handle 10,000+ vector embeddings

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Educational-First Design: RAG system directly supports learning by providing contextual textbook answers
- ✅ AI-Native Content Creation: Following spec-driven development with Claude Code assistance
- ✅ RAG-First Information Architecture: Primary interface for dynamic learning via chatbot
- ✅ Security & Privacy by Design: No PII in vector embeddings, using environment variables for API keys
- ✅ Performance & Scalability Standards: <500ms retrieval target, concurrent access with rate limiting
- ✅ Open Source & Reproducibility: Using open-source libraries and documented architecture

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
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
│   ├── models/
│   ├── services/
│   │   ├── rag_service.py          # RAG implementation and vector operations
│   │   ├── qdrant_service.py       # Qdrant client operations
│   │   ├── ingestion_service.py    # Markdown parsing and text chunking
│   │   └── gemini_service.py       # Gemini API integration for embeddings
│   ├── tools/
│   │   └── textbook_search_tool.py # OpenAI Agent tool for textbook search
│   ├── api/
│   │   └── chat_router.py          # Updated chat endpoint with tool integration
│   ├── config/
│   │   └── settings.py             # Configuration for Qdrant and Gemini
│   └── scripts/
│       └── sync_db.py              # Ingestion script for syncing textbook content
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

**Structure Decision**: Web application structure with backend service containing RAG functionality, vector database integration, and OpenAI Agent tools.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## System Architecture and Flow

### Ingestion Pipeline
1. **Markdown Source** → Load Docusaurus Markdown files from textbook content
2. **Text Splitter** → Split content into 150-token chunks using langchain text splitters
3. **Gemini Embeddings** → Generate embeddings using Google's Generative AI API
4. **Qdrant Upsert** → Store embeddings and metadata in Qdrant Cloud collection

### Retrieval (RAG) Flow
1. **User Query** → Student asks question via chat interface
2. **Agent** → OpenAI Agent receives query in FastAPI `/chat` endpoint
3. **Agent Tool Call** → Agent invokes `search_textbook` tool
4. **Tool Logic** → Tool queries embeddings via Gemini API → Qdrant Search → Returns relevant text
5. **Agent Response** → Agent generates response using retrieved context and returns to user

## Dependencies

### New Python Dependencies for Backend
- `qdrant-client`: For connecting to Qdrant Cloud
- `google-generativeai`: For using Gemini API for embeddings
- `langchain-text-splitters`: For text splitting and document loading utilities
- `tiktoken`: For token counting (for chunking strategy)
- `python-dotenv`: For environment variable management

## High-Level Plan Steps

### 1. SETUP & CONFIG
- Configure Qdrant Cloud connection and collection setup
- Set up Gemini API integration and configuration
- Install and configure new dependencies in backend
- Create configuration files for API keys and service settings

### 2. INGESTION SCRIPT DEVELOPMENT
- Develop Markdown file loader for Docusaurus content
- Implement text chunking logic (150-token segments)
- Create embedding generation using Gemini API
- Build upsert functionality to Qdrant
- Create sync_db script for content synchronization

### 3. VECTOR TOOL CREATION
- Design `search_textbook` function as OpenAI-compatible tool
- Implement vector search functionality in Qdrant
- Add result ranking and filtering (max 5 results)
- Include error handling and rate limiting

### 4. AGENT INTEGRATION
- Update FastAPI `/chat` endpoint to register the new tool
- Integrate tool with existing OpenAI Agent workflow
- Test tool invocation and response handling
- Ensure proper context injection into agent responses

### 5. VALIDATION
- Test end-to-end RAG flow with sample textbook queries
- Validate response accuracy and citation quality
- Performance testing for response times and concurrent access
- Verify proper error handling and edge cases

## ADR Suggestion: Text Chunking Strategy

### Architectural Decision Record: Text Chunking Strategy for Markdown Content

**Issue**: How should we chunk the textbook Markdown content for optimal retrieval in the RAG system?

**Decision Drivers**:
- Need to balance context retention with embedding efficiency
- Must preserve semantic meaning within chunks
- Performance considerations for vector search
- Alignment with the 150-token requirement from spec

**Alternatives Considered**:
1. **Recursive Character Splitting**: Simple character-based splitting with overlap
2. **Contextual Splitting**: Split along semantic boundaries (headers, paragraphs)
3. **Token-based Splitting**: Precise token count control using tiktoken
4. **Custom Markdown-aware Splitting**: Respect document structure (sections, headers)

**Selected Approach**: Token-based splitting with 150-token limit using langchain's TokenTextSplitter with overlap to maintain context continuity.

**Rationale**: This approach provides precise control over chunk size, ensuring consistency with the specification requirement while maintaining semantic coherence. The token-based approach is more reliable than character-based methods since tokens better represent meaningful linguistic units.

**Consequences**:
- Positive: Consistent chunk sizes, predictable embedding generation
- Negative: May split semantically coherent paragraphs
- Neutral: Requires token counting library dependency
