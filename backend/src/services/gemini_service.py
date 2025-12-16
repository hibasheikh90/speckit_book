import google.generativeai as genai
from typing import List
from src.config.settings import settings


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model_name

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Google's Gemini API.
        """
        try:
            # The Gemini API doesn't have an async embedding function, so we wrap it
            import asyncio
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                lambda: [genai.embed_content(self.model_name, text)["embedding"] for text in texts]
            )
            return embeddings
        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")

    async def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate a single embedding for a text using Google's Gemini API.
        """
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                lambda: genai.embed_content(self.model_name, text)["embedding"]
            )
            return embedding
        except Exception as e:
            raise Exception(f"Failed to generate single embedding: {str(e)}")