"""Registration service for user registration operations."""

from typing import Tuple, Optional
from sqlalchemy.orm import Session
from ..models.user import User
from .user_service import UserService
from ..utils.validation import validate_email_format, validate_password_strength
from ..exceptions import UserAlreadyExistsException, WeakPasswordException, InvalidEmailException


class RegistrationService:
    """Service class for user registration operations."""

    @staticmethod
    def register_user(db: Session, email: str, password: str) -> Tuple[Optional[User], str]:
        """
        Register a new user with email and password validation.

        Args:
            db: Database session
            email: User's email address
            password: User's password

        Returns:
            Tuple of (User object if successful, message string)
        """
        # Validate email format
        is_valid_email, email_msg = validate_email_format(email)
        if not is_valid_email:
            raise InvalidEmailException(email_msg)

        # Validate password strength
        is_valid_password, password_msg = validate_password_strength(password)
        if not is_valid_password:
            raise WeakPasswordException(password_msg)

        # Check if user already exists
        existing_user = UserService.get_user_by_email(db, email)
        if existing_user:
            raise UserAlreadyExistsException("Email already registered")

        # Create the new user
        user = UserService.create_user(db, email, password)
        if not user:
            # This could happen due to a race condition where another request
            # created the user between our check and creation
            raise UserAlreadyExistsException("Email already registered")

        return user, "User registered successfully"