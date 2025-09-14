from typing import Protocol

from src.domain.value_objects.user_role import UserRole


class Authorizer(Protocol):
    """
    Port for access control checks.
    """

    def require_role(self, *roles: UserRole) -> None:
        """Raise if the caller does not have one of the required roles."""
