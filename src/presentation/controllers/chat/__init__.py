from abc import ABC, abstractmethod
from typing import Dict, Any
from core.dtos.chat.chat_dtos import CreateChatResponseDto


class ChatControllerInterface(ABC):
    """Interface para o controller de chat seguindo Clean Architecture"""

    @abstractmethod
    async def create_chat(self, token: str) -> CreateChatResponseDto:
        """Cria um novo chat"""
        pass
