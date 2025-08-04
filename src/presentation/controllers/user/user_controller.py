from typing import Any, Dict

from core.dtos.user.user_dtos import CreateRequestUserDto
from core.exceptions.user.exceptions import UserNotFoundException
from core.usecases.user.usecases import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
)
from presentation.controllers.user import UserControllerInterface
from presentation.presenters.user.user_presenter import UserPresenterInterface


class UserController(UserControllerInterface):
    """Controller responsável por orquestrar as operações de usuário"""

    def __init__(
        self,
        create_user_usecase: CreateUserUseCase,
        get_user_usecase: GetUserUseCase,
        update_user_usecase: UpdateUserUseCase,
        presenter: UserPresenterInterface,
    ):
        self._create_user_usecase = create_user_usecase
        self._get_user_usecase = get_user_usecase
        self._update_user_usecase = update_user_usecase
        self._presenter = presenter

    async def create_user(self, user_data: CreateRequestUserDto) -> Dict[str, Any]:
        """Cria um novo usuário e retorna a resposta formatada"""
        user = self._create_user_usecase.execute(user_data)
        return self._presenter.present_user_created(user)

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Obtém um usuário por ID e retorna a resposta formatada"""
        user = self._get_user_usecase.execute(user_id)

        if user is None:
            raise UserNotFoundException(identifier=user_id, field="id")

        return self._presenter.present_user(user)

    async def update_user(
        self, user_id: str, user_data: CreateRequestUserDto
    ) -> Dict[str, Any]:
        """Atualiza um usuário e retorna a resposta formatada"""
        # Converter DTO para dict para o UseCase
        user_dict = user_data.model_dump()
        user = self._update_user_usecase.execute(user_id, user_dict)

        if user is None:
            raise UserNotFoundException(identifier=user_id, field="id")

        return self._presenter.present_user_updated(user)
