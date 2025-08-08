from presentation.presenters.agent import AgentPresenterInterface
from typing import Any, Dict, List


class AgentPresenter(AgentPresenterInterface):
    """Presenter responsável pela formatação das respostas de agente"""

    def present_agent_creation(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Apresenta o resultado da criação de um agente"""
        return {
            "success": True,
            "agent": agent,
        }

    def present_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Apresenta um agente"""
        return {
            "success": True,
            "agent": agent,
        }

    def present_agents_list(self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apresenta uma lista de agentes"""
        return {
            "success": True,
            "agents": agents,
            "total": len(agents),
        }
        
    def _forma_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Formata os dados do agente para a resposta"""
        return {
            "id": agent.get("agent_id"),
            "name": agent.get("name"),
            "description": agent.get("description"),
            "created_at": agent.get("created_at"),
            "updated_at": agent.get("updated_at"),
        }