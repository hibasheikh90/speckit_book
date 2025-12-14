"""FastAPI application for Physical AI Textbook chat service."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from backend.models import ChatRequest, ChatResponse, ErrorResponse
from backend.agent import initialize_agent, get_agent, AITutor
from backend.config import settings
from backend.exceptions import RateLimitExceeded, EmptyAIResponse, AIServiceError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize AI agent on startup, cleanup on shutdown."""
    # Startup
    initialize_agent()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(
    title="Physical AI Textbook Chat Service",
    description="AI tutor backend for Physical AI & Humanoid Robotics textbook",
    version="0.1.0",
    lifespan=lifespan,
)


@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Service error"},
    },
    summary="Submit question to AI tutor",
    description="Submit a student question and receive an educational response guided by the Global Constitution."
)
async def chat(
    chat_request: ChatRequest,
    request: Request,
    agent: AITutor = Depends(get_agent),
):
    """Submit a question to the AI tutor and receive an educational response.

    Timeout: 30 seconds maximum.

    Args:
        chat_request: Student question (3-10,000 characters)
        request: FastAPI request object
        agent: Injected AITutor instance

    Returns:
        ChatResponse: AI-generated educational response

    Raises:
        HTTPException: 500 if AI service fails, times out, or returns empty response
    """
    # Generate AI response
    try:
        response_text = await agent.generate_response(chat_request.message)
        return ChatResponse(response=response_text)

    except EmptyAIResponse:
        # ADR-007: Specific error message for empty responses
        raise HTTPException(
            status_code=500,
            detail="Unable to generate a response. Please try rephrasing your question or try again later."
        )

    except AIServiceError as e:
        # Check if it's a timeout error
        if "timed out" in str(e).lower():
            raise HTTPException(
                status_code=500,
                detail="The request took too long to process. Please try again later."
            )
        # Generic AI service error
        raise HTTPException(
            status_code=500,
            detail="The AI tutor service is temporarily unavailable. Please try again later."
        )


@app.get(
    "/health",
    summary="Health check",
    description="Check if the service is healthy and constitution is loaded."
)
async def health_check(agent: AITutor = Depends(get_agent)):
    """Health check endpoint.

    Returns:
        dict: Service status and constitution loaded flag
    """
    return {
        "status": "healthy",
        "constitution_loaded": agent.system_prompt is not None and len(agent.system_prompt) > 0,
    }
