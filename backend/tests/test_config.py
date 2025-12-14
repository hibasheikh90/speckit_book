"""Tests for configuration module."""
import pytest
from pathlib import Path
from backend.config import Settings


def test_config_loads_defaults():
    """Test that Settings loads with default values (API key from environment)."""
    # With API key set via test fixture, this should succeed
    settings = Settings(_env_file=None)
    # Verify the test API key was loaded from environment
    assert settings.gemini_api_key == "test-api-key-for-testing"


def test_config_gemini_base_url_default():
    """Test default Gemini base URL."""
    settings = Settings(
        GEMINI_API_KEY="test-key",
        _env_file=None
    )
    assert settings.gemini_base_url == "https://generativelanguage.googleapis.com/v1beta/openai/"


def test_config_gemini_model_default():
    """Test default Gemini model."""
    settings = Settings(
        GEMINI_API_KEY="test-key",
        _env_file=None
    )
    assert settings.gemini_model == "gemini-2.0-flash"


def test_config_request_timeout_default():
    """Test default request timeout."""
    settings = Settings(
        GEMINI_API_KEY="test-key",
        _env_file=None
    )
    assert settings.request_timeout == 30


def test_config_rate_limit_defaults():
    """Test default rate limit settings."""
    settings = Settings(
        GEMINI_API_KEY="test-key",
        _env_file=None
    )
    assert settings.rate_limit_requests == 10
    assert settings.rate_limit_window == 60


def test_config_constitution_path_exists():
    """Test that constitution path points to valid location."""
    settings = Settings(
        GEMINI_API_KEY="test-key",
        _env_file=None
    )
    # Constitution path should be relative to backend directory
    assert isinstance(settings.constitution_path, Path)
    # Check the path structure (should go up to project root and into .specify/memory)
    assert str(settings.constitution_path).endswith("constitution.md")


def test_config_loads_from_env(monkeypatch):
    """Test that Settings loads values from environment variables."""
    monkeypatch.setenv("GEMINI_API_KEY", "env-test-key")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "45")

    settings = Settings(_env_file=None)

    assert settings.gemini_api_key == "env-test-key"
    assert settings.gemini_model == "test-model"
    assert settings.request_timeout == 45


def test_config_custom_values():
    """Test creating Settings with custom values."""
    settings = Settings(
        GEMINI_API_KEY="custom-key",
        GEMINI_BASE_URL="https://custom.api/",
        GEMINI_MODEL="custom-model",
        REQUEST_TIMEOUT_SECONDS=60,
        RATE_LIMIT_REQUESTS=20,
        RATE_LIMIT_WINDOW_SECONDS=120,
        _env_file=None
    )

    assert settings.gemini_api_key == "custom-key"
    assert settings.gemini_base_url == "https://custom.api/"
    assert settings.gemini_model == "custom-model"
    assert settings.request_timeout == 60
    assert settings.rate_limit_requests == 20
    assert settings.rate_limit_window == 120
