# Research Summary: RAG Tool & Vector Sync (Qdrant)

## Decision: Text Chunking Strategy
**Rationale**: Selected token-based splitting with 150-token limit using langchain's TokenTextSplitter with overlap to maintain context continuity. This approach provides precise control over chunk size, ensuring consistency with the specification requirement while maintaining semantic coherence.

**Alternatives considered**:
1. Recursive Character Splitting - Simple character-based splitting with overlap
2. Contextual Splitting - Split along semantic boundaries (headers, paragraphs)
3. Token-based Splitting - Precise token count control using tiktoken (selected)
4. Custom Markdown-aware Splitting - Respect document structure (sections, headers)

## Decision: Vector Database
**Rationale**: Selected Qdrant Cloud Free Tier based on specification requirement and cost considerations. Qdrant provides efficient vector search capabilities with good performance for the textbook RAG system.

## Decision: Embedding Model
**Rationale**: Selected Google's Generative AI (Gemini) API for embeddings as specified in requirements. Gemini provides high-quality embeddings suitable for the textbook content retrieval.

## Decision: Architecture Pattern
**Rationale**: Selected RAG (Retrieval-Augmented Generation) pattern with separate ingestion and retrieval flows. This allows for efficient updating of the knowledge base while providing real-time context retrieval for the AI agent.

## Technology Best Practices Researched
- **FastAPI**: Best practice for async API endpoints with built-in OpenAPI documentation
- **Qdrant**: Industry standard for vector search with good performance and cloud options
- **Langchain**: Standard library for text processing and RAG implementations
- **Tiktoken**: Reliable token counting for consistent chunking
- **Rate limiting**: Essential for handling concurrent users and API quota management