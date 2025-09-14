from collections.abc import Sequence
from typing import Protocol

from src.domain.entities.user import UserEntity
from src.domain.value_objects.email_address import EmailAddress


class IUserRepository(Protocol):
    """
    Repository interface for User entity (port for persistence).
    Application services depend on this, not on concrete ORMs.
    """

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        """Return user by id or None if not found."""

    async def get_by_email(self, email: EmailAddress) -> UserEntity | None:
        """Return user by email or None if not found."""

    async def list_paginated(self, offset: int, limit: int) -> Sequence[UserEntity]:
        """Return a paginated list of users."""

    async def add(self, data: dict) -> UserEntity:
        """Persist a new user and return it with assigned identity."""

    async def update(self, user_id: int, data: dict) -> UserEntity:
        """Persist changes to an existing user and return it."""

    async def delete(self, user_id: int) -> None:
        """Delete user by id (idempotent)."""
