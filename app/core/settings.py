from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Required: DATABASE_URL must be set in .env or environment.
    See .env.example for configuration template.
    """

    # Application settings
    service_name: str = "core-user-service"
    service_version: str = "1.0.0"
    env: str = "dev"
    port: int = 8080
    log_level: str = "info"
    cors_origins: list[AnyHttpUrl] | list[str] = []

    # Database settings
    database_url: str = ""  # Loaded from .env, empty default for validation
    database_echo: bool = False  # Set to True for SQL query logging

    # Security settings (RS256)
    rsa_private_key: str = ""  # PEM-encoded RSA private key (env: RSA_PRIVATE_KEY)
    jwt_algorithm: str = "RS256"
    jwt_kid: str = "visiobook-key-1"
    jwt_issuer: str = "core-user-service"
    access_token_expire_minutes: int = 30

    model_config = {"env_file": ".env", "case_sensitive": False, "extra": "ignore"}


settings = Settings()
