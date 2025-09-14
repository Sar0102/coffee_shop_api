from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DB_",
        extra="ignore",
    )

    USER: str = "postgres"
    PASS: str = "postgres"
    HOST: str = "postgres"
    PORT: int = 5432
    NAME: str = "postgres"

    POOL_SIZE: int = 30
    MAX_POOL_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 30

    @property
    def DSN(self) -> str:  # noqa: N802
        return f"postgresql+asyncpg://{self.USER}:{quote_plus(self.PASS)}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def MIGRATION_DSN(self) -> str:  # noqa: N802
        return f"postgresql+psycopg2://{self.USER}:{quote_plus(self.PASS)}@{self.HOST}:{self.PORT}/{self.NAME}"


settings = DBSettings()
