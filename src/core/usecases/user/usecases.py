from typing import Any, Dict, List, Optional

from core.dtos.user.user_dtos import CreateRequestUserDto
from core.entities.user import User
from core.exceptions import InfrastructureException, ValidationException
from core.exceptions.auth.auth_exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
)
from core.exceptions.user.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserValidationException,
)
from infraestructure.utils.generate_slug import generate_slug
from interface.auth.auth_interface import AuthInterface
from interface.user.user_interface import UserInterface


class CreateUserUseCase:
    def __init__(self, user_interface: UserInterface, auth_interface: AuthInterface):
        self.user_interface = user_interface
        self.auth_interface = auth_interface

    def execute(self, user_data: CreateRequestUserDto) -> User:
        try:
            # Criar usuário no serviço de autenticação primeiro
            self.auth_interface.signup(
                user_data.email,
                user_data.password,
                user_data.first_name,
                user_data.last_name,
            )

            # Criar usuário no banco de dados
            user_dict = user_data.model_dump()
            user = User(
                **user_dict,
                slug=generate_slug(
                    user_data.first_name if user_data.first_name else user_data.email
                ),
            )

            created_user = self.user_interface.create_user(user)
            if not created_user:
                # Se falhou ao criar no banco, remover do auth service
                try:
                    self.user_interface.delete_user(user.user_id)
                except Exception:
                    pass  # Ignorar erro de cleanup

                raise InfrastructureException(
                    message_pt="Erro ao criar usuário no banco de dados",
                    message_en="Error creating user in database",
                    service="user_service",
                    operation="create",
                    error_code="USER_CREATE_ERROR",
                )

            return created_user

        except UserAlreadyExistsException:
            # Re-raise exceções específicas de usuário
            raise
        except AuthenticationException as e:
            # Converter exceções de auth para o contexto de criação de usuário
            raise UserValidationException(
                message_pt=f"Erro na criação da conta de autenticação: {e.message_pt}",
                message_en=f"Error creating authentication account: {e.message_en}",
                error_code="USER_AUTH_CREATION_ERROR",
            )
        except InfrastructureException:
            # Re-raise exceções de infraestrutura
            raise
        except Exception as e:
            # Capturar outras exceções não esperadas
            raise InfrastructureException(
                message_pt="Erro inesperado ao criar usuário",
                message_en="Unexpected error creating user",
                service="user_service",
                operation="create",
                details={"original_error": str(e)},
                error_code="USER_CREATE_UNEXPECTED_ERROR",
            )


class LoginUserUseCase:
    def __init__(self, auth_interface: AuthInterface):
        self.auth_interface = auth_interface

    def execute(self, email: str, password: str) -> Dict[str, Any]:
        try:
            auth_data = self.auth_interface.login(email, password)

            if not auth_data:
                raise InvalidCredentialsException(details={"email": email})

            return {
                "success": True,
                "access_token": auth_data.get("access_token"),
                "token_type": auth_data.get("token_type", "Bearer"),
                "expires_in": auth_data.get("expires_in"),
                "refresh_token": auth_data.get("refresh_token"),
            }
        except InvalidCredentialsException:
            # Re-raise exceções específicas de auth
            raise
        except AuthenticationException:
            # Re-raise outras exceções de auth
            raise
        except Exception as e:
            # Converter exceções genéricas para auth específicas
            raise AuthenticationException(
                message_pt="Erro inesperado durante o login",
                message_en="Unexpected error during login",
                details={"original_error": str(e)},
                error_code="LOGIN_UNEXPECTED_ERROR",
            )


class GetUserUseCase:
    def __init__(self, user_interface: UserInterface):
        self.user_interface = user_interface

    def execute(self, user_id: str) -> Optional[User]:
        try:
            return self.user_interface.get_user(user_id)
        except UserNotFoundException:
            # Re-raise exceções específicas de usuário
            raise
        except Exception as e:
            # Converter exceções genéricas
            raise UserNotFoundException(
                identifier=user_id, field="id", details={"original_error": str(e)}
            )


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
