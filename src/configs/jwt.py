from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    """
    JWT configuration settings.
    """

    secret: str = "super-secret"  #  override in .env
    algorithm: str = "HS256"
    access_ttl_min: int = 15  # access token lifetime in minutes
    refresh_ttl_days: int = 7  # refresh token lifetime in days

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JWT_",
        extra="ignore",
    )


jwt_settings = JWTSettings()
