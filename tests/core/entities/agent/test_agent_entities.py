"""Testes para as entidades de agentes"""

import pytest
from agno.tools.dalle import DalleTools
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import ValidationError

from src.core.entities.agent import (
    AgentConfig,
    BaseAgent,
    ComplexityAgent,
    GeneratorImageAgent,
    JudgingBaseAgent,
    TeamAgent,
)


class TestAgentConfig:
    """Testes para AgentConfig"""

    def test_agent_config_default_values(self):
        """Testa os valores padrão do AgentConfig"""
        config = AgentConfig()

        assert config.temperature == 0.7  # Valor real do padrão
        assert config.max_tokens == 1000  # Valor real do padrão
        assert config.top_p == 1.0
        assert config.frequency_penalty == 0.0
        assert config.presence_penalty == 0.0

    def test_agent_config_custom_values(self):
        """Testa valores customizados do AgentConfig"""
        config = AgentConfig(
            temperature=0.8,
            max_tokens=2000,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.3,
        )

        assert config.temperature == 0.8
        assert config.max_tokens == 2000
        assert config.top_p == 0.9
        assert config.frequency_penalty == 0.5
        assert config.presence_penalty == 0.3


class TestBaseAgent:
    """Testes para BaseAgent"""

    def test_base_agent_creation(self):
        """Testa a criação de um BaseAgent"""
        agent = BaseAgent(name="test_agent", user_id="user123", session_id="session123")

        assert agent.name == "test_agent"
        assert agent.user_id == "user123"
        assert agent.session_id == "session123"
        assert agent.model_id == "gpt-4o-mini"  # valor padrão
        assert agent.tools is not None
        if agent.tools:
            assert len(agent.tools) == 1  # DuckDuckGoTools por padrão
            assert isinstance(agent.tools[0], DuckDuckGoTools)

    def test_base_agent_minimal(self):
        """Testa BaseAgent com apenas nome obrigatório"""
        agent = BaseAgent(name="test_agent")

        assert agent.name == "test_agent"
        assert agent.user_id is None
        assert agent.session_id is None
        assert agent.model_id == "gpt-4o-mini"

    def test_base_agent_custom_tools(self):
        """Testa BaseAgent com ferramentas customizadas"""
        agent = BaseAgent(name="test_agent", tools=[DalleTools(), DuckDuckGoTools()])

        assert agent.tools is not None
        if agent.tools:
            assert len(agent.tools) == 2
            assert any(isinstance(tool, DalleTools) for tool in agent.tools)
            assert any(isinstance(tool, DuckDuckGoTools) for tool in agent.tools)


class TestComplexityAgent:
    """Testes para ComplexityAgent"""

    def test_complexity_agent_creation(self):
        """Testa a criação de um ComplexityAgent"""
        agent = ComplexityAgent(
            name="complex_agent", user_id="user123", session_id="session123"
        )

        assert agent.name == "complex_agent"
        assert "complex tasks" in agent.description  # Texto real da descrição
        assert "complex task" in agent.instructions  # Texto real das instruções
        assert agent.tools is not None

    def test_complexity_agent_inherits_base(self):
        """Testa que ComplexityAgent herda de BaseAgent"""
        agent = ComplexityAgent(name="test", user_id="user123", session_id="session123")
        assert isinstance(agent, BaseAgent)


class TestJudgingBaseAgent:
    """Testes para JudgingBaseAgent"""

    def test_judging_agent_creation(self):
        """Testa a criação de um JudgingBaseAgent"""
        agent = JudgingBaseAgent(
            name="judge_agent", user_id="user123", session_id="session123"
        )

        assert agent.name == "judge_agent"
        assert (
            "judges the intent" in agent.description.lower()
        )  # Texto real da descrição
        assert agent.tools == []  # Não tem ferramentas
        assert agent.response_model is not None

    def test_judging_agent_inherits_base(self):
        """Testa que JudgingBaseAgent herda de BaseAgent"""
        agent = JudgingBaseAgent(
            name="test", user_id="user123", session_id="session123"
        )
        assert isinstance(agent, BaseAgent)


class TestGeneratorImageAgent:
    """Testes para GeneratorImageAgent"""

    def test_generator_image_agent_creation(self):
        """Testa a criação de um GeneratorImageAgent"""
        agent = GeneratorImageAgent(
            name="image_agent", user_id="user123", session_id="session123"
        )

        assert agent.name == "image_agent"
        assert "DALL-E" in agent.description
        assert "create_image" in agent.instructions
        assert agent.tools is not None
        if agent.tools:
            assert len(agent.tools) == 1
            assert isinstance(agent.tools[0], DalleTools)

    def test_generator_image_agent_inherits_base(self):
        """Testa que GeneratorImageAgent herda de BaseAgent"""
        agent = GeneratorImageAgent(
            name="test", user_id="user123", session_id="session123"
        )
        assert isinstance(agent, BaseAgent)


class TestTeamAgent:
    """Testes para TeamAgent"""

    def test_team_agent_creation(self):
        """Testa a criação de um TeamAgent"""
        team = TeamAgent(
            team_name="test_team", user_id="user123", session_id="session123"
        )

        assert team.team_name == "test_team"
        assert team.user_id == "user123"
        assert team.session_id == "session123"
        assert team.members is None
        assert team.description is None

    def test_team_agent_with_description(self):
        """Testa TeamAgent com descrição"""
        team = TeamAgent(
            team_name="test_team",
            user_id="user123",
            session_id="session123",
            description="Team de teste",
        )

        assert team.description == "Team de teste"
        assert team.members is None

    def test_team_agent_requires_fields(self):
        """Testa que TeamAgent requer campos obrigatórios"""
        with pytest.raises(ValidationError):
            TeamAgent()  # Deve falhar sem team_name, user_id e session_id

    def test_team_agent_with_custom_instructions(self):
        """Testa TeamAgent com instruções customizadas"""
        custom_instructions = "Instruções customizadas para o team"
        team = TeamAgent(
            team_name="test_team",
            user_id="user123",
            session_id="session123",
            instructions=custom_instructions,
        )

        assert team.instructions == custom_instructions
        assert team.members is None
