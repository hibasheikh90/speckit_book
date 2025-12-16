"""Password utility functions for hashing and validation."""

from passlib.context import CryptContext
import re
from typing import Tuple

# Create password context for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with configured work factor."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength according to requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"

    return True, "Password is valid"


def validate_email_format(email: str) -> Tuple[bool, str]:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not email:
        return False, "Email is required"

    if len(email) < 5:
        return False, "Email is too short"

    if len(email) > 255:
        return False, "Email is too long"

    if re.match(pattern, email):
        return True, "Email format is valid"
    else:
        return False, "Invalid email format"