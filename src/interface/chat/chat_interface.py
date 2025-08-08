from abc import ABC, abstractmethod
from typing import Any, Dict, List

from core.entities.chat import Chat


class AsyncChatInterface(ABC):
    @abstractmethod
    async def get_chats(self, user_id: str) -> List[Chat]:
        """
        Retrieve a list of chats for a given user.

        :param user_id: Unique identifier for the user.
        :return: List of chats associated with the user.
        """
        pass

    @abstractmethod
    async def create_chat(self, chat_data: Chat) -> Chat:
        """
        Create a new chat for a given user.

        :param user_id: Unique identifier for the user.
        :param chat_data: Data for the new chat.
        :return: Details of the created chat.
        """
        pass
    
    @abstractmethod
    async def update_chat(self, chat_id: str, chat_data: Chat) -> Chat:
        """
        Update an existing chat.

        :param chat_id: Unique identifier for the chat to be updated.
        :param chat_data: Updated data for the chat.
        :return: Updated chat details.
        """
        pass

    @abstractmethod
    async def delete_chat(self, chat_id: str) -> bool:
        """
        Delete a chat by its ID.

        :param chat_id: Unique identifier for the chat to be deleted.
        :return: True if deletion was successful, False otherwise.
        """
        pass


class ChatInterface(ABC):
    @abstractmethod
    def get_chats(self, user_id: str) -> List[Chat]:
        """
        Retrieve a list of chats for a given user.

        :param user_id: Unique identifier for the user.
        :return: List of chats associated with the user.
        """
        pass

    @abstractmethod
    def create_chat(self, chat_data: Chat) -> Chat:
        """
        Create a new chat for a given user.

        :param user_id: Unique identifier for the user.
        :param chat_data: Data for the new chat.
        :return: Details of the created chat.
        """
        pass
    
    @abstractmethod
    def update_chat(self, chat_id: str, chat_data: Chat) -> Chat:
        """
        Update an existing chat.

        :param chat_id: Unique identifier for the chat to be updated.
        :param chat_data: Updated data for the chat.
        :return: Updated chat details.
        """
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> bool:
        """
        Delete a chat by its ID.

        :param chat_id: Unique identifier for the chat to be deleted.
        :return: True if deletion was successful, False otherwise.
        """
        pass
