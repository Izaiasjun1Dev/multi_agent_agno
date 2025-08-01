from abc import ABC, abstractmethod
from typing import Any, Dict, List

from core.entities.user import User


class UserPresenterInterface(ABC):
    """Interface para o presenter de usuário seguindo Clean Architecture"""

    @abstractmethod
    def present_user_created(self, user: User) -> Dict[str, Any]:
        """Apresenta o resultado da criação de usuário"""
        pass

    @abstractmethod
    def present_user(self, user: User) -> Dict[str, Any]:
        """Apresenta um usuário"""
        pass

    @abstractmethod
    def present_users_list(self, users: List[User]) -> Dict[str, Any]:
        """Apresenta uma lista de usuários"""
        pass

    @abstractmethod
    def present_user_updated(self, user: User) -> Dict[str, Any]:
        """Apresenta o resultado da atualização de usuário"""
        pass

    @abstractmethod
    def present_error(self, error: Exception) -> Dict[str, Any]:
        """Apresenta um erro"""
        pass
