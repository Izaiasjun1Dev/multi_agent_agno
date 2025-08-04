from abc import ABC, abstractmethod
from typing import Any, Dict

from core.dtos.user.user_dtos import CreateRequestUserDto


class UserControllerInterface(ABC):
    """Interface para o controller de usuário seguindo Clean Architecture"""

    @abstractmethod
    async def create_user(self, user_data: CreateRequestUserDto) -> Dict[str, Any]:
        """Cria um novo usuário"""
        pass

    @abstractmethod
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Obtém um usuário por ID"""
        pass

    @abstractmethod
    async def update_user(
        self, user_id: str, user_data: CreateRequestUserDto
    ) -> Dict[str, Any]:
        """Atualiza um usuário"""
        pass
