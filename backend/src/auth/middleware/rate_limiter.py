"""Rate limiting configuration for authentication endpoints."""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, HTTPException


# Create a limiter instance
limiter = Limiter(key_func=get_remote_address)

# Define the rate limit for authentication endpoints (5 attempts per 15 minutes as specified)
AUTH_RATE_LIMIT = "5/15minutes"


def add_rate_limiting_to_app(app: FastAPI):
    """Add rate limiting to the FastAPI application."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def get_rate_limit_for_auth():
    """Get the configured rate limit for authentication endpoints."""
    return AUTH_RATE_LIMIT