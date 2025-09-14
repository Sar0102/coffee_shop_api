from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        extra="ignore",
    )

    HOST: str = "localhost"
    PORT: int = 6379
    USER: str = ""
    PASS: str = ""

    def DSN(self, db: int) -> str:  # noqa: N802
        return f"redis://{redis_settings.USER}:{redis_settings.PASS}@{redis_settings.HOST}:{redis_settings.PORT}/{db}"


redis_settings = Settings()
