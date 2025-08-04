"""
Exceções relacionadas à autenticação.
Authentication related exceptions.
"""

from .auth_exceptions import (
    AuthenticationException,
    EmailNotVerifiedException,
    InsufficientPermissionsException,
    InvalidCredentialsException,
    InvalidMFACodeException,
    InvalidTokenException,
    MFARequiredException,
    MissingTokenException,
    PasswordResetRequiredException,
    RefreshTokenException,
    SessionExpiredException,
    TokenExpiredException,
    TooManyLoginAttemptsException,
    UnauthorizedAccessException,
    UserNotActiveException,
)

__all__ = [
    "AuthenticationException",
    "InvalidCredentialsException",
    "UserNotActiveException",
    "TokenExpiredException",
    "InvalidTokenException",
    "MissingTokenException",
    "UnauthorizedAccessException",
    "PasswordResetRequiredException",
    "TooManyLoginAttemptsException",
    "SessionExpiredException",
    "InsufficientPermissionsException",
    "EmailNotVerifiedException",
    "RefreshTokenException",
    "MFARequiredException",
    "InvalidMFACodeException",
]
