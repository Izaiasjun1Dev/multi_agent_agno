from typing import Dict, Optional

from ..base_exceptions import BaseApplicationException


class ChatCreationException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro ao criar o chat.",
            message_en="Error creating chat.",
            details=details,
            error_code="CHAT_CREATION_ERROR",
        )


class ChatNotFoundException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Chat não encontrado.",
            message_en="Chat not found.",
            details=details,
            error_code="CHAT_NOT_FOUND",
        )


class ChatUpdateException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro ao atualizar o chat.",
            message_en="Error updating chat.",
            details=details,
            error_code="CHAT_UPDATE_ERROR",
        )


class ChatDeletionException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro ao deletar o chat.",
            message_en="Error deleting chat.",
            details=details,
            error_code="CHAT_DELETION_ERROR",
        )


class ChatListException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro ao listar os chats.",
            message_en="Error listing chats.",
            details=details,
            error_code="CHAT_LIST_ERROR",
        )


class ChatAccessDeniedException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Acesso negado ao chat.",
            message_en="Access denied to chat.",
            details=details,
            error_code="CHAT_ACCESS_DENIED",
            status_code=403,
        )


class ChatMessageException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro ao processar mensagem do chat.",
            message_en="Error processing chat message.",
            details=details,
            error_code="CHAT_MESSAGE_ERROR",
        )


class ChatParticipantException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro ao gerenciar participantes do chat.",
            message_en="Error managing chat participants.",
            details=details,
            error_code="CHAT_PARTICIPANT_ERROR",
        )


class ChatValidationException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro de validação do chat.",
            message_en="Chat validation error.",
            details=details,
            error_code="CHAT_VALIDATION_ERROR",
            status_code=400,
        )


class ChatConnectionException(BaseApplicationException):
    def __init__(self, details: Optional[Dict] = None):
        super().__init__(
            message_pt="Erro de conexão com o chat.",
            message_en="Chat connection error.",
            details=details,
            error_code="CHAT_CONNECTION_ERROR",
        )
