from datetime import datetime

import pytest

from core.entities.chat import Chat
from core.entities.org import Org
from core.entities.user import User


class TestUser:
    """Testes para a entidade User"""

    def test_user_creation_with_required_fields(self):
        """Testa criação de usuário com campos obrigatórios"""
        user = User(
            userId="user_123",
            email="test@example.com",
            name=None,
            org="org_123",
            isActive=True,
            slug="test-user",
            avatarUrl=None,
        )

        assert user.user_id == "user_123"
        assert user.email == "test@example.com"
        assert user.org_id == "org_123"
        assert user.is_active is True
        assert user.slug == "test-user"
        assert user.avatar_url is None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_creation_with_optional_fields(self):
        """Testa criação de usuário com campos opcionais"""
        user = User(
            userId="user_123",
            email="test@example.com",
            name="Test User",
            org="org_123",
            isActive=True,
            slug="test-user",
            avatarUrl="https://example.com/avatar.jpg",
            roles=["admin", "user"],
        )

        assert user.name == "Test User"
        assert user.avatar_url == "https://example.com/avatar.jpg"
        assert user.roles == ["admin", "user"]

    def test_user_default_values(self):
        """Testa valores padrão do usuário"""
        user = User(
            userId="user_123",
            email="test@example.com",
            name=None,
            org="org_123",
            isActive=True,
            slug="test-user",
            avatarUrl=None,
        )

        assert user.roles == []
        assert user.chats == []
        assert user.is_active is True

    def test_user_validation(self):
        """Testa validação de email"""
        with pytest.raises(ValueError):
            User(
                userId="user_123",
                email="invalid-email",
                name=None,
                org="org_123",
                isActive=True,
                slug="test-user",
                avatarUrl=None,
            )
