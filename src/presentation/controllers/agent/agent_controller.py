from typing import Any, AsyncGenerator, Dict, List

from core.dtos.agent.agent_dtos import CreateAgentDTO
from core.entities.agent import BaseAgent
from core.exceptions.agent import (
    AgentAuthenticationException,
    AgentCreationException,
    AgentStreamException,
    AgentValidationException,
)
from core.usecases.agent.agent_usecases import (
    CreateAgentUseCase,
    StreamAgentResponseUseCase,
)
from presentation.controllers.agent import AgentControllerInterface
from presentation.presenters.agent import AgentPresenterInterface


class AgentController(AgentControllerInterface):
    def __init__(
        self,
        create_agent_usecase: CreateAgentUseCase,
        stream_agent_response_usecase: StreamAgentResponseUseCase,
        presenter: AgentPresenterInterface,
    ):
        self._create_agent_usecase = create_agent_usecase
        self._stream_agent_response_usecase = stream_agent_response_usecase
        self._presenter = presenter

    async def create_agent(
        self, token: str, agent_data: CreateAgentDTO
    ) -> Dict[str, Any]:
        """Create a new agent"""
        try:
            # Validar dados de entrada
            if not agent_data.name or not agent_data.name.strip():
                raise AgentValidationException(
                    details={
                        "field": "name",
                        "message": "Agent name cannot be empty",
                        "operation": "create_agent",
                    }
                )

            if not agent_data.description or not agent_data.description.strip():
                raise AgentValidationException(
                    details={
                        "field": "description",
                        "message": "Agent description cannot be empty",
                        "operation": "create_agent",
                    }
                )

            if not agent_data.instructions or not agent_data.instructions.strip():
                raise AgentValidationException(
                    details={
                        "field": "instructions",
                        "message": "Agent instructions cannot be empty",
                        "operation": "create_agent",
                    }
                )

            # Converter DTO para entidade
            base_agent = BaseAgent(
                name=agent_data.name,
                description=agent_data.description,
                instructions=agent_data.instructions,
                tools=[],  # Lista vazia por padrão
                user_id=None,  # Será preenchido pelo use case após validar token
                session_id=None,  # Session ID opcional
                model_id="default-model",
                storage=None,
                knowledge_base=None,
            )

            result = await self._create_agent_usecase.execute(token, base_agent)
            # Converter o objeto Agent para dict antes de passar para o presenter
            agent_dict = {
                "agent_id": getattr(result, "agent_id", str(id(result))),
                "name": getattr(result, "name", agent_data.name),
                "description": getattr(result, "description", agent_data.description),
                "instructions": getattr(
                    result, "instructions", agent_data.instructions
                ),
                "status": "created",
            }
            return self._presenter.present_agent(agent_dict)

        except AgentValidationException:
            # Re-raise validation exceptions as is
            raise
        except ValueError as e:
            if "Invalid token" in str(e):
                raise AgentAuthenticationException(
                    details={
                        "original_error": str(e),
                        "operation": "create_agent",
                        "token_status": "invalid",
                    }
                )
            else:
                raise AgentCreationException(
                    details={
                        "original_error": str(e),
                        "operation": "create_agent",
                        "agent_name": agent_data.name,
                    }
                )
        except Exception as e:
            raise AgentCreationException(
                details={
                    "original_error": str(e),
                    "operation": "create_agent",
                    "agent_name": agent_data.name,
                }
            ) from e

    async def stream_chat_response(
        self, token: str, messages: List[Dict[str, Any]]
    ) -> AsyncGenerator:
        try:
            # Validar dados de entrada
            if not messages:
                raise AgentValidationException(
                    details={
                        "field": "messages",
                        "message": "Messages list cannot be empty",
                        "operation": "stream_chat_response",
                    }
                )

            # Validar estrutura das mensagens
            for i, msg in enumerate(messages):
                if not isinstance(msg, dict):
                    raise AgentValidationException(
                        details={
                            "field": f"messages[{i}]",
                            "message": "Each message must be a dictionary",
                            "operation": "stream_chat_response",
                        }
                    )

                if "role" not in msg or "content" not in msg:
                    raise AgentValidationException(
                        details={
                            "field": f"messages[{i}]",
                            "message": "Each message must have 'role' and 'content' fields",
                            "operation": "stream_chat_response",
                        }
                    )

                if not msg.get("content", "").strip():
                    raise AgentValidationException(
                        details={
                            "field": f"messages[{i}].content",
                            "message": "Message content cannot be empty",
                            "operation": "stream_chat_response",
                        }
                    )

        except (AgentValidationException, AgentAuthenticationException) as e:
            # Para erros de validação e autenticação, lançar antes do streaming começar
            raise

        # Envolver o streaming em try/catch para capturar erros durante o streaming
        try:
            response = self._stream_agent_response_usecase.execute(token, messages)
            async for chunk in response:
                try:
                    # Garantir que chunk não seja None ou vazio
                    if chunk is not None:
                        # Se chunk for string, usar diretamente, senão converter para string
                        if isinstance(chunk, str):
                            if chunk.strip():  # Só yield se não for string vazia
                                yield chunk
                        else:
                            # Se não for string, converter para string
                            chunk_str = str(chunk)
                            if chunk_str.strip():
                                yield chunk_str
                except Exception as chunk_error:
                    # Se houver erro processando um chunk específico, logar e continuar
                    error_message = (
                        f"data: [ERROR] Erro processando chunk: {str(chunk_error)}\n\n"
                    )
                    yield error_message

        except AgentAuthenticationException:
            # Para erros de autenticação durante streaming, enviar como mensagem de erro
            error_message = "data: [ERROR] Token inválido ou expirado\n\n"
            yield error_message
        except AgentStreamException as e:
            # Para erros de streaming, enviar detalhes do erro
            error_details = e.details if hasattr(e, "details") else {}
            error_message = f"data: [ERROR] Erro de streaming: {error_details.get('original_error', str(e))}\n\n"
            yield error_message
        except ValueError as e:
            if "Invalid token" in str(e):
                error_message = "data: [ERROR] Token inválido\n\n"
                yield error_message
            else:
                error_message = f"data: [ERROR] Erro de valor: {str(e)}\n\n"
                yield error_message
        except Exception as e:
            # Para qualquer outro erro durante streaming, enviar mensagem genérica
            error_message = f"data: [ERROR] Erro inesperado: {str(e)}\n\n"
            yield error_message
