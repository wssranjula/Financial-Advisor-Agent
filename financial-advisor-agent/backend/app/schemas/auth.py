"""
Authentication schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class OAuthCallbackRequest(BaseModel):
    """Schema for OAuth callback request"""
    code: str
    state: Optional[str] = None


class OAuthURLResponse(BaseModel):
    """Schema for OAuth URL response"""
    authorization_url: str
    state: str


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    has_google_auth: bool
    has_hubspot_auth: bool

    class Config:
        from_attributes = True


class AuthStatusResponse(BaseModel):
    """Schema for authentication status response"""
    authenticated: bool
    user: Optional[UserResponse] = None
    google_connected: bool
    hubspot_connected: bool
