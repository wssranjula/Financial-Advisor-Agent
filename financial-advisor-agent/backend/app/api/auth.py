"""
Authentication API endpoints for OAuth
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user
from app.integrations.google_auth import google_oauth_service
from app.integrations.hubspot_auth import hubspot_oauth_service
from app.security import encryption_service
from app.models import User
from app.schemas.auth import (
    OAuthURLResponse,
    AuthStatusResponse,
    UserResponse
)
from typing import Optional

router = APIRouter()


# ==================== Google OAuth ====================

@router.get("/google/login", response_model=OAuthURLResponse)
async def google_login(state: Optional[str] = None):
    """
    Initiate Google OAuth flow

    Args:
        state: Optional state parameter for CSRF protection

    Returns:
        Authorization URL and state
    """
    authorization_url, state = google_oauth_service.get_authorization_url(state)

    return OAuthURLResponse(
        authorization_url=authorization_url,
        state=state
    )


@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback

    Args:
        code: Authorization code from Google
        state: State parameter for CSRF protection
        db: Database session

    Returns:
        Success message and user info
    """
    try:
        # Exchange code for token
        token_dict = google_oauth_service.exchange_code_for_token(code)

        # Get user info from Google
        credentials = google_oauth_service.get_credentials(token_dict)

        # For MVP, extract email from credentials
        # In production, make API call to get user info
        user_email = "user@example.com"  # TODO: Get from Google People API

        # Find or create user
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email, is_active=True)
            db.add(user)

        # Encrypt and store token
        encrypted_token = encryption_service.encrypt_token(token_dict)
        user.google_token = encrypted_token

        db.commit()

        return {
            "message": "Google OAuth successful",
            "user_id": str(user.id),
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth failed: {str(e)}")


# ==================== HubSpot OAuth ====================

@router.get("/hubspot/login", response_model=OAuthURLResponse)
async def hubspot_login(state: Optional[str] = None):
    """
    Initiate HubSpot OAuth flow

    Args:
        state: Optional state parameter for CSRF protection

    Returns:
        Authorization URL and state
    """
    authorization_url, state = hubspot_oauth_service.get_authorization_url(state)

    return OAuthURLResponse(
        authorization_url=authorization_url,
        state=state
    )


@router.get("/hubspot/callback")
async def hubspot_callback(
    code: str = Query(...),
    state: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Handle HubSpot OAuth callback

    Args:
        code: Authorization code from HubSpot
        state: State parameter for CSRF protection
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    try:
        # Exchange code for token
        token_dict = hubspot_oauth_service.exchange_code_for_token(code)

        # Encrypt and store token
        encrypted_token = encryption_service.encrypt_token(token_dict)
        current_user.hubspot_token = encrypted_token

        db.commit()

        return {
            "message": "HubSpot OAuth successful",
            "user_id": str(current_user.id)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth failed: {str(e)}")


# ==================== Status ====================

@router.get("/status", response_model=AuthStatusResponse)
async def auth_status(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get authentication status for current user

    Args:
        current_user: Current authenticated user

    Returns:
        Authentication status including OAuth connections
    """
    user_response = UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        has_google_auth=bool(current_user.google_token),
        has_hubspot_auth=bool(current_user.hubspot_token)
    )

    return AuthStatusResponse(
        authenticated=True,
        user=user_response,
        google_connected=bool(current_user.google_token),
        hubspot_connected=bool(current_user.hubspot_token)
    )
