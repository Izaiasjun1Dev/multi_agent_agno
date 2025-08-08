"""
Testes para as exceções do repositório de chat PostgreSQL.
Tests for PostgreSQL chat repository exceptions.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from core.entities.chat import Chat
from core.exceptions.chat import (
    ChatCreationException,
    ChatDeletionException,
    ChatListException,
    ChatNotFoundException,
    ChatUpdateException,
)
from infraestructure.repositoryes.chat.postgres_chat_repository import (
    PostgresChatRepository,
)


class TestPostgresChatRepositoryExceptions:
    """Testes para as exceções do repositório de chat PostgreSQL."""

    @pytest.fixture
    def repository(self):
        """Fixture para criar uma instância do repositório."""
        return PostgresChatRepository()

    @pytest.fixture
    def sample_chat(self):
        """Fixture para criar um chat de exemplo."""
        return Chat(
            chatId="test-chat-id", userId="test-user-id", messages=[], isActive=True
        )

    @pytest.mark.asyncio
    async def test_create_chat_raises_exception_on_database_error(
        self, repository, sample_chat
    ):
        """Testa se ChatCreationException é lançada quando há erro no banco."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que vai falhar
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None

            # Mock do commit que vai falhar
            mock_session.commit = AsyncMock(
                side_effect=SQLAlchemyError("Database connection failed")
            )
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatCreationException) as exc_info:
                await repository.create_chat(sample_chat)

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_CREATION_ERROR"
            assert "Database connection failed" in str(
                exc_info.value.details["original_error"]
            )
            assert exc_info.value.details["user_id"] == "test-user-id"
            assert exc_info.value.details["operation"] == "create_chat"

    @pytest.mark.asyncio
    async def test_get_chats_raises_exception_on_database_error(self, repository):
        """Testa se ChatListException é lançada quando há erro no banco."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que vai falhar
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.execute.side_effect = SQLAlchemyError("Connection timeout")
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatListException) as exc_info:
                await repository.get_chats("test-user-id")

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_LIST_ERROR"
            assert "Connection timeout" in str(exc_info.value.details["original_error"])
            assert exc_info.value.details["user_id"] == "test-user-id"
            assert exc_info.value.details["operation"] == "get_chats"

    @pytest.mark.asyncio
    async def test_update_chat_raises_not_found_exception(
        self, repository, sample_chat
    ):
        """Testa se ChatNotFoundException é lançada quando chat não existe."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que retorna None (chat não encontrado)
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get.return_value = None
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatNotFoundException) as exc_info:
                await repository.update_chat("nonexistent-chat-id", sample_chat)

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_NOT_FOUND"
            assert exc_info.value.details["chat_id"] == "nonexistent-chat-id"
            assert exc_info.value.details["operation"] == "update_chat"

    @pytest.mark.asyncio
    async def test_update_chat_raises_exception_on_database_error(
        self, repository, sample_chat
    ):
        """Testa se ChatUpdateException é lançada quando há erro no banco durante update."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que encontra o chat mas falha no commit
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None

            mock_chat = MagicMock()
            mock_chat.model_dump.return_value = {"chat_id": "test", "user_id": "test"}
            mock_session.get.return_value = mock_chat
            mock_session.commit.side_effect = SQLAlchemyError("Constraint violation")
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatUpdateException) as exc_info:
                await repository.update_chat("test-chat-id", sample_chat)

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_UPDATE_ERROR"
            assert "Constraint violation" in str(
                exc_info.value.details["original_error"]
            )
            assert exc_info.value.details["chat_id"] == "test-chat-id"
            assert exc_info.value.details["operation"] == "update_chat"

    @pytest.mark.asyncio
    async def test_delete_chat_raises_not_found_exception(self, repository):
        """Testa se ChatNotFoundException é lançada quando chat não existe para deletar."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que retorna None (chat não encontrado)
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get.return_value = None
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatNotFoundException) as exc_info:
                await repository.delete_chat("nonexistent-chat-id")

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_NOT_FOUND"
            assert exc_info.value.details["chat_id"] == "nonexistent-chat-id"
            assert exc_info.value.details["operation"] == "delete_chat"

    @pytest.mark.asyncio
    async def test_delete_chat_raises_exception_on_database_error(self, repository):
        """Testa se ChatDeletionException é lançada quando há erro no banco durante delete."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que encontra o chat mas falha no delete
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None

            mock_chat = MagicMock()
            mock_session.get.return_value = mock_chat
            mock_session.delete.side_effect = SQLAlchemyError("Foreign key constraint")
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatDeletionException) as exc_info:
                await repository.delete_chat("test-chat-id")

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_DELETION_ERROR"
            assert "Foreign key constraint" in str(
                exc_info.value.details["original_error"]
            )
            assert exc_info.value.details["chat_id"] == "test-chat-id"
            assert exc_info.value.details["operation"] == "delete_chat"

    @pytest.mark.asyncio
    async def test_list_chats_raises_exception_on_database_error(self, repository):
        """Testa se ChatListException é lançada quando há erro no banco durante listagem."""
        with patch.object(repository, "session_factory") as mock_session_factory:
            # Mock da sessão que vai falhar
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.execute.side_effect = SQLAlchemyError("Query timeout")
            mock_session_factory.return_value = mock_session

            with pytest.raises(ChatListException) as exc_info:
                await repository.list_chats("test-user-id")

            # Verifica os detalhes da exceção
            assert exc_info.value.error_code == "CHAT_LIST_ERROR"
            assert "Query timeout" in str(exc_info.value.details["original_error"])
            assert exc_info.value.details["user_id"] == "test-user-id"
            assert exc_info.value.details["operation"] == "list_chats"
