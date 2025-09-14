from types import TracebackType
from typing import Protocol

from src.domain.interfaces.user_repo import IUserRepository
from src.domain.interfaces.verification_repo import IVerificationRepository


class IUnitOfWork(Protocol):
    """
    Abstraction for transaction boundary.
    """

    users: IUserRepository
    verifications: IVerificationRepository

    async def __aenter__(self) -> "IUnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
