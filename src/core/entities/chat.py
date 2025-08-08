from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """Modelo de mensagem de chat"""
    message_id: str = Field(
        ...,
        title="Message ID",
        description="Unique identifier for the message",
        alias="messageId"
    )
    user_id: str = Field(
        ...,
        title="User ID",
        description="Identifier of the user who sent the message",
        alias="userId"
    )
    content: str = Field(
        ...,
        title="Content",
        description="Content of the message",
        alias="content"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(),
        title="Timestamp",
        description="Timestamp when the message was sent",
        alias="timestamp"
    )


class Chat(BaseModel):
    chat_id: str = Field(
        ...,
        title="Chat ID",
        description="Unique identifier for the chat",
        alias="chatId"
    )
    user_id: str = Field(
        ...,
        title="User ID",
        description="Identifier of the user associated with the chat",
        alias="userId"
    )
    messages: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        title="Messages",
        description="List of messages in the chat",
        alias="messages"
    )
    is_active: bool = Field(
        True,
        title="Active Status",
        description="Indicates if the chat is active",
        alias="isActive"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        title="Creation Timestamp",
        description="Timestamp when the chat was created",
        alias="createdAt"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        title="Update Timestamp",
        description="Timestamp when the chat was last updated",
        alias="updatedAt"
    )