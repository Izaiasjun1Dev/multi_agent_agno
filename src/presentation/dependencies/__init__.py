from functools import lru_cache
from typing import Any, Dict, List

from core.usecases.auth.auth_usecases import ConfirmUserUseCase
from core.usecases.user.usecases import (
    CreateUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
    LoginUserUseCase,
    UpdateUserUseCase,
)
from infraestructure.repositories.auth.repository import AuthRepository
from infraestructure.repositories.user.repository import UserRepository
from interface.auth.auth_interface import AuthInterface
from interface.user.user_interface import UserInterface
from presentation.controllers.auth.auth_controller import AuthController
from presentation.controllers.user.user_controller import UserController
from presentation.presenters.user.user_presenter import UserPresenter


# Mock implementation for AuthInterface (você pode implementar uma versão real)
class MockAuthInterface(AuthInterface):
    def login(self, username: str, password: str) -> Dict[str, Any]:
        return {"token": "mock_token", "user_id": "mock_user_id"}

    def logout(self, token: str) -> bool:
        return True

    def signup(self, username: str, password: str) -> Dict[str, Any]:
        return {"user_id": "mock_user_id", "username": username}

    def reset_password(self, username: str, new_password: str) -> bool:
        return True

    def get_user_details(self, token: str) -> Dict[str, Any]:
        return {"user_id": "mock_user_id", "username": "mock_username"}

    def list_active_sessions(self) -> List[Dict[str, Any]]:
        return [{"session_id": "mock_session", "user_id": "mock_user_id"}]

    def revoke_session(self, token: str) -> bool:
        return True

    def confirm_email(self, token: str) -> bool:
        return True


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
