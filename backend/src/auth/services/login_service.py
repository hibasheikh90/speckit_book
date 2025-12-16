"""Login service for user authentication operations."""

from datetime import timedelta
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from ..models.user import User
from .user_service import UserService
from ..utils.password import verify_password
from ..utils.jwt import create_access_token
from ..exceptions import InvalidCredentialsException
from ...config.settings import settings


class LoginService:
    """Service class for user login and authentication operations."""

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Tuple[Optional[User], Optional[str], str]:
        """
        Authenticate a user with email and password.

        Args:
            db: Database session
            email: User's email address
            password: User's password

        Returns:
            Tuple of (User object if authenticated, access token if successful, message string)
        """
        # Get user by email
        user = UserService.get_user_by_email(db, email)
        if not user:
            raise InvalidCredentialsException("Incorrect email or password")

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException("Incorrect email or password")

        # Create access token
        token_data = {"sub": str(user.id)}
        expire = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        access_token = create_access_token(data=token_data, expires_delta=expire)

        return user, access_token, "Login successful"