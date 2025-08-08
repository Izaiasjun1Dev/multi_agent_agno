"""
Exceções específicas para operações de Agent
Agent-specific exceptions
"""

from typing import Any, Dict, Optional

from ..base_exceptions import BaseApplicationException


class AgentCreationException(BaseApplicationException):
    """
    Exceção lançada quando há erro na criação de um agent
    Exception raised when there's an error creating an agent
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_CREATION_ERROR",
        status_code: int = 500,
    ):
        super().__init__(
            message_pt="Erro ao criar o agent.",
            message_en="Error creating agent.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentNotFoundException(BaseApplicationException):
    """
    Exceção lançada quando um agent não é encontrado
    Exception raised when an agent is not found
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_NOT_FOUND",
        status_code: int = 404,
    ):
        super().__init__(
            message_pt="Agent não encontrado.",
            message_en="Agent not found.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentUpdateException(BaseApplicationException):
    """
    Exceção lançada quando há erro na atualização de um agent
    Exception raised when there's an error updating an agent
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_UPDATE_ERROR",
        status_code: int = 500,
    ):
        super().__init__(
            message_pt="Erro ao atualizar o agent.",
            message_en="Error updating agent.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentDeletionException(BaseApplicationException):
    """
    Exceção lançada quando há erro na exclusão de um agent
    Exception raised when there's an error deleting an agent
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_DELETION_ERROR",
        status_code: int = 500,
    ):
        super().__init__(
            message_pt="Erro ao deletar o agent.",
            message_en="Error deleting agent.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentListException(BaseApplicationException):
    """
    Exceção lançada quando há erro na listagem de agents
    Exception raised when there's an error listing agents
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_LIST_ERROR",
        status_code: int = 500,
    ):
        super().__init__(
            message_pt="Erro ao listar os agents.",
            message_en="Error listing agents.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentValidationException(BaseApplicationException):
    """
    Exceção lançada quando há erro de validação nos dados do agent
    Exception raised when there's a validation error in agent data
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_VALIDATION_ERROR",
        status_code: int = 400,
    ):
        super().__init__(
            message_pt="Dados do agent inválidos.",
            message_en="Invalid agent data.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentStreamException(BaseApplicationException):
    """
    Exceção lançada quando há erro no streaming de mensagens do agent
    Exception raised when there's an error streaming agent messages
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_STREAM_ERROR",
        status_code: int = 500,
    ):
        super().__init__(
            message_pt="Erro no streaming de mensagens do agent.",
            message_en="Error streaming agent messages.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentAuthenticationException(BaseApplicationException):
    """
    Exceção lançada quando há erro de autenticação com o agent
    Exception raised when there's an authentication error with the agent
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_AUTHENTICATION_ERROR",
        status_code: int = 401,
    ):
        super().__init__(
            message_pt="Erro de autenticação do agent.",
            message_en="Agent authentication error.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentPermissionException(BaseApplicationException):
    """
    Exceção lançada quando há erro de permissão para acessar o agent
    Exception raised when there's a permission error accessing the agent
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_PERMISSION_ERROR",
        status_code: int = 403,
    ):
        super().__init__(
            message_pt="Permissão negada para acessar o agent.",
            message_en="Permission denied to access agent.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )


class AgentConnectionException(BaseApplicationException):
    """
    Exceção lançada quando há erro de conexão com o agent
    Exception raised when there's a connection error with the agent
    """

    def __init__(
        self,
        details: Optional[Dict[str, Any]] = None,
        error_code: str = "AGENT_CONNECTION_ERROR",
        status_code: int = 503,
    ):
        super().__init__(
            message_pt="Erro de conexão com o agent.",
            message_en="Connection error with agent.",
            details=details,
            error_code=error_code,
            status_code=status_code,
        )
