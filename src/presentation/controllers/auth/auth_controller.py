from typing import Any, Dict

from core.usecases.user.usecases import LoginUserUseCase
from core.usecases.auth.auth_usecases import ConfirmUserUseCase
from presentation.controllers.auth import AuthControllerInterface
from presentation.presenters.user.user_presenter import UserPresenterInterface


class AuthController(AuthControllerInterface):
    def __init__(
        self,
        login_usecase: LoginUserUseCase,
        confirm_usecase: ConfirmUserUseCase,
        presenter: UserPresenterInterface,
    ):
        self.login_usecase = login_usecase
        self.confirm_usecase = confirm_usecase
        self.presenter = presenter

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Realiza o login do usuário e retorna os detalhes de autenticação"""
        auth_details = self.login_usecase.execute(email, password)
        return self.presenter.present_user_authentication(auth_details)

    def confirm_email(self, email: str, token: str) -> Dict[str, Any]:
        """Confirma o email do usuário com o token fornecido"""
        confirmation = self.confirm_usecase.execute(email, token)
        return self.presenter.present_email_confirmation(confirmation)