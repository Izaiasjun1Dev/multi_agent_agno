"""
Exceções específicas para infraestrutura e integração.
Infrastructure and integration specific exceptions.
"""

from typing import Any, Dict, Optional

from .base_exceptions import BaseApplicationException


class InfrastructureException(BaseApplicationException):
    """
    Exceção base para erros de infraestrutura.
    Base exception for infrastructure errors.
    """

    def __init__(
        self,
        message_pt: str = "Erro de infraestrutura",
        message_en: str = "Infrastructure error",
        service: Optional[str] = None,
        operation: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "INFRASTRUCTURE_ERROR",
        status_code: int = 503,
    ):
        infra_details = details or {}
        if service:
            infra_details["service"] = service
        if operation:
            infra_details["operation"] = operation

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            details=infra_details,
            error_code=error_code,
            status_code=status_code,
        )


class DatabaseException(InfrastructureException):
    """
    Exceção para erros de banco de dados.
    Exception for database errors.
    """

    def __init__(
        self,
        message_pt: str = "Erro ao acessar banco de dados",
        message_en: str = "Database access error",
        operation: Optional[str] = None,
        table: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "DATABASE_ERROR",
    ):
        db_details = details or {}
        if table:
            db_details["table"] = table

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            service="database",
            operation=operation,
            details=db_details,
            error_code=error_code,
        )


class ConnectionException(InfrastructureException):
    """
    Exceção para erros de conexão.
    Exception for connection errors.
    """

    def __init__(
        self,
        service: str,
        message_pt: Optional[str] = None,
        message_en: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "CONNECTION_ERROR",
    ):
        if not message_pt:
            message_pt = f"Erro ao conectar com {service}"
        if not message_en:
            message_en = f"Error connecting to {service}"

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            service=service,
            operation="connect",
            details=details,
            error_code=error_code,
        )


class TimeoutException(InfrastructureException):
    """
    Exceção para timeout.
    Exception for timeout.
    """

    def __init__(
        self,
        service: str,
        operation: str,
        timeout_seconds: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "TIMEOUT_ERROR",
    ):
        timeout_details = details or {}
        if timeout_seconds:
            timeout_details["timeout_seconds"] = timeout_seconds

        super().__init__(
            message_pt=f"Tempo esgotado ao executar {operation} em {service}",
            message_en=f"Timeout executing {operation} on {service}",
            service=service,
            operation=operation,
            details=timeout_details,
            error_code=error_code,
            status_code=504,
        )


class ExternalServiceException(InfrastructureException):
    """
    Exceção para erros de serviços externos.
    Exception for external service errors.
    """

    def __init__(
        self,
        service: str,
        message_pt: str,
        message_en: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "EXTERNAL_SERVICE_ERROR",
    ):
        external_details = details or {}
        if status_code:
            external_details["external_status_code"] = status_code
        if response_body:
            external_details["response_body"] = response_body

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            service=service,
            details=external_details,
            error_code=error_code,
            status_code=502,  # Bad Gateway
        )


class CacheException(InfrastructureException):
    """
    Exceção para erros de cache.
    Exception for cache errors.
    """

    def __init__(
        self,
        operation: str,
        key: Optional[str] = None,
        message_pt: Optional[str] = None,
        message_en: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "CACHE_ERROR",
    ):
        cache_details = details or {}
        if key:
            cache_details["key"] = key

        if not message_pt:
            message_pt = f"Erro ao executar {operation} no cache"
        if not message_en:
            message_en = f"Error executing {operation} on cache"

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            service="cache",
            operation=operation,
            details=cache_details,
            error_code=error_code,
            status_code=503,
        )


class FileSystemException(InfrastructureException):
    """
    Exceção para erros de sistema de arquivos.
    Exception for file system errors.
    """

    def __init__(
        self,
        operation: str,
        path: Optional[str] = None,
        message_pt: Optional[str] = None,
        message_en: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "FILE_SYSTEM_ERROR",
    ):
        fs_details = details or {}
        if path:
            fs_details["path"] = path

        if not message_pt:
            message_pt = f"Erro ao executar {operation} no sistema de arquivos"
        if not message_en:
            message_en = f"Error executing {operation} on file system"

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            service="file_system",
            operation=operation,
            details=fs_details,
            error_code=error_code,
            status_code=500,
        )


class MessageQueueException(InfrastructureException):
    """
    Exceção para erros de fila de mensagens.
    Exception for message queue errors.
    """

    def __init__(
        self,
        queue_name: str,
        operation: str,
        message_pt: Optional[str] = None,
        message_en: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = "MESSAGE_QUEUE_ERROR",
    ):
        queue_details = details or {}
        queue_details["queue_name"] = queue_name

        if not message_pt:
            message_pt = f"Erro ao executar {operation} na fila {queue_name}"
        if not message_en:
            message_en = f"Error executing {operation} on queue {queue_name}"

        super().__init__(
            message_pt=message_pt,
            message_en=message_en,
            service="message_queue",
            operation=operation,
            details=queue_details,
            error_code=error_code,
            status_code=503,
        )
