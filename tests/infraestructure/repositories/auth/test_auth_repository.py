"""
Testes para o repositório de autenticação.
Tests for authentication repository.
"""

from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError

from core.exceptions.auth.auth_exceptions import InvalidCredentialsException
from infraestructure.repositoryes.auth.repository import AuthRepository


class TestAuthRepository:
    """Testes para o repositório de autenticação Cognito"""

    @pytest.fixture
    def auth_repository(self):
        with patch(
            "infraestructure.repositoryes.auth.repository.settings"
        ) as mock_settings:
            mock_settings.cognito_user_pool_id = "us-east-1_XXXXXXXXX"
            mock_settings.cognito_user_pool_client_id = "mock_client_id"

            with patch(
                "infraestructure.repositoryes.auth.repository.AWSClientFactory"
            ) as mock_aws_factory:
                mock_cognito = Mock()
                mock_aws_factory.return_value.cognito.return_value = mock_cognito

                repository = AuthRepository()
                repository.cognito = mock_cognito
                return repository

    def test_signup_success(self, auth_repository):
        """Testa cadastro bem-sucedido"""
        # Arrange
        auth_repository.cognito.sign_up.return_value = {
            "UserSub": "user_sub_123",
            "CodeDeliveryDetails": {
                "Destination": "test@example.com",
                "DeliveryMedium": "EMAIL",
            },
        }

        # Act
        result = auth_repository.signup(
            email="test@example.com",
            password="SecurePassword123!",
            first_name="Test",
            last_name="User",
        )

        # Assert
        assert result["user_sub"] == "user_sub_123"
        assert result["email"] == "test@example.com"
        auth_repository.cognito.sign_up.assert_called_once()

    def test_signup_handles_exception(self, auth_repository):
        """Testa tratamento de exceção no cadastro"""
        # Arrange
        auth_repository.cognito.sign_up.side_effect = ClientError(
            error_response={"Error": {"Code": "UsernameExistsException"}},
            operation_name="SignUp",
        )

        # Act
        result = auth_repository.signup(
            email="existing@example.com",
            password="SecurePassword123!",
            first_name="Test",
            last_name="User",
        )

        # Assert
        assert "error" in result
        assert "UsernameExistsException" in str(result["error"])

    def test_login_success(self, auth_repository):
        """Testa login bem-sucedido"""
        # Arrange
        auth_repository.cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "AccessToken": "mock_access_token",
                "RefreshToken": "mock_refresh_token",
                "TokenType": "Bearer",
                "ExpiresIn": 3600,
            }
        }

        # Act
        result = auth_repository.login("test@example.com", "SecurePassword123!")

        # Assert
        assert result["access_token"] == "mock_access_token"
        assert result["refresh_token"] == "mock_refresh_token"
        assert result["token_type"] == "Bearer"
        assert result["expires_in"] == 3600
        auth_repository.cognito.initiate_auth.assert_called_once()

    def test_login_invalid_credentials(self, auth_repository):
        """Testa login com credenciais inválidas"""
        # Arrange
        auth_repository.cognito.initiate_auth.side_effect = ClientError(
            error_response={"Error": {"Code": "NotAuthorizedException"}},
            operation_name="InitiateAuth",
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            auth_repository.login("test@example.com", "wrong_password")

    def test_login_handles_generic_exception(self, auth_repository):
        """Testa tratamento de exceção genérica no login"""
        # Arrange
        auth_repository.cognito.initiate_auth.side_effect = Exception("Generic error")

        # Act
        result = auth_repository.login("test@example.com", "password123")

        # Assert
        assert "error" in result
        assert "Generic error" in str(result["error"])

    def test_confirm_email_success(self, auth_repository):
        """Testa confirmação de email bem-sucedida"""
        # Arrange
        auth_repository.cognito.confirm_sign_up.return_value = {}

        # Act
        result = auth_repository.confirm_email("test@example.com", "123456")

        # Assert
        assert result is True
        auth_repository.cognito.confirm_sign_up.assert_called_once_with(
            ClientId=auth_repository.user_pool_client_id,
            Username="test@example.com",
            ConfirmationCode="123456",
        )

    def test_confirm_email_failure(self, auth_repository):
        """Testa falha na confirmação de email"""
        # Arrange
        auth_repository.cognito.confirm_sign_up.side_effect = ClientError(
            error_response={"Error": {"Code": "CodeMismatchException"}},
            operation_name="ConfirmSignUp",
        )

        # Act
        result = auth_repository.confirm_email("test@example.com", "wrong_code")

        # Assert
        assert result is False

    def test_get_user_details_success(self, auth_repository):
        """Testa obtenção de detalhes do usuário bem-sucedida"""
        # Arrange
        auth_repository.cognito.get_user.return_value = {
            "Username": "user_sub_123",
            "UserAttributes": [
                {"Name": "sub", "Value": "user_sub_123"},
                {"Name": "email", "Value": "test@example.com"},
                {"Name": "name", "Value": "Test User"},
                {"Name": "email_verified", "Value": "true"},
            ],
            "UserStatus": "CONFIRMED",
        }

        # Act
        result = auth_repository.get_user_details("mock_access_token")

        # Assert
        assert result.user_sub == "user_sub_123"
        assert result.email == "test@example.com"
        assert result.name == "Test User"
        assert result.email_verified is True

    def test_get_user_details_handles_exception(self, auth_repository):
        """Testa tratamento de exceção ao obter detalhes do usuário"""
        # Arrange
        auth_repository.cognito.get_user.side_effect = ClientError(
            error_response={"Error": {"Code": "NotAuthorizedException"}},
            operation_name="GetUser",
        )

        # Act
        result = auth_repository.get_user_details("invalid_token")

        # Assert
        assert result is None

    def test_refresh_access_token_success(self, auth_repository):
        """Testa renovação de token bem-sucedida"""
        # Arrange
        auth_repository.cognito.initiate_auth.return_value = {
            "AuthenticationResult": {
                "AccessToken": "new_access_token",
                "TokenType": "Bearer",
                "ExpiresIn": 3600,
            }
        }

        # Act
        result = auth_repository.refresh_access_token("mock_refresh_token")

        # Assert
        assert result["access_token"] == "new_access_token"
        assert result["token_type"] == "Bearer"
        assert result["expires_in"] == 3600

    def test_refresh_access_token_failure(self, auth_repository):
        """Testa falha na renovação de token"""
        # Arrange
        auth_repository.cognito.initiate_auth.side_effect = ClientError(
            error_response={"Error": {"Code": "NotAuthorizedException"}},
            operation_name="InitiateAuth",
        )

        # Act
        result = auth_repository.refresh_access_token("invalid_refresh_token")

        # Assert
        assert "error" in result

    def test_logout_success(self, auth_repository):
        """Testa logout bem-sucedido"""
        # Arrange
        auth_repository.cognito.global_sign_out.return_value = {}

        # Act
        result = auth_repository.logout("mock_access_token")

        # Assert
        assert result is True
        auth_repository.cognito.global_sign_out.assert_called_once()

    def test_logout_handles_exception(self, auth_repository):
        """Testa tratamento de exceção no logout"""
        # Arrange
        auth_repository.cognito.global_sign_out.side_effect = ClientError(
            error_response={"Error": {"Code": "NotAuthorizedException"}},
            operation_name="GlobalSignOut",
        )

        # Act
        result = auth_repository.logout("invalid_token")

        # Assert
        assert result is False

    def test_resend_confirmation_code_success(self, auth_repository):
        """Testa reenvio de código de confirmação bem-sucedido"""
        # Arrange
        auth_repository.cognito.resend_confirmation_code.return_value = {
            "CodeDeliveryDetails": {
                "Destination": "test@example.com",
                "DeliveryMedium": "EMAIL",
            }
        }

        # Act
        result = auth_repository.resend_confirmation_code("test@example.com")

        # Assert
        assert result is True
        auth_repository.cognito.resend_confirmation_code.assert_called_once()

    def test_resend_confirmation_code_failure(self, auth_repository):
        """Testa falha no reenvio de código de confirmação"""
        # Arrange
        auth_repository.cognito.resend_confirmation_code.side_effect = ClientError(
            error_response={"Error": {"Code": "UserNotFoundException"}},
            operation_name="ResendConfirmationCode",
        )

        # Act
        result = auth_repository.resend_confirmation_code("nonexistent@example.com")

        # Assert
        assert result is False
