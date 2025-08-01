import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime

from core.entities.user import User
from core.dtos.user.user_dtos import CreateUserDto
from core.usecases.user.usecases import (
    CreateUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from interface.user.user_interface import UserInterface
from interface.auth.auth_interface import AuthInterface


class TestCreateUserUseCase:
    """Testes para o caso de uso de criação de usuário"""

    @pytest.fixture
    def user_interface_mock(self):
        return Mock(spec=UserInterface)

    @pytest.fixture
    def auth_interface_mock(self):
        return Mock(spec=AuthInterface)

    @pytest.fixture
    def create_user_use_case(self, user_interface_mock, auth_interface_mock):
        return CreateUserUseCase(user_interface_mock, auth_interface_mock)

    @pytest.fixture
    def create_user_dto(self):
        return CreateUserDto(
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
            create_user_dto.email, create_user_dto.password
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
            name="Test User",
            org="org_123",
            isActive=True,
            slug="test-user",
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

    @pytest.fixture
    def sample_users(self):
        return [
            User(
                userId="user_1",
                email="user1@example.com",
                name="User 1",
                org="org_123",
                isActive=True,
                slug="user-1",
                avatarUrl=None,
            ),
            User(
                userId="user_2",
                email="user2@example.com",
                name="User 2",
                org="org_123",
                isActive=True,
                slug="user-2",
                avatarUrl=None,
            ),
        ]

    def test_execute_returns_all_users(
        self, list_users_use_case, user_interface_mock, sample_users
    ):
        # Arrange
        user_interface_mock.list_users.return_value = sample_users

        # Act
        result = list_users_use_case.execute()

        # Assert
        assert result == sample_users
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
            name="Test User",
            org="org_123",
            isActive=True,
            slug="test-user",
            avatarUrl=None,
        )

    def test_execute_updates_user_successfully(
        self, update_user_use_case, user_interface_mock, sample_user
    ):
        # Arrange
        user_interface_mock.get_user.return_value = sample_user
        update_data = {"name": "Updated Name"}

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
