from typing import List, Optional

from core.dtos.user.user_dtos import CreateUserDto
from core.entities.user import User
from interface.auth.auth_interface import AuthInterface
from interface.user.user_interface import UserInterface


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface, auth_interface: AuthInterface):
        self.user_interface = user_interface
        self.auth_interface = auth_interface

    def execute(self, user_data: CreateUserDto) -> User:
        # Mapear os campos do DTO para os aliases da entidade User
        user_dict = user_data.model_dump()

        user_id = user_dict.get("user_id")
        email = user_dict.get("email")

        if not user_id or not email:
            raise ValueError("user_id and email are required")

        full_name = (
            f"{user_dict.get('first_name', '')} {user_dict.get('last_name', '')}".strip()
            or None
        )

        user = User(
            userId=user_id,
            email=email,
            name=full_name,
            isActive=True,
            org="default_org",  # Definir uma organização padrão ou pegar de algum lugar
            slug=None,
            avatarUrl=None,
        )
        self.user_interface.create_user(user)
        self.auth_interface.signup(user_data.email, user_data.password)
        return user


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def execute(self, user_id: str) -> Optional[User]:
        return self.user_interface.get_user(user_id)


class ListUsersUseCase:
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def execute(self) -> List[User]:
        return self.user_interface.list_users()


class UpdateUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def execute(self, user_id: str, user_data: dict) -> Optional[User]:
        user = self.user_interface.get_user(user_id)
        if user:
            # Usar model_copy para criar uma nova instância com os dados atualizados
            updated_user = user.model_copy(update=user_data)
            self.user_interface.update_user(updated_user)
            return updated_user
        return None


class DeleteUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def execute(self, user_id: str) -> bool:
        return self.user_interface.delete_user(user_id)
