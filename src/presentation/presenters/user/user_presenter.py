from typing import Any, Dict, List

from fastapi import status

from core.entities.user import User
from core.exceptions.base_exceptions import BaseApplicationException
from presentation.presenters.user import UserPresenterInterface


class UserPresenter(UserPresenterInterface):
    """Presenter responsável pela formatação das respostas de usuário"""

    def present_user_created(self, user: User) -> Dict[str, Any]:
        """Apresenta o resultado da criação de usuário"""
        return {
            "success": True,
            "message": "Usuário criado com sucesso",
            "data": self._format_user(user),
            "status_code": status.HTTP_201_CREATED,
        }

    def present_user(self, user: User) -> Dict[str, Any]:
        """Apresenta um usuário"""
        return {
            "success": True,
            "data": self._format_user(user),
            "status_code": status.HTTP_200_OK,
        }

    def present_users_list(self, users: List[User]) -> Dict[str, Any]:
        """Apresenta uma lista de usuários"""
        return {
            "success": True,
            "data": [self._format_user(user) for user in users],
            "total": len(users),
            "status_code": status.HTTP_200_OK,
        }

    def present_user_updated(self, user: User) -> Dict[str, Any]:
        """Apresenta o resultado da atualização de usuário"""
        return {
            "success": True,
            "message": "Usuário atualizado com sucesso",
            "data": self._format_user(user),
            "status_code": status.HTTP_200_OK,
        }

    def present_error(self, error: Exception) -> Dict[str, Any]:
        """Apresenta um erro"""
        if isinstance(error, BaseApplicationException):
            return {
                "success": False,
                "error": error.message_pt,
                "error_code": error.error_code,
                "status_code": error.status_code,
            }

        return {
            "success": False,
            "error": "Erro interno do servidor",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

    def _format_user(self, user: User) -> Dict[str, Any]:
        """Formata os dados do usuário para apresentação"""
        return {
            "id": user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "roles": user.roles,
            "created_at": (
                user.created_at.isoformat()
                if hasattr(user, "created_at") and user.created_at
                else None
            ),
            "updated_at": (
                user.updated_at.isoformat()
                if hasattr(user, "updated_at") and user.updated_at
                else None
            ),
        }
