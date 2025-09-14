import asyncio
import datetime as dt
from typing import Final

from celery.utils.log import get_task_logger
from sqlalchemy import delete, and_

from src.configs.celery_beat import celery_beat_settings
from src.infrastructure.db.base import async_session_maker
from src.infrastructure.db.models.user import UserORM
from src.infrastructure.tasks.celery_app import celery

log = get_task_logger(__name__)
UNVERIFIED_TTL_DAYS: Final[int] = celery_beat_settings.UNVERIFIED_TTL_DAYS


@celery.task(name="src.infrastructure.tasks.cleanup.cleanup_unverified")
def cleanup_unverified() -> int:
    """
    Delete users who are not verified within UNVERIFIED_TTL_DAYS.
    Synchronous Celery task that runs async DB code via asyncio.run.
    Returns the number of deleted users.
    """

    async def _run() -> int:
        cutoff = dt.datetime.now() - dt.timedelta(days=UNVERIFIED_TTL_DAYS)
        async with async_session_maker() as s:
            result = await s.execute(
                delete(UserORM)
                .where(and_(UserORM.is_verified.is_(False), UserORM.created_at < cutoff))
                .returning(UserORM.id)
            )
            ids = result.scalars().all()
            if ids:
                await s.commit()
                log.info("cleanup_unverified: deleted %d users (ids=%s)", len(ids), ids)
            else:
                log.info("cleanup_unverified: nothing to delete")
            return len(ids)

    return asyncio.run(_run())
