"""
API dependencies for authentication and database access
"""
from typing import Generator
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User


def get_db() -> Generator:
    """
    Dependency to get database session

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user

    For MVP, we'll use a simple header-based auth.
    In production, implement JWT tokens.

    Args:
        authorization: Authorization header
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If user not authenticated
    """
    # For MVP: Simple user lookup by email in header
    # In production: Validate JWT token
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Extract user email from header (simplified for MVP)
    # Format: "Bearer user@example.com"
    try:
        user_email = authorization.replace("Bearer ", "")
        user = db.query(User).filter(User.email == user_email).first()

        if not user:
            # Create user if doesn't exist (for MVP)
            user = User(email=user_email, is_active=True)
            db.add(user)
            db.commit()
            db.refresh(user)

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication: {str(e)}"
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user

    Args:
        current_user: Current user from get_current_user

    Returns:
        User: Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
