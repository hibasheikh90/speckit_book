from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    # Authentication Settings
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    neon_database_url: str = ""

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_chunks"

    # Google Gemini API Configuration
    gemini_api_key: str
    gemini_model_name: str = "models/text-embedding-004"  # Default embedding model
    gemini_model: str = "gemini-2.0-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

    # Application Configuration
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = False
    constitution_path: Path = Path("../.specify/memory/constitution.md")
    request_timeout_seconds: int = 30

    # JWT Configuration
    jwt_access_token_expire_minutes: int = 1440  # 24 hours

    # Rate Limit Configuration
    rate_limit_per_minute: int = 10

    # RAG Configuration
    max_search_results: int = 5
    chunk_token_limit: int = 150
    embedding_dimension: int = 768  # Default for Gemini embedding model

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create a singleton instance
settings = Settings()


def validate_auth_settings():
    """Validate that all required authentication settings are properly configured."""
    errors = []

    if not settings.neon_database_url:
        errors.append("NEON_DATABASE_URL environment variable must be set")

    if not settings.jwt_secret_key or settings.jwt_secret_key == "your-super-secret-key-change-in-production":
        errors.append("JWT_SECRET_KEY environment variable must be set to a secure value")

    if errors:
        return False, "; ".join(errors)

    return True, "All authentication settings are valid"