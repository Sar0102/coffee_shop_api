from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.value_objects.email_address import EmailAddress
from src.domain.value_objects.user_role import UserRole


@dataclass(slots=True)
class UserEntity(BaseEntity):
    """
    Domain User entity (pure business object).

    Attributes:
        email: Email address (value object).
        password: Hashed password (algorithm hidden behind PasswordHasher port).
        first_name: Optional first name.
        last_name: Optional last name.
        is_verified: Whether the user has completed verification.
        role: User role
    """

    email: EmailAddress
    password: str
    first_name: str | None
    last_name: str | None
    is_verified: bool
    role: UserRole

    def verify(self) -> None:
        """Mark user as verified."""
        self.is_verified = True

    def promote_to_admin(self) -> None:
        """Promote user to ADMIN role."""
        self.role = UserRole.ADMIN

    def demote_to_user(self) -> None:
        """Demote user to USER role."""
        self.role = UserRole.USER
