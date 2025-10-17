"""
HubSpot OAuth integration
"""
import httpx
from typing import Dict, Optional
from urllib.parse import urlencode
from app.config import settings


# HubSpot OAuth scopes
SCOPES = [
    'crm.objects.contacts.read',
    'crm.objects.contacts.write',
    'crm.schemas.contacts.read',
    'crm.objects.companies.read',
    'crm.objects.deals.read',
    'timeline',
]


class HubSpotOAuthService:
    """Service for handling HubSpot OAuth flow"""

    def __init__(self):
        self.client_id = settings.HUBSPOT_CLIENT_ID
        self.client_secret = settings.HUBSPOT_CLIENT_SECRET
        self.redirect_uri = settings.HUBSPOT_REDIRECT_URI
        self.auth_url = "https://app.hubspot.com/oauth/authorize"
        self.token_url = "https://api.hubapi.com/oauth/v1/token"

    def get_authorization_url(self, state: Optional[str] = None) -> tuple[str, str]:
        """
        Generate HubSpot OAuth authorization URL

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Tuple of (authorization_url, state)
        """
        import secrets
        if state is None:
            state = secrets.token_urlsafe(32)

        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(SCOPES),
        }

        if state:
            params['state'] = state

        authorization_url = f"{self.auth_url}?{urlencode(params)}"

        return authorization_url, state

    def exchange_code_for_token(self, code: str) -> Dict:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from OAuth callback

        Returns:
            Token dictionary with access_token, refresh_token, etc.
        """
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }

        with httpx.Client() as client:
            response = client.post(self.token_url, data=data)
            response.raise_for_status()
            token_data = response.json()

        return {
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'expires_in': token_data['expires_in'],
            'token_type': token_data.get('token_type', 'bearer'),
        }

    def refresh_token(self, token_dict: Dict) -> Dict:
        """
        Refresh expired access token

        Args:
            token_dict: Current token dictionary

        Returns:
            Updated token dictionary with new access_token
        """
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': token_dict['refresh_token'],
        }

        with httpx.Client() as client:
            response = client.post(self.token_url, data=data)
            response.raise_for_status()
            token_data = response.json()

        return {
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'expires_in': token_data['expires_in'],
            'token_type': token_data.get('token_type', 'bearer'),
        }

    def get_access_token(self, token_dict: Dict) -> str:
        """
        Get access token from token dictionary

        Args:
            token_dict: Token dictionary

        Returns:
            Access token string
        """
        return token_dict['access_token']


# Create singleton instance
hubspot_oauth_service = HubSpotOAuthService()
