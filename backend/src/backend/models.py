"""Pydantic models for the chat API."""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="Student's learning question (3-10000 characters)"
    )

    @validator('message')
    def message_not_empty_whitespace(cls, v):
        """Validate that message is not only whitespace."""
        if not v.strip():
            raise ValueError('Message cannot be only whitespace')
        return v.strip()


class ChatResponse(BaseModel):
    """Response model for successful chat requests."""

    response: str = Field(
        ...,
        description="Educational response from the AI tutor"
    )
    agent_name: str = Field(
        default="Educational Tutor",
        description="Name of the agent that generated the response"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the response was generated (UTC)"
    )


class ErrorResponse(BaseModel):
    """Response model for error cases."""

    detail: str = Field(
        ...,
        description="Error message explaining what went wrong"
    )