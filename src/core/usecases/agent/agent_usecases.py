from typing import Any, AsyncGenerator, Dict, List, Optional
from uuid import uuid4

from agno.agent import Agent
from agno.team.team import Team

from core.dtos.auth.auth_dtos import UserDetailsResponseDto
from core.entities.agent import (
    BaseAgent,
    ComplexityAgent,
    GeneratorImageAgent,
    JudgingBaseAgent,
    TeamAgent,
)
from core.exceptions.agent import (
    AgentAuthenticationException,
    AgentCreationException,
    AgentStreamException,
)
from interface.agent.agent_interface import AgentInterface
from interface.auth.auth_interface import AuthInterface


class CreateAgentUseCase:
    def __init__(
        self,
        auth_repository: AuthInterface,
        agent_repository: AgentInterface,
    ):
        self.auth_repository = auth_repository
        self.agent_repository = agent_repository

    def validate_token(self, token: str) -> UserDetailsResponseDto:
        """Validate the provided token"""
        try:
            user = self.auth_repository.get_user_details(token)
            if not user:
                raise AgentAuthenticationException(
                    details={
                        "message": "Invalid token or user not found",
                        "operation": "validate_token",
                    }
                )
            return user
        except Exception as e:
            raise AgentAuthenticationException(
                details={"original_error": str(e), "operation": "validate_token"}
            ) from e

    async def execute(self, token, agent_data: BaseAgent) -> Agent:
        """Create a new agent"""
        try:
            session_id = str(uuid4())
            user = self.validate_token(token)

            agent_data = BaseAgent(
                model_id=agent_data.model_id,
                session_id=session_id,
                user_id=user.user_id,
                name=agent_data.name,
                description=agent_data.description,
                instructions=agent_data.instructions,
                tools=agent_data.tools,
                storage=agent_data.storage,
                knowledge_base=agent_data.knowledge_base,
            )

            return await self.agent_repository.create_basic_agent_chat(agent_data)

        except AgentAuthenticationException:
            # Re-raise authentication exceptions as is
            raise
        except Exception as e:
            raise AgentCreationException(
                details={
                    "original_error": str(e),
                    "operation": "execute_create_agent",
                    "user_id": (
                        getattr(user, "user_id", "unknown")
                        if "user" in locals()
                        else "unknown"
                    ),
                    "agent_name": agent_data.name if agent_data else "unknown",
                }
            ) from e


class StreamAgentResponseUseCase:
    def __init__(
        self,
        agent_create_usecase: CreateAgentUseCase,
        auth_repository: AuthInterface,
        agent_repository: AgentInterface,
    ):
        self.agent_create_usecase = agent_create_usecase
        self.auth_repository = auth_repository
        self.agent_repository = agent_repository

    def validate_token(self, token: str) -> UserDetailsResponseDto:
        """Validate the provided token"""
        try:
            user = self.auth_repository.get_user_details(token)
            if not user:
                raise AgentAuthenticationException(
                    details={
                        "message": "Invalid token or user not found",
                        "operation": "validate_token_stream",
                    }
                )
            return user
        except Exception as e:
            raise AgentAuthenticationException(
                details={"original_error": str(e), "operation": "validate_token_stream"}
            ) from e

    async def execute(
        self, token: str, messages: List[Dict[str, Any]]
    ) -> AsyncGenerator:
        """Stream response from the agent"""
        try:
            session_id = str(uuid4())
            user = self.validate_token(token)

            basic_agent_data = BaseAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_basic_chat_agent",
                description="Basic chat agent for streaming responses",
                instructions="You are a basic chat agent that streams responses.",
            )

            judge_agent_data = JudgingBaseAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_judge_chat_agent",
            )

            complex_agent_data = ComplexityAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_complexity_chat_agent",
            )

            generator_image_data = GeneratorImageAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_generator_image_agent",
            )

            team_agent_data = TeamAgent(
                members=[],
                user_id=user.user_id,
                session_id=session_id,
                team_name="inner_team_chat_agent",
                description="Team chat agent for collaborative responses",
            )

            team_agent = await self.agent_repository.create_team_agent_chat(
                basic_agent_data,
                judge_agent_data,
                generator_image_data,
                complex_agent_data,
                team_agent_data,
            )

            # Converter mensagens para o formato esperado pela biblioteca agno
            formatted_messages = []
            for msg in messages:
                if isinstance(msg, dict):
                    if msg.get("role") == "user":
                        formatted_messages.append(msg.get("content", ""))
                    else:
                        formatted_messages.append(
                            f"{msg.get('role', '')}: {msg.get('content', '')}"
                        )
                else:
                    formatted_messages.append(str(msg))

            response = await team_agent.arun(
                formatted_messages, stream=True, stream_intermediate_steps=True
            )

            async for chunk in response:
                try:
                    if (
                        chunk
                        and hasattr(chunk, "content")
                        and chunk.content is not None
                    ):
                        content = chunk.content

                        # Converter content para string se necessário
                        if isinstance(content, dict):
                            import json

                            content = json.dumps(content, ensure_ascii=False)
                        elif not isinstance(content, str):
                            content = str(content)

                        if content.strip():
                            yield content

                except Exception as chunk_error:
                    # Se houver erro processando um chunk específico, logar e continuar
                    error_msg = f"Erro processando chunk: {str(chunk_error)}"
                    yield f"data: [ERROR] {error_msg}\n\n"

            # Após o streaming, verificar se há imagens geradas
            try:
                images = team_agent.get_images()
                if images:
                    yield "\n\n**IMAGENS GERADAS:**\n"
                    for i, image in enumerate(images, 1):
                        if hasattr(image, "url"):
                            yield f"Imagem {i}: {image.url}\n"
                        else:
                            yield f"Imagem {i}: {str(image)}\n"
            except Exception as img_error:
                yield f"\n[INFO] Verificação de imagens: {str(img_error)}\n"

        except AgentAuthenticationException:
            # Re-raise authentication exceptions as is
            raise
        except Exception as e:
            raise AgentStreamException(
                details={
                    "original_error": str(e),
                    "operation": "execute_stream_agent",
                    "messages_count": len(messages) if messages else 0,
                    "user_id": (
                        getattr(user, "user_id", "unknown")
                        if "user" in locals()
                        else "unknown"
                    ),
                }
            ) from e


class DefineTeamToPlaygroundUseCase:
    def __init__(
        self,
        agent_create_usecase: CreateAgentUseCase,
        auth_repository: AuthInterface,
        agent_repository: AgentInterface,
    ):
        self.agent_create_usecase = agent_create_usecase
        self.auth_repository = auth_repository
        self.agent_repository = agent_repository

    def validate_token(self, token: str) -> UserDetailsResponseDto:
        """Validate the provided token"""
        try:
            user = self.auth_repository.get_user_details(token)
            if not user:
                raise AgentAuthenticationException(
                    details={
                        "message": "Invalid token or user not found",
                        "operation": "validate_token_stream",
                    }
                )
            return user
        except Exception as e:
            raise AgentAuthenticationException(
                details={"original_error": str(e), "operation": "validate_token_stream"}
            ) from e

    async def execute(
        self,
        token: str,
    ):
        """Stream response from the agent"""
        try:
            session_id = str(uuid4())
            user = self.validate_token(token)

            basic_agent_data = BaseAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_basic_chat_agent",
                description="Basic chat agent for streaming responses",
                instructions="You are a basic chat agent that streams responses.",
            )

            judge_agent_data = JudgingBaseAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_judge_chat_agent",
            )

            complex_agent_data = ComplexityAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_complexity_chat_agent",
            )

            generator_image_data = GeneratorImageAgent(
                user_id=user.user_id,
                session_id=session_id,
                name="inner_generator_image_agent",
            )

            team_agent_data = TeamAgent(
                members=[],
                user_id=user.user_id,
                session_id=session_id,
                team_name="inner_team_chat_agent",
                description="Team chat agent for collaborative responses",
            )

            team = await self.agent_repository.create_team_agent_chat(
                basic_agent_data,
                judge_agent_data,
                generator_image_data,
                complex_agent_data,
                team_agent_data,
            )

            basic_agent = await self.agent_repository.create_basic_agent_chat(
                basic_agent_data
            )

            complex_agent = await self.agent_repository.create_complexity_agent_chat(
                complex_agent_data
            )

            image_agent = await self.agent_repository.create_generator_image_agent_chat(
                generator_image_data
            )

            judge_agent = await self.agent_repository.create_judge_intent_user_message(
                judge_agent_data
            )

            return team, [
                basic_agent,
                complex_agent,
                image_agent,
                judge_agent,
            ]

        except AgentAuthenticationException:
            # Re-raise authentication exceptions as is
            raise
        except Exception as e:
            raise AgentStreamException(
                details={
                    "original_error": str(e),
                    "operation": "execute_stream_agent",
                    "user_id": (
                        getattr(user, "user_id", "unknown")
                        if "user" in locals()
                        else "unknown"
                    ),
                }
            ) from e
