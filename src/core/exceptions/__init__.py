"""
Sistema de exceções da aplicação.
Application exception system.
"""

from .base_exceptions import (
    BaseApplicationException,
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from .user import (
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
    "BaseApplicationException",
    "ValidationException",
    "BusinessRuleException",
    "NotFoundException",
    "ConflictException",
    "UnauthorizedException",
    "ForbiddenException",
    # User exceptions
    "UserValidationException",
    "UserBusinessRuleException",
    "UserEmailValidationException",
    "UserPasswordValidationException",
    "UserNameValidationException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "UserInactiveException",
    "UserPasswordMismatchException",
    "UserAccountLockedException",
    "UserProfileIncompleteException",
    "UserOrgMismatchException",
    "UserSlugConflictException",
    "UserUnauthorizedException",
    "UserForbiddenException",
    "UserTokenExpiredException",
    "UserTokenInvalidException",
]
