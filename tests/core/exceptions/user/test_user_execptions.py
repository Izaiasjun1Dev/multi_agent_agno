"""
Testes para as exceções de usuário.
Tests for user exceptions.
"""

from typing import Any, Dict

import pytest

from core.exceptions import (  # Base exceptions; User exceptions
    BaseApplicationException,
    BusinessRuleException,
    ConflictException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    UserAccountLockedException,
    UserAlreadyExistsException,
    UserBusinessRuleException,
    UserEmailValidationException,
    UserForbiddenException,
    UserInactiveException,
    UserNameValidationException,
    UserNotFoundException,
    UserPasswordMismatchException,
    UserPasswordValidationException,
    UserProfileIncompleteException,
    UserSlugConflictException,
    UserTokenExpiredException,
    UserTokenInvalidException,
    UserUnauthorizedException,
    UserValidationException,
    ValidationException,
)


class TestBaseApplicationException:
    """Testes para a exceção base da aplicação"""

    def test_create_base_exception_with_all_parameters(self):
        """Testa criação da exceção base com todos os parâmetros"""
        exception = BaseApplicationException(
            message_pt="Erro em português",
            message_en="Error in english",
            details={"field": "value"},
            error_code="TEST_ERROR",
            status_code=400,
        )

        assert exception.message_pt == "Erro em português"
        assert exception.message_en == "Error in english"
        assert exception.details == {"field": "value"}
        assert exception.error_code == "TEST_ERROR"
        assert exception.status_code == 400

    def test_to_dict_portuguese(self):
        """Testa conversão para dicionário em português"""
        exception = BaseApplicationException(
            message_pt="Erro em português",
            message_en="Error in english",
            error_code="TEST_ERROR",
            status_code=400,
        )

        result = exception.to_dict("pt")
        expected = {
            "error": True,
            "message": "Erro em português",
            "error_code": "TEST_ERROR",
            "status_code": 400,
            "details": {},
        }

        assert result == expected

    def test_to_dict_english(self):
        """Testa conversão para dicionário em inglês"""
        exception = BaseApplicationException(
            message_pt="Erro em português",
            message_en="Error in english",
            error_code="TEST_ERROR",
            status_code=400,
        )

        result = exception.to_dict("en")
        expected = {
            "error": True,
            "message": "Error in english",
            "error_code": "TEST_ERROR",
            "status_code": 400,
            "details": {},
        }

        assert result == expected

    def test_str_representation(self):
        """Testa representação string da exceção"""
        exception = BaseApplicationException(
            message_pt="Erro em português", message_en="Error in english"
        )

        assert str(exception) == "Erro em português | Error in english"


class TestUserEmailValidationException:
    """Testes para exceção de validação de email"""

    def test_create_email_validation_exception(self):
        """Testa criação da exceção de validação de email"""
        email = "invalid-email"
        exception = UserEmailValidationException(email=email)

        assert exception.message_pt == f"Email '{email}' não é válido"
        assert exception.message_en == f"Email '{email}' is not valid"
        assert exception.error_code == "USER_INVALID_EMAIL"
        assert exception.status_code == 400
        assert exception.details["field"] == "email"
        assert exception.details["value"] == email

    def test_email_validation_exception_with_details(self):
        """Testa exceção de email com detalhes customizados"""
        email = "test@"
        details = {"reason": "Domínio incompleto"}

        exception = UserEmailValidationException(email=email, details=details)

        assert exception.details["field"] == "email"
        assert exception.details["value"] == email
        assert exception.details["reason"] == "Domínio incompleto"


class TestUserPasswordValidationException:
    """Testes para exceção de validação de senha"""

    def test_create_password_validation_exception(self):
        """Testa criação da exceção de validação de senha"""
        reason_pt = "deve ter pelo menos 8 caracteres"
        reason_en = "must have at least 8 characters"

        exception = UserPasswordValidationException(
            reason_pt=reason_pt, reason_en=reason_en
        )

        assert exception.message_pt == f"Senha inválida: {reason_pt}"
        assert exception.message_en == f"Invalid password: {reason_en}"
        assert exception.error_code == "USER_INVALID_PASSWORD"
        assert exception.status_code == 400
        assert exception.details["field"] == "password"

    def test_password_validation_exception_with_details(self):
        """Testa exceção de senha com detalhes customizados"""
        details = {"min_length": 8, "current_length": 4}

        exception = UserPasswordValidationException(
            reason_pt="muito curta", reason_en="too short", details=details
        )

        assert exception.details["min_length"] == 8
        assert exception.details["current_length"] == 4


class TestUserNameValidationException:
    """Testes para exceção de validação de nome"""

    def test_create_name_validation_exception(self):
        """Testa criação da exceção de validação de nome"""
        field_name = "first_name"
        value = "123"

        exception = UserNameValidationException(field_name=field_name, value=value)

        expected_message_pt = f"Nome '{field_name}' não é válido: '{value}'"
        expected_message_en = f"Name '{field_name}' is not valid: '{value}'"

        assert exception.message_pt == expected_message_pt
        assert exception.message_en == expected_message_en
        assert exception.error_code == "USER_INVALID_NAME"
        assert exception.details["field"] == field_name
        assert exception.details["value"] == value


class TestUserAlreadyExistsException:
    """Testes para exceção de usuário já existente"""

    def test_create_user_already_exists_exception(self):
        """Testa criação da exceção de usuário já existente"""
        email = "test@example.com"

        exception = UserAlreadyExistsException(email=email)

        assert exception.message_pt == f"Usuário com email '{email}' já existe"
        assert exception.message_en == f"User with email '{email}' already exists"
        assert exception.error_code == "USER_ALREADY_EXISTS"
        assert exception.status_code == 409
        assert exception.details["conflicting_field"] == "email"
        assert exception.details["conflicting_value"] == email

    def test_user_already_exists_exception_with_details(self):
        """Testa exceção de usuário existente com detalhes"""
        email = "test@example.com"
        details = {"created_at": "2024-01-01"}

        exception = UserAlreadyExistsException(email=email, details=details)

        assert exception.details["created_at"] == "2024-01-01"


class TestUserNotFoundException:
    """Testes para exceção de usuário não encontrado"""

    def test_create_user_not_found_exception_default_field(self):
        """Testa criação da exceção de usuário não encontrado com campo padrão"""
        identifier = "user_123"

        exception = UserNotFoundException(identifier=identifier)

        assert exception.message_pt == f"Usuário não encontrado com id: '{identifier}'"
        assert exception.message_en == f"User not found with id: '{identifier}'"
        assert exception.error_code == "USER_NOT_FOUND"
        assert exception.status_code == 404
        assert exception.details["resource"] == "user"
        assert exception.details["identifier"] == identifier
        assert exception.details["search_field"] == "id"

    def test_create_user_not_found_exception_custom_field(self):
        """Testa criação da exceção de usuário não encontrado com campo customizado"""
        identifier = "test@example.com"
        field = "email"

        exception = UserNotFoundException(identifier=identifier, field=field)

        assert (
            exception.message_pt
            == f"Usuário não encontrado com {field}: '{identifier}'"
        )
        assert exception.message_en == f"User not found with {field}: '{identifier}'"
        assert exception.details["search_field"] == field


class TestUserInactiveException:
    """Testes para exceção de usuário inativo"""

    def test_create_user_inactive_exception(self):
        """Testa criação da exceção de usuário inativo"""
        user_id = "user_456"

        exception = UserInactiveException(user_id=user_id)

        assert exception.message_pt == f"Usuário '{user_id}' está inativo"
        assert exception.message_en == f"User '{user_id}' is inactive"
        assert exception.error_code == "USER_INACTIVE"
        assert exception.status_code == 422
        assert exception.details["rule"] == "user_must_be_active"
        assert exception.details["user_id"] == user_id


class TestUserPasswordMismatchException:
    """Testes para exceção de senha incorreta"""

    def test_create_password_mismatch_exception(self):
        """Testa criação da exceção de senha incorreta"""
        user_id = "user_789"

        exception = UserPasswordMismatchException(user_id=user_id)

        assert exception.message_pt == "Senha incorreta"
        assert exception.message_en == "Incorrect password"
        assert exception.error_code == "USER_PASSWORD_MISMATCH"
        assert exception.status_code == 422
        assert exception.details["rule"] == "password_must_match"
        assert exception.details["user_id"] == user_id


class TestUserAccountLockedException:
    """Testes para exceção de conta bloqueada"""

    def test_create_account_locked_exception(self):
        """Testa criação da exceção de conta bloqueada"""
        user_id = "user_locked"
        lock_reason = "Muitas tentativas de login"

        exception = UserAccountLockedException(user_id=user_id, lock_reason=lock_reason)

        expected_message_pt = (
            f"Conta do usuário '{user_id}' está bloqueada: {lock_reason}"
        )
        expected_message_en = f"User account '{user_id}' is locked: {lock_reason}"

        assert exception.message_pt == expected_message_pt
        assert exception.message_en == expected_message_en
        assert exception.error_code == "USER_ACCOUNT_LOCKED"
        assert exception.details["user_id"] == user_id
        assert exception.details["lock_reason"] == lock_reason

    def test_account_locked_exception_with_details(self):
        """Testa exceção de conta bloqueada com detalhes adicionais"""
        user_id = "user_locked"
        lock_reason = "Suspeita de fraude"
        details = {
            "locked_at": "2024-08-01T10:00:00Z",
            "unlock_at": "2024-08-02T10:00:00Z",
        }

        exception = UserAccountLockedException(
            user_id=user_id, lock_reason=lock_reason, details=details
        )

        assert exception.details["locked_at"] == "2024-08-01T10:00:00Z"
        assert exception.details["unlock_at"] == "2024-08-02T10:00:00Z"


class TestUserTokenExceptions:
    """Testes para exceções de token"""

    def test_create_token_expired_exception(self):
        """Testa criação da exceção de token expirado"""
        token_type = "access"

        exception = UserTokenExpiredException(token_type=token_type)

        assert exception.message_pt == f"Token {token_type} expirado"
        assert exception.message_en == f"{token_type.title()} token expired"
        assert exception.error_code == "USER_TOKEN_EXPIRED"
        assert exception.status_code == 401
        assert exception.details["token_type"] == token_type

    def test_create_token_invalid_exception(self):
        """Testa criação da exceção de token inválido"""
        token_type = "refresh"

        exception = UserTokenInvalidException(token_type=token_type)

        assert exception.message_pt == f"Token {token_type} inválido"
        assert exception.message_en == f"Invalid {token_type} token"
        assert exception.error_code == "USER_TOKEN_INVALID"
        assert exception.status_code == 401
        assert exception.details["token_type"] == token_type


class TestUserProfileIncompleteException:
    """Testes para exceção de perfil incompleto"""

    def test_create_profile_incomplete_exception(self):
        """Testa criação da exceção de perfil incompleto"""
        user_id = "user_incomplete"
        missing_fields = ["first_name", "last_name", "phone"]

        exception = UserProfileIncompleteException(
            user_id=user_id, missing_fields=missing_fields
        )

        missing_fields_str = ", ".join(missing_fields)
        expected_message_pt = (
            f"Perfil do usuário incompleto. Campos obrigatórios: {missing_fields_str}"
        )
        expected_message_en = (
            f"Incomplete user profile. Required fields: {missing_fields_str}"
        )

        assert exception.message_pt == expected_message_pt
        assert exception.message_en == expected_message_en
        assert exception.error_code == "USER_PROFILE_INCOMPLETE"
        assert exception.details["user_id"] == user_id
        assert exception.details["missing_fields"] == missing_fields

    def test_profile_incomplete_exception_with_details(self):
        """Testa exceção de perfil incompleto com detalhes adicionais"""
        user_id = "user_incomplete"
        missing_fields = ["avatar"]
        details = {"completion_percentage": 80}

        exception = UserProfileIncompleteException(
            user_id=user_id, missing_fields=missing_fields, details=details
        )

        assert exception.details["completion_percentage"] == 80


class TestUserSlugConflictException:
    """Testes para exceção de conflito de slug"""

    def test_create_slug_conflict_exception(self):
        """Testa criação da exceção de conflito de slug"""
        slug = "john-doe"

        exception = UserSlugConflictException(slug=slug)

        expected_message_pt = f"Slug '{slug}' já está em uso por outro usuário"
        expected_message_en = f"Slug '{slug}' is already in use by another user"

        assert exception.message_pt == expected_message_pt
        assert exception.message_en == expected_message_en
        assert exception.error_code == "USER_SLUG_CONFLICT"
        assert exception.status_code == 409
        assert exception.details["conflicting_field"] == "slug"
        assert exception.details["conflicting_value"] == slug


class TestUserAuthorizationExceptions:
    """Testes para exceções de autorização"""

    def test_create_user_unauthorized_exception(self):
        """Testa criação da exceção de usuário não autorizado"""
        action = "delete_user"
        user_id = "user_123"

        exception = UserUnauthorizedException(action=action, user_id=user_id)

        expected_message_pt = f"Usuário não autorizado para executar a ação: {action}"
        expected_message_en = f"User unauthorized to perform action: {action}"

        assert exception.message_pt == expected_message_pt
        assert exception.message_en == expected_message_en
        assert exception.error_code == "USER_UNAUTHORIZED"
        assert exception.status_code == 401
        assert exception.details["action"] == action
        assert exception.details["user_id"] == user_id

    def test_create_user_forbidden_exception(self):
        """Testa criação da exceção de acesso proibido"""
        permission = "admin_access"
        user_id = "user_456"

        exception = UserForbiddenException(permission=permission, user_id=user_id)

        expected_message_pt = f"Usuário não possui a permissão necessária: {permission}"
        expected_message_en = f"User does not have required permission: {permission}"

        assert exception.message_pt == expected_message_pt
        assert exception.message_en == expected_message_en
        assert exception.error_code == "USER_FORBIDDEN"
        assert exception.status_code == 403
        assert exception.details["permission"] == permission
        assert exception.details["user_id"] == user_id


class TestExceptionInheritance:
    """Testes para verificar a herança das exceções"""

    def test_user_validation_exception_inheritance(self):
        """Testa se UserValidationException herda de ValidationException"""
        exception = UserEmailValidationException("test@invalid")

        assert isinstance(exception, UserValidationException)
        assert isinstance(exception, ValidationException)
        assert isinstance(exception, BaseApplicationException)
        assert isinstance(exception, Exception)

    def test_user_business_rule_exception_inheritance(self):
        """Testa se UserBusinessRuleException herda de BusinessRuleException"""
        exception = UserInactiveException("user_123")

        assert isinstance(exception, UserBusinessRuleException)
        assert isinstance(exception, BusinessRuleException)
        assert isinstance(exception, BaseApplicationException)

    def test_user_not_found_exception_inheritance(self):
        """Testa se UserNotFoundException herda de NotFoundException"""
        exception = UserNotFoundException("user_123")

        assert isinstance(exception, NotFoundException)
        assert isinstance(exception, BaseApplicationException)

    def test_user_conflict_exception_inheritance(self):
        """Testa se exceções de conflito herdam de ConflictException"""
        email_exception = UserAlreadyExistsException("test@example.com")
        slug_exception = UserSlugConflictException("john-doe")

        assert isinstance(email_exception, ConflictException)
        assert isinstance(slug_exception, ConflictException)

    def test_user_authorization_exception_inheritance(self):
        """Testa se exceções de autorização herdam corretamente"""
        unauthorized_exception = UserUnauthorizedException("delete_user")
        forbidden_exception = UserForbiddenException("admin_access")
        token_expired_exception = UserTokenExpiredException()
        token_invalid_exception = UserTokenInvalidException()

        assert isinstance(unauthorized_exception, UnauthorizedException)
        assert isinstance(forbidden_exception, ForbiddenException)
        assert isinstance(token_expired_exception, UnauthorizedException)
        assert isinstance(token_invalid_exception, UnauthorizedException)


class TestExceptionApiIntegration:
    """Testes para integração com APIs"""

    def test_exception_to_api_response_portuguese(self):
        """Testa conversão de exceção para resposta de API em português"""
        exception = UserEmailValidationException(
            email="invalid@email", details={"additional_info": "test"}
        )

        api_response = exception.to_dict("pt")

        assert api_response["error"] is True
        assert "não é válido" in api_response["message"]
        assert api_response["error_code"] == "USER_INVALID_EMAIL"
        assert api_response["status_code"] == 400
        assert api_response["details"]["field"] == "email"
        assert api_response["details"]["value"] == "invalid@email"
        assert api_response["details"]["additional_info"] == "test"

    def test_exception_to_api_response_english(self):
        """Testa conversão de exceção para resposta de API em inglês"""
        exception = UserNotFoundException("user_123", "id")

        api_response = exception.to_dict("en")

        assert api_response["error"] is True
        assert "not found" in api_response["message"]
        assert api_response["error_code"] == "USER_NOT_FOUND"
        assert api_response["status_code"] == 404

    def test_multiple_exceptions_consistency(self):
        """Testa consistência entre múltiplas exceções"""
        exceptions = [
            UserEmailValidationException("invalid@email"),
            UserPasswordValidationException("muito curta", "too short"),
            UserAlreadyExistsException("test@example.com"),
            UserNotFoundException("user_123"),
            UserInactiveException("user_456"),
        ]

        for exception in exceptions:
            # Todas devem ter mensagens em PT e EN
            assert exception.message_pt
            assert exception.message_en
            assert exception.error_code
            assert exception.status_code > 0

            # Todas devem ter to_dict funcionando
            pt_dict = exception.to_dict("pt")
            en_dict = exception.to_dict("en")

            assert pt_dict["error"] is True
            assert en_dict["error"] is True
            assert pt_dict["message"] == exception.message_pt
            assert en_dict["message"] == exception.message_en
