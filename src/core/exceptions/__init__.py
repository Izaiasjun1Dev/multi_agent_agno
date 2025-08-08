"""
Sistema de exceções da aplicação.
Application exception system.
"""

# Agent exceptions
from .agent import (
    AgentAuthenticationException,
    AgentConnectionException,
    AgentCreationException,
    AgentDeletionException,
    AgentListException,
    AgentNotFoundException,
    AgentPermissionException,
    AgentStreamException,
    AgentUpdateException,
    AgentValidationException,
)

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

# Chat exceptions
from .chat import (
    ChatAccessDeniedException,
    ChatConnectionException,
    ChatCreationException,
    ChatDeletionException,
    ChatListException,
    ChatMessageException,
    ChatNotFoundException,
    ChatParticipantException,
    ChatUpdateException,
    ChatValidationException,
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
    "UserSlugConflictException",
    # Chat exceptions
    "ChatCreationException",
    "ChatNotFoundException",
    "ChatUpdateException",
    "ChatDeletionException",
    "ChatListException",
    "ChatAccessDeniedException",
    "ChatMessageException",
    "ChatParticipantException",
    "ChatValidationException",
    "ChatConnectionException",
    # Agent exceptions
    "AgentCreationException",
    "AgentNotFoundException",
    "AgentUpdateException",
    "AgentDeletionException",
    "AgentListException",
    "AgentValidationException",
    "AgentStreamException",
    "AgentAuthenticationException",
    "AgentPermissionException",
    "AgentConnectionException",
]
