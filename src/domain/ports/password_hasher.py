from typing import Protocol


class PasswordHasher(Protocol):
    """
    Port for password hashing.
    """

    def hash(self, raw: str) -> str:
        """Return a secure hash for the provided raw password."""

    def verify(self, raw: str, hashed: str) -> bool:
        """Return True if raw password matches the given hash."""
