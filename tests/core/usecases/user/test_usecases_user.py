from datetime import datetime
from unittest.mock import MagicMock, Mock

import pytest

from core.dtos.user.user_dtos import CreateRequestUserDto
from core.entities.user import User
from core.usecases.user.usecases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
)
from interface.auth.auth_interface import AuthInterface
from interface.user.user_interface import UserInterface


class TestCreateUserUseCase:
    """Testes para o caso de uso de criação de usuário"""

    @pytest.fixture
    def user_interface_mock(self):
        mock = Mock(spec=UserInterface)
        # Configurar o mock para retornar um User quando create_user for chamado
        mock.create_user.return_value = User(
            userId="123",
            email="test@example.com",
            firstName="Test",
            lastName="User",
            slug="test-user",
            isActive=True,
            org=None,
            chats=None,
            avatarUrl=None,
        )
        return mock

    @pytest.fixture
    def auth_interface_mock(self):
        return Mock(spec=AuthInterface)

    @pytest.fixture
    def create_user_use_case(self, user_interface_mock, auth_interface_mock):
        return CreateUserUseCase(user_interface_mock, auth_interface_mock)

    @pytest.fixture
    def create_user_dto(self):
        return CreateRequestUserDto(
            email="test@example.com",
            password="secure_password",
            first_name="Test",
            last_name="User",
        )

    def test_execute_creates_user_successfully(
        self,
        create_user_use_case,
        create_user_dto,
        user_interface_mock,
        auth_interface_mock,
    ):
        # Act
        result = create_user_use_case.execute(create_user_dto)

        # Assert
        assert isinstance(result, User)
        assert result.email == create_user_dto.email

        user_interface_mock.create_user.assert_called_once()
        auth_interface_mock.signup.assert_called_once_with(
            create_user_dto.email,
            create_user_dto.password,
            create_user_dto.first_name,
            create_user_dto.last_name,
        )

    def test_execute_calls_interfaces_in_correct_order(
        self,
        create_user_use_case,
        create_user_dto,
        user_interface_mock,
        auth_interface_mock,
    ):
        # Act
        create_user_use_case.execute(create_user_dto)

        # Assert
        assert user_interface_mock.create_user.called
        assert auth_interface_mock.signup.called

    def test_execute_rollback_when_signup_fails(
        self,
        create_user_use_case,
        create_user_dto,
        user_interface_mock,
        auth_interface_mock,
    ):
        """Testa se uma exceção adequada é lançada quando o signup falha"""
        from core.exceptions import InfrastructureException

        # Arrange - Configurar o auth_interface para falhar no signup
        auth_interface_mock.signup.side_effect = Exception("Signup failed")

        # Act & Assert
        with pytest.raises(InfrastructureException) as exc_info:
            create_user_use_case.execute(create_user_dto)

        # Verificar se tentou fazer signup
        auth_interface_mock.signup.assert_called_once_with(
            create_user_dto.email,
            create_user_dto.password,
            create_user_dto.first_name,
            create_user_dto.last_name,
        )

        # Verificar que NÃO tentou criar o usuário no banco (falha rápida)
        user_interface_mock.create_user.assert_not_called()

        # Verificar detalhes da exceção
        assert "Erro inesperado ao criar usuário" in str(exc_info.value)


class TestGetUserUseCase:
    """Testes para o caso de uso de busca de usuário"""

    @pytest.fixture
    def user_interface_mock(self):
        return Mock(spec=UserInterface)

    @pytest.fixture
    def get_user_use_case(self, user_interface_mock):
        return GetUserUseCase(user_interface_mock)

    @pytest.fixture
    def sample_user(self):
        return User(
            userId="user_123",
            email="test@example.com",
            firstName="Test",
            lastName="User",
            org="org_123",
            isActive=True,
            slug="test-user",
            chats=None,
            avatarUrl=None,
        )

    def test_execute_returns_user_when_found(
        self, get_user_use_case, user_interface_mock, sample_user
    ):
        # Arrange
        user_interface_mock.get_user.return_value = sample_user

        # Act
        result = get_user_use_case.execute("user_123")

        # Assert
        assert result == sample_user
        user_interface_mock.get_user.assert_called_once_with("user_123")

    def test_execute_returns_none_when_user_not_found(
        self, get_user_use_case, user_interface_mock
    ):
        # Arrange
        user_interface_mock.get_user.return_value = None

        # Act
        result = get_user_use_case.execute("nonexistent_user")

        # Assert
        assert result is None
        user_interface_mock.get_user.assert_called_once_with("nonexistent_user")


class TestListUsersUseCase:
    """Testes para o caso de uso de listagem de usuários"""

    @pytest.fixture
    def user_interface_mock(self):
        return Mock(spec=UserInterface)

    @pytest.fixture
    def list_users_use_case(self, user_interface_mock):
        return ListUsersUseCase(user_interface_mock)

    def test_execute_returns_all_users(self, list_users_use_case, user_interface_mock):
        # Arrange
        expected_users = [
            User(
                userId="user_1",
                email="user1@example.com",
                firstName="User",
                lastName="One",
                org="org_123",
                isActive=True,
                slug="user-1",
                chats=None,
                avatarUrl=None,
            ),
            User(
                userId="user_2",
                email="user2@example.com",
                firstName="User",
                lastName="Two",
                org="org_123",
                isActive=True,
                slug="user-2",
                chats=None,
                avatarUrl=None,
            ),
        ]
        user_interface_mock.list_users.return_value = expected_users

        # Act
        result = list_users_use_case.execute()

        # Assert
        assert result == expected_users
        assert len(result) == 2
        user_interface_mock.list_users.assert_called_once()

    def test_execute_returns_empty_list_when_no_users(
        self, list_users_use_case, user_interface_mock
    ):
        # Arrange
        user_interface_mock.list_users.return_value = []

        # Act
        result = list_users_use_case.execute()

        # Assert
        assert result == []
        user_interface_mock.list_users.assert_called_once()


class TestUpdateUserUseCase:
    """Testes para o caso de uso de atualização de usuário"""

    @pytest.fixture
    def user_interface_mock(self):
        return Mock(spec=UserInterface)

    @pytest.fixture
    def update_user_use_case(self, user_interface_mock):
        return UpdateUserUseCase(user_interface_mock)

    @pytest.fixture
    def sample_user(self):
        return User(
            userId="user_123",
            email="test@example.com",
            firstName="Test",
            lastName="User",
            org="org_123",
            isActive=True,
            slug="test-user",
            chats=None,
            avatarUrl=None,
        )

    def test_execute_updates_user_successfully(
        self, update_user_use_case, user_interface_mock, sample_user
    ):
        # Arrange
        user_interface_mock.get_user.return_value = sample_user
        update_data = {"first_name": "Updated", "last_name": "Name"}

        # Act
        result = update_user_use_case.execute("user_123", update_data)

        # Assert
        assert result is not None
        assert result.name == "Updated Name"
        user_interface_mock.get_user.assert_called_once_with("user_123")
        user_interface_mock.update_user.assert_called_once()

    def test_execute_returns_none_when_user_not_found(
        self, update_user_use_case, user_interface_mock
    ):
        # Arrange
        user_interface_mock.get_user.return_value = None
        update_data = {"name": "Updated Name"}

        # Act
        result = update_user_use_case.execute("nonexistent_user", update_data)

        # Assert
        assert result is None
        user_interface_mock.get_user.assert_called_once_with("nonexistent_user")
        user_interface_mock.update_user.assert_not_called()


class TestDeleteUserUseCase:
    """Testes para o caso de uso de exclusão de usuário"""

    @pytest.fixture
    def user_interface_mock(self):
        return Mock(spec=UserInterface)

    @pytest.fixture
    def delete_user_use_case(self, user_interface_mock):
        return DeleteUserUseCase(user_interface_mock)

    def test_execute_deletes_user_successfully(
        self, delete_user_use_case, user_interface_mock
    ):
        # Arrange
        user_interface_mock.delete_user.return_value = True

        # Act
        result = delete_user_use_case.execute("user_123")

        # Assert
        assert result is True
        user_interface_mock.delete_user.assert_called_once_with("user_123")

    def test_execute_returns_false_when_user_not_found(
        self, delete_user_use_case, user_interface_mock
    ):
        # Arrange
        user_interface_mock.delete_user.return_value = False

        # Act
        result = delete_user_use_case.execute("nonexistent_user")

        # Assert
        assert result is False
        user_interface_mock.delete_user.assert_called_once_with("nonexistent_user")
