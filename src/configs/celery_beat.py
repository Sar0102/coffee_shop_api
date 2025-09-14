from pydantic_settings import BaseSettings, SettingsConfigDict


class CeleryBeatSettings(BaseSettings):
    """
    Celery Beat configuration settings.
    """

    UNVERIFIED_TTL_DAYS: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CELERY_BEAT_",
        extra="ignore",
    )


celery_beat_settings = CeleryBeatSettings()
