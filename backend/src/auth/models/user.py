"""User model definition for authentication."""

import sys
from pathlib import Path
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Add src directory to path for sibling package imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.database import Base


class User(Base):
    """User model for authentication system."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True)  # Using string to store UUID
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())