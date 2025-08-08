from typing import Any, AsyncGenerator, Dict, List, Optional, cast

from agno.agent import Agent as AgnoAgent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from agno.team.team import Team
from langsmith import traceable
from langsmith.wrappers import wrap_anthropic, wrap_openai

from configs.load_env import settings
from core.entities.agent import (
    BaseAgent,
    ComplexityAgent,
    GeneratorImageAgent,
    JudgingBaseAgent,
    TeamAgent,
)
from infraestructure.database.config import AsyncSessionLocal, DatabaseConfig
from infraestructure.telemetry.langsmith.telemetry import LangSmithTelemetry
from interface.agent.agent_interface import AgentInterface


class AgentRepository(AgentInterface):
    def __init__(self) -> None:
        self.db_config = DatabaseConfig()
        self.session = AsyncSessionLocal()
        self.storage = PostgresStorage(
            db_url=self.db_config.database_url,
            table_name="chat_messages",
        )

    @traceable
    async def create_basic_agent_chat(self, agent_data: BaseAgent) -> AgnoAgent:

        agent_chat = AgnoAgent(
            user_id=agent_data.user_id,
            name=agent_data.name,
            session_id=agent_data.user_id,
            agent_id=agent_data.name,
            model=OpenAIChat(
                    id=agent_data.model_id,
                    api_key=settings.openai_api_key,
                    max_tokens=agent_data.configs.max_tokens,
                    temperature=agent_data.configs.temperature,
                )
            ,
            tools=cast(Any, agent_data.tools),
            description=agent_data.description,
            instructions=agent_data.instructions,
            storage=agent_data.storage,
            knowledge=agent_data.knowledge_base,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            debug_mode=True,
        )

        LangSmithTelemetry(agent_chat)

        return agent_chat

    @traceable
    async def create_complexity_agent_chat(
        self, agent_data: ComplexityAgent
    ) -> AgnoAgent:
        """Create a complexity agent for handling complex tasks"""

        agent_chat = AgnoAgent(
            user_id=agent_data.user_id,
            name=agent_data.name,
            session_id=agent_data.session_id,
            agent_id=agent_data.name,
            model=Claude(
                    api_key=settings.anthropic_api_key,
                    id=agent_data.configs.model,
                    max_tokens=agent_data.configs.max_tokens,
                    temperature=agent_data.configs.temperature,
                    default_headers=agent_data.configs.default_headers,
                )
            ,
            reasoning=True,
            reasoning_max_steps=5,
            reasoning_min_steps=2,
            tools=cast(Any, agent_data.tools),
            description=agent_data.description,
            instructions=agent_data.instructions,
            storage=agent_data.storage,
            knowledge=agent_data.knowledge_base,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            debug_mode=True,
        )

        LangSmithTelemetry(agent_chat)

        return agent_chat

    @traceable
    async def create_judge_intent_user_message(
        self, agent_data: JudgingBaseAgent
    ) -> AgnoAgent:
        agent_chat = AgnoAgent(
            user_id=agent_data.user_id,
            name=agent_data.name,
            session_id=agent_data.user_id,
            agent_id=agent_data.name,
            response_model=agent_data.response_model,
            model=OpenAIChat(
                id=agent_data.model_id,
                api_key=settings.openai_api_key,
                max_tokens=agent_data.configs.max_tokens,
                temperature=agent_data.configs.temperature,
            )
            ,
            tools=cast(Any, agent_data.tools),
            description=agent_data.description,
            instructions=agent_data.instructions,
            storage=agent_data.storage,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            debug_mode=True,
        )

        LangSmithTelemetry(agent_chat)

        return agent_chat

    @traceable
    async def create_generator_image_agent_chat(
        self, agent_data: GeneratorImageAgent
    ) -> AgnoAgent:
        agent_chat = AgnoAgent(
            user_id=agent_data.user_id,
            name=agent_data.name,
            session_id=agent_data.user_id,
            agent_id=agent_data.name,  # Usar o nome como ID único do agente
            model=OpenAIChat(
                id="gpt-4o-mini",
                api_key=settings.openai_api_key,
            ),
            tools=cast(Any, agent_data.tools),
            description=agent_data.description,
            instructions=agent_data.instructions,
            storage=agent_data.storage,
            markdown=True,
            show_tool_calls=True,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            debug_mode=True,
        )

        LangSmithTelemetry(agent_chat)

        return agent_chat

    @traceable
    async def create_team_agent_chat(
        self,
        basic_agent_data: BaseAgent,
        judging_agent_data: JudgingBaseAgent,
        generator_agent_data: GeneratorImageAgent,
        complexity_data: ComplexityAgent,
        team_agent_data: TeamAgent,
    ) -> Team:
        inner_team_chat = Team(
            mode="coordinate",
            name=team_agent_data.team_name,
            user_id=team_agent_data.user_id,
            session_id=team_agent_data.session_id,
            model=Claude(
                api_key=settings.anthropic_api_key,
                max_tokens=basic_agent_data.configs.max_tokens,
                temperature=basic_agent_data.configs.temperature,
            ),
            members=[
                await self.create_basic_agent_chat(basic_agent_data),
                await self.create_complexity_agent_chat(complexity_data),
                await self.create_judge_intent_user_message(judging_agent_data),
                await self.create_generator_image_agent_chat(generator_agent_data),
            ],
            instructions=team_agent_data.instructions,
            description=team_agent_data.description,
            storage=basic_agent_data.storage,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            markdown=True,
            debug_mode=True,
        )

        LangSmithTelemetry(inner_team_chat)

        return inner_team_chat
