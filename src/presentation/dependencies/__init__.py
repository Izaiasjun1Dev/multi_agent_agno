from functools import lru_cache
from typing import Any, Dict, List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.usecases.agent.agent_usecases import (
    CreateAgentUseCase,
    StreamAgentResponseUseCase,
)
from core.usecases.auth.auth_usecases import ConfirmUserUseCase
from core.usecases.chat.chat_usecases import AsyncCreateChatUseCase, CreateChatUseCase
from core.usecases.user.usecases import (
    CreateUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    LoginUserUseCase,
    UpdateUserUseCase,
)
from infraestructure.database.config import get_db_session
from infraestructure.repositoryes.agent.agent_repository import AgentRepository
from infraestructure.repositoryes.auth.repository import AuthRepository
from infraestructure.repositoryes.chat.chat_repository import ChatRepository
from infraestructure.repositoryes.chat.postgres_chat_repository import (
    PostgresChatRepository,
)
from infraestructure.repositoryes.user.repository import UserRepository
from interface.auth.auth_interface import AuthInterface
from interface.chat.chat_interface import AsyncChatInterface, ChatInterface
from interface.user.user_interface import UserInterface
from presentation.controllers.agent.agent_controller import AgentController
from presentation.controllers.auth.auth_controller import AuthController
from presentation.controllers.chat.chat_controller import (
    AsyncChatController,
    ChatController,
)
from presentation.controllers.user.user_controller import UserController
from presentation.presenters.agent.agent_presenter import AgentPresenter
from presentation.presenters.user.user_presenter import UserPresenter


@lru_cache()
def get_auth_interface() -> AuthInterface:
    """Factory para a interface de autenticação"""
    return AuthRepository()


@lru_cache()
def get_user_repository() -> UserInterface:
    """Factory para o repositório de usuário"""
    return UserRepository()


@lru_cache()
def get_user_presenter() -> UserPresenter:
    """Factory para o presenter de usuário"""
    return UserPresenter()


@lru_cache()
def get_create_user_usecase() -> CreateUserUseCase:
    """Factory para o caso de uso de criação de usuário"""
    repository = get_user_repository()
    auth_interface = get_auth_interface()
    return CreateUserUseCase(repository, auth_interface)


@lru_cache()
def get_get_user_usecase() -> GetUserUseCase:
    """Factory para o caso de uso de obtenção de usuário"""
    repository = get_user_repository()
    return GetUserUseCase(repository)


@lru_cache()
def get_list_users_usecase() -> ListUsersUseCase:
    """Factory para o caso de uso de listagem de usuários"""
    repository = get_user_repository()
    return ListUsersUseCase(repository)


@lru_cache()
def get_update_user_usecase() -> UpdateUserUseCase:
    """Factory para o caso de uso de atualização de usuário"""
    repository = get_user_repository()
    return UpdateUserUseCase(repository)


@lru_cache()
def get_user_controller() -> UserController:
    """Factory para o controller de usuário"""
    return UserController(
        create_user_usecase=get_create_user_usecase(),
        get_user_usecase=get_get_user_usecase(),
        update_user_usecase=get_update_user_usecase(),
        presenter=get_user_presenter(),
    )


@lru_cache()
def get_auth_controller() -> AuthController:
    """Factory para o controller de autenticação"""
    login_usecase = LoginUserUseCase(get_auth_interface())
    return AuthController(
        login_usecase=login_usecase,
        confirm_usecase=ConfirmUserUseCase(get_user_repository(), get_auth_interface()),
        presenter=get_user_presenter(),
    )


@lru_cache()
def get_chat_interface() -> ChatInterface:
    """Factory para a interface de chat"""
    return ChatRepository()


@lru_cache()
def get_async_chat_interface() -> AsyncChatInterface:
    """Factory para a interface assíncrona de chat"""
    return PostgresChatRepository()


@lru_cache()
def get_create_chat_usecase() -> CreateChatUseCase:
    """Factory para o caso de uso de criação de chat"""
    chat_interface = get_chat_interface()
    return CreateChatUseCase(chat_interface, get_auth_interface())


@lru_cache()
def get_async_create_chat_usecase() -> AsyncCreateChatUseCase:
    """Factory para o caso de uso assíncrono de criação de chat"""
    chat_interface = get_async_chat_interface()
    return AsyncCreateChatUseCase(chat_interface, get_auth_interface())


@lru_cache()
def get_chat_controller() -> ChatController:
    """Factory para o controller de chat"""
    return ChatController(create_chat_usecase=get_create_chat_usecase())


lru_cache()


def get_async_chat_controller() -> AsyncChatController:
    """Factory para o controller assíncrono de chat"""
    return AsyncChatController(create_chat_usecase=get_async_create_chat_usecase())


# Configuração do esquema de autenticação Bearer
security = HTTPBearer()


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extrai o token Bearer do header Authorization da requisição.

    Args:
        credentials: Credenciais de autorização HTTP

    Returns:
        str: O token de acesso

    Raises:
        HTTPException: Se o token não for fornecido ou estiver inválido
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorização não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials


def get_optional_bearer_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[str]:
    """
    Extrai o token Bearer do header Authorization de forma opcional.

    Args:
        credentials: Credenciais de autorização HTTP (opcional)

    Returns:
        Optional[str]: O token de acesso ou None se não fornecido
    """
    if credentials:
        return credentials.credentials
    return None


@lru_cache()
def get_agent_repository() -> AgentRepository:
    """Factory para o repositório de agente"""
    return AgentRepository()


@lru_cache()
def get_create_agent_usecase() -> CreateAgentUseCase:
    """Factory para o caso de uso de criação de agente"""
    return CreateAgentUseCase(get_auth_interface(), get_agent_repository())


@lru_cache()
def get_agent_stream_usecase() -> StreamAgentResponseUseCase:
    """Factory para o caso de uso de streaming de resposta de agente"""
    return StreamAgentResponseUseCase(
        get_create_agent_usecase(), get_auth_interface(), get_agent_repository()
    )


def get_agent_controller() -> AgentController:
    """
    Factory para o controller de agente.

    Returns:
        AgentController: Instância do controller de agente
    """

    presenter = AgentPresenter()

    return AgentController(
        create_agent_usecase=get_create_agent_usecase(),
        stream_agent_response_usecase=get_agent_stream_usecase(),
        presenter=presenter,
    )
