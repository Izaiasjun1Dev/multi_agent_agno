"""
Exceções relacionadas ao chat.
Chat related exceptions.
"""

from .chat_exceptions import (
    ChatAccessDeniedException,
    ChatConnectionException,
    ChatCreationException,
    ChatDeletionException,
    ChatListException,
    ChatMessageException,
    ChatNotFoundException,
    ChatParticipantException,
    ChatUpdateException,
    ChatValidationException,
)

__all__ = [
    "ChatCreationException",
    "ChatNotFoundException",
    "ChatUpdateException",
    "ChatDeletionException",
    "ChatListException",
    "ChatAccessDeniedException",
    "ChatMessageException",
    "ChatParticipantException",
    "ChatValidationException",
    "ChatConnectionException",
]
