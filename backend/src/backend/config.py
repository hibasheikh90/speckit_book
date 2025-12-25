"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Authentication Settings
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    neon_database_url: str = ""

    # Cohere API Configuration (OpenAI-compatible endpoint)
    cohere_api_key: str
    cohere_base_url: str = "https://api.cohere.ai/compatibility/v1"
    cohere_model: str = "command-a-03-2025"

    # Qdrant Configuration (for RAG functionality)
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "textbook_chunks"

    # Application Configuration
    constitution_path: Path = Path("../.specify/memory/constitution.md")
    rate_limit_per_minute: int = 10
    request_timeout_seconds: int = 30
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Global settings instance
settings = Settings()