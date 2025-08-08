"""
Testes para o repositório de usuários.
Tests for user repository.
"""

from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError

from core.entities.user import User
from core.exceptions.base_exceptions import BaseApplicationException
from core.exceptions.user.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from infraestructure.repositoryes.user.repository import UserRepository


class TestUserRepository:
    """Testes para o repositório de usuários DynamoDB"""

    @pytest.fixture
    def user_repository(self):
        with patch(
            "infraestructure.repositoryes.user.repository.settings"
        ) as mock_settings:
            mock_settings.app_prefix = "test"
            mock_settings.environment = "test"

            with patch(
                "infraestructure.repositoryes.user.repository.AWSClientFactory"
            ) as mock_factory:
                mock_table = Mock()
                mock_factory.return_value.dynamo_table.return_value = mock_table

                repository = UserRepository()
                repository.table = mock_table
                return repository

    @pytest.fixture
    def sample_user(self):
        return User(
            userId="user_123",
            email="test@example.com",
            firstName="Test",
            lastName="User",
            isActive=True,
            slug="test-user",
            avatarUrl=None,
            chats=None,
        )

    @pytest.fixture
    def sample_user_dict(self):
        return {
            "userId": "user_123",
            "email": "test@example.com",
            "firstName": "Test",
            "lastName": "User",
            "isActive": True,
            "slug": "test-user",
            "avatarUrl": None,
            "createdAt": "2024-01-01T00:00:00",
            "updatedAt": "2024-01-01T00:00:00",
        }

    def test_create_user_success(self, user_repository, sample_user, sample_user_dict):
        """Testa criação de usuário bem-sucedida"""
        # Arrange
        # Mock para get_user_by_email retornar None (usuário não existe)
        user_repository.table.query.side_effect = ClientError(
            error_response={"Error": {"Code": "ValidationException"}},
            operation_name="Query",
        )
        user_repository.table.scan.return_value = {
            "Items": []
        }  # Usuário não existe no scan por email

        user_repository.table.put_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        # Act
        result = user_repository.create_user(sample_user)

        # Assert
        assert result == sample_user
        user_repository.table.put_item.assert_called_once()

    def test_create_user_already_exists_exception(
        self, user_repository, sample_user, sample_user_dict
    ):
        """Testa exceção quando usuário já existe"""
        # Arrange
        # Mock para get_user_by_email retornar usuário existente
        user_repository.table.query.side_effect = ClientError(
            error_response={"Error": {"Code": "ValidationException"}},
            operation_name="Query",
        )
        user_repository.table.scan.return_value = {"Items": [sample_user_dict]}

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException) as exc_info:
            user_repository.create_user(sample_user)

        assert exc_info.value.details["conflicting_value"] == sample_user.email

    def test_create_user_handles_client_error(
        self, user_repository, sample_user, sample_user_dict
    ):
        """Testa tratamento de ClientError do DynamoDB"""
        # Arrange
        # Mock get_user_by_email para retornar None
        user_repository.table.query.side_effect = ClientError(
            error_response={"Error": {"Code": "ValidationException"}},
            operation_name="Query",
        )
        user_repository.table.scan.return_value = {"Items": []}

        # Mock put_item para gerar ClientError genérico (não ConditionalCheckFailedException)
        user_repository.table.put_item.side_effect = ClientError(
            error_response={"Error": {"Code": "ResourceNotFoundException"}},
            operation_name="PutItem",
        )

        # Act & Assert - Esperando BaseApplicationException para erro genérico
        with pytest.raises(BaseApplicationException):
            user_repository.create_user(sample_user)

    def test_get_user_success(self, user_repository, sample_user_dict):
        """Testa busca bem-sucedida de usuário"""
        # Arrange
        user_repository.table.get_item.return_value = {"Item": sample_user_dict}

        # Act
        result = user_repository.get_user("user_123")

        # Assert
        assert result.user_id == "user_123"
        assert result.email == "test@example.com"

    def test_get_user_not_found(self, user_repository):
        """Testa quando usuário não é encontrado"""
        # Arrange
        user_repository.table.get_item.return_value = {}

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            user_repository.get_user("nonexistent_user")

    def test_get_user_by_email_success(self, user_repository, sample_user_dict):
        """Testa busca por email bem-sucedida"""
        # Arrange - Fazer query falhar para usar scan
        user_repository.table.query.side_effect = ClientError(
            error_response={"Error": {"Code": "ValidationException"}},
            operation_name="Query",
        )
        user_repository.table.scan.return_value = {"Items": [sample_user_dict]}

        # Act
        result = user_repository.get_user_by_email("test@example.com")

        # Assert
        assert result.email == "test@example.com"

    def test_get_user_by_email_not_found(self, user_repository):
        """Testa busca por email quando não encontrado"""
        # Arrange - Fazer query falhar para usar scan
        user_repository.table.query.side_effect = ClientError(
            error_response={"Error": {"Code": "ValidationException"}},
            operation_name="Query",
        )
        user_repository.table.scan.return_value = {"Items": []}

        # Act
        result = user_repository.get_user_by_email("nonexistent@example.com")

        # Assert
        assert result is None

    def test_update_user_success(self, user_repository, sample_user, sample_user_dict):
        """Testa atualização bem-sucedida de usuário"""
        # Arrange
        # Mock get_user para retornar usuário existente
        user_repository.table.get_item.return_value = {"Item": sample_user_dict}

        user_repository.table.update_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        # Act
        result = user_repository.update_user(sample_user)

        # Assert
        assert result == sample_user
        user_repository.table.update_item.assert_called_once()

    def test_update_user_not_found(self, user_repository, sample_user):
        """Testa atualização quando usuário não existe"""
        # Arrange
        # Mock get_user para retornar usuário não encontrado
        user_repository.table.get_item.return_value = {}

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            user_repository.update_user(sample_user)

    def test_delete_user_success(self, user_repository, sample_user_dict):
        """Testa exclusão bem-sucedida de usuário"""
        # Arrange
        # Mock get_user para retornar usuário existente
        user_repository.table.get_item.return_value = {"Item": sample_user_dict}

        user_repository.table.delete_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }

        # Act
        result = user_repository.delete_user("user_123")

        # Assert
        assert result is True
        user_repository.table.delete_item.assert_called_once()

    def test_delete_user_handles_client_error(self, user_repository, sample_user_dict):
        """Testa tratamento de erro na exclusão"""
        # Arrange
        # Mock get_user para retornar usuário existente
        user_repository.table.get_item.return_value = {"Item": sample_user_dict}

        user_repository.table.delete_item.side_effect = ClientError(
            error_response={"Error": {"Code": "ResourceNotFoundException"}},
            operation_name="DeleteItem",
        )

        # Act & Assert
        with pytest.raises(
            BaseApplicationException
        ):  # O método atual não converte para UserNotFoundException
            user_repository.delete_user("user_123")

    def test_list_users_success(self, user_repository, sample_user_dict):
        """Testa listagem bem-sucedida de usuários"""
        # Arrange
        user_repository.table.scan.return_value = {"Items": [sample_user_dict]}

        # Act
        result = user_repository.list_users()

        # Assert
        assert len(result) == 1
        assert result[0].user_id == "user_123"

    def test_list_users_empty(self, user_repository):
        """Testa listagem quando não há usuários"""
        # Arrange
        user_repository.table.scan.return_value = {"Items": []}

        # Act
        result = user_repository.list_users()

        # Assert
        assert result == []
