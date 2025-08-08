from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List

from core.dtos.agent.agent_dtos import CreateAgentDTO


class AgentControllerInterface(ABC):
    """
    Interface for AgentController
    """

    @abstractmethod
    async def create_agent(
        self, token: str, agent_data: CreateAgentDTO
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def stream_chat_response(
        self, token: str, messages: List[Dict[str, Any]]
    ) -> AsyncGenerator:
        pass
