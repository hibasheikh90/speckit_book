# Data Model: RAG Tool & Vector Sync (Qdrant)

## Entities

### Textbook Content Chunk
- **id**: String (Qdrant point ID)
- **content**: String (text content of the chunk)
- **metadata**: Object
  - source_file: String (path to original markdown file)
  - chapter_title: String
  - section_id: String
  - page_url: String (URL to the original content)
  - content_type: String (text/code/diagram)
  - token_count: Integer
- **vector**: Array<Float> (embedding vector from Gemini API)

### Qdrant Collection Schema
- **Collection Name**: `textbook_chunks`
- **Vector Size**: Determined by Gemini embedding model (typically 768-3072 dimensions)
- **Distance Metric**: Cosine similarity
- **Payload Fields**:
  - content: keyword (indexed for filtering)
  - source_file: keyword (indexed for filtering)
  - chapter_title: keyword (indexed for filtering)
  - content_type: keyword (indexed for filtering)

### Search Results
- **query_embedding**: Array<Float> (query converted to embedding)
- **search_results**: Array of objects containing:
  - id: String (point ID in Qdrant)
  - content: String (retrieved text content)
  - score: Float (similarity score)
  - metadata: Object (source information)

## Relationships
- Textbook content is chunked and stored as individual points in Qdrant collection
- Each chunk maintains reference to its source document through metadata
- Search queries are converted to embeddings and matched against stored vectors