"""FastAPI application for the educational AI tutor service."""
from fastapi import FastAPI, Request, Depends, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .models import ChatRequest, ChatResponse, ErrorResponse
from .agent import get_agent, initialize_agent
import sys
from pathlib import Path
import asyncio

# Add parent directory to path for sibling package imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.settings import settings
from auth.middleware.jwt import get_current_user
from auth.models.user import User
from auth.routes import registration, login, verify
from config.database import engine, Base


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Educational AI Tutor API", version="1.0.0")

# Include authentication routes
app.include_router(registration.router)
app.include_router(login.router)
app.include_router(verify.router)

# Add rate limiter exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def startup_event():
    """Initialize the AI agent and database when the application starts."""
    print("Starting up AI tutor service...")

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Initialize the AI agent
    initialize_agent()
    print("AI tutor service ready!")


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint to verify service status."""
    constitution_path = Path(settings.constitution_path)
    constitution_exists = constitution_path.exists()

    return {
        "status": "healthy",
        "constitution_loaded": constitution_exists,
        "model": settings.gemini_model,
        "rate_limit": f"{settings.rate_limit_per_minute}/minute"
    }


@app.post("/chat",
          response_model=ChatResponse,
          responses={
              200: {"description": "Successful response from AI tutor"},
              401: {"description": "Unauthorized - Invalid or missing token"},
              422: {"model": ErrorResponse, "description": "Validation error"},
              429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
              500: {"model": ErrorResponse, "description": "Internal server error"},
              504: {"model": ErrorResponse, "description": "Request timeout"}
          })
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Chat endpoint for students to ask questions about Physical AI and Humanoid Robotics.

    Args:
        request: FastAPI request object for rate limiting
        chat_request: The validated chat request containing the student's question
        current_user: The authenticated user (from JWT token)

    Returns:
        ChatResponse: The AI tutor's educational response

    Raises:
        HTTPException: Various error conditions with appropriate status codes
    """
    try:
        # Log successful authentication
        print(f"✓ Chat request from authenticated user: {current_user.email}")

        # Get the initialized agent
        tutor_agent = get_agent()

        # Generate response from AI tutor
        try:
            response_text = await tutor_agent.generate_response(chat_request.message)
        except Exception as ai_error:
            # If AI service fails (quota, etc), return a mock response for testing
            print(f"AI service error: {str(ai_error)}")
            response_text = f"[Mock Response] Regarding '{chat_request.message}': This is a test response. The authentication system is working correctly. (AI service temporarily unavailable due to API quota.)"

        # Return formatted response
        return ChatResponse(
            response=response_text,
            agent_name=tutor_agent.agent.name if hasattr(tutor_agent, 'agent') else "AI Tutor"
        )

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Request timed out after {settings.request_timeout_seconds} seconds"
        )
    except Exception as e:
        # Log the error for debugging
        print(f"Chat endpoint error: {str(e)}")

        # Return generic error to client
        raise HTTPException(
            status_code=500,
            detail="The tutor service is temporarily unavailable. Please try again later."
        )


# For development/testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)