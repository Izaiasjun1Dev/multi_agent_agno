from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AgentPresenterInterface(ABC):
    @abstractmethod
    def present_agent_creation(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Apresenta o resultado da criação de um agente"""
        pass
    
    @abstractmethod
    def present_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Apresenta um agente"""
        pass
    
    