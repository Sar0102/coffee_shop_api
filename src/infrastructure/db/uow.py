from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.uow import IUnitOfWork
from src.infrastructure.db.base import async_session_maker
from src.infrastructure.db.repositories.user_repo import UserRepository
from src.infrastructure.db.repositories.verification_repository import VerificationRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session: AsyncSession | None = None
        self.users: UserRepository | None = None
        self.verifications: VerificationRepository | None = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = async_session_maker()
        self.users = UserRepository(self.session)
        self.verifications = VerificationRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
