import logging
from typing import Any, Dict, List
from uuid import uuid4

from core.dtos.chat.chat_dtos import CreateChatResponseDto
from core.entities.chat import Chat
from interface.auth.auth_interface import AuthInterface
from interface.chat.chat_interface import ChatInterface, AsyncChatInterface


logger = logging.getLogger(__name__)


class CreateChatUseCase:
    """
    Caso de uso para criação de um chat
    """

    def __init__(
        self,
        chat_interface: ChatInterface,
        auth_interface: AuthInterface,
    ):
        self.chat_interface = chat_interface
        self.auth_interface = auth_interface

    def execute(
        self,
        token: str,
    ) -> CreateChatResponseDto:
        """
        Cria um novo chat
        """
        user = self.auth_interface.get_user_details(token)
        if not user:
            raise ValueError("Invalid token")

        if not user.is_active:
            raise ValueError("User is not active")
        
        if not user.user_id:
            raise ValueError("User not found")
        
        chat = Chat(
            userId=user.user_id,
            chatId=str(uuid4()),
            isActive=True,
            messages=[],
        )

        try:
            self.chat_interface.create_chat(
                chat_data=chat
            )

            return CreateChatResponseDto(
                chat_id=chat.chat_id, message="Chat created successfully"
            )
            
        except Exception as e:
            logger.error(f"Failed to create chat: {str(e)}")
            raise ValueError("Failed to create chat") from e
        
        
class AsyncCreateChatUseCase:
    """
    Caso de uso assíncrono para criação de um chat
    """

    def __init__(
        self,
        chat_interface: AsyncChatInterface,
        auth_interface: AuthInterface,
    ):
        self.chat_interface = chat_interface
        self.auth_interface = auth_interface

    async def execute(
        self,
        token: str,
    ) -> CreateChatResponseDto:
        """
        Cria um novo chat de forma assíncrona
        """
        user = self.auth_interface.get_user_details(token)
        if not user:
            raise ValueError("Invalid token")
        
        if not user.is_active:
            raise ValueError("User is not active")
        
        if not user.user_id:
            raise ValueError("User not found")
        
        chat = Chat(
            userId=user.user_id,
            chatId=str(uuid4()),
            isActive=True,
            messages=[],
        )
        
        try:
            await self.chat_interface.create_chat(
                chat_data=chat
            )

            return CreateChatResponseDto(
                chat_id=chat.chat_id, message="Chat created successfully"
            )
        except Exception as e:
            logger.error(f"Failed to create chat: {str(e)}")
            raise ValueError("Failed to create chat") from e
