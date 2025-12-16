"""Custom exception classes for the AI tutor service."""


class EmptyAIResponse(Exception):
    """Raised when the AI service returns an empty or unusable response."""

    def __init__(self, message: str = "AI service returned empty response"):
        self.message = message
        super().__init__(self.message)


class AIServiceError(Exception):
    """Raised when the AI service encounters an error."""

    def __init__(self, message: str = "AI service error occurred"):
        self.message = message
        super().__init__(self.message)