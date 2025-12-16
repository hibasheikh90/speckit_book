"""Custom authentication exceptions."""


class AuthException(Exception):
    """Base authentication exception."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserAlreadyExistsException(AuthException):
    """Raised when trying to create a user with an email that already exists."""
    def __init__(self, message: str = "Email already registered"):
        super().__init__(message, 409)  # 409 Conflict


class InvalidCredentialsException(AuthException):
    """Raised when provided credentials are invalid."""
    def __init__(self, message: str = "Incorrect email or password"):
        super().__init__(message, 401)  # 401 Unauthorized


class UserNotFoundException(AuthException):
    """Raised when a user is not found in the database."""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, 404)  # 404 Not Found


class TokenValidationException(AuthException):
    """Raised when a token is invalid or expired."""
    def __init__(self, message: str = "Token has expired or is invalid"):
        super().__init__(message, 401)  # 401 Unauthorized


class WeakPasswordException(AuthException):
    """Raised when a password doesn't meet strength requirements."""
    def __init__(self, message: str = "Password does not meet strength requirements"):
        super().__init__(message, 400)  # 400 Bad Request


class InvalidEmailException(AuthException):
    """Raised when an email doesn't meet format requirements."""
    def __init__(self, message: str = "Invalid email format"):
        super().__init__(message, 400)  # 400 Bad Request