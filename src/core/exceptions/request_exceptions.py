"""
Exceções específicas para requisições e limites.
Request and limit specific exceptions.
"""

from typing import Any, Dict, Optional

from .base_exceptions import BaseApplicationException


class RequestException(BaseApplicationException):
    """
    Exceção base para erros de requisição.
    Base exception for request errors.
    """

    pass


class RateLimitException(RequestException):
    """
    Exceção para rate limit excedido.
    Exception for rate limit exceeded.
    """

    def __init__(
        self,
        limit: int,
        period: str,
        retry_after: Optional[int] = None,
        identifier: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "RATE_LIMIT_EXCEEDED",
    ):
        rate_limit_details = details or {}
        rate_limit_details.update(
            {
                "limit": limit,
                "period": period,
            }
        )
        if retry_after:
            rate_limit_details["retry_after_seconds"] = retry_after
        if identifier:
            rate_limit_details["identifier"] = identifier

        super().__init__(
            message_pt=f"Limite de requisições excedido: {limit} por {period}",
            message_en=f"Rate limit exceeded: {limit} per {period}",
            details=rate_limit_details,
            error_code=error_code,
            status_code=429,
        )


class PayloadTooLargeException(RequestException):
    """
    Exceção para payload muito grande.
    Exception for payload too large.
    """

    def __init__(
        self,
        max_size: str,
        actual_size: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "PAYLOAD_TOO_LARGE",
    ):
        payload_details = details or {}
        payload_details["max_size"] = max_size
        if actual_size:
            payload_details["actual_size"] = actual_size

        super().__init__(
            message_pt=f"Payload muito grande. Tamanho máximo: {max_size}",
            message_en=f"Payload too large. Maximum size: {max_size}",
            details=payload_details,
            error_code=error_code,
            status_code=413,
        )


class BadRequestException(RequestException):
    """
    Exceção para requisição mal formada.
    Exception for bad request.
    """

    def __init__(
        self,
        message_pt: str,
        message_en: str,
        reason: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "BAD_REQUEST",
    ):
        request_details = details or {}
        if reason:
            request_details["reason"] = reason

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=request_details,
            error_code=error_code,
            status_code=400,
        )


class MethodNotAllowedException(RequestException):
    """
    Exceção para método HTTP não permitido.
    Exception for HTTP method not allowed.
    """

    def __init__(
        self,
        method: str,
        allowed_methods: list[str],
        resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "METHOD_NOT_ALLOWED",
    ):
        method_details = details or {}
        method_details.update(
            {
                "method": method,
                "allowed_methods": allowed_methods,
            }
        )
        if resource:
            method_details["resource"] = resource

        super().__init__(
            message_pt=f"Método {method} não é permitido",
            message_en=f"Method {method} is not allowed",
            details=method_details,
            error_code=error_code,
            status_code=405,
        )


class ResourceLockedException(RequestException):
    """
    Exceção para recurso bloqueado.
    Exception for locked resource.
    """

    def __init__(
        self,
        resource: str,
        locked_by: Optional[str] = None,
        locked_until: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "RESOURCE_LOCKED",
    ):
        lock_details = details or {}
        lock_details["resource"] = resource
        if locked_by:
            lock_details["locked_by"] = locked_by
        if locked_until:
            lock_details["locked_until"] = locked_until

        super().__init__(
            message_pt=f"Recurso {resource} está bloqueado",
            message_en=f"Resource {resource} is locked",
            details=lock_details,
            error_code=error_code,
            status_code=423,
        )


class ServiceUnavailableException(RequestException):
    """
    Exceção para serviço indisponível.
    Exception for service unavailable.
    """

    def __init__(
        self,
        service: Optional[str] = None,
        reason: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "SERVICE_UNAVAILABLE",
    ):
        service_details = details or {}
        if service:
            service_details["service"] = service
        if reason:
            service_details["reason"] = reason
        if retry_after:
            service_details["retry_after_seconds"] = retry_after

        message_pt = "Serviço temporariamente indisponível"
        message_en = "Service temporarily unavailable"

        if service:
            message_pt = f"Serviço {service} temporariamente indisponível"
            message_en = f"Service {service} temporarily unavailable"

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=service_details,
            error_code=error_code,
            status_code=503,
        )


class FeatureNotAvailableException(RequestException):
    """
    Exceção para funcionalidade não disponível.
    Exception for feature not available.
    """

    def __init__(
        self,
        feature: str,
        reason: Optional[str] = None,
        available_in: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "FEATURE_NOT_AVAILABLE",
    ):
        feature_details = details or {}
        feature_details["feature"] = feature
        if reason:
            feature_details["reason"] = reason
        if available_in:
            feature_details["available_in"] = available_in

        super().__init__(
            message_pt=f"Funcionalidade '{feature}' não está disponível",
            message_en=f"Feature '{feature}' is not available",
            details=feature_details,
            error_code=error_code,
            status_code=501,  # Not Implemented
        )
