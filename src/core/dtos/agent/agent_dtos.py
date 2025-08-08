from typing import Any, Dict, List

from pydantic import BaseModel, Field


class CreateAgentDTO(BaseModel):
    name: str = Field(..., description="Nome do agente")
    description: str = Field(..., description="Descrição do agente")
    instructions: str = Field(..., description="Instruções específicas para o agente")


class ChatMessageDTO(BaseModel):
    role: str = Field(..., description="Papel da mensagem (user, assistant, system)")
    content: str = Field(..., description="Conteúdo da mensagem")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadados adicionais da mensagem"
    )


class StreamChatRequestDTO(BaseModel):
    messages: List[ChatMessageDTO] = Field(
        ..., description="Lista de mensagens para processar"
    )
