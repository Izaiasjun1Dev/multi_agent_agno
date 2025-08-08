"""
Testes para o controller de autenticação.
Tests for authentication controller.
"""

from typing import Any, Dict
from unittest.mock import Mock

import pytest

from core.usecases.auth.auth_usecases import ConfirmUserUseCase
from core.usecases.user.usecases import LoginUserUseCase
from presentation.controllers.auth.auth_controller import AuthController
from presentation.presenters.user.user_presenter import UserPresenterInterface


class TestAuthController:
    """Testes para o controller de autenticação"""

    @pytest.fixture
    def login_usecase_mock(self):
        return Mock(spec=LoginUserUseCase)

    @pytest.fixture
    def confirm_usecase_mock(self):
        return Mock(spec=ConfirmUserUseCase)

    @pytest.fixture
    def presenter_mock(self):
        return Mock(spec=UserPresenterInterface)

    @pytest.fixture
    def auth_controller(self, login_usecase_mock, confirm_usecase_mock, presenter_mock):
        return AuthController(
            login_usecase=login_usecase_mock,
            confirm_usecase=confirm_usecase_mock,
            presenter=presenter_mock,
        )

    def test_login_success(self, auth_controller, login_usecase_mock, presenter_mock):
        """Testa login bem-sucedido"""
        # Arrange
        auth_details = {
            "success": True,
            "access_token": "mock_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "mock_refresh_token",
        }
        expected_response = {
            "success": True,
            "message": "Login successful",
            "data": {
                "access_token": "mock_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        }

        login_usecase_mock.execute.return_value = auth_details
        presenter_mock.present_user_authentication.return_value = expected_response

        # Act
        result = auth_controller.login("test@example.com", "SecurePassword123!")

        # Assert
        assert result == expected_response
        login_usecase_mock.execute.assert_called_once_with(
            "test@example.com", "SecurePassword123!"
        )
        presenter_mock.present_user_authentication.assert_called_once_with(auth_details)

    def test_login_handles_usecase_exception(
        self, auth_controller, login_usecase_mock, presenter_mock
    ):
        """Testa tratamento de exceção do caso de uso no login"""
        from core.exceptions.auth.auth_exceptions import InvalidCredentialsException

        # Arrange
        login_usecase_mock.execute.side_effect = InvalidCredentialsException(
            details={"email": "test@example.com"}
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            auth_controller.login("test@example.com", "wrong_password")

        login_usecase_mock.execute.assert_called_once_with(
            "test@example.com", "wrong_password"
        )
        presenter_mock.present_user_authentication.assert_not_called()

    def test_login_with_authentication_exception(
        self, auth_controller, login_usecase_mock, presenter_mock
    ):
        """Testa tratamento de exceção de autenticação"""
        from core.exceptions.auth.auth_exceptions import AuthenticationException

        # Arrange
        login_usecase_mock.execute.side_effect = AuthenticationException(
            message_pt="Erro de autenticação",
            message_en="Authentication error",
            error_code="AUTH_ERROR",
        )

        # Act & Assert
        with pytest.raises(AuthenticationException):
            auth_controller.login("test@example.com", "password123")

        login_usecase_mock.execute.assert_called_once()
        presenter_mock.present_user_authentication.assert_not_called()

    def test_confirm_email_success(
        self, auth_controller, confirm_usecase_mock, presenter_mock
    ):
        """Testa confirmação de email bem-sucedida"""
        # Arrange
        confirmation_result = {"status": "success"}
        expected_response = {
            "success": True,
            "message": "Email confirmed successfully",
            "data": {"status": "confirmed"},
        }

        confirm_usecase_mock.execute.return_value = confirmation_result
        presenter_mock.present_email_confirmation.return_value = expected_response

        # Act
        result = auth_controller.confirm_email("test@example.com", "123456")

        # Assert
        assert result == expected_response
        confirm_usecase_mock.execute.assert_called_once_with(
            "test@example.com", "123456"
        )
        presenter_mock.present_email_confirmation.assert_called_once_with(
            confirmation_result
        )

    def test_confirm_email_handles_user_not_found_exception(
        self, auth_controller, confirm_usecase_mock, presenter_mock
    ):
        """Testa tratamento de exceção quando usuário não é encontrado"""
        from core.exceptions.user.exceptions import UserNotFoundException

        # Arrange
        confirm_usecase_mock.execute.side_effect = UserNotFoundException(
            identifier="nonexistent@example.com", field="email"
        )

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            auth_controller.confirm_email("nonexistent@example.com", "123456")

        confirm_usecase_mock.execute.assert_called_once_with(
            "nonexistent@example.com", "123456"
        )
        presenter_mock.present_email_confirmation.assert_not_called()

    def test_confirm_email_handles_authentication_exception(
        self, auth_controller, confirm_usecase_mock, presenter_mock
    ):
        """Testa tratamento de exceção de autenticação na confirmação"""
        from core.exceptions.auth.auth_exceptions import AuthenticationException

        # Arrange
        confirm_usecase_mock.execute.side_effect = AuthenticationException(
            message_pt="Token inválido",
            message_en="Invalid token",
            error_code="INVALID_TOKEN",
        )

        # Act & Assert
        with pytest.raises(AuthenticationException):
            auth_controller.confirm_email("test@example.com", "invalid_token")

        confirm_usecase_mock.execute.assert_called_once()
        presenter_mock.present_email_confirmation.assert_not_called()

    def test_confirm_email_handles_infrastructure_exception(
        self, auth_controller, confirm_usecase_mock, presenter_mock
    ):
        """Testa tratamento de exceção de infraestrutura"""
        from core.exceptions import InfrastructureException

        # Arrange
        confirm_usecase_mock.execute.side_effect = InfrastructureException(
            message_pt="Erro de infraestrutura",
            message_en="Infrastructure error",
            service="auth_service",
            operation="confirm_email",
            error_code="INFRA_ERROR",
        )

        # Act & Assert
        with pytest.raises(InfrastructureException):
            auth_controller.confirm_email("test@example.com", "123456")

        confirm_usecase_mock.execute.assert_called_once()
        presenter_mock.present_email_confirmation.assert_not_called()


class TestAuthControllerIntegration:
    """Testes de integração para o controller de autenticação"""

    @pytest.fixture
    def full_auth_controller_setup(self):
        """Setup completo com mocks configurados"""
        login_usecase = Mock(spec=LoginUserUseCase)
        confirm_usecase = Mock(spec=ConfirmUserUseCase)
        presenter = Mock(spec=UserPresenterInterface)

        controller = AuthController(
            login_usecase=login_usecase,
            confirm_usecase=confirm_usecase,
            presenter=presenter,
        )

        return {
            "controller": controller,
            "login_usecase": login_usecase,
            "confirm_usecase": confirm_usecase,
            "presenter": presenter,
        }

    def test_complete_authentication_flow(self, full_auth_controller_setup):
        """Testa fluxo completo de autenticação: login e confirmação"""
        setup = full_auth_controller_setup
        controller = setup["controller"]
        login_usecase = setup["login_usecase"]
        confirm_usecase = setup["confirm_usecase"]
        presenter = setup["presenter"]

        # Dados de teste
        email = "flow@example.com"
        password = "SecurePassword123!"
        confirmation_token = "123456"

        # Configurar mocks para confirmação
        confirmation_result = {"status": "success"}
        confirm_response = {"success": True, "message": "Email confirmed successfully"}
        confirm_usecase.execute.return_value = confirmation_result
        presenter.present_email_confirmation.return_value = confirm_response

        # Configurar mocks para login
        auth_details = {
            "success": True,
            "access_token": "token_after_confirmation",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        login_response = {
            "success": True,
            "message": "Login successful",
            "data": auth_details,
        }
        login_usecase.execute.return_value = auth_details
        presenter.present_user_authentication.return_value = login_response

        # 1. Confirmar email primeiro
        confirm_result = controller.confirm_email(email, confirmation_token)
        assert confirm_result["success"] is True

        # 2. Fazer login após confirmação
        login_result = controller.login(email, password)
        assert login_result["success"] is True

        # Verificar todas as chamadas
        confirm_usecase.execute.assert_called_once_with(email, confirmation_token)
        login_usecase.execute.assert_called_once_with(email, password)
        presenter.present_email_confirmation.assert_called_once_with(
            confirmation_result
        )
        presenter.present_user_authentication.assert_called_once_with(auth_details)

    def test_login_retry_after_failed_attempt(self, full_auth_controller_setup):
        """Testa retry de login após tentativa falhada"""
        setup = full_auth_controller_setup
        controller = setup["controller"]
        login_usecase = setup["login_usecase"]
        presenter = setup["presenter"]

        email = "retry@example.com"
        wrong_password = "WrongPassword"
        correct_password = "CorrectPassword123!"

        # Primeira tentativa - falha
        from core.exceptions.auth.auth_exceptions import InvalidCredentialsException

        login_usecase.execute.side_effect = [
            InvalidCredentialsException(details={"email": email}),
            {
                "success": True,
                "access_token": "success_token",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        ]

        success_response = {
            "success": True,
            "message": "Login successful",
            "data": {"access_token": "success_token"},
        }
        presenter.present_user_authentication.return_value = success_response

        # Primeira tentativa - deve falhar
        with pytest.raises(InvalidCredentialsException):
            controller.login(email, wrong_password)

        # Segunda tentativa - deve funcionar
        result = controller.login(email, correct_password)
        assert result["success"] is True

        # Verificar chamadas
        assert login_usecase.execute.call_count == 2
        presenter.present_user_authentication.assert_called_once()
