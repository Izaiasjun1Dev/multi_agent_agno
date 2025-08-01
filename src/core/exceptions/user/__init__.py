"""
Exceções do domínio de usuários.
User domain exceptions.
"""

from .exceptions import (  # Base exceptions; Validation exceptions; Business rule exceptions; Authorization exceptions
    UserAccountLockedException,
    UserAlreadyExistsException,
    UserBusinessRuleException,
    UserEmailValidationException,
    UserForbiddenException,
    UserInactiveException,
    UserNameValidationException,
    UserNotFoundException,
    UserOrgMismatchException,
    UserPasswordMismatchException,
    UserPasswordValidationException,
    UserProfileIncompleteException,
    UserSlugConflictException,
    UserTokenExpiredException,
    UserTokenInvalidException,
    UserUnauthorizedException,
    UserValidationException,
)

__all__ = [
    # Base exceptions
    "UserValidationException",
    "UserBusinessRuleException",
    # Validation exceptions
    "UserEmailValidationException",
    "UserPasswordValidationException",
    "UserNameValidationException",
    # Business rule exceptions
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "UserInactiveException",
    "UserPasswordMismatchException",
    "UserAccountLockedException",
    "UserProfileIncompleteException",
    "UserOrgMismatchException",
    "UserSlugConflictException",
    # Authorization exceptions
    "UserUnauthorizedException",
    "UserForbiddenException",
    "UserTokenExpiredException",
    "UserTokenInvalidException",
]
