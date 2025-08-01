from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


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
    messages: List[str] = Field(
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