"""
Exception handlers para a aplicação FastAPI.
FastAPI exception handlers for the application.
"""

import logging
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exceptions.agent import (
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
from core.exceptions.auth.auth_exceptions import (
    AuthenticationException,
    EmailNotVerifiedException,
    InsufficientPermissionsException,
    InvalidCredentialsException,
    InvalidMFACodeException,
    InvalidTokenException,
    MFARequiredException,
    MissingTokenException,
    PasswordResetRequiredException,
    RefreshTokenException,
    SessionExpiredException,
    TokenExpiredException,
    TooManyLoginAttemptsException,
    UnauthorizedAccessException,
    UserNotActiveException,
)
from core.exceptions.base_exceptions import (
    BaseApplicationException,
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from core.exceptions.chat import (
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
from core.exceptions.infrastructure_exceptions import (
    CacheException,
    ConnectionException,
    DatabaseException,
    ExternalServiceException,
    FileSystemException,
    InfrastructureException,
    MessageQueueException,
    TimeoutException,
)
from core.exceptions.request_exceptions import (
    BadRequestException,
    FeatureNotAvailableException,
    MethodNotAllowedException,
    PayloadTooLargeException,
    RateLimitException,
    RequestException,
    ResourceLockedException,
    ServiceUnavailableException,
)
from core.exceptions.user import (
    UserAlreadyExistsException,
    UserEmailValidationException,
    UserNotFoundException,
    UserPasswordMismatchException,
    UserPasswordValidationException,
    UserTokenExpiredException,
    UserTokenInvalidException,
    UserUnauthorizedException,
    UserValidationException,
)

# Configurar logger
logger = logging.getLogger(__name__)


def get_accept_language(request: Request) -> str:
    """
    Obtém o idioma preferido do cliente a partir do header Accept-Language.
    Gets the client's preferred language from the Accept-Language header.
    """
    accept_language = request.headers.get("accept-language", "pt")
    # Simplifica para apenas verificar se é inglês ou português
    if "en" in accept_language.lower():
        return "en"
    return "pt"


async def base_application_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Handler para todas as exceções customizadas da aplicação.
    Handler for all custom application exceptions.
    """
    # Verifica se é uma exceção do tipo BaseApplicationException
    if not isinstance(exc, BaseApplicationException):
        # Se não for, redireciona para o handler genérico
        return await generic_exception_handler(request, exc)

    language = get_accept_language(request)
    error_response = exc.to_dict(language=language)

    # Log da exceção
    logger.error(
        f"Application exception: {exc.__class__.__name__} - {exc}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(status_code=exc.status_code, content=error_response)


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler para erros de validação do FastAPI/Pydantic.
    Handler for FastAPI/Pydantic validation errors.
    """
    # Verifica se é um erro de validação
    if not isinstance(exc, RequestValidationError):
        return await generic_exception_handler(request, exc)

    language = get_accept_language(request)

    # Formata os erros de validação
    errors = []
    for error in exc.errors():
        field_name = ".".join(
            str(loc) for loc in error["loc"][1:]
        )  # Remove 'body' do início
        errors.append(
            {
                "field": field_name,
                "message": error["msg"],
                "type": error["type"],
            }
        )

    message = "Dados de entrada inválidos" if language == "pt" else "Invalid input data"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": message,
            "error_code": "VALIDATION_ERROR",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "details": {"validation_errors": errors},
        },
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler para exceções HTTP padrão.
    Handler for standard HTTP exceptions.
    """
    # Verifica se é uma exceção HTTP válida
    if not isinstance(exc, (HTTPException, StarletteHTTPException)):
        return await generic_exception_handler(request, exc)

    language = get_accept_language(request)

    # Mapeamento de mensagens por status code
    status_messages = {
        400: ("Requisição inválida", "Bad request"),
        401: ("Não autorizado", "Unauthorized"),
        403: ("Acesso proibido", "Forbidden"),
        404: ("Recurso não encontrado", "Resource not found"),
        405: ("Método não permitido", "Method not allowed"),
        409: ("Conflito de recursos", "Resource conflict"),
        422: ("Entidade não processável", "Unprocessable entity"),
        429: ("Muitas requisições", "Too many requests"),
        500: ("Erro interno do servidor", "Internal server error"),
        502: ("Gateway inválido", "Bad gateway"),
        503: ("Serviço indisponível", "Service unavailable"),
        504: ("Tempo de resposta esgotado", "Gateway timeout"),
    }

    message_pt, message_en = status_messages.get(
        exc.status_code, ("Erro no servidor", "Server error")
    )

    message = message_pt if language == "pt" else message_en

    # Se a exceção tem detalhes, usa eles
    if hasattr(exc, "detail") and exc.detail:
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        else:
            message = str(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": message,
            "error_code": f"HTTP_{exc.status_code}",
            "status_code": exc.status_code,
            "details": {},
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler para exceções não tratadas.
    Handler for unhandled exceptions.
    """
    language = get_accept_language(request)

    # Log completo do erro
    logger.exception(
        f"Unhandled exception: {exc.__class__.__name__}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "headers": dict(request.headers),
        },
    )

    message = (
        "Erro interno do servidor" if language == "pt" else "Internal server error"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": message,
            "error_code": "INTERNAL_SERVER_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "details": {
                "type": exc.__class__.__name__,
                # Em produção, não expor detalhes do erro
                "message": str(exc) if __debug__ else None,
            },
        },
    )


def register_auth_exception_handlers(app: FastAPI) -> None:
    """
    Registra os exception handlers específicos para o módulo de autenticação.
    Registers the specific exception handlers for the authentication module.
    """
    # Handlers específicos para exceções de autenticação
    app.add_exception_handler(
        AuthenticationException, base_application_exception_handler
    )
    app.add_exception_handler(
        InvalidCredentialsException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserNotActiveException, base_application_exception_handler
    )
    app.add_exception_handler(TokenExpiredException, base_application_exception_handler)
    app.add_exception_handler(InvalidTokenException, base_application_exception_handler)
    app.add_exception_handler(MissingTokenException, base_application_exception_handler)
    app.add_exception_handler(
        UnauthorizedAccessException, base_application_exception_handler
    )
    app.add_exception_handler(
        PasswordResetRequiredException, base_application_exception_handler
    )
    app.add_exception_handler(
        TooManyLoginAttemptsException, base_application_exception_handler
    )
    app.add_exception_handler(
        SessionExpiredException, base_application_exception_handler
    )
    app.add_exception_handler(
        InsufficientPermissionsException, base_application_exception_handler
    )
    app.add_exception_handler(
        EmailNotVerifiedException, base_application_exception_handler
    )
    app.add_exception_handler(RefreshTokenException, base_application_exception_handler)
    app.add_exception_handler(MFARequiredException, base_application_exception_handler)
    app.add_exception_handler(
        InvalidMFACodeException, base_application_exception_handler
    )


def register_chat_exception_handlers(app: FastAPI) -> None:
    """
    Registra os exception handlers específicos para o módulo de chat.
    Registers the specific exception handlers for the chat module.
    """
    # Handlers específicos para exceções de chat
    app.add_exception_handler(ChatCreationException, base_application_exception_handler)
    app.add_exception_handler(ChatNotFoundException, base_application_exception_handler)
    app.add_exception_handler(ChatUpdateException, base_application_exception_handler)
    app.add_exception_handler(ChatDeletionException, base_application_exception_handler)
    app.add_exception_handler(ChatListException, base_application_exception_handler)
    app.add_exception_handler(
        ChatAccessDeniedException, base_application_exception_handler
    )
    app.add_exception_handler(ChatMessageException, base_application_exception_handler)
    app.add_exception_handler(
        ChatParticipantException, base_application_exception_handler
    )
    app.add_exception_handler(
        ChatValidationException, base_application_exception_handler
    )
    app.add_exception_handler(
        ChatConnectionException, base_application_exception_handler
    )


def register_agent_exception_handlers(app: FastAPI) -> None:
    """
    Registra os exception handlers específicos para o módulo de agent.
    Registers the specific exception handlers for the agent module.
    """
    # Handlers específicos para exceções de agent
    app.add_exception_handler(
        AgentCreationException, base_application_exception_handler
    )
    app.add_exception_handler(
        AgentNotFoundException, base_application_exception_handler
    )
    app.add_exception_handler(AgentUpdateException, base_application_exception_handler)
    app.add_exception_handler(
        AgentDeletionException, base_application_exception_handler
    )
    app.add_exception_handler(AgentListException, base_application_exception_handler)
    app.add_exception_handler(
        AgentValidationException, base_application_exception_handler
    )
    app.add_exception_handler(AgentStreamException, base_application_exception_handler)
    app.add_exception_handler(
        AgentAuthenticationException, base_application_exception_handler
    )
    app.add_exception_handler(
        AgentPermissionException, base_application_exception_handler
    )
    app.add_exception_handler(
        AgentConnectionException, base_application_exception_handler
    )


def register_user_exception_handlers(app: FastAPI) -> None:
    """
    Registra os exception handlers específicos para o módulo de usuários.
    Registers the specific exception handlers for the user module.
    """
    # Handlers específicos para exceções de usuário
    app.add_exception_handler(
        UserAlreadyExistsException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserValidationException, base_application_exception_handler
    )
    app.add_exception_handler(UserNotFoundException, base_application_exception_handler)
    app.add_exception_handler(
        UserEmailValidationException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserTokenExpiredException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserUnauthorizedException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserTokenInvalidException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserPasswordValidationException, base_application_exception_handler
    )
    app.add_exception_handler(
        UserPasswordMismatchException, base_application_exception_handler
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos os exception handlers na aplicação.
    Registers all exception handlers in the application.
    """
    # Registrar handlers específicos para os módulos PRIMEIRO (mais específicos)
    register_user_exception_handlers(app)
    register_auth_exception_handlers(app)
    register_chat_exception_handlers(app)
    register_agent_exception_handlers(app)

    # Handlers específicos para cada tipo de exceção customizada
    app.add_exception_handler(ValidationException, base_application_exception_handler)
    app.add_exception_handler(BusinessRuleException, base_application_exception_handler)
    app.add_exception_handler(NotFoundException, base_application_exception_handler)
    app.add_exception_handler(ConflictException, base_application_exception_handler)
    app.add_exception_handler(UnauthorizedException, base_application_exception_handler)
    app.add_exception_handler(ForbiddenException, base_application_exception_handler)

    # Infrastructure exceptions
    app.add_exception_handler(
        InfrastructureException, base_application_exception_handler
    )
    app.add_exception_handler(DatabaseException, base_application_exception_handler)
    app.add_exception_handler(ConnectionException, base_application_exception_handler)
    app.add_exception_handler(TimeoutException, base_application_exception_handler)
    app.add_exception_handler(
        ExternalServiceException, base_application_exception_handler
    )
    app.add_exception_handler(CacheException, base_application_exception_handler)
    app.add_exception_handler(FileSystemException, base_application_exception_handler)
    app.add_exception_handler(MessageQueueException, base_application_exception_handler)

    # Request exceptions
    app.add_exception_handler(RequestException, base_application_exception_handler)
    app.add_exception_handler(RateLimitException, base_application_exception_handler)
    app.add_exception_handler(
        PayloadTooLargeException, base_application_exception_handler
    )
    app.add_exception_handler(BadRequestException, base_application_exception_handler)
    app.add_exception_handler(
        MethodNotAllowedException, base_application_exception_handler
    )
    app.add_exception_handler(
        ResourceLockedException, base_application_exception_handler
    )
    app.add_exception_handler(
        ServiceUnavailableException, base_application_exception_handler
    )
    app.add_exception_handler(
        FeatureNotAvailableException, base_application_exception_handler
    )

    # Handler para exceções base da aplicação (mais genérico)
    app.add_exception_handler(
        BaseApplicationException, base_application_exception_handler
    )

    # Handler para erros de validação do FastAPI
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    # Handler para exceções HTTP
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)

    # Handler genérico para qualquer exceção não tratada (ÚLTIMO)
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("Exception handlers registered successfully")
