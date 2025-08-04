"""
Middlewares customizados para a aplicação.
Custom middlewares for the application.
"""

import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar um ID único a cada requisição.
    Middleware to add a unique ID to each request.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para log detalhado de requisições.
    Middleware for detailed request logging.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Log da requisição
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_host": request.client.host if request.client else None,
                "request_id": getattr(request.state, "request_id", None),
            },
        )

        response = await call_next(request)

        # Tempo de processamento
        process_time = time.time() - start_time

        # Log da resposta
        logger.info(
            f"Request completed: {request.method} {request.url.path} - {response.status_code}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}s",
                "request_id": getattr(request.state, "request_id", None),
            },
        )

        # Adicionar cabeçalhos de performance
        response.headers["X-Process-Time"] = str(process_time)

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar cabeçalhos de segurança.
    Middleware to add security headers.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Adicionar cabeçalhos de segurança
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        return response


class ErrorContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar contexto adicional em erros.
    Middleware to add additional context to errors.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Adicionar contexto da requisição à exceção se for uma exceção customizada
            from core.exceptions.base_exceptions import BaseApplicationException

            if isinstance(exc, BaseApplicationException) and hasattr(exc, "details"):
                exc.details["request_context"] = {
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "request_id": getattr(request.state, "request_id", None),
                }
            raise
