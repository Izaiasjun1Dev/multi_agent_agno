"""
Sistema de exceções da aplicação.
Application exception system.
"""

# Base exceptions
from .base_exceptions import (
    BaseApplicationException,
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)

# Infrastructure exceptions
from .infrastructure_exceptions import (
    CacheException,
    ConnectionException,
    DatabaseException,
    ExternalServiceException,
    FileSystemException,
    InfrastructureException,
    MessageQueueException,
    TimeoutException,
)

# Request exceptions
from .request_exceptions import (
    BadRequestException,
    FeatureNotAvailableException,
    MethodNotAllowedException,
    PayloadTooLargeException,
    RateLimitException,
    RequestException,
    ResourceLockedException,
    ServiceUnavailableException,
)

# User exceptions
from .user.exceptions import (
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
    "BusinessRuleException",
    "ConflictException",
    "ForbiddenException",
    "NotFoundException",
    "UnauthorizedException",
    "ValidationException",
    # Infrastructure exceptions
    "CacheException",
    "ConnectionException",
    "DatabaseException",
    "ExternalServiceException",
    "FileSystemException",
    "InfrastructureException",
    "MessageQueueException",
    "TimeoutException",
    # Request exceptions
    "BadRequestException",
    "FeatureNotAvailableException",
    "MethodNotAllowedException",
    "PayloadTooLargeException",
    "RateLimitException",
    "RequestException",
    "ResourceLockedException",
    "ServiceUnavailableException",
    # User exceptions
    "UserValidationException",
    "UserEmailValidationException",
    "UserPasswordValidationException",
    "UserNameValidationException",
    "UserBusinessRuleException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "UserInactiveException",
    "UserUnauthorizedException",
    "UserForbiddenException",
    "UserPasswordMismatchException",
    "UserAccountLockedException",
    "UserTokenExpiredException",
    "UserTokenInvalidException",
    "UserProfileIncompleteException",
    "UserOrgMismatchException",
    "UserSlugConflictException",
]
