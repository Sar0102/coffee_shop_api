from typing import Protocol


class TokenProvider(Protocol):
    """
    Port for issuing and decoding tokens (e.g., JWT).
    """

    def issue_access(self, subject: str, claims: dict) -> str:
        """Issue an access token for the given subject and claims."""

    def issue_refresh(self, subject: str) -> str:
        """Issue a refresh token for the given subject."""

    def decode(self, token: str) -> dict:
        """Decode token and return claims; raise on invalid tokens."""
