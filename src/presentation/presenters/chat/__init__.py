from abc import ABC, abstractmethod
from typing import Any, Dict, List

from core.entities.chat import Chat


class ChatPresenterInterface(ABC):
    """Interface para o presenter de chat seguindo Clean Architecture"""

    @abstractmethod
    def present_chat_creation(self, chat: Chat) -> Dict[str, Any]:
        """Apresenta o resultado da criação de um chat"""
        pass

    @abstractmethod
    def present_chat(self, chat: Chat) -> Dict[str, Any]:
        """Apresenta um chat"""
        pass

    @abstractmethod
    def present_chats_list(self, chats: List[Chat]) -> Dict[str, Any]:
        """Apresenta uma lista de chats"""
        pass

    @abstractmethod
    def present_chat_updated(self, chat: Chat) -> Dict[str, Any]:
        """Apresenta o resultado da atualização de um chat"""
        pass

    @abstractmethod
    def present_error(self, error: Exception) -> Dict[str, Any]:
        """Apresenta um erro"""
        pass
