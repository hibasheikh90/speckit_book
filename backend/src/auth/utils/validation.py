"""Validation utility functions for authentication."""

from typing import Tuple
import re


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