from typing import Any, Dict

from core.exceptions import InfrastructureException
from core.exceptions.auth.auth_exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
)
from core.exceptions.user.exceptions import UserNotFoundException
from interface.auth.auth_interface import AuthInterface
from interface.user.user_interface import UserInterface


class ConfirmUserUseCase:
    def __init__(self, user_interface: UserInterface, auth_interface: AuthInterface):
        self.user_interface = user_interface
        self.auth_interface = auth_interface

    def execute(self, email: str, confirmation_token: str) -> Dict[str, Any]:
        try:
            # Verifica se o usuário existe
            user = self.user_interface.get_user_by_email(email)
            if not user:
                raise UserNotFoundException(
                    identifier=email,
                    field="email",
                    details={"email": email},
                )

            # Confirma o usuário no serviço de autenticação
            if self.auth_interface.confirm_email(user.email, confirmation_token):
                return {"status": "success"}
            
            return {"status": "error"}

        except InvalidCredentialsException as e:
            raise AuthenticationException(
                message_pt="Credenciais inválidas",
                message_en="Invalid credentials",
                details={"email": email},
                error_code="INVALID_CREDENTIALS",
            ) from e
        except Exception as e:
            raise InfrastructureException(
                message_pt="Erro ao confirmar usuário",
                message_en="Error confirming user",
                service="user_service",
                operation="confirm",
                error_code="USER_CONFIRM_ERROR",
            ) from e
