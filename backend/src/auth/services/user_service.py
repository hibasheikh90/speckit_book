"""User service for database operations."""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from ..utils.password import hash_password
import uuid


class UserService:
    """Service class for user-related database operations."""

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by their email address."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get a user by their ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, email: str, password: str) -> Optional[User]:
        """Create a new user with hashed password."""
        hashed_pwd = hash_password(password)
        user_id = str(uuid.uuid4())  # Generate UUID string
        db_user = User(id=user_id, email=email, hashed_password=hashed_pwd)

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            # Email already exists
            db.rollback()
            return None

    @staticmethod
    def update_user_password(db: Session, user_id: str, new_password: str) -> bool:
        """Update a user's password."""
        hashed_pwd = hash_password(new_password)
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return False

        user.hashed_password = hashed_pwd
        db.commit()
        return True

    @staticmethod
    def delete_user(db: Session, user_id: str) -> bool:
        """Delete a user by ID."""
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return False

        db.delete(user)
        db.commit()
        return True