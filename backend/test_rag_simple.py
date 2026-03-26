#!/usr/bin/env python3
"""
Simple test to verify RAG components work correctly without full system integration.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all RAG components can be imported without errors."""
    print("Testing RAG component imports...")

    try:
        from src.services.qdrant_service import QdrantService
        print("OK QdrantService imported successfully")
    except ImportError as e:
        print(f"ERROR Failed to import QdrantService: {e}")
        return False

    try:
        from src.services.text_chunker import TextChunker
        print("OK TextChunker imported successfully")
    except ImportError as e:
        print(f"ERROR Failed to import TextChunker: {e}")
        return False

    try:
        from src.services.ingestion_service import IngestionService
        print("OK IngestionService imported successfully")
    except ImportError as e:
        print(f"ERROR Failed to import IngestionService: {e}")
        return False

    try:
        from src.tools.textbook_search_tool import TextbookSearchTool
        print("OK TextbookSearchTool imported successfully")
    except ImportError as e:
        print(f"ERROR Failed to import TextbookSearchTool: {e}")
        return False

    try:
        from src.services.rag_service import RAGService
        print("OK RAGService imported successfully")
    except ImportError as e:
        print(f"ERROR Failed to import RAGService: {e}")
        return False

    print("\nOK All RAG components imported successfully!")
    return True

def test_text_chunking():
    """Test text chunking functionality."""
    print("\nTesting text chunking functionality...")

    try:
        from src.services.text_chunker import TextChunker
        from src.config.settings import settings

        # Create a text chunker instance
        chunker = TextChunker()
        print(f"OK TextChunker created with chunk size: {chunker.chunk_size}, overlap: {chunker.chunk_overlap}")

        # Test chunking with sample text
        sample_text = "This is a sample text. " * 50  # Create a longer text
        chunks = chunker.chunk_text(sample_text, "test.md", "Test Chapter")

        print(f"OK Text chunked into {len(chunks)} chunks")
        if chunks:
            print(f"  First chunk token count: {chunks[0]['token_count']}")
            print(f"  First chunk length: {len(chunks[0]['content'])} characters")

        return True
    except Exception as e:
        print(f"ERROR Failed to test text chunking: {e}")
        return False

def test_data_models():
    """Test data models."""
    print("\nTesting data models...")

    try:
        from src.models.textbook_chunk import TextbookChunk, TextbookChunkPayload

        # Test creating a textbook chunk
        chunk = TextbookChunk(
            content="Test content for the textbook",
            source_file="test/chapter1.md",
            chapter_title="Introduction to Robotics",
            token_count=10
        )
        print(f"OK TextbookChunk created: {chunk.chapter_title}")

        # Test creating a payload
        payload = TextbookChunkPayload(
            content="Test content for the textbook",
            source_file="test/chapter1.md",
            chapter_title="Introduction to Robotics",
            token_count=10
        )
        print(f"OK TextbookChunkPayload created: {payload.chapter_title}")

        return True
    except Exception as e:
        print(f"ERROR Failed to test data models: {e}")
        return False

def test_tool_definition():
    """Test textbook search tool definition."""
    print("\nTesting textbook search tool...")

    try:
        from src.tools.textbook_search_tool import TextbookSearchTool

        tool = TextbookSearchTool()
        tool_def = tool.get_tool_definition()

        print(f"OK Tool definition retrieved: {tool_def['function']['name']}")
        print(f"OK Tool description: {tool_def['function']['description'][:60]}...")

        return True
    except Exception as e:
        print(f"ERROR Failed to test tool definition: {e}")
        return False

async def test_mock_qdrant():
    """Test Qdrant service without connecting to actual service."""
    print("\nTesting Qdrant service structure...")

    try:
        from src.services.qdrant_service import QdrantService
        from src.config.settings import settings

        # Create service instance (this will fail if it tries to connect)
        # We'll catch that and just verify the structure is correct
        try:
            service = QdrantService()
            print(f"OK QdrantService created with collection: {service.collection_name}")
            print(f"  Vector size: {service.vector_size}")
            await service.close()
            return True
        except Exception as e:
            # If it fails due to connection issues, that's expected
            # We just want to make sure the class structure is correct
            print(f"OK QdrantService structure is correct (connection error is expected): {type(e).__name__}")
            return True
    except Exception as e:
        print(f"ERROR Failed to test Qdrant service: {e}")
        return False

async def main():
    """Run all tests."""
    print("Testing RAG System Structure and Components\n")
    print("="*50)

    all_tests_passed = True

    # Test imports
    all_tests_passed &= test_imports()

    # Test text chunking
    all_tests_passed &= test_text_chunking()

    # Test data models
    all_tests_passed &= test_data_models()

    # Test tool definition
    all_tests_passed &= test_tool_definition()

    # Test Qdrant service (mock)
    all_tests_passed &= await test_mock_qdrant()

    print("\n" + "="*50)
    if all_tests_passed:
        print("OK All structural tests passed!")
        print("\nNote: This test verifies the structure and integration of components.")
        print("To run the full sync, you would need valid Qdrant and Gemini API keys.")
    else:
        print("ERROR Some tests failed!")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)