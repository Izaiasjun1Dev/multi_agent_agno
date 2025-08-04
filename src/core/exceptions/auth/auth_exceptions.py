"""
Exceções específicas para autenticação.
Authentication specific exceptions.
"""

from typing import Any, Dict, Optional

from ..base_exceptions import BaseApplicationException


class AuthenticationException(BaseApplicationException):
    """
    Exceção base para erros de autenticação.
    Base exception for authentication errors.
    """

    def __init__(
        self,
        message_pt: str = "Erro de autenticação",
        message_en: str = "Authentication error",
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "AUTH_ERROR",
        status_code: int = 401,
    ):
        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class InvalidCredentialsException(AuthenticationException):
    """
    Exceção para credenciais inválidas.
    Exception for invalid credentials.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Credenciais inválidas",
            message_en="Invalid credentials",
            details=details,
            error_code="INVALID_CREDENTIALS",
            status_code=401,
        )


class UserNotActiveException(AuthenticationException):
    """
    Exceção para usuário não ativo.
    Exception for inactive user.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if username:
            details = details or {}
            details["username"] = username

        super().__init__(
            message_pt="Usuário não está ativo",
            message_en="User is not active",
            details=details,
            error_code="USER_NOT_ACTIVE",
            status_code=403,
        )


class TokenExpiredException(AuthenticationException):
    """
    Exceção para token expirado.
    Exception for expired token.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Token de autenticação expirado",
            message_en="Authentication token expired",
            details=details,
            error_code="TOKEN_EXPIRED",
            status_code=401,
        )


class InvalidTokenException(AuthenticationException):
    """
    Exceção para token inválido.
    Exception for invalid token.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Token de autenticação inválido",
            message_en="Invalid authentication token",
            details=details,
            error_code="INVALID_TOKEN",
            status_code=401,
        )


class MissingTokenException(AuthenticationException):
    """
    Exceção para token ausente.
    Exception for missing token.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Token de autenticação não fornecido",
            message_en="Authentication token not provided",
            details=details,
            error_code="MISSING_TOKEN",
            status_code=401,
        )


class UnauthorizedAccessException(AuthenticationException):
    """
    Exceção para acesso não autorizado.
    Exception for unauthorized access.
    """

    def __init__(
        self,
        resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if resource:
            details = details or {}
            details["resource"] = resource

        super().__init__(
            message_pt="Acesso não autorizado ao recurso",
            message_en="Unauthorized access to resource",
            details=details,
            error_code="UNAUTHORIZED_ACCESS",
            status_code=403,
        )


class PasswordResetRequiredException(AuthenticationException):
    """
    Exceção quando é necessário redefinir a senha.
    Exception when password reset is required.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="É necessário redefinir a senha",
            message_en="Password reset required",
            details=details,
            error_code="PASSWORD_RESET_REQUIRED",
            status_code=403,
        )


class TooManyLoginAttemptsException(AuthenticationException):
    """
    Exceção para muitas tentativas de login.
    Exception for too many login attempts.
    """

    def __init__(
        self,
        attempts: Optional[int] = None,
        lockout_time: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        details = details or {}
        if attempts:
            details["attempts"] = attempts
        if lockout_time:
            details["lockout_time_seconds"] = lockout_time

        super().__init__(
            message_pt="Muitas tentativas de login. Conta temporariamente bloqueada",
            message_en="Too many login attempts. Account temporarily locked",
            details=details,
            error_code="TOO_MANY_LOGIN_ATTEMPTS",
            status_code=429,
        )


class SessionExpiredException(AuthenticationException):
    """
    Exceção para sessão expirada.
    Exception for expired session.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Sessão expirada. Por favor, faça login novamente",
            message_en="Session expired. Please login again",
            details=details,
            error_code="SESSION_EXPIRED",
            status_code=401,
        )


class InsufficientPermissionsException(AuthenticationException):
    """
    Exceção para permissões insuficientes.
    Exception for insufficient permissions.
    """

    def __init__(
        self,
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if required_permission:
            details = details or {}
            details["required_permission"] = required_permission

        super().__init__(
            message_pt="Permissões insuficientes para executar esta ação",
            message_en="Insufficient permissions to perform this action",
            details=details,
            error_code="INSUFFICIENT_PERMISSIONS",
            status_code=403,
        )


class EmailNotVerifiedException(AuthenticationException):
    """
    Exceção para email não verificado.
    Exception for unverified email.
    """

    def __init__(
        self,
        email: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if email:
            details = details or {}
            details["email"] = email

        super().__init__(
            message_pt="Email não verificado. Por favor, verifique seu email",
            message_en="Email not verified. Please verify your email",
            details=details,
            error_code="EMAIL_NOT_VERIFIED",
            status_code=403,
        )


class RefreshTokenException(AuthenticationException):
    """
    Exceção para erro ao renovar token.
    Exception for token refresh error.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Erro ao renovar token de autenticação",
            message_en="Error refreshing authentication token",
            details=details,
            error_code="REFRESH_TOKEN_ERROR",
            status_code=401,
        )


class MFARequiredException(AuthenticationException):
    """
    Exceção quando autenticação multi-fator é necessária.
    Exception when multi-factor authentication is required.
    """

    def __init__(
        self,
        mfa_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        if mfa_type:
            details = details or {}
            details["mfa_type"] = mfa_type

        super().__init__(
            message_pt="Autenticação multi-fator necessária",
            message_en="Multi-factor authentication required",
            details=details,
            error_code="MFA_REQUIRED",
            status_code=403,
        )


class InvalidMFACodeException(AuthenticationException):
    """
    Exceção para código MFA inválido.
    Exception for invalid MFA code.
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message_pt="Código de autenticação multi-fator inválido",
            message_en="Invalid multi-factor authentication code",
            details=details,
            error_code="INVALID_MFA_CODE",
            status_code=401,
        )
