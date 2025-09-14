from typing import Protocol

from src.domain.entities.verification import VerificationEntity


class IVerificationRepository(Protocol):
    """
    Repository interface for Verification artifacts.
    """

    async def add(self, verification: VerificationEntity) -> VerificationEntity:
        """Persist a new verification and return it."""

    async def get_latest_for_user(self, user_id: int) -> VerificationEntity | None:
        """Return the latest verification for a user or None."""

    async def mark_consumed(self, verification: VerificationEntity) -> None:
        """Persist consumption moment (idempotent)."""
