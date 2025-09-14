from collections.abc import Sequence

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import UserEntity
from src.domain.interfaces.user_repo import IUserRepository
from src.domain.value_objects.email_address import EmailAddress
from src.domain.value_objects.user_role import UserRole
from src.infrastructure.db.models.user import UserORM


class UserRepository(IUserRepository):
    """
    SQLAlchemy-based repository for User domain entity.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        """Return domain User by id or None if not found."""
        orm = await self.session.get(UserORM, user_id)
        return self._to_domain(orm)

    async def get_by_email(self, email: EmailAddress) -> UserEntity | None:
        """Return domain User by email or None if not found."""
        stmt = select(UserORM).where(UserORM.email == email.as_str())
        orm = (await self.session.execute(stmt)).scalar_one_or_none()
        return self._to_domain(orm)

    async def list_paginated(self, offset: int, limit: int) -> Sequence[UserEntity]:
        """Return a page of domain Users."""
        stmt = select(UserORM).order_by(UserORM.id).offset(offset).limit(limit)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(o) for o in rows]

    async def add(self, data: dict) -> UserEntity:
        """Persist a new domain User and return it with identity assigned."""
        stmt = insert(UserORM).values(**data).returning(UserORM)
        result = await self.session.execute(stmt)
        orm: UserORM = result.scalar_one()
        return self._to_domain(orm)

    async def update(self, user_id: int, data: dict) -> UserEntity | None:
        """Persist changes to existing User and return it."""

        stmt = update(UserORM).where(UserORM.id == user_id).values(**data).returning(UserORM)

        result = await self.session.execute(stmt)
        orm: UserORM | None = result.scalar_one_or_none()
        return self._to_domain(orm)

    async def delete(self, user_id: int) -> None:
        """Delete a user by id (idempotent)."""
        stmt = delete(UserORM).where(UserORM.id == user_id)
        await self.session.execute(stmt)

    # ---------- mapping helpers ----------
    @staticmethod
    def _to_domain(orm: UserORM | None) -> UserEntity | None:
        """Convert ORM model into domain entity."""
        if orm is None:
            return None
        return UserEntity(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            email=EmailAddress(orm.email),
            password=orm.password,
            first_name=orm.first_name,
            last_name=orm.last_name,
            is_verified=orm.is_verified,
            role=UserRole(orm.role),
        )

    @staticmethod
    def _to_orm(ent: UserEntity) -> UserORM:
        """Convert domain entity into ORM model."""
        return UserORM(
            id=ent.id,  # may be None for new entities
            email=ent.email.as_str(),
            password=ent.password,
            first_name=ent.first_name,
            last_name=ent.last_name,
            is_verified=ent.is_verified,
            role=ent.role,
        )
