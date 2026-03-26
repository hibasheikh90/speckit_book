import asyncio
from typing import List, Dict, Optional, Any
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from src.config.settings import settings


class QdrantService:
    def __init__(self):
        self.client = AsyncQdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=True
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.embedding_dimension

    async def ensure_collection_exists(self):
        """Ensure the textbook chunks collection exists with proper configuration."""
        try:
            collections = await self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )

                # Create payload index for faster filtering
                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="source_file",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="chapter_title",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="content_type",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

        except Exception as e:
            raise Exception(f"Failed to ensure collection exists: {str(e)}")

    async def upsert_vectors(self, points: List[Dict[str, Any]]):
        """Upsert vectors to the collection."""
        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        except Exception as e:
            raise Exception(f"Failed to upsert vectors: {str(e)}")

    async def search_vectors(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in the collection."""
        try:
            search_results = await self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True
            )

            results = []
            # The query_points response has a different structure
            # It should have a points attribute containing the results
            for hit in search_results.points:
                result = {
                    "id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "source_file": hit.payload.get("source_file", ""),
                    "chapter_title": hit.payload.get("chapter_title", ""),
                    "score": hit.score,
                    "page_url": hit.payload.get("page_url", ""),
                    "content_type": hit.payload.get("content_type", "text")
                }
                results.append(result)

            return results
        except Exception as e:
            raise Exception(f"Failed to search vectors: {str(e)}")

    async def delete_collection(self):
        """Delete the collection (useful for testing/reindexing)."""
        try:
            await self.client.delete_collection(self.collection_name)
        except Exception as e:
            raise Exception(f"Failed to delete collection: {str(e)}")

    async def get_collection_info(self):
        """Get information about the collection."""
        try:
            return await self.client.get_collection(self.collection_name)
        except Exception as e:
            raise Exception(f"Failed to get collection info: {str(e)}")

    async def close(self):
        """Close the client connection."""
        # Check if the client has aclose method (newer versions) or close method (older versions)
        if hasattr(self.client, 'aclose'):
            await self.client.aclose()
        elif hasattr(self.client, 'close'):
            await self.client.close()