"""Application configuration using pydantic-settings."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Gemini API Configuration
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/openai/",
        alias="GEMINI_BASE_URL"
    )
    gemini_model: str = Field(default="gemini-2.0-flash", alias="GEMINI_MODEL")

    # Application Configuration
    constitution_path: Path = Field(
        default=Path(__file__).parent.parent.parent.parent / ".specify" / "memory" / "constitution.md",
        alias="CONSTITUTION_PATH"
    )
    request_timeout: int = Field(default=30, alias="REQUEST_TIMEOUT_SECONDS")
    rate_limit_requests: int = Field(default=10, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")

    # Server Configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global settings instance
settings = Settings()
