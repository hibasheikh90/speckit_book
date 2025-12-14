"""Tests for Pydantic model validation."""
import pytest
from pydantic import ValidationError
from backend.models import ChatRequest, ChatResponse, ErrorResponse


def test_chat_request_valid_message():
    """Test ChatRequest accepts valid message."""
    request = ChatRequest(message="What is Physical AI?")
    assert request.message == "What is Physical AI?"


def test_chat_request_valid_long_message():
    """Test ChatRequest accepts long message within limit."""
    long_message = "A" * 10000
    request = ChatRequest(message=long_message)
    assert request.message == long_message


def test_chat_request_valid_message_strips_whitespace():
    """Test ChatRequest strips leading/trailing whitespace."""
    request = ChatRequest(message="  What is Physical AI?  ")
    assert request.message == "What is Physical AI?"


def test_chat_request_minimum_length():
    """Test ChatRequest accepts 3-character message (minimum)."""
    request = ChatRequest(message="Hi!")
    assert request.message == "Hi!"


def test_chat_request_message_too_short():
    """Test ChatRequest rejects message shorter than 3 characters."""
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(message="Hi")

    errors = exc_info.value.errors()
    assert any("at least 3 characters" in str(error).lower() for error in errors)


def test_chat_request_message_too_long():
    """Test ChatRequest rejects message longer than 10,000 characters."""
    long_message = "A" * 10001
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(message=long_message)

    errors = exc_info.value.errors()
    assert any("at most 10000 characters" in str(error).lower() for error in errors)


def test_chat_request_whitespace_only():
    """Test ChatRequest rejects whitespace-only message."""
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(message="   ")

    errors = exc_info.value.errors()
    assert any("cannot be only whitespace" in str(error).lower() for error in errors)


def test_chat_request_empty_string():
    """Test ChatRequest rejects empty string."""
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest(message="")

    # Should fail minimum length validation
    errors = exc_info.value.errors()
    assert len(errors) > 0


def test_chat_request_missing_message():
    """Test ChatRequest rejects missing message field."""
    with pytest.raises(ValidationError) as exc_info:
        ChatRequest()

    errors = exc_info.value.errors()
    assert any(error["loc"][0] == "message" for error in errors)


def test_chat_response_valid():
    """Test ChatResponse accepts valid response."""
    response = ChatResponse(response="This is a test response about Physical AI.")
    assert response.response == "This is a test response about Physical AI."


def test_chat_response_missing_field():
    """Test ChatResponse rejects missing response field."""
    with pytest.raises(ValidationError):
        ChatResponse()


def test_error_response_valid():
    """Test ErrorResponse accepts valid error message."""
    error = ErrorResponse(error="Service temporarily unavailable")
    assert error.error == "Service temporarily unavailable"


def test_error_response_missing_field():
    """Test ErrorResponse rejects missing error field."""
    with pytest.raises(ValidationError):
        ErrorResponse()
