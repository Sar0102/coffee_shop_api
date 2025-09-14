from collections.abc import Sequence

from src.application.dto.user import UserUpdateDTO
from src.domain.entities.user import UserEntity
from src.domain.exceptions import UserNotFoundError
from src.domain.interfaces.uow import IUnitOfWork


class UserService:
    """
    User read/update/delete use-cases.
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def me(self, user_id: int) -> UserEntity:
        """Return current user entity."""
        async with self.uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise UserNotFoundError("User not found")
            return user

    async def list_users(self, offset: int, limit: int) -> Sequence[UserEntity]:
        """Return a page of users."""
        async with self.uow as uow:
            return await uow.users.list_paginated(offset, limit)

    async def get_user(self, user_id: int) -> UserEntity:
        """Return user by id."""
        async with self.uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise UserNotFoundError("User not found")
            return user

    async def patch_user(self, user_id: int, dto: UserUpdateDTO) -> UserEntity:
        """Partial update of selected user fields."""
        async with self.uow as uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                raise UserNotFoundError("User not found")
            return await uow.users.update(user_id, dto.model_dump(exclude_unset=True))

    async def delete_user(self, user_id: int) -> None:
        """Delete user by id (idempotent)."""
        async with self.uow as uow:
            await uow.users.delete(user_id)
