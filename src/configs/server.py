from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SERVER_",
        extra="ignore",
    )

    HOST: str = "localhost"
    PORT: int = 8000


server_settings = Settings()
