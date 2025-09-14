from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.value_objects.verification_channel import VerificationChannel


@dataclass(slots=True)
class VerificationEntity:
    """
    Domain verification artifact (code or link bound to a user).

    Attributes:
        user_id: Target user id.
        code: Opaque verification code.
        channel: 'email' or 'sms' (keep domain simple).
        created_at: Creation time in UTC.
        expires_at: Expiration time in UTC.
        consumed_at: When the code was consumed (if any).
    """

    user_id: int
    code: str
    channel: VerificationChannel
    created_at: datetime
    expires_at: datetime
    consumed_at: datetime | None = None

    def is_expired(self, now: datetime) -> bool:
        """Return True if the verification code is expired at the given moment."""
        return now >= self.expires_at

    def is_consumed(self) -> bool:
        """Return True if the code has already been consumed."""
        return self.consumed_at is not None

    def consume(self, now: datetime) -> None:
        """Mark this verification as consumed at the given time."""
        self.consumed_at = now

    @staticmethod
    def new(user_id: int, code: str, channel: VerificationChannel, ttl_minutes: int, now: datetime) -> "VerificationEntity":
        """
        Factory method to create a new verification with TTL.

        Args:
            user_id: Target user id.
            code: Opaque code.
            channel: 'email' | 'sms'.
            ttl_minutes: Time to live in minutes.
            now: Current UTC time.

        Returns:
            VerificationEntity: New domain verification object.
        """
        return VerificationEntity(
            user_id=user_id,
            code=code,
            channel=channel,
            created_at=now,
            expires_at=now + timedelta(minutes=ttl_minutes),
            consumed_at=None,
        )
