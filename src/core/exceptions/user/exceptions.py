"""
Exceções específicas para o domínio de usuários.
User domain specific exceptions.
"""

from typing import Any, Dict, Optional

from ..base_exceptions import (
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)


class UserValidationException(ValidationException):
    """
    Exceção base para validações de usuário.
    Base exception for user validations.
    """

    pass


class UserEmailValidationException(UserValidationException):
    """
    Exceção para validação de email de usuário.
    Exception for user email validation.
    """

    def __init__(self, email: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_pt=f"Email '{email}' não é válido",
            message_en=f"Email '{email}' is not valid",
            field="email",
            value=email,
            details=details,
            error_code="USER_INVALID_EMAIL",
        )


class UserPasswordValidationException(UserValidationException):
    """
    Exceção para validação de senha de usuário.
    Exception for user password validation.
    """

    def __init__(
        self, reason_pt: str, reason_en: str, details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message_pt=f"Senha inválida: {reason_pt}",
            message_en=f"Invalid password: {reason_en}",
            field="password",
            details=details,
            error_code="USER_INVALID_PASSWORD",
        )


class UserNameValidationException(UserValidationException):
    """
    Exceção para validação de nome de usuário.
    Exception for user name validation.
    """

    def __init__(
        self, field_name: str, value: str, details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message_pt=f"Nome '{field_name}' não é válido: '{value}'",
            message_en=f"Name '{field_name}' is not valid: '{value}'",
            field=field_name,
            value=value,
            details=details,
            error_code="USER_INVALID_NAME",
        )


class UserBusinessRuleException(BusinessRuleException):
    """
    Exceção base para regras de negócio de usuário.
    Base exception for user business rules.
    """

    pass


class UserAlreadyExistsException(ConflictException):
    """
    Exceção para usuário já existente.
    Exception for user already exists.
    """

    def __init__(self, email: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_pt=f"Usuário com email '{email}' já existe",
            message_en=f"User with email '{email}' already exists",
            conflicting_field="email",
            conflicting_value=email,
            details=details,
            error_code="USER_ALREADY_EXISTS",
        )


class UserNotFoundException(NotFoundException):
    """
    Exceção para usuário não encontrado.
    Exception for user not found.
    """

    def __init__(
        self,
        identifier: str,
        field: str = "id",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt=f"Usuário não encontrado com {field}: '{identifier}'",
            message_en=f"User not found with {field}: '{identifier}'",
            resource="user",
            identifier=identifier,
            details=(
                {**details, "search_field": field}
                if details
                else {"search_field": field}
            ),
            error_code="USER_NOT_FOUND",
        )


class UserInactiveException(UserBusinessRuleException):
    """
    Exceção para usuário inativo.
    Exception for inactive user.
    """

    def __init__(self, user_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_pt=f"Usuário '{user_id}' está inativo",
            message_en=f"User '{user_id}' is inactive",
            rule="user_must_be_active",
            details=(
                {**details, "user_id": user_id} if details else {"user_id": user_id}
            ),
            error_code="USER_INACTIVE",
        )


class UserUnauthorizedException(UnauthorizedException):
    """
    Exceção para usuário não autorizado.
    Exception for unauthorized user.
    """

    def __init__(
        self,
        action: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        auth_details = details or {}
        if user_id:
            auth_details["user_id"] = user_id

        super().__init__(
            message_pt=f"Usuário não autorizado para executar a ação: {action}",
            message_en=f"User unauthorized to perform action: {action}",
            action=action,
            resource="user",
            details=auth_details,
            error_code="USER_UNAUTHORIZED",
        )


class UserForbiddenException(ForbiddenException):
    """
    Exceção para acesso proibido ao usuário.
    Exception for forbidden user access.
    """

    def __init__(
        self,
        permission: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        forbidden_details = details or {}
        if user_id:
            forbidden_details["user_id"] = user_id

        super().__init__(
            message_pt=f"Usuário não possui a permissão necessária: {permission}",
            message_en=f"User does not have required permission: {permission}",
            permission=permission,
            resource="user",
            details=forbidden_details,
            error_code="USER_FORBIDDEN",
        )


class UserPasswordMismatchException(UserBusinessRuleException):
    """
    Exceção para senha incorreta.
    Exception for incorrect password.
    """

    def __init__(self, user_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_pt="Senha incorreta",
            message_en="Incorrect password",
            rule="password_must_match",
            details=(
                {**details, "user_id": user_id} if details else {"user_id": user_id}
            ),
            error_code="USER_PASSWORD_MISMATCH",
        )


class UserAccountLockedException(UserBusinessRuleException):
    """
    Exceção para conta de usuário bloqueada.
    Exception for locked user account.
    """

    def __init__(
        self, user_id: str, lock_reason: str, details: Optional[Dict[str, Any]] = None
    ):
        lock_details = details or {}
        lock_details.update({"user_id": user_id, "lock_reason": lock_reason})

        super().__init__(
            message_pt=f"Conta do usuário '{user_id}' está bloqueada: {lock_reason}",
            message_en=f"User account '{user_id}' is locked: {lock_reason}",
            rule="account_must_be_unlocked",
            details=lock_details,
            error_code="USER_ACCOUNT_LOCKED",
        )


class UserTokenExpiredException(UnauthorizedException):
    """
    Exceção para token de usuário expirado.
    Exception for expired user token.
    """

    def __init__(
        self, token_type: str = "access", details: Optional[Dict[str, Any]] = None
    ):
        token_details = details or {}
        token_details["token_type"] = token_type

        super().__init__(
            message_pt=f"Token {token_type} expirado",
            message_en=f"{token_type.title()} token expired",
            action="authenticate",
            details=token_details,
            error_code="USER_TOKEN_EXPIRED",
        )


class UserTokenInvalidException(UnauthorizedException):
    """
    Exceção para token de usuário inválido.
    Exception for invalid user token.
    """

    def __init__(
        self, token_type: str = "access", details: Optional[Dict[str, Any]] = None
    ):
        token_details = details or {}
        token_details["token_type"] = token_type

        super().__init__(
            message_pt=f"Token {token_type} inválido",
            message_en=f"Invalid {token_type} token",
            action="authenticate",
            details=token_details,
            error_code="USER_TOKEN_INVALID",
        )


class UserProfileIncompleteException(UserBusinessRuleException):
    """
    Exceção para perfil de usuário incompleto.
    Exception for incomplete user profile.
    """

    def __init__(
        self,
        user_id: str,
        missing_fields: list,
        details: Optional[Dict[str, Any]] = None,
    ):
        profile_details = details or {}
        profile_details.update({"user_id": user_id, "missing_fields": missing_fields})

        missing_fields_str = ", ".join(missing_fields)
        super().__init__(
            message_pt=f"Perfil do usuário incompleto. Campos obrigatórios: {missing_fields_str}",
            message_en=f"Incomplete user profile. Required fields: {missing_fields_str}",
            rule="profile_must_be_complete",
            details=profile_details,
            error_code="USER_PROFILE_INCOMPLETE",
        )


class UserSlugConflictException(ConflictException):
    """
    Exceção para conflito de slug de usuário.
    Exception for user slug conflict.
    """

    def __init__(self, slug: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_pt=f"Slug '{slug}' já está em uso por outro usuário",
            message_en=f"Slug '{slug}' is already in use by another user",
            conflicting_field="slug",
            conflicting_value=slug,
            details=details,
            error_code="USER_SLUG_CONFLICT",
        )
