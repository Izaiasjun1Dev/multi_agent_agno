import pytest
import sys
from pathlib import Path

# Adiciona o diretório src ao path para importações
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def test_config():
    """Configurações globais para os testes"""
    return {
        "test_mode": True,
        "database_url": "sqlite:///:memory:",
    }


@pytest.fixture
def sample_user_data():
    """Dados de exemplo para testes de usuário"""
    return {
        "id": "user_123",
        "name": "João Silva",
        "email": "joao@example.com",
        "created_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_org_data():
    """Dados de exemplo para testes de organização"""
    return {
        "id": "org_123",
        "name": "Empresa XYZ",
        "created_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_chat_data():
    """Dados de exemplo para testes de chat"""
    return {
        "id": "chat_123",
        "title": "Chat de exemplo",
        "user_id": "user_123",
        "created_at": "2024-01-01T00:00:00Z"
    }
