"""
Testes para as exceções de chat.
Tests for chat exceptions.
"""

import pytest

from core.exceptions import (
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


class TestChatExceptions:
    """Testes para as exceções de chat."""

    def test_chat_creation_exception(self):
        """Testa a exceção de criação de chat."""
        details = {"chat_id": "123", "user_id": "456"}
        exception = ChatCreationException(details=details)

        assert exception.error_code == "CHAT_CREATION_ERROR"
        assert exception.status_code == 500
        assert exception.details == details
        assert "Erro ao criar o chat" in exception.message_pt
        assert "Error creating chat" in exception.message_en

    def test_chat_not_found_exception(self):
        """Testa a exceção de chat não encontrado."""
        details = {"chat_id": "non-existent"}
        exception = ChatNotFoundException(details=details)

        assert exception.error_code == "CHAT_NOT_FOUND"
        assert exception.status_code == 500
        assert exception.details == details
        assert "Chat não encontrado" in exception.message_pt
        assert "Chat not found" in exception.message_en

    def test_chat_update_exception(self):
        """Testa a exceção de atualização de chat."""
        exception = ChatUpdateException()

        assert exception.error_code == "CHAT_UPDATE_ERROR"
        assert exception.status_code == 500
        assert exception.details == {}

    def test_chat_deletion_exception(self):
        """Testa a exceção de deleção de chat."""
        exception = ChatDeletionException()

        assert exception.error_code == "CHAT_DELETION_ERROR"
        assert exception.status_code == 500

    def test_chat_list_exception(self):
        """Testa a exceção de listagem de chat."""
        exception = ChatListException()

        assert exception.error_code == "CHAT_LIST_ERROR"
        assert exception.status_code == 500

    def test_chat_access_denied_exception(self):
        """Testa a exceção de acesso negado ao chat."""
        details = {"user_id": "123", "chat_id": "456"}
        exception = ChatAccessDeniedException(details=details)

        assert exception.error_code == "CHAT_ACCESS_DENIED"
        assert exception.status_code == 403  # Forbidden
        assert exception.details == details
        assert "Acesso negado ao chat" in exception.message_pt
        assert "Access denied to chat" in exception.message_en

    def test_chat_message_exception(self):
        """Testa a exceção de mensagem de chat."""
        details = {"message_id": "msg123"}
        exception = ChatMessageException(details=details)

        assert exception.error_code == "CHAT_MESSAGE_ERROR"
        assert exception.status_code == 500
        assert exception.details == details

    def test_chat_participant_exception(self):
        """Testa a exceção de participantes de chat."""
        exception = ChatParticipantException()

        assert exception.error_code == "CHAT_PARTICIPANT_ERROR"
        assert exception.status_code == 500

    def test_chat_validation_exception(self):
        """Testa a exceção de validação de chat."""
        details = {"field": "name", "error": "required"}
        exception = ChatValidationException(details=details)

        assert exception.error_code == "CHAT_VALIDATION_ERROR"
        assert exception.status_code == 400  # Bad Request
        assert exception.details == details

    def test_chat_connection_exception(self):
        """Testa a exceção de conexão de chat."""
        exception = ChatConnectionException()

        assert exception.error_code == "CHAT_CONNECTION_ERROR"
        assert exception.status_code == 500

    def test_to_dict_functionality(self):
        """Testa a funcionalidade to_dict das exceções."""
        details = {"test": "data"}
        exception = ChatCreationException(details=details)

        result_pt = exception.to_dict(language="pt")
        result_en = exception.to_dict(language="en")

        assert result_pt["error"] is True
        assert result_pt["message"] == exception.message_pt
        assert result_pt["error_code"] == "CHAT_CREATION_ERROR"
        assert result_pt["status_code"] == 500
        assert result_pt["details"] == details

        assert result_en["message"] == exception.message_en

    def test_exception_inheritance(self):
        """Testa se as exceções herdam corretamente da classe base."""
        from core.exceptions.base_exceptions import BaseApplicationException

        exceptions = [
            ChatCreationException(),
            ChatNotFoundException(),
            ChatUpdateException(),
            ChatDeletionException(),
            ChatListException(),
            ChatAccessDeniedException(),
            ChatMessageException(),
            ChatParticipantException(),
            ChatValidationException(),
            ChatConnectionException(),
        ]

        for exception in exceptions:
            assert isinstance(exception, BaseApplicationException)
            assert isinstance(exception, Exception)
