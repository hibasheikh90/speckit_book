from pydantic import BaseModel
from typing import Optional, Dict, Any


class TextbookChunk(BaseModel):
    """
    Data model for representing a chunk of textbook content.
    This matches the structure defined in the data model.
    """
    id: Optional[str] = None  # Qdrant point ID
    content: str  # Text content of the chunk
    source_file: str  # Path to original markdown file
    chapter_title: str  # Title of the chapter
    section_id: Optional[str] = None  # Section identifier
    page_url: Optional[str] = None  # URL to the original content
    content_type: str = "text"  # Type: text/code/diagram
    token_count: Optional[int] = None  # Number of tokens in the chunk
    embedding: Optional[list] = None  # Embedding vector (when stored separately)
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata


class TextbookChunkPayload(BaseModel):
    """
    Payload structure for storing in Qdrant.
    """
    content: str
    source_file: str
    chapter_title: str
    section_id: Optional[str] = None
    page_url: Optional[str] = None
    content_type: str = "text"
    token_count: Optional[int] = None