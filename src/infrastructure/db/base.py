import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.configs.database import settings

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)


class ORMBase(DeclarativeBase):
    """Declarative base for all ORM models."""

    pass


db_settings = settings

engine = create_async_engine(
    url=db_settings.DSN,
    pool_size=db_settings.POOL_SIZE,
    max_overflow=db_settings.MAX_POOL_OVERFLOW,
    pool_timeout=db_settings.POOL_TIMEOUT,
    echo=False,
    logging_name=f"sqlalchemy.engine.Postgres.{db_settings.NAME}",
    pool_logging_name=f"sqlalchemy.pool.Postgres.{db_settings.NAME}",
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
