from typing import Any, Dict, List, Literal, Optional, Type, Union

from agno.agent import Agent as AgnoAgent
from agno.knowledge.agent import AgentKnowledge
from agno.storage.base import Storage
from agno.storage.postgres import PostgresStorage
from agno.tools import Toolkit
from agno.tools.dalle import DalleTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.pgvector import PgVector, SearchType
from pydantic import BaseModel, ConfigDict, Field

from configs.load_env import settings
from infraestructure.database.config import get_database_url


class AgentConfig(BaseModel):
    model: str = Field(
        default=settings.default_model,
        title="Model",
        description="The model to be used by the agent",
    )
    temperature: float = Field(
        default=0.7,
        title="Temperature",
        description="Sampling temperature for the model",
    )
    max_tokens: int = Field(
        default=1000,
        title="Max Tokens",
        description="Maximum number of tokens to generate",
    )
    top_p: float = Field(
        default=1.0, title="Top P", description="Nucleus sampling parameter"
    )
    frequency_penalty: float = Field(
        default=0.0,
        title="Frequency Penalty",
        description="Penalty for frequent tokens",
    )
    presence_penalty: float = Field(
        default=0.0, title="Presence Penalty", description="Penalty for new tokens"
    )


class AntropicConfig(BaseModel):
    model: str = Field(
        default=settings.default_anthropic_model,
        title="Model",
        description="The model to be used by the agent",
    )
    temperature: float = Field(
        default=0.5,
        title="Temperature",
        description="Sampling temperature for the model",
    )
    default_headers: Dict[str, str] = Field(
        default={"anthropic-beta": "code-execution-2025-05-22"},
        title="Default Headers",
        description="Default headers for Anthropic API requests",
    )
    max_tokens: int = Field(
        default=5000,
        title="Max Tokens",
        description="Maximum number of tokens to generate",
    )
    top_p: float = Field(
        default=1.0, title="Top P", description="Nucleus sampling parameter"
    )


class BaseAgent(BaseModel):
    model_id: str = Field(
        default="gpt-4o-mini",
        title="Model ID",
        description="Identifier for the agent model",
    )
    user_id: Optional[str] = Field(
        None, title="User ID", description="ID of the user who owns the agent"
    )
    session_id: Optional[str] = Field(
        None, title="Session ID", description="ID of the session for the agent"
    )
    name: str = Field(..., title="Name", description="Name of the agent")
    tools: Optional[List[Toolkit]] = Field(
        default=[DuckDuckGoTools()],
        title="Tools",
        description="List of tools the agent can use",
    )
    storage: Optional[Storage] = Field(
        default=PostgresStorage(
            db_url=get_database_url(),
            table_name="chat_messages",
        ),
        title="Storage",
        description="Storage mechanism for the agent",
    )
    configs: AgentConfig = Field(
        default=AgentConfig(),
        title="Configurations",
        description="Configuration settings for the agent",
    )
    description: Optional[str] = Field(
        None, title="Description", description="Description of the agent"
    )
    instructions: Optional[str] = Field(
        None, title="Instructions", description="Instructions for the agent"
    )
    knowledge_base: Optional[AgentKnowledge] = Field(
        default=AgentKnowledge(
            vector_db=PgVector(
                db_url=get_database_url(),
                table_name="agent_knowledge_base",
                search_type=SearchType.hybrid,
            )
        ),
        title="Knowledge Base",
        description="Knowledge base for the agent",
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class ComplexityAgent(BaseAgent):
    """Base class for complex agents that handle more sophisticated tasks"""

    tools: Optional[List[Union[Toolkit, Dict[str, str]]]] = Field(
        default=[
            DalleTools(),
            DuckDuckGoTools(),
            {
                "type": "code_execution_20250522",
                "name": "code_execution",
            },
        ],
        title="Tools",
        description="List of tools the agent can use for complex tasks",
    )
    description: str = "You are an AI agent that handles complex tasks."
    instructions: str = (
        "When the user asks you to perform a complex task, use the appropriate tools to complete it."
    )
    configs: AntropicConfig = Field(
        default=AntropicConfig(),
        title="Configurations",
        description="Configuration settings for the complex agent",
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class OutputIntent(BaseModel):
    """Model for the output intent of a user message"""

    intent: List[
        Literal[
            "generate_image",
            "complexity_task",
            "simple_task",
        ]
    ] = Field(
        default=["simple_task"],
        title="Intent",
        description="The intent of the user message",
    )


class JudgingBaseAgent(BaseAgent):
    """Base class for agents that judge user messages"""

    tools: Optional[List[Toolkit]] = Field(
        default=[],
        title="Tools",
        description="List of tools the agent can use for judging intents",
    )
    response_model: Type = Field(
        default=OutputIntent,
        title="Response Model",
        description="Model for the response of the agent when judging intents of last 5 user messages",
    )
    configs: AgentConfig = Field(
        default=AgentConfig(
            max_tokens=30,
            temperature=0.0,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        ),
        title="Configurations",
        description="Configuration settings for the agent when judging intents",
    )
    description: str = "You are an AI agent that judges the intent of user messages."
    instructions: str = """
        analize a mensagem do usuario e retorne a intenção
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class GeneratorImageAgent(BaseAgent):
    """Base class for agents that generate images"""

    tools: Optional[List[Toolkit]] = Field(
        default=[
            DalleTools(
                api_key=settings.openai_api_key,
                model="dall-e-3",
            )
        ],
        title="Tools",
        description="List of tools the agent can use for generating images",
    )
    description: str = (
        "You are an AI agent specialized in generating high-quality images using DALL-E."
    )
    instructions: str = (
        "You are an expert image generator. When the user requests an image, use the `create_image` tool to generate it. "
        "Always provide detailed prompts to create high-quality, visually appealing images. "
        "After generating the image, provide the image URL(s) in your response."
    )
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class TeamAgent(BaseModel):
    """Model for a team of agents"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    members: Optional[List[AgnoAgent]] = Field(
        None, title="Members", description="List of agent members in the team"
    )
    user_id: str = Field(
        ..., title="User ID", description="ID of the user who owns the team"
    )
    session_id: str = Field(
        ..., title="Session ID", description="ID of the session for the team"
    )
    team_name: str = Field(..., title="Team Name", description="Name of the team")
    description: Optional[str] = Field(
        None, title="Description", description="Description of the team"
    )
    instructions: Optional[str] = Field(
        default="""Você é um coordenador de equipe de IA que analisa mensagens e delega tarefas para agentes especializados.

            CRITÉRIOS DE CLASSIFICAÇÃO:
            - GENERATE_IMAGE: Criação, geração ou produção de imagens
            - COMPLEXITY_TASK: Análise complexa, programação, relatórios, múltiplas etapas
            - SIMPLE_TASK: Perguntas diretas, explicações, conversação casual

            PROCESSO:
            1. Identifique a intenção da mensagem
            2. Selecione o agente apropriado:
            - Agent 1 (gpt-4o-mini): Tarefas simples
            - Agent 2 (gpt-4o-mini): Tarefas complexas  
            - Agent 4 (gpt-4o-mini): Geração de imagens
            3. Delegue usando transfer_task_to_member

            FORMATO DE RESPOSTA:
            ANÁLISE: [Intenção identificada]
            AGENTE: [Agente selecionado] 
            PROCESSANDO: [Delegando tarefa...]

            Seja direto e conciso. Evite explicações longas.
        """,
        title="Instructions",
        description="Instructions for the team",
    )
