from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional

from agno.agent import Agent
from agno.team.team import Team

from core.entities.agent import (
    BaseAgent,
    ComplexityAgent,
    GeneratorImageAgent,
    JudgingBaseAgent,
    TeamAgent,
)


class AgentInterface(ABC):
    @abstractmethod
    async def create_basic_agent_chat(self, agent_data: BaseAgent) -> Agent:
        """Response all basic questions with a basic agent"""
        pass

    @abstractmethod
    async def create_complexity_agent_chat(self, agent_data: BaseAgent) -> Agent:
        """Response all complex questions with a complex agent"""
        pass

    @abstractmethod
    async def create_judge_intent_user_message(
        self, agent_data: JudgingBaseAgent
    ) -> Agent:
        """Judge the intent of a user message"""
        pass

    @abstractmethod
    async def create_generator_image_agent_chat(
        self, agent_data: GeneratorImageAgent
    ) -> Agent:
        """Create a new image generator agent"""
        pass

    @abstractmethod
    async def create_team_agent_chat(
        self,
        basic_agent_data: BaseAgent,
        judging_agent_data: JudgingBaseAgent,
        generator_agent_data: GeneratorImageAgent,
        complexity_data: ComplexityAgent,
        team_agent_data: TeamAgent,
    ) -> Team:
        """Create a team of agents"""
        pass