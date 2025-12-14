"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """Student question input model."""
    message: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="Student question (3-10,000 characters)"
    )

    @field_validator('message')
    @classmethod
    def validate_message_not_whitespace(cls, v: str) -> str:
        """Ensure message is not only whitespace."""
        if not v.strip():
            raise ValueError('Message cannot be only whitespace')
        return v.strip()


class ChatResponse(BaseModel):
    """Successful AI tutor response."""
    response: str = Field(..., description="AI-generated educational response")


class ErrorResponse(BaseModel):
    """Error response for all failure modes."""
    error: str = Field(..., description="Human-readable error message")
