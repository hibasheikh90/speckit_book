"""AI agent module for Gemini-powered educational tutor using agents-sdk."""
import asyncio
from pathlib import Path
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from .config import settings
from .exceptions import EmptyAIResponse, AIServiceError
from ..tools.textbook_search_tool import textbook_search_tool


class AITutor:
    """Gemini-powered AI tutor initialized with Global Constitution."""

    def __init__(self):
        """Initialize AI tutor with agents-sdk and Gemini."""
        # Validate API key is set
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is required")

        # Create Gemini-configured AsyncOpenAI client
        gemini_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url,
        )

        # Wrap in OpenAIChatCompletionsModel
        model = OpenAIChatCompletionsModel(
            model=settings.gemini_model,
            openai_client=gemini_client
        )

        # Load constitution and create agent with instructions
        constitution = self._load_constitution()

        # Get the tool definition for textbook search
        textbook_search_def = textbook_search_tool.get_tool_definition()

        self.agent = Agent(
            name="Educational Tutor",
            instructions=constitution,  # System prompt
            model=model,
            tools=[textbook_search_def]  # Add the textbook search tool
        )

    def _load_constitution(self) -> str:
        """Load Global Constitution from filesystem.

        Returns:
            str: Constitution content

        Raises:
            RuntimeError: If constitution file cannot be loaded
        """
        try:
            constitution_path = Path(settings.constitution_path)
            if not constitution_path.exists():
                raise FileNotFoundError(f"Constitution not found: {constitution_path}")
            return constitution_path.read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to load Global Constitution: {e}")

    async def generate_response(self, message: str) -> str:
        """Generate educational response using agents-sdk Runner.

        Args:
            message: Student question

        Returns:
            str: AI-generated educational response

        Raises:
            EmptyAIResponse: If AI service returns empty/unusable response
            AIServiceError: If AI service fails or times out
        """
        try:
            # Run agent with timeout and tool mapping
            result = await asyncio.wait_for(
                Runner.run(
                    starting_agent=self.agent,
                    input=message,
                    tool_mapping={
                        "search_textbook": self._handle_search_textbook
                    }
                ),
                timeout=settings.request_timeout_seconds
            )

            # Extract and validate response
            content = result.final_output
            if not content or not content.strip():
                raise EmptyAIResponse("AI service returned empty response")

            return content.strip()

        except asyncio.TimeoutError:
            raise AIServiceError(f"Request timed out after {settings.request_timeout_seconds} seconds")
        except EmptyAIResponse:
            # Re-raise EmptyAIResponse as-is
            raise
        except Exception as e:
            # Catch all other exceptions and wrap in AIServiceError
            raise AIServiceError(f"AI service error: {str(e)}")

    async def _handle_search_textbook(self, query: str) -> str:
        """
        Handle the search_textbook tool call by searching the textbook content.

        Args:
            query: The search query about textbook content

        Returns:
            str: Formatted results or error message
        """
        try:
            results = await textbook_search_tool.search_textbook(query)

            # Format results for the agent
            if results and isinstance(results, list) and len(results) > 0:
                formatted_results = []
                for result in results:
                    if "error" in result:
                        return f"Error: {result['error']}"

                    formatted_result = (
                        f"Source: {result.get('source_file', 'Unknown')}\n"
                        f"Chapter: {result.get('chapter_title', 'Unknown')}\n"
                        f"Content: {result.get('content', '')}\n"
                        f"Relevance Score: {result.get('score', 0.0):.3f}\n"
                        f"---\n"
                    )
                    formatted_results.append(formatted_result)

                return "Found the following textbook content:\n\n" + "\n".join(formatted_results)
            else:
                return "No relevant textbook content found for the query."

        except Exception as e:
            return f"Error searching textbook: {str(e)}"


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