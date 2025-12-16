"""Request and response models for authentication endpoints."""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class UserRegistrationRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength: minimum 8 chars with uppercase, lowercase, and number."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        return v


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


class UserRegistrationResponse(BaseModel):
    """Response model for user registration."""
    id: str
    email: EmailStr
    message: str = "User registered successfully"


class UserLoginResponse(BaseModel):
    """Response model for user login."""
    access_token: str
    token_type: str = "bearer"
    user_id: str


class TokenVerificationRequest(BaseModel):
    """Request model for token verification."""
    token: str


class TokenVerificationResponse(BaseModel):
    """Response model for token verification."""
    user_id: str
    valid: bool


class TokenPayload(BaseModel):
    """Payload model for JWT token."""
    sub: str
    exp: int
    iat: int