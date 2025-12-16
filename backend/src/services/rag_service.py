from typing import List, Dict, Any
from src.services.qdrant_service import QdrantService
from src.services.gemini_service import GeminiService
from src.config.settings import settings


class RAGService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.gemini_service = GeminiService()

    async def search_textbook(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the textbook content using the RAG system.
        1. Generate embedding for the query
        2. Search in Qdrant for similar content
        3. Return up to max_search_results results
        """
        try:
            # Generate embedding for the query
            query_embedding = await self.gemini_service.generate_single_embedding(query)

            # Search in Qdrant
            search_results = await self.qdrant_service.search_vectors(
                query_vector=query_embedding,
                limit=settings.max_search_results
            )

            return search_results
        except Exception as e:
            raise Exception(f"Failed to search textbook: {str(e)}")

    async def ensure_qdrant_collection(self):
        """Ensure the Qdrant collection exists."""
        await self.qdrant_service.ensure_collection_exists()

    async def close(self):
        """Close connections."""
        await self.qdrant_service.close()