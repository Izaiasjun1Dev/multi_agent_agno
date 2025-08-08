"""
Testes para o controller de usuários.
Tests for user controller.
"""

from typing import Any, Dict
from unittest.mock import Mock

import pytest

from core.dtos.user.user_dtos import CreateRequestUserDto
from core.entities.user import User
from core.exceptions.user.exceptions import UserNotFoundException
from core.usecases.user.usecases import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
)
from presentation.controllers.user.user_controller import UserController
from presentation.presenters.user.user_presenter import UserPresenterInterface


class TestUserController:
    """Testes para o controller de usuários"""

    @pytest.fixture
    def create_user_usecase_mock(self):
        return Mock(spec=CreateUserUseCase)

    @pytest.fixture
    def get_user_usecase_mock(self):
        return Mock(spec=GetUserUseCase)

    @pytest.fixture
    def update_user_usecase_mock(self):
        return Mock(spec=UpdateUserUseCase)

    @pytest.fixture
    def presenter_mock(self):
        return Mock(spec=UserPresenterInterface)

    @pytest.fixture
    def user_controller(
        self,
        create_user_usecase_mock,
        get_user_usecase_mock,
        update_user_usecase_mock,
        presenter_mock,
    ):
        return UserController(
            create_user_usecase=create_user_usecase_mock,
            get_user_usecase=get_user_usecase_mock,
            update_user_usecase=update_user_usecase_mock,
            presenter=presenter_mock,
        )

    @pytest.fixture
    def sample_user(self):
        return User(
            userId="user_123",
            email="test@example.com",
            firstName="Test",
            lastName="User",
            isActive=True,
            slug="test-user",
            chats=None,
            avatarUrl=None,
        )

    @pytest.fixture
    def create_user_dto(self):
        return CreateRequestUserDto(
            email="test@example.com",
            password="SecurePassword123!",
            first_name="Test",
            last_name="User",
        )

    @pytest.mark.asyncio
    async def test_create_user_success(
        self,
        user_controller,
        create_user_usecase_mock,
        presenter_mock,
        create_user_dto,
        sample_user,
    ):
        """Testa criação bem-sucedida de usuário"""
        # Arrange
        create_user_usecase_mock.execute.return_value = sample_user
        expected_response = {
            "success": True,
            "message": "User created successfully",
            "data": {"user_id": "user_123", "email": "test@example.com"},
        }
        presenter_mock.present_user_created.return_value = expected_response

        # Act
        result = await user_controller.create_user(create_user_dto)

        # Assert
        assert result == expected_response
        create_user_usecase_mock.execute.assert_called_once_with(create_user_dto)
        presenter_mock.present_user_created.assert_called_once_with(sample_user)

    @pytest.mark.asyncio
    async def test_create_user_handles_usecase_exception(
        self, user_controller, create_user_usecase_mock, presenter_mock, create_user_dto
    ):
        """Testa tratamento de exceção do caso de uso na criação"""
        from core.exceptions.user.exceptions import UserAlreadyExistsException

        # Arrange
        create_user_usecase_mock.execute.side_effect = UserAlreadyExistsException(
            email="test@example.com"
        )

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException):
            await user_controller.create_user(create_user_dto)

        create_user_usecase_mock.execute.assert_called_once_with(create_user_dto)
        presenter_mock.present_user_created.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_user_success(
        self, user_controller, get_user_usecase_mock, presenter_mock, sample_user
    ):
        """Testa busca bem-sucedida de usuário"""
        # Arrange
        get_user_usecase_mock.execute.return_value = sample_user
        expected_response = {
            "success": True,
            "data": {
                "user_id": "user_123",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
            },
        }
        presenter_mock.present_user.return_value = expected_response

        # Act
        result = await user_controller.get_user("user_123")

        # Assert
        assert result == expected_response
        get_user_usecase_mock.execute.assert_called_once_with("user_123")
        presenter_mock.present_user.assert_called_once_with(sample_user)

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self, user_controller, get_user_usecase_mock, presenter_mock
    ):
        """Testa busca de usuário quando não encontrado"""
        # Arrange
        get_user_usecase_mock.execute.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundException) as exc_info:
            await user_controller.get_user("nonexistent_user")

        assert exc_info.value.details["identifier"] == "nonexistent_user"
        assert exc_info.value.details["search_field"] == "id"
        get_user_usecase_mock.execute.assert_called_once_with("nonexistent_user")
        presenter_mock.present_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_user_handles_usecase_exception(
        self, user_controller, get_user_usecase_mock, presenter_mock
    ):
        """Testa tratamento de exceção do caso de uso na busca"""
        # Arrange
        get_user_usecase_mock.execute.side_effect = UserNotFoundException(
            identifier="user_123", field="id"
        )

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await user_controller.get_user("user_123")

        get_user_usecase_mock.execute.assert_called_once_with("user_123")
        presenter_mock.present_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        user_controller,
        update_user_usecase_mock,
        presenter_mock,
        create_user_dto,
        sample_user,
    ):
        """Testa atualização bem-sucedida de usuário"""
        # Arrange
        updated_user = User(
            userId="user_123",
            email="test@example.com",
            firstName="Updated",
            lastName="User",
            isActive=True,
            slug="test-user",
            chats=None,
            avatarUrl=None,
        )
        update_user_usecase_mock.execute.return_value = updated_user
        expected_response = {
            "success": True,
            "message": "User updated successfully",
            "data": {"user_id": "user_123", "first_name": "Updated"},
        }
        presenter_mock.present_user_updated.return_value = expected_response

        # Act
        result = await user_controller.update_user("user_123", create_user_dto)

        # Assert
        assert result == expected_response
        update_user_usecase_mock.execute.assert_called_once()
        # Verificar se o DTO foi convertido para dict
        call_args = update_user_usecase_mock.execute.call_args
        assert call_args[0][0] == "user_123"  # user_id
        assert isinstance(call_args[0][1], dict)  # user_data como dict
        presenter_mock.present_user_updated.assert_called_once_with(updated_user)

    @pytest.mark.asyncio
    async def test_update_user_not_found(
        self, user_controller, update_user_usecase_mock, presenter_mock, create_user_dto
    ):
        """Testa atualização quando usuário não é encontrado"""
        # Arrange
        update_user_usecase_mock.execute.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await user_controller.update_user("nonexistent_user", create_user_dto)

        update_user_usecase_mock.execute.assert_called_once()
        presenter_mock.present_user_updated.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_handles_usecase_exception(
        self, user_controller, update_user_usecase_mock, presenter_mock, create_user_dto
    ):
        """Testa tratamento de exceção do caso de uso na atualização"""
        from core.exceptions.user.exceptions import UserValidationException

        # Arrange
        update_user_usecase_mock.execute.side_effect = UserValidationException(
            message_pt="Email inválido",
            message_en="Invalid email",
            error_code="INVALID_EMAIL",
        )

        # Act & Assert
        with pytest.raises(UserValidationException):
            await user_controller.update_user("user_123", create_user_dto)

        update_user_usecase_mock.execute.assert_called_once()
        presenter_mock.present_user_updated.assert_not_called()


class TestUserControllerIntegration:
    """Testes de integração para o controller de usuários"""

    @pytest.fixture
    def full_controller_setup(self):
        """Setup completo com mocks configurados"""
        create_usecase = Mock(spec=CreateUserUseCase)
        get_usecase = Mock(spec=GetUserUseCase)
        update_usecase = Mock(spec=UpdateUserUseCase)
        presenter = Mock(spec=UserPresenterInterface)

        controller = UserController(
            create_user_usecase=create_usecase,
            get_user_usecase=get_usecase,
            update_user_usecase=update_usecase,
            presenter=presenter,
        )

        return {
            "controller": controller,
            "create_usecase": create_usecase,
            "get_usecase": get_usecase,
            "update_usecase": update_usecase,
            "presenter": presenter,
        }

    @pytest.mark.asyncio
    async def test_full_user_lifecycle(self, full_controller_setup):
        """Testa o ciclo completo de um usuário: criação, busca e atualização"""
        setup = full_controller_setup
        controller = setup["controller"]
        create_usecase = setup["create_usecase"]
        get_usecase = setup["get_usecase"]
        update_usecase = setup["update_usecase"]
        presenter = setup["presenter"]

        # Dados de teste
        create_dto = CreateRequestUserDto(
            email="lifecycle@example.com",
            password="SecurePassword123!",
            first_name="Lifecycle",
            last_name="Test",
        )

        created_user = User(
            userId="lifecycle_123",
            email="lifecycle@example.com",
            firstName="Lifecycle",
            lastName="Test",
            isActive=True,
            slug="lifecycle-test",
            chats=None,
            avatarUrl=None,
        )

        updated_user = User(
            userId="lifecycle_123",
            email="lifecycle@example.com",
            firstName="Updated",
            lastName="Test",
            isActive=True,
            slug="lifecycle-test",
            chats=None,
            avatarUrl=None,
        )

        # Configurar mocks
        create_usecase.execute.return_value = created_user
        get_usecase.execute.return_value = created_user
        update_usecase.execute.return_value = updated_user

        presenter.present_user_created.return_value = {
            "success": True,
            "user_id": "lifecycle_123",
        }
        presenter.present_user.return_value = {
            "success": True,
            "data": {"user_id": "lifecycle_123"},
        }
        presenter.present_user_updated.return_value = {
            "success": True,
            "data": {"user_id": "lifecycle_123"},
        }

        # 1. Criar usuário
        create_result = await controller.create_user(create_dto)
        assert create_result["success"] is True

        # 2. Buscar usuário criado
        get_result = await controller.get_user("lifecycle_123")
        assert get_result["success"] is True

        # 3. Atualizar usuário
        update_dto = CreateRequestUserDto(
            email="lifecycle@example.com",
            password="SecurePassword123!",
            first_name="Updated",
            last_name="Test",
        )
        update_result = await controller.update_user("lifecycle_123", update_dto)
        assert update_result["success"] is True

        # Verificar todas as chamadas
        create_usecase.execute.assert_called_once()
        get_usecase.execute.assert_called_once()
        update_usecase.execute.assert_called_once()
        assert presenter.present_user_created.call_count == 1
        assert presenter.present_user.call_count == 1  # apenas get
        assert presenter.present_user_updated.call_count == 1  # update
