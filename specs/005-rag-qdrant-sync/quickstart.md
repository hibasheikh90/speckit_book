# Quickstart: RAG Tool & Vector Sync (Qdrant)

## Prerequisites
- Python 3.11+
- Qdrant Cloud account with API key
- Google Gemini API key
- uv package manager

## Setup

### 1. Environment Configuration
```bash
# Copy the environment template
cp backend/.env.example backend/.env

# Update backend/.env with your API keys:
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 2. Install Dependencies
```bash
# Navigate to backend directory
cd backend

# Install dependencies with uv
uv sync
```

### 3. Initialize Vector Database
```bash
# Run the sync script to ingest textbook content
uv run python -m scripts.sync_db
```

## Usage

### 1. Start the Backend Server
```bash
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

### 2. Test the RAG Endpoint
```bash
# Test the chat endpoint which now includes the textbook search tool
curl -X POST http://localhost:8000/chat \
  -H "Content-Type": "application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "What are the key concepts about ROS 2 nodes from the textbook?"
      }
    ]
  }'
```

## Key Components

### Ingestion Pipeline
- `scripts/sync_db.py`: Main script to sync textbook content to Qdrant
- `src/services/ingestion_service.py`: Handles Markdown parsing and chunking
- `src/services/gemini_service.py`: Generates embeddings using Gemini API
- `src/services/qdrant_service.py`: Manages Qdrant operations

### RAG Tool
- `src/tools/textbook_search_tool.py`: OpenAI-compatible tool for textbook search
- `src/services/rag_service.py`: Core RAG functionality

### Integration
- `src/api/chat_router.py`: Updated chat endpoint with tool registration
- The `search_textbook` tool is automatically registered with the OpenAI Agent