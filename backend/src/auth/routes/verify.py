"""Token verification endpoint implementation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...config.database import get_db
from ..models.request import TokenVerificationRequest, TokenVerificationResponse
from ..middleware.jwt import validate_token_only

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/verify", response_model=TokenVerificationResponse)
def verify_token_endpoint(
    # Note: We're using the middleware to handle token validation automatically
    token_payload: dict = Depends(validate_token_only)
):
    """
    Verify a JWT token and return user information if valid.
    """
    try:
        user_id = token_payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return TokenVerificationResponse(
            user_id=user_id,
            valid=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during token verification"
        )