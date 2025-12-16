"""Database configuration for database connection."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings
import os

# Get database URL from settings
DATABASE_URL = settings.neon_database_url

# For SQLite, we need to handle the URL format properly
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, we don't use connection pooling
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # Create engine with connection pooling settings for other databases
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,  # Connection pool size
        max_overflow=20,  # Maximum overflow connections
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections after 5 minutes
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()