"""
Security utilities for encryption and token management
"""
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
from app.config import settings


class EncryptionService:
    """Service for encrypting and decrypting sensitive data like OAuth tokens"""

    def __init__(self):
        # Derive encryption key from master key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'financial_advisor_agent_salt',  # In production, use per-user salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(settings.ENCRYPTION_KEY.encode()))
        self.cipher = Fernet(key)

    def encrypt_token(self, token: dict) -> str:
        """
        Encrypt OAuth token dictionary

        Args:
            token: OAuth token dictionary

        Returns:
            Encrypted token as string
        """
        token_json = json.dumps(token)
        encrypted = self.cipher.encrypt(token_json.encode())
        return encrypted.decode()

    def decrypt_token(self, encrypted_token: str) -> dict:
        """
        Decrypt OAuth token

        Args:
            encrypted_token: Encrypted token string

        Returns:
            Decrypted token dictionary
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_token.encode())
            return json.loads(decrypted.decode())
        except Exception as e:
            raise ValueError(f"Failed to decrypt token: {str(e)}")


# Create singleton instance
encryption_service = EncryptionService()
