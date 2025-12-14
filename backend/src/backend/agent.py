"""AI agent module for Gemini-powered educational tutor."""
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from backend.config import settings
from backend.exceptions import EmptyAIResponse, AIServiceError


class AITutor:
    """Gemini-powered AI tutor initialized with Global Constitution."""

    def __init__(self):
        """Initialize AI tutor with Gemini API client and constitution."""
        # Validate API key is set
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is required")

        self.client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
        )
        self.model = settings.gemini_model
        self.system_prompt = self._load_constitution()

    def _load_constitution(self) -> str:
        """Load Global Constitution from filesystem.

        Returns:
            str: Constitution content

        Raises:
            RuntimeError: If constitution file cannot be loaded
        """
        try:
            constitution_path = settings.constitution_path
            if not constitution_path.exists():
                raise FileNotFoundError(f"Constitution not found: {constitution_path}")
            return constitution_path.read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to load Global Constitution: {e}")

    async def generate_response(self, message: str) -> str:
        """Generate educational response using Gemini API.

        Args:
            message: Student question

        Returns:
            str: AI-generated educational response

        Raises:
            EmptyAIResponse: If AI service returns empty/unusable response
            AIServiceError: If AI service fails or times out
        """
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": message},
                    ],
                ),
                timeout=settings.request_timeout,
            )

            # Extract response text and validate
            content = response.choices[0].message.content
            if not content or not content.strip():
                raise EmptyAIResponse("AI service returned empty response")

            return content.strip()

        except asyncio.TimeoutError:
            raise AIServiceError(f"Request timed out after {settings.request_timeout} seconds")
        except EmptyAIResponse:
            # Re-raise EmptyAIResponse as-is
            raise
        except Exception as e:
            # Catch all other exceptions and wrap in AIServiceError
            raise AIServiceError(f"AI service error: {str(e)}")


# Global agent instance (initialized on startup)
agent: AITutor | None = None


def initialize_agent() -> AITutor:
    """Initialize AI agent (called during app lifespan).

    Returns:
        AITutor: Initialized agent instance
    """
    global agent
    agent = AITutor()
    return agent


def get_agent() -> AITutor:
    """FastAPI dependency to get initialized agent.

    Returns:
        AITutor: The initialized agent

    Raises:
        RuntimeError: If agent not initialized
    """
    if agent is None:
        raise RuntimeError("AI agent not initialized. Call initialize_agent() first.")
    return agent
