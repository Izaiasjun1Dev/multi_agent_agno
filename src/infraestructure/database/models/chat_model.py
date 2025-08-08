"""
Modelo SQLAlchemy para chat e mensagens de chat
SQLAlchemy model for chat and chat messages
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from infraestructure.database.config import Base


class ChatModel(Base):
    """
    Modelo SQLAlchemy para chat
    SQLAlchemy model for chat
    """

    __tablename__ = "chats"

    chat_id = Column(String(36), primary_key=True, nullable=False)
    user_id = Column(
        String(36), nullable=False, index=True
    )  # Referência ao usuário no DynamoDB
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamento com mensagens
    messages = relationship(
        "ChatMessageModel", back_populates="chat", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ChatModel(chat_id='{self.chat_id}', user_id='{self.user_id}')>"


class ChatMessageModel(Base):
    """
    Modelo SQLAlchemy para mensagem de chat
    SQLAlchemy model for chat message
    """

    __tablename__ = "chat_messages"

    message_id = Column(String(36), primary_key=True, nullable=False)
    chat_id = Column(
        String(36), ForeignKey("chats.chat_id"), nullable=False, index=True
    )
    user_id = Column(
        String(36), nullable=False, index=True
    )  # Referência ao usuário no DynamoDB
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento com chat
    chat = relationship("ChatModel", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessageModel(message_id='{self.message_id}', chat_id='{self.chat_id}')>"
