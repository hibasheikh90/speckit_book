"""Custom exception classes for the chat service."""


class RateLimitExceeded(Exception):
    """Raised when client exceeds rate limit."""
    pass


class EmptyAIResponse(Exception):
    """Raised when AI service returns empty or unusable response."""
    pass


class AIServiceError(Exception):
    """Raised when AI service fails (network, auth, timeout)."""
    pass
