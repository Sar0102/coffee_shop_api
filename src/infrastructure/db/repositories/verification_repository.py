from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.verification import VerificationEntity
from src.domain.interfaces.verification_repo import IVerificationRepository
from src.infrastructure.db.models.verification import VerificationORM


class VerificationRepository(IVerificationRepository):
    """
    SQLAlchemy-based repository for Verification domain artifacts.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, verification: VerificationEntity) -> VerificationEntity:
        """Persist a new verification and return it."""
        orm = self._to_orm(verification)
        self.session.add(orm)
        await self.session.flush()
        return self._to_domain(orm)

    async def get_latest_for_user(self, user_id: int) -> VerificationEntity | None:
        """Return latest verification for a user or None."""
        stmt = (
            select(VerificationORM)
            .where(VerificationORM.user_id == user_id)
            .order_by(VerificationORM.created_at.desc())
            .limit(1)
        )
        orm = (await self.session.execute(stmt)).scalar_one_or_none()
        return self._to_domain(orm)

    async def mark_consumed(self, verification: VerificationEntity) -> None:
        """Mark a verification as consumed (idempotent)."""
        await self.session.execute(
            update(VerificationORM)
            .where(
                VerificationORM.user_id == verification.user_id,
                VerificationORM.code == verification.code,
            )
            .values(consumed_at=verification.consumed_at)
        )

    # ---------- mapping helpers ----------

    @staticmethod
    def _to_domain(orm: VerificationORM | None) -> VerificationEntity | None:
        """Convert ORM model into domain object."""
        if orm is None:
            return None
        return VerificationEntity(
            user_id=orm.user_id,
            code=orm.code,
            channel=orm.channel,
            created_at=orm.created_at,
            expires_at=orm.expires_at,
            consumed_at=orm.consumed_at,
        )

    @staticmethod
    def _to_orm(v: VerificationEntity) -> VerificationORM:
        """Convert domain object into ORM model."""
        return VerificationORM(
            user_id=v.user_id,
            code=v.code,
            channel=v.channel,
            created_at=v.created_at,
            expires_at=v.expires_at,
            consumed_at=v.consumed_at,
        )
