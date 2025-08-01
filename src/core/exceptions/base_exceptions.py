"""
Exceções base do sistema.
Base exceptions for the system.
"""

from typing import Any, Dict, Optional


class BaseApplicationException(Exception):
    """
    Exceção base para todas as exceções da aplicação.
    Base exception for all application exceptions.
    """

    def __init__(
        self,
        message_pt: str,
        message_en: str,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        status_code: int = 500,
    ):
        self.message_pt = message_pt
        self.message_en = message_en
        self.details = details or {}
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message_pt)

    def to_dict(self, language: str = "pt") -> Dict[str, Any]:
        """
        Converte a exceção em um dicionário.
        Converts the exception to a dictionary.
        """
        message = self.message_pt if language == "pt" else self.message_en
        return {
            "error": True,
            "message": message,
            "error_code": self.error_code,
            "status_code": self.status_code,
            "details": self.details,
        }

    def __str__(self) -> str:
        return f"{self.message_pt} | {self.message_en}"


class ValidationException(BaseApplicationException):
    """
    Exceção para erros de validação.
    Exception for validation errors.
    """

    def __init__(
        self,
        message_pt: str,
        message_en: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        validation_details = details or {}
        if field:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = value

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=validation_details,
            error_code=error_code,
            status_code=400,
        )


class BusinessRuleException(BaseApplicationException):
    """
    Exceção para violações de regras de negócio.
    Exception for business rule violations.
    """

    def __init__(
        self,
        message_pt: str,
        message_en: str,
        rule: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        business_details = details or {}
        if rule:
            business_details["rule"] = rule

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=business_details,
            error_code=error_code,
            status_code=422,
        )


class NotFoundException(BaseApplicationException):
    """
    Exceção para recursos não encontrados.
    Exception for resources not found.
    """

    def __init__(
        self,
        message_pt: str,
        message_en: str,
        resource: Optional[str] = None,
        identifier: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        not_found_details = details or {}
        if resource:
            not_found_details["resource"] = resource
        if identifier:
            not_found_details["identifier"] = identifier

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=not_found_details,
            error_code=error_code,
            status_code=404,
        )


class ConflictException(BaseApplicationException):
    """
    Exceção para conflitos de recursos.
    Exception for resource conflicts.
    """

    def __init__(
        self,
        message_pt: str,
        message_en: str,
        conflicting_field: Optional[str] = None,
        conflicting_value: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        conflict_details = details or {}
        if conflicting_field:
            conflict_details["conflicting_field"] = conflicting_field
        if conflicting_value is not None:
            conflict_details["conflicting_value"] = conflicting_value

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=conflict_details,
            error_code=error_code,
            status_code=409,
        )


class UnauthorizedException(BaseApplicationException):
    """
    Exceção para acesso não autorizado.
    Exception for unauthorized access.
    """

    def __init__(
        self,
        message_pt: str = "Acesso não autorizado",
        message_en: str = "Unauthorized access",
        action: Optional[str] = None,
        resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        auth_details = details or {}
        if action:
            auth_details["action"] = action
        if resource:
            auth_details["resource"] = resource

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=auth_details,
            error_code=error_code,
            status_code=401,
        )


class ForbiddenException(BaseApplicationException):
    """
    Exceção para acesso proibido.
    Exception for forbidden access.
    """

    def __init__(
        self,
        message_pt: str = "Acesso proibido",
        message_en: str = "Forbidden access",
        permission: Optional[str] = None,
        resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ):
        forbidden_details = details or {}
        if permission:
            forbidden_details["permission"] = permission
        if resource:
            forbidden_details["resource"] = resource

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=forbidden_details,
            error_code=error_code,
            status_code=403,
        )
