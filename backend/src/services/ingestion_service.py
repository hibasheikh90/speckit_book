from typing import List, Dict, Any
from pathlib import Path
import asyncio
import aiofiles
import re
from src.services.text_chunker import TextChunker
from src.services.gemini_service import GeminiService
from src.services.qdrant_service import QdrantService
from src.models.textbook_chunk import TextbookChunkPayload
import hashlib


class IngestionService:
    """
    Service for ingesting textbook content from Markdown files into the vector database.
    Handles parsing, chunking, embedding, and storing textbook content in Qdrant.
    """

    def __init__(self):
        self.text_chunker = TextChunker()
        self.gemini_service = GeminiService()
        self.qdrant_service = QdrantService()

    async def ingest_textbook_content(self, content_dir: str, base_url: str = "") -> int:
        """
        Ingest all Markdown content from the specified directory.

        Args:
            content_dir: Directory containing textbook Markdown files
            base_url: Base URL for generating page URLs

        Returns:
            Number of chunks successfully ingested
        """
        content_path = Path(content_dir)
        if not content_path.exists():
            raise ValueError(f"Content directory does not exist: {content_dir}")

        # Find all markdown files
        markdown_files = list(content_path.rglob("*.md")) + list(content_path.rglob("*.mdx"))

        total_chunks_ingested = 0

        for file_path in markdown_files:
            print(f"Processing file: {file_path}")
            try:
                # Extract chapter title from file path or content
                chapter_title = self._extract_chapter_title(file_path, content_path)

                # Read and parse the markdown file
                content = await self._read_markdown_file(file_path)

                # Extract additional metadata from content
                metadata = {
                    "source_file": str(file_path.relative_to(content_path)),
                    "chapter_title": chapter_title,
                    "page_url": f"{base_url}/{file_path.relative_to(content_path).with_suffix('')}" if base_url else ""
                }

                # Chunk the content
                chunks = self.text_chunker.chunk_markdown_content(content, metadata)

                # Process and store each chunk
                for chunk_data in chunks:
                    await self._process_and_store_chunk(chunk_data)
                    total_chunks_ingested += 1

                print(f"Successfully processed {len(chunks)} chunks from {file_path}")

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                continue  # Continue with other files even if one fails

        return total_chunks_ingested

    async def _read_markdown_file(self, file_path: Path) -> str:
        """
        Read and clean markdown file content.

        Args:
            file_path: Path to the markdown file

        Returns:
            Cleaned content string
        """
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            content = await file.read()

        # Remove frontmatter if present (common in Docusaurus)
        content = self._remove_frontmatter(content)

        # Clean up content (remove excessive whitespace, etc.)
        content = self._clean_content(content)

        return content

    def _remove_frontmatter(self, content: str) -> str:
        """
        Remove YAML frontmatter from markdown content if present.

        Args:
            content: Raw markdown content

        Returns:
            Content without frontmatter
        """
        # Look for YAML frontmatter (--- to ---)
        frontmatter_pattern = r'^---\s*\n.*?\n---\s*\n'
        content = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL)
        return content.strip()

    def _clean_content(self, content: str) -> str:
        """
        Clean up markdown content by removing excessive whitespace.

        Args:
            content: Markdown content

        Returns:
            Cleaned content
        """
        # Remove excessive newlines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in content.split('\n')]
        content = '\n'.join(lines)

        return content.strip()

    def _extract_chapter_title(self, file_path: Path, content_path: Path) -> str:
        """
        Extract chapter title from file path or content.

        Args:
            file_path: Path to the markdown file
            content_path: Base content directory path

        Returns:
            Chapter title
        """
        # Try to get title from the filename or directory structure
        # If not available, return a reasonable default
        relative_path = file_path.relative_to(content_path)

        # Remove extension and replace underscores/dashes with spaces
        title = relative_path.stem.replace('_', ' ').replace('-', ' ').title()

        # If it's in a subdirectory, include that in the title
        if relative_path.parent != Path('.'):
            parent_dir = relative_path.parent.name.replace('_', ' ').replace('-', ' ').title()
            title = f"{parent_dir} - {title}"

        return title

    async def _process_and_store_chunk(self, chunk_data: Dict[str, Any]):
        """
        Process a chunk by generating embeddings and storing in Qdrant.

        Args:
            chunk_data: Dictionary containing chunk content and metadata
        """
        # Generate embedding for the content
        embedding = await self.gemini_service.generate_single_embedding(chunk_data["content"])

        # Create a unique ID for this chunk based on content hash
        content_hash = hashlib.md5(f"{chunk_data['content']}{chunk_data['source_file']}".encode()).hexdigest()

        # Prepare the payload for Qdrant
        payload = TextbookChunkPayload(
            content=chunk_data["content"],
            source_file=chunk_data["source_file"],
            chapter_title=chunk_data["chapter_title"],
            page_url=chunk_data.get("page_url", ""),
            content_type="text",
            token_count=chunk_data.get("token_count", 0)
        ).dict()

        # Create the point for Qdrant
        point = {
            "id": content_hash,
            "vector": embedding,
            "payload": payload
        }

        # Upsert to Qdrant
        await self.qdrant_service.upsert_vectors([point])

    async def close(self):
        """Close all service connections."""
        await self.qdrant_service.close()