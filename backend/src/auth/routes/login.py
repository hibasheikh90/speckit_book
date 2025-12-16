"""Login endpoint implementation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...config.database import get_db
from ..models.request import UserLoginRequest, UserLoginResponse
from ..services.login_service import LoginService
from ..exceptions import InvalidCredentialsException
from ..middleware.rate_limiter import limiter, get_rate_limit_for_auth

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=UserLoginResponse)
@limiter.limit(get_rate_limit_for_auth())  # Apply rate limiting (5 attempts per 15 minutes)
def login_user(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password, returning a JWT access token.
    """
    try:
        user, access_token, message = LoginService.authenticate_user(
            db=db,
            email=request.email,
            password=request.password
        )

        return UserLoginResponse(
            access_token=access_token,
            user_id=str(user.id),
            token_type="bearer"
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )