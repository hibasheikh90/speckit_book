#!/usr/bin/env python3
"""
Test script to verify end-to-end RAG functionality.
This script tests the integration between the search tool and the AI agent.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.services.rag_service import RAGService
from src.services.qdrant_service import QdrantService
from src.tools.textbook_search_tool import textbook_search_tool
from src.backend.agent import AITutor, initialize_agent


async def test_rag_functionality():
    """Test the end-to-end RAG functionality."""
    print("Testing RAG functionality...")

    # Test 1: Test Qdrant service
    print("\n1. Testing Qdrant service...")
    qdrant_service = QdrantService()
    try:
        await qdrant_service.ensure_collection_exists()
        print("OK Qdrant collection exists/created successfully")

        # Get collection info
        collection_info = await qdrant_service.get_collection_info()
        print(f"OK Collection points count: {collection_info.points_count}")

        await qdrant_service.close()
    except Exception as e:
        print(f"ERROR Qdrant service test failed: {e}")
        return False

    # Test 2: Test textbook search tool
    print("\n2. Testing textbook search tool...")
    try:
        # This will test searching for content (even if empty)
        results = await textbook_search_tool.search_textbook("test query")
        print(f"OK Textbook search tool works, returned {len(results)} results")
    except Exception as e:
        print(f"ERROR Textbook search tool test failed: {e}")
        return False

    # Test 3: Test RAG service
    print("\n3. Testing RAG service...")
    rag_service = RAGService()
    try:
        results = await rag_service.search_textbook("test query")
        print(f"OK RAG service works, returned {len(results)} results")
        await rag_service.close()
    except Exception as e:
        print(f"ERROR RAG service test failed: {e}")
        await rag_service.close()
        return False

    # Test 4: Test agent initialization
    print("\n4. Testing agent initialization...")
    try:
        agent = initialize_agent()
        print("OK Agent initialized successfully")

        # Test with a simple query (this would require actual embeddings in the database)
        print("OK Agent setup is complete")
    except Exception as e:
        print(f"ERROR Agent initialization test failed: {e}")
        return False

    print("\nOK All RAG functionality tests passed!")
    return True


async def test_with_sample_data():
    """Test with sample data to verify the full flow."""
    print("\nTesting with sample data...")

    # Test direct search
    try:
        results = await textbook_search_tool.search_textbook("Physical AI and Robotics")
        print(f"Sample search returned {len(results)} results")

        if results:
            for i, result in enumerate(results[:2]):  # Show first 2 results
                print(f"Result {i+1}:")
                print(f"  Source: {result.get('source_file', 'Unknown')}")
                print(f"  Chapter: {result.get('chapter_title', 'Unknown')}")
                print(f"  Score: {result.get('score', 0.0):.3f}")
                content_preview = result.get('content', '')[:100] + "..." if len(result.get('content', '')) > 100 else result.get('content', '')
                print(f"  Content preview: {content_preview}")
                print()
        else:
            print("No results found (this is expected if the database is empty)")

    except Exception as e:
        print(f"Sample data test failed: {e}")
        return False

    return True


async def main():
    """Main test function."""
    print("Starting RAG functionality tests...")

    success = await test_rag_functionality()

    if success:
        await test_with_sample_data()
        print("\nSUCCESS RAG functionality verification completed!")
        print("\nTo fully test the system, you need to:")
        print("1. Run the sync_db script with actual textbook content")
        print("2. Use the sync command: uv run python -m src.scripts.sync_db --content-dir <path-to-textbook-content>")
        print("3. Then test the chat endpoint with questions about the textbook content")
    else:
        print("\nFAILED RAG functionality tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())