#!/usr/bin/env python3
"""
Script to sync textbook content to the Qdrant vector database.

This script:
1. Reads markdown files from the textbook content directory
2. Chunks the content into 150-token segments
3. Generates embeddings using the Gemini API
4. Upserts the embeddings to Qdrant
"""
import asyncio
import sys
from pathlib import Path
import os

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.services.ingestion_service import IngestionService
from src.services.rag_service import RAGService
from src.config.settings import settings


async def sync_textbook_content(content_dir: str, base_url: str = ""):
    """
    Sync textbook content to the vector database.

    Args:
        content_dir: Directory containing textbook Markdown files
        base_url: Base URL for generating page URLs (optional)
    """
    print(f"Starting textbook content sync from: {content_dir}")
    print(f"Target Qdrant collection: {settings.qdrant_collection_name}")
    print(f"Base URL: {base_url}")

    ingestion_service = IngestionService()
    rag_service = RAGService()

    try:
        # Ensure the Qdrant collection exists
        print("Ensuring Qdrant collection exists...")
        await rag_service.ensure_qdrant_collection()
        print("Qdrant collection is ready.")

        # Ingest the content
        print("Starting content ingestion...")
        total_chunks = await ingestion_service.ingest_textbook_content(content_dir, base_url)

        print(f"Successfully ingested {total_chunks} chunks into the vector database.")
        print("Textbook content sync completed successfully!")

    except Exception as e:
        print(f"Error during content sync: {str(e)}")
        raise
    finally:
        # Close connections
        await ingestion_service.close()
        await rag_service.close()


def main():
    """Main function to run the sync script."""
    import argparse

    parser = argparse.ArgumentParser(description="Sync textbook content to Qdrant vector database")
    parser.add_argument(
        "--content-dir",
        type=str,
        default="./textbook-content",  # Default location for textbook content
        help="Directory containing textbook Markdown files (default: ./textbook-content)"
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="",
        help="Base URL for generating page URLs (optional)"
    )

    args = parser.parse_args()

    # Check if required environment variables are set
    if not settings.qdrant_url or not settings.gemini_api_key:
        print("Error: Required environment variables are not set.")
        print("Please ensure QDRANT_URL and GEMINI_API_KEY are set in your environment.")
        sys.exit(1)

    content_path = Path(args.content_dir)
    if not content_path.exists():
        print(f"Error: Content directory does not exist: {args.content_dir}")
        print("Please provide a valid path to the textbook content directory.")
        sys.exit(1)

    print("Starting textbook content sync...")
    print(f"Content directory: {args.content_dir}")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Collection: {settings.qdrant_collection_name}")

    # Run the async sync function
    asyncio.run(sync_textbook_content(args.content_dir, args.base_url))


if __name__ == "__main__":
    main()