from pydantic import BaseModel, Field
from typing import Optional, List


class AgentInputDto(BaseModel):
    user_id: str = Field(..., description="ID do usuário que está interagindo com o agente")
    message: str = Field(..., description="Mensagem do usuário para o agente")
    chat_history: Optional[List[dict]] = Field(
        None, description="Histórico de mensagens anteriores na conversa"
    )
    
    