from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    service_name: str = "core-user-service"
    service_version: str = "1.0.0"
    env: str = "dev"
    port: int = 8080
    log_level: str = "info"
    cors_origins: list[AnyHttpUrl] | list[str] = []

    # Database settings
    database_url: str = "postgresql://visiobook_user:visiobook_pass@localhost:5432/visiobook_users"
    database_echo: bool = False  # Set to True for SQL query logging

    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = {"env_file": ".env", "case_sensitive": False, "extra": "ignore"}


settings = Settings()
