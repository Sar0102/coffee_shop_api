from celery import Celery
from celery.schedules import crontab

from src.configs.redis import redis_settings

celery = Celery(
    "coffee_users",
    broker=redis_settings.DSN(0),
    backend=redis_settings.DSN(1),
    include=["src.infrastructure.tasks.cleanup"],
)
celery.conf.update(
    beat_schedule={
        "cleanup-unverified-every-day": {
            "task": "src.infrastructure.tasks.cleanup.cleanup_unverified",
            "schedule": crontab(hour=0, minute=0),  # every day at midnight
        }
    },
)
