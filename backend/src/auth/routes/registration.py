"""Registration endpoint implementation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...config.database import get_db
from ..models.request import UserRegistrationRequest, UserRegistrationResponse
from ..services.registration_service import RegistrationService
from ..exceptions import UserAlreadyExistsException, WeakPasswordException, InvalidEmailException
from ..middleware.rate_limiter import limiter, get_rate_limit_for_auth

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(get_rate_limit_for_auth())  # Apply rate limiting (5 attempts per 15 minutes)
def register_user(
    request: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user with email and password.
    """
    try:
        user, message = RegistrationService.register_user(
            db=db,
            email=request.email,
            password=request.password
        )

        return UserRegistrationResponse(
            id=str(user.id),
            email=user.email,
            message=message
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    except WeakPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except InvalidEmailException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )