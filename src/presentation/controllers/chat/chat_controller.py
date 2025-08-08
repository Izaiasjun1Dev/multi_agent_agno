from typing import Any, Dict
from core.dtos.chat.chat_dtos import CreateChatResponseDto
from presentation.controllers.chat import ChatControllerInterface
from core.usecases.chat.chat_usecases import AsyncCreateChatUseCase, CreateChatUseCase



class ChatController(ChatControllerInterface):
    """Implementação do controller de chat seguindo a interface"""

    def __init__(
        self, create_chat_usecase: CreateChatUseCase
    ) -> None:
        """Inicializa o controller com o caso de uso de criação de chat"""
        self.create_chat_usecase = create_chat_usecase

    def create_chat(self, token: str) -> CreateChatResponseDto:
        return self.create_chat_usecase.execute(token)
    
    
class AsyncChatController(ChatControllerInterface):
    """Implementação assíncrona do controller de chat seguindo a interface"""

    def __init__(
        self, create_chat_usecase: AsyncCreateChatUseCase
    ) -> None:
        """Inicializa o controller com o caso de uso assíncrono de criação de chat"""
        self.create_chat_usecase = create_chat_usecase

    async def create_chat(self, token: str) -> CreateChatResponseDto:
        return await self.create_chat_usecase.execute(token)