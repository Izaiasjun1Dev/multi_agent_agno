from abc import ABC, abstractmethod
from typing import Dict, Any


class AuthControllerInterface(ABC):
    """Interface para o controller de autenticação seguindo Clean Architecture"""

    @abstractmethod
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Realiza o login do usuário e retorna os detalhes de autenticação"""
        pass
    
    