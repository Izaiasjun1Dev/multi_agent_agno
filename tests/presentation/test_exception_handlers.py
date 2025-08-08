"""
Testes para os exception handlers da aplicação.
Tests for application exception handlers.
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from core.exceptions import (
    ConflictException,
    DatabaseException,
    ForbiddenException,
    NotFoundException,
    RateLimitException,
    UnauthorizedException,
    ValidationException,
)
from core.exceptions.user.exceptions import UserAlreadyExistsException
from presentation.app import app

client = TestClient(app)


class TestExceptionHandlers:
    """Testes para os exception handlers"""

    def setup_method(self):
        """Setup executado antes de cada teste"""
        # Limpar todos os caches das dependências
        from presentation.dependencies import (
            get_create_user_usecase,
            get_get_user_usecase,
            get_update_user_usecase,
            get_user_controller,
            get_user_presenter,
            get_user_repository,
        )

        # Limpar caches
        for func in [
            get_create_user_usecase,
            get_get_user_usecase,
            get_update_user_usecase,
            get_user_controller,
            get_user_presenter,
            get_user_repository,
        ]:
            if hasattr(func, "cache_clear"):
                func.cache_clear()

    def test_validation_exception_handler(self):
        """Testa o handler para ValidationException"""
        with patch(
            "presentation.controllers.user.user_controller.UserController.create_user"
        ) as mock_create_user:
            mock_create_user.side_effect = ValidationException(
                message_pt="Email inválido",
                message_en="Invalid email",
                field="email",
                value="validation-test@example.com",
                error_code="INVALID_EMAIL",
            )

            response = client.post(
                "/api/v1/users",
                json={
                    "email": "validation-test@example.com",
                    "password": "12345678",
                    "first_name": "Test",
                },
            )

            assert response.status_code == 400
            data = response.json()
            assert data["error"] is True
            assert data["error_code"] == "INVALID_EMAIL"
            assert data["details"]["field"] == "email"

    def test_not_found_exception_handler(self):
        """Testa o handler para NotFoundException"""
        with patch("presentation.dependencies.get_user_controller") as mock_controller:
            mock_controller.return_value.get_user.side_effect = NotFoundException(
                message_pt="Usuário não encontrado",
                message_en="User not found",
                resource="user",
                identifier="123",
                error_code="USER_NOT_FOUND",
            )

            response = client.get("/api/v1/users/123")

            assert response.status_code == 404
            data = response.json()
            assert data["error"] is True
            assert data["error_code"] == "USER_NOT_FOUND"
            assert data["details"]["resource"] == "user"

    def test_conflict_exception_handler(self):
        """Testa o handler para ConflictException"""
        # Limpar cache do lru_cache antes do teste
        from presentation.dependencies import get_create_user_usecase

        get_create_user_usecase.cache_clear()

        with patch("presentation.dependencies.get_create_user_usecase") as mock_usecase:
            mock_usecase.return_value.execute.side_effect = UserAlreadyExistsException(
                email="test@example.com"
            )

            response = client.post(
                "/api/v1/users",
                json={
                    "email": "test@example.com",
                    "password": "12345678",
                    "first_name": "Test",
                },
            )

            assert response.status_code == 409
            data = response.json()
            assert data["error"] is True
            assert data["error_code"] == "USER_ALREADY_EXISTS"

    def test_unauthorized_exception_handler(self):
        """Testa o handler para UnauthorizedException"""
        with patch(
            "presentation.controllers.user.user_controller.UserController.get_user"
        ) as mock_get_user:
            mock_get_user.side_effect = UnauthorizedException(
                action="read", resource="user"
            )

            response = client.get("/api/v1/users/123")

            assert response.status_code == 401
            data = response.json()
            assert data["error"] is True
            assert data["status_code"] == 401

    def test_database_exception_handler(self):
        """Testa o handler para DatabaseException"""
        with patch(
            "presentation.controllers.user.user_controller.UserController.create_user"
        ) as mock_create_user:
            mock_create_user.side_effect = DatabaseException(
                operation="insert", table="users", error_code="DB_CONNECTION_ERROR"
            )

            response = client.post(
                "/api/v1/users",
                json={"email": "database-test@example.com", "password": "12345678"},
            )

            assert response.status_code == 503
            data = response.json()
            assert data["error"] is True
            assert data["error_code"] == "DB_CONNECTION_ERROR"

    def test_rate_limit_exception_handler(self):
        """Testa o handler para RateLimitException"""
        with patch(
            "presentation.controllers.user.user_controller.UserController.get_user"
        ) as mock_get_user:
            mock_get_user.side_effect = RateLimitException(
                limit=100, period="hour", retry_after=3600
            )

            response = client.get("/api/v1/users/123")

            assert response.status_code == 429
            data = response.json()
            assert data["error"] is True
            assert data["error_code"] == "RATE_LIMIT_EXCEEDED"
            assert data["details"]["limit"] == 100

    def test_validation_error_handler(self):
        """Testa o handler para erros de validação do Pydantic"""
        response = client.post(
            "/api/v1/users",
            json={
                "email": "not-an-email",  # Email inválido
                # password ausente (obrigatório)
            },
        )

        assert response.status_code == 422
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "validation_errors" in data["details"]

    def test_accept_language_header_pt(self):
        """Testa mensagens em português"""
        with patch("presentation.dependencies.get_user_controller") as mock_controller:
            mock_controller.return_value.get_user.side_effect = NotFoundException(
                message_pt="Usuário não encontrado",
                message_en="User not found",
                resource="user",
                identifier="123",
            )

            response = client.get(
                "/api/v1/users/123", headers={"Accept-Language": "pt-BR"}
            )

            data = response.json()
            assert "Usuário não encontrado" in data["message"]

    def test_accept_language_header_en(self):
        """Testa mensagens em inglês"""
        with patch("presentation.dependencies.get_user_controller") as mock_controller:
            mock_controller.return_value.get_user.side_effect = NotFoundException(
                message_pt="Usuário não encontrado",
                message_en="User not found",
                resource="user",
                identifier="123",
            )

            response = client.get(
                "/api/v1/users/123", headers={"Accept-Language": "en-US"}
            )

            data = response.json()
            assert "User not found" in data["message"]
