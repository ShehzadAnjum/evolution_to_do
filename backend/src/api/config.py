"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql://placeholder:placeholder@localhost/todo"

    # Auth
    better_auth_secret: str = "development-secret-key-at-least-32-chars"
    better_auth_url: str = "http://localhost:8000"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # OpenAI (Phase III - AI Chatbot)
    openai_api_key: str = ""

    # Dapr (Phase V - Event-driven)
    dapr_enabled: bool = False
    dapr_http_port: str = "3500"

    # MQTT (Phase IV - IoT Device Control)
    mqtt_broker: str = ""
    mqtt_port: int = 8883
    mqtt_username: str = ""
    mqtt_password: str = ""
    mqtt_enabled: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    # Log the secret (first 20 chars only) for debugging
    secret_preview = settings.better_auth_secret[:20] if len(settings.better_auth_secret) > 20 else settings.better_auth_secret
    print(f"✅ Loaded settings - BETTER_AUTH_SECRET: {secret_preview}... (length: {len(settings.better_auth_secret)})")
    return settings
