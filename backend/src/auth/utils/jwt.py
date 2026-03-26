"""JWT utility functions for creation and validation."""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt

# Add src directory to path for sibling package imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token with the provided data.

    Args:
        data: Dictionary containing the claims to include in the token
        expires_delta: Optional timedelta for custom expiration (defaults to 24 hours)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    # Set expiration time (24 hours in seconds)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=24 * 60 * 60)  # 24 hours

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    # Encode the token
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return its payload if valid.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            return None

        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidSignatureError:
        # Invalid signature
        print(f"DEBUG: Invalid signature - token may have been signed with different key")
        return None
    except Exception as e:
        # Invalid token or other error
        print(f"DEBUG: Token validation error: {type(e).__name__}: {str(e)}")
        return None


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token without verification (use only for non-sensitive operations).

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload if format is valid, None if format is invalid
    """
    try:
        # This does NOT verify the signature - only use for non-sensitive operations
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.DecodeError:
        return None