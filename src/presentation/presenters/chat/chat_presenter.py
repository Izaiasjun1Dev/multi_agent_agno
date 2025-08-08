from typing import Any, Dict, List
from fastapi import status
from core.entities.chat import Chat
from core.exceptions.base_exceptions import BaseApplicationException
from presentation.presenters.chat import ChatPresenterInterface


class ChatPresenter(ChatPresenterInterface):
    """Presenter responsável pela formatação das respostas de chat"""

    def present_chat_creation(self, chat: Chat) -> Dict[str, Any]:
        """Apresenta o resultado da criação de um chat"""
        return {
            "success": True,
            "chat": self._format_chat(chat),
        }

    def present_chat(self, chat: Chat) -> Dict[str, Any]:
        """Apresenta um chat"""
        return {
            "success": True,
            "chat": self._format_chat(chat),
        }

    def present_chats_list(self, chats: List[Chat]) -> Dict[str, Any]:
        """Apresenta uma lista de chats"""
        return {
            "success": True,
            "chats": [self._format_chat(chat) for chat in chats],
            "total": len(chats),
        }

    def present_chat_updated(self, chat: Chat) -> Dict[str, Any]:
        """Apresenta o resultado da atualização de um chat"""
        return {
            "success": True,
            "chat": self._format_chat(chat),
        }

    def present_error(self, error: Exception) -> Dict[str, Any]:
        """Apresenta um erro"""
        if isinstance(error, BaseApplicationException):
            return {
                "error": True,
                "error_code": error.error_code,
                "message": error.message_pt,
                "status_code": error.status_code,
            }
        return {
            "error": True,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": str(error),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

    def _format_chat(self, chat: Chat) -> Dict[str, Any]:
        """Formata os dados do chat para a resposta"""
        return {
            "id": chat.chat_id,
            "user_id": chat.user_id,
            "messages": chat.messages,
            "created_at": chat.created_at.isoformat() if chat.created_at else None,
            "updated_at": chat.updated_at.isoformat() if chat.updated_at else None,
        }