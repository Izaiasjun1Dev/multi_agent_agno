from typing import List, Optional

from core.entities.chat import Chat
from core.exceptions.chat import (
    ChatCreationException,
    ChatDeletionException,
    ChatListException,
    ChatNotFoundException,
    ChatUpdateException,
)
from infraestructure.database.config import AsyncSessionLocal
from interface.chat.chat_interface import AsyncChatInterface


class PostgresChatRepository(AsyncChatInterface):
    """
    Repositório de chat para PostgreSQL
    PostgreSQL chat repository
    """

    def __init__(self):
        """
        Inicializa o repositório com a factory de sessão do banco de dados
        Initializes the repository with the database session factory
        """
        self.session_factory = AsyncSessionLocal

    async def create_chat(self, chat_data: Chat) -> Chat:
        """
        Cria um novo chat no banco de dados
        Creates a new chat in the database
        """
        from infraestructure.database.models import ChatModel

        async with self.session_factory() as session:
            try:
                new_chat = ChatModel(**chat_data.model_dump())
                session.add(new_chat)
                await session.commit()
                await session.refresh(new_chat)
                return Chat(
                    chatId=str(new_chat.chat_id),
                    userId=str(new_chat.user_id),
                    isActive=bool(new_chat.is_active),
                    messages=[],
                )

            except Exception as e:
                await session.rollback()
                raise ChatCreationException(
                    details={
                        "original_error": str(e),
                        "user_id": chat_data.user_id,
                        "operation": "create_chat",
                    }
                ) from e

    async def get_chats(self, user_id: str) -> Optional[List[Chat]]:
        """
        Obtém todos os chats de um usuário
        Gets all chats of a user
        """
        from sqlalchemy import select

        from infraestructure.database.models import ChatModel

        try:
            async with self.session_factory() as session:
                result = await session.execute(
                    select(ChatModel).filter(ChatModel.user_id == user_id)
                )
                chats = result.scalars().all()
                return (
                    [
                        Chat(
                            chatId=str(chat.chat_id),
                            userId=str(chat.user_id),
                            isActive=bool(chat.is_active),
                            messages=[],
                        )
                        for chat in chats
                    ]
                    if chats
                    else []
                )
        except Exception as e:
            raise ChatListException(
                details={
                    "original_error": str(e),
                    "user_id": user_id,
                    "operation": "get_chats",
                }
            ) from e

    async def update_chat(self, chat_id: str, chat_data: Chat) -> Optional[Chat]:
        """
        Atualiza um chat existente
        Updates an existing chat
        """
        from infraestructure.database.models import ChatModel

        try:
            async with self.session_factory() as session:
                chat = await session.get(ChatModel, chat_id)
                if not chat:
                    raise ChatNotFoundException(
                        details={"chat_id": chat_id, "operation": "update_chat"}
                    )

                for key, value in chat_data.model_dump().items():
                    setattr(chat, key, value)

                await session.commit()
                return Chat(
                    chatId=str(chat.chat_id),
                    userId=str(chat.user_id),
                    isActive=bool(chat.is_active),
                    messages=[],
                )
        except ChatNotFoundException:
            # Re-raise ChatNotFoundException as is
            raise
        except Exception as e:
            raise ChatUpdateException(
                details={
                    "original_error": str(e),
                    "chat_id": chat_id,
                    "operation": "update_chat",
                }
            ) from e

    async def delete_chat(self, chat_id: str) -> bool:
        """
        Deleta um chat pelo ID
        Deletes a chat by ID
        """
        from infraestructure.database.models import ChatModel

        try:
            async with self.session_factory() as session:
                chat = await session.get(ChatModel, chat_id)
                if not chat:
                    raise ChatNotFoundException(
                        details={"chat_id": chat_id, "operation": "delete_chat"}
                    )

                await session.delete(chat)
                await session.commit()
                return True
        except ChatNotFoundException:
            # Re-raise ChatNotFoundException as is
            raise
        except Exception as e:
            raise ChatDeletionException(
                details={
                    "original_error": str(e),
                    "chat_id": chat_id,
                    "operation": "delete_chat",
                }
            ) from e

    async def list_chats(self, user_id: str) -> list[Chat]:
        """
        Lista todos os chats de um usuário
        Lists all chats of a user
        """
        from sqlalchemy import select

        from infraestructure.database.models import ChatModel

        try:
            async with self.session_factory() as session:
                result = await session.execute(
                    select(ChatModel).filter(ChatModel.user_id == user_id)
                )
                chats = result.scalars().all()
                return (
                    [
                        Chat(
                            chatId=str(chat.chat_id),
                            userId=str(chat.user_id),
                            isActive=bool(chat.is_active),
                            messages=[],
                        )
                        for chat in chats
                    ]
                    if chats
                    else []
                )
        except Exception as e:
            raise ChatListException(
                details={
                    "original_error": str(e),
                    "user_id": user_id,
                    "operation": "list_chats",
                }
            ) from e
