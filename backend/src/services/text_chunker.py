from typing import List, Dict, Any
from langchain_text_splitters import TokenTextSplitter
from src.config.settings import settings
import tiktoken


class TextChunker:
    """
    Utility class for chunking text content into 150-token segments.
    Uses langchain's TokenTextSplitter with tiktoken for accurate token counting.
    """

    def __init__(self, chunk_size: int = None, chunk_overlap: int = 20):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Maximum number of tokens per chunk (defaults to settings value)
            chunk_overlap: Number of tokens to overlap between chunks for context continuity
        """
        self.chunk_size = chunk_size or settings.chunk_token_limit
        self.chunk_overlap = chunk_overlap

        # Use TokenTextSplitter from langchain with tiktoken encoder
        # Using gpt-3.5-turbo encoding as it's similar to what Gemini uses
        self.text_splitter = TokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            encoding_name="cl100k_base"  # This is the encoding for gpt-3.5-turbo and gpt-4
        )

    def chunk_text(self, text: str, source_file: str = "", chapter_title: str = "") -> List[Dict[str, Any]]:
        """
        Chunk the input text into segments of specified token size.

        Args:
            text: The text content to chunk
            source_file: Path to the original markdown file
            chapter_title: Title of the chapter this text belongs to

        Returns:
            List of dictionaries containing the chunked text and metadata
        """
        # Split the text using the TokenTextSplitter
        chunks = self.text_splitter.split_text(text)

        # Create chunk objects with metadata
        chunked_data = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "content": chunk,
                "source_file": source_file,
                "chapter_title": chapter_title,
                "chunk_index": i,
                "token_count": self._count_tokens(chunk)
            }
            chunked_data.append(chunk_data)

        return chunked_data

    def _count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string using tiktoken.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens in the text
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def chunk_markdown_content(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk markdown content with provided metadata.

        Args:
            content: The markdown content to chunk
            metadata: Metadata dictionary containing source_file, chapter_title, etc.

        Returns:
            List of chunked data with metadata
        """
        source_file = metadata.get("source_file", "")
        chapter_title = metadata.get("chapter_title", "")

        return self.chunk_text(content, source_file, chapter_title)


# Global instance for use in the application
text_chunker = TextChunker()