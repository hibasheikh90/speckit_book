"""Registration endpoint implementation."""

import sys
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import traceback

# Add src directory to path for sibling package imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.database import get_db
from auth.models.request import UserRegistrationRequest, UserRegistrationResponse
from auth.services.registration_service import RegistrationService
from auth.exceptions import UserAlreadyExistsException, WeakPasswordException, InvalidEmailException
from auth.middleware.rate_limiter import limiter, get_rate_limit_for_auth

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(get_rate_limit_for_auth())  # Apply rate limiting (5 attempts per 15 minutes)
def register_user(
    user_request: UserRegistrationRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Register a new user with email and password.
    """
    try:
        user, message = RegistrationService.register_user(
            db=db,
            email=user_request.email,
            password=user_request.password
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
        # Log the full error for debugging
        print(f"ERROR in registration endpoint: {type(e).__name__}: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {type(e).__name__}: {str(e)}"
        )