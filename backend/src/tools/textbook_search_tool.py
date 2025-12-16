from typing import Dict, Any, List
from src.services.rag_service import RAGService
import asyncio


class TextbookSearchTool:
    """
    OpenAI-compatible tool for searching textbook content using RAG.
    This tool allows the OpenAI Agent to retrieve relevant textbook content
    before answering student questions.
    """

    def __init__(self):
        self.rag_service = RAGService()

    def get_tool_definition(self):
        """
        Return the OpenAI tool definition for this search tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "search_textbook",
                "description": "Search the Physical AI & Humanoid Robotics textbook for relevant content to answer student questions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query about textbook content (e.g., 'ROS 2 nodes', 'Gazebo simulation', 'kinematics')"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    async def search_textbook(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the textbook content for relevant information.

        Args:
            query: The search query about textbook content

        Returns:
            List of relevant textbook content chunks with metadata
        """
        try:
            results = await self.rag_service.search_textbook(query)
            return results
        except Exception as e:
            # Return an error result instead of raising to maintain compatibility with OpenAI tools
            return [{
                "error": f"Failed to search textbook: {str(e)}",
                "content": "No textbook content found due to an error.",
                "source_file": "",
                "chapter_title": "",
                "score": 0.0
            }]

    async def close(self):
        """Close the RAG service connections."""
        await self.rag_service.close()


# Global instance for use in the application
textbook_search_tool = TextbookSearchTool()