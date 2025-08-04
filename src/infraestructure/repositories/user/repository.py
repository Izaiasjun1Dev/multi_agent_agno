"""
Repositório de usuários para operações com DynamoDB.
User repository for DynamoDB operations.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from configs.load_env import settings
from core.entities.user import User
from core.exceptions.base_exceptions import BaseApplicationException
from core.exceptions.user import (
    UserAlreadyExistsException,
    UserBusinessRuleException,
    UserNotFoundException,
    UserOrgMismatchException,
)
from infraestructure.client_factory.aws import AWSClientFactory
from interface.user.user_interface import UserInterface

logger = logging.getLogger(__name__)


class UserRepository(UserInterface):
    """
    Implementação do repositório de usuários usando DynamoDB.
    Implementation of user repository using DynamoDB.
    """

    def __init__(self):
        """
        Inicializa o repositório de usuários.
        Initializes the user repository.
        """
        self.table_name = f"{settings.app_prefix}-{settings.environment}-users"
        self.aws_factory = AWSClientFactory()

        try:
            self.table = self.aws_factory.dynamo_table(self.table_name)

            if not self.table:
                raise BaseApplicationException(
                    message_pt=f"Falha ao conectar à tabela DynamoDB: {self.table_name}",
                    message_en=f"Failed to connect to DynamoDB table: {self.table_name}",
                    details={
                        "table_name": self.table_name,
                        "environment": settings.environment,
                        "app_prefix": settings.app_prefix,
                    },
                    error_code="DYNAMODB_CONNECTION_ERROR",
                )

            logger.info(f"UserRepository initialized with table: {self.table_name}")

        except Exception as e:
            logger.error(f"Failed to initialize UserRepository: {str(e)}")
            raise

    def _serialize_user_data(self, user: User) -> dict:
        """
        Serializa os dados do usuário para o formato aceito pelo DynamoDB.
        Serializes user data to DynamoDB-compatible format.

        Args:
            user: User entity

        Returns:
            dict: Serialized user data
        """
        user_data = user.model_dump(by_alias=True)

        # Converter datetime objects para strings ISO
        for field in ["createdAt", "updatedAt"]:
            if field in user_data and isinstance(user_data[field], datetime):
                user_data[field] = user_data[field].isoformat()

        # Garantir que campos datetime existam
        if "createdAt" not in user_data or user_data["createdAt"] is None:
            user_data["createdAt"] = datetime.now().isoformat()

        if "updatedAt" not in user_data or user_data["updatedAt"] is None:
            user_data["updatedAt"] = datetime.now().isoformat()

        return user_data

    def create_user(self, user: User) -> User:
        """
        Cria um novo usuário no banco de dados.
        Creates a new user in the database.

        Args:
            user: Entidade de usuário a ser criada

        Returns:
            User: Usuário criado

        Raises:
            UserAlreadyExistsException: Se o usuário já existe
            BaseApplicationException: Se houver erro na criação
        """
        try:
            # Verificar se o usuário já existe pelo email
            existing_user = self.get_user_by_email(user.email)
            if existing_user:
                raise UserAlreadyExistsException(email=user.email)

            # Preparar dados para salvar no DynamoDB
            user_data = self._serialize_user_data(user)

            # Salvar no DynamoDB
            self.table.put_item(Item=user_data)

            logger.info(f"User created successfully: {user.user_id}")
            return user

        except UserAlreadyExistsException:
            logger.warning(f"Attempt to create duplicate user with email: {user.email}")
            raise

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            logger.error(f"DynamoDB ClientError creating user: {error_code} - {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Falha ao criar usuário: {user.user_id}",
                message_en=f"Failed to create user: {user.user_id}",
                details={
                    "user_id": user.user_id,
                    "error": str(e),
                    "error_code": error_code,
                    "environment": settings.environment,
                },
                error_code="USER_CREATION_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error creating user: {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Erro inesperado ao criar usuário: {user.user_id}",
                message_en=f"Unexpected error creating user: {user.user_id}",
                details={
                    "user_id": user.user_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                error_code="USER_CREATION_UNEXPECTED_ERROR",
                status_code=500,
            )

    def get_user(self, user_id: str) -> User:
        """
        Busca um usuário pelo ID.
        Retrieves a user by ID.

        Args:
            user_id: ID do usuário

        Returns:
            User: Usuário encontrado

        Raises:
            UserNotFoundException: Se o usuário não for encontrado
            BaseApplicationException: Se houver erro na busca
        """
        try:
            if not user_id:
                raise ValueError("User ID cannot be empty")

            response = self.table.get_item(Key={"userId": user_id})

            if "Item" not in response:
                raise UserNotFoundException(identifier=user_id, field="id")

            user_data = response["Item"]
            user = User.model_validate(user_data)

            logger.info(f"User retrieved successfully: {user_id}")
            return user

        except UserNotFoundException:
            logger.warning(f"User not found: {user_id}")
            raise

        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            raise UserBusinessRuleException(
                message_pt=f"ID de usuário inválido: {str(e)}",
                message_en=f"Invalid user ID: {str(e)}",
                rule="valid_user_id_required",
                error_code="INVALID_USER_ID",
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            logger.error(f"DynamoDB ClientError getting user: {error_code} - {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Falha ao obter usuário: {user_id}",
                message_en=f"Failed to get user: {user_id}",
                details={
                    "user_id": user_id,
                    "error": str(e),
                    "error_code": error_code,
                },
                error_code="USER_RETRIEVAL_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error getting user: {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Erro inesperado ao obter usuário: {user_id}",
                message_en=f"Unexpected error getting user: {user_id}",
                details={
                    "user_id": user_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                error_code="USER_RETRIEVAL_UNEXPECTED_ERROR",
                status_code=500,
            )

    def update_user(self, user: User) -> User:
        """
        Atualiza um usuário existente.
        Updates an existing user.

        Args:
            user: Entidade de usuário com os dados atualizados

        Returns:
            User: Usuário atualizado

        Raises:
            UserNotFoundException: Se o usuário não for encontrado
            BaseApplicationException: Se houver erro na atualização
        """
        try:
            # Verificar se o usuário existe
            existing_user = self.get_user(user.user_id)


            # Preparar dados para atualizar
            user_data = self._serialize_user_data(user)

            # Construir expressões de atualização
            update_expression_parts = []
            expression_attribute_names = {}
            expression_attribute_values = {}

            # Campos que podem ser atualizados
            updatable_fields = {
                "email": "email",
                "firstName": "first_name",
                "lastName": "last_name",
                "roles": "roles",
                "isActive": "is_active",
                "chats": "chats",
                "slug": "slug",
                "avatarUrl": "avatar_url",
                "updatedAt": "updated_at",
            }

            for dynamo_field, model_field in updatable_fields.items():
                if dynamo_field in user_data:
                    placeholder = f"#{dynamo_field}"
                    value_placeholder = f":{dynamo_field}"

                    update_expression_parts.append(
                        f"{placeholder} = {value_placeholder}"
                    )
                    expression_attribute_names[placeholder] = dynamo_field
                    expression_attribute_values[value_placeholder] = user_data[
                        dynamo_field
                    ]

            if not update_expression_parts:
                logger.warning(f"No fields to update for user: {user.user_id}")
                return user

            update_expression = "SET " + ", ".join(update_expression_parts)

            # Atualizar no DynamoDB
            self.table.update_item(
                Key={"userId": user.user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression=Attr("userId").exists(),
            )

            logger.info(f"User updated successfully: {user.user_id}")
            return user

        except UserNotFoundException:
            logger.warning(f"Attempt to update non-existent user: {user.user_id}")
            raise

        except UserOrgMismatchException:
            logger.warning(f"Attempt to change user organization: {user.user_id}")
            raise

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")

            if error_code == "ConditionalCheckFailedException":
                raise UserNotFoundException(identifier=user.user_id, field="id")

            logger.error(f"DynamoDB ClientError updating user: {error_code} - {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Falha ao atualizar usuário: {user.user_id}",
                message_en=f"Failed to update user: {user.user_id}",
                details={
                    "user_id": user.user_id,
                    "error": str(e),
                    "error_code": error_code,
                },
                error_code="USER_UPDATE_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error updating user: {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Erro inesperado ao atualizar usuário: {user.user_id}",
                message_en=f"Unexpected error updating user: {user.user_id}",
                details={
                    "user_id": user.user_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                error_code="USER_UPDATE_UNEXPECTED_ERROR",
                status_code=500,
            )

    def delete_user(self, user_id: str) -> bool:
        """
        Deleta um usuário.
        Deletes a user.

        Args:
            user_id: ID do usuário a ser deletado

        Returns:
            bool: True se deletado com sucesso

        Raises:
            UserNotFoundException: Se o usuário não for encontrado
            BaseApplicationException: Se houver erro na deleção
        """
        try:
            # Verificar se o usuário existe
            self.get_user(user_id)

            # Deletar usuário
            self.table.delete_item(
                Key={"userId": user_id}, ConditionExpression=Attr("userId").exists()
            )

            logger.info(f"User deleted successfully: {user_id}")
            return True

        except UserNotFoundException:
            logger.warning(f"Attempt to delete non-existent user: {user_id}")
            raise

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")

            if error_code == "ConditionalCheckFailedException":
                raise UserNotFoundException(identifier=user_id, field="id")

            logger.error(f"DynamoDB ClientError deleting user: {error_code} - {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Falha ao deletar usuário: {user_id}",
                message_en=f"Failed to delete user: {user_id}",
                details={
                    "user_id": user_id,
                    "error": str(e),
                    "error_code": error_code,
                },
                error_code="USER_DELETE_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error deleting user: {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Erro inesperado ao deletar usuário: {user_id}",
                message_en=f"Unexpected error deleting user: {user_id}",
                details={
                    "user_id": user_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                error_code="USER_DELETE_UNEXPECTED_ERROR",
                status_code=500,
            )

    def list_users(self) -> List[User]:
        """
        Lista todos os usuários.
        Lists all users.

        Returns:
            List[User]: Lista de usuários

        Raises:
            BaseApplicationException: Se houver erro na listagem
        """
        try:
            users = []
            last_evaluated_key = None

            # Fazer scan completo para obter todos os usuários
            while True:
                scan_kwargs: Dict[str, Any] = {}

                if last_evaluated_key:
                    scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

                response = self.table.scan(**scan_kwargs)

                items = response.get("Items", [])
                users.extend([User.model_validate(item) for item in items])

                last_evaluated_key = response.get("LastEvaluatedKey")
                if not last_evaluated_key:
                    break

            logger.info(f"Listed {len(users)} total users")
            return users

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            logger.error(f"DynamoDB ClientError listing users: {error_code} - {str(e)}")

            raise BaseApplicationException(
                message_pt="Falha ao listar usuários",
                message_en="Failed to list users",
                details={
                    "error": str(e),
                    "error_code": error_code,
                },
                error_code="USER_LIST_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error listing users: {str(e)}")

            raise BaseApplicationException(
                message_pt="Erro inesperado ao listar usuários",
                message_en="Unexpected error listing users",
                details={
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                error_code="USER_LIST_UNEXPECTED_ERROR",
                status_code=500,
            )

    def get_users_by_org(self, org_id: str, limit: int = 100) -> List[User]:
        """
        Lista usuários de uma organização.
        Lists users from an organization.

        Args:
            org_id: ID da organização
            limit: Número máximo de usuários a retornar

        Returns:
            List[User]: Lista de usuários da organização

        Raises:
            BaseApplicationException: Se houver erro na listagem
        """
        try:
            # Criar índice GSI se necessário: org-index
            response = self.table.query(
                IndexName="org-index",
                KeyConditionExpression=Key("org").eq(org_id),
                Limit=limit,
            )

            users = [User.model_validate(item) for item in response.get("Items", [])]

            logger.info(f"Listed {len(users)} users for org: {org_id}")
            return users

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")

            # Se o índice não existir, fazer scan com filtro
            if error_code == "ValidationException":
                logger.warning("org-index not found, falling back to scan")
                return self._scan_users_by_org(org_id, limit)

            logger.error(
                f"DynamoDB ClientError querying users by org: {error_code} - {str(e)}"
            )

            raise BaseApplicationException(
                message_pt=f"Falha ao listar usuários da organização: {org_id}",
                message_en=f"Failed to list users from organization: {org_id}",
                details={
                    "org_id": org_id,
                    "error": str(e),
                    "error_code": error_code,
                },
                error_code="USER_LIST_BY_ORG_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error listing users by org: {str(e)}")

            raise BaseApplicationException(
                message_pt=f"Erro inesperado ao listar usuários da organização: {org_id}",
                message_en=f"Unexpected error listing users from organization: {org_id}",
                details={
                    "org_id": org_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                error_code="USER_LIST_BY_ORG_UNEXPECTED_ERROR",
                status_code=500,
            )

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Busca usuário por email.
        Searches user by email.
        """
        try:
            # Assumindo que existe um índice GSI: email-index
            response = self.table.query(
                IndexName="email-index",
                KeyConditionExpression=Key("email").eq(email),
                Limit=1,
            )

            items = response.get("Items", [])
            if items:
                return User.model_validate(items[0])

            return None

        except ClientError as e:
            # Se o índice não existir, fazer scan
            if e.response.get("Error", {}).get("Code") == "ValidationException":
                return self._scan_user_by_email(email)
            raise

    def _scan_user_by_email(self, email: str) -> Optional[User]:
        """
        Busca usuário por email usando scan (fallback).
        Searches user by email using scan (fallback).
        """
        try:
            response = self.table.scan(
                FilterExpression=Attr("email").eq(email), Limit=1
            )

            items = response.get("Items", [])
            if items:
                return User.model_validate(items[0])

            return None

        except Exception as e:
            logger.error(f"Error scanning user by email: {str(e)}")
            return None

    def _scan_users_by_org(self, org_id: str, limit: int) -> List[User]:
        """
        Busca usuários por organização usando scan (fallback).
        Searches users by organization using scan (fallback).
        """
        try:
            response = self.table.scan(
                FilterExpression=Attr("org").eq(org_id), Limit=limit
            )

            return [User.model_validate(item) for item in response.get("Items", [])]

        except Exception as e:
            logger.error(f"Error scanning users by org: {str(e)}")
            return []

    def list_users_paginated(
        self, limit: int = 100, last_evaluated_key: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Lista usuários com paginação (método adicional não definido na interface).
        Lists users with pagination (additional method not defined in interface).

        Args:
            limit: Número máximo de usuários a retornar
            last_evaluated_key: Chave para continuar a paginação

        Returns:
            Dict contendo usuários e chave para próxima página

        Raises:
            BaseApplicationException: Se houver erro na listagem
        """
        try:
            scan_kwargs: Dict[str, Any] = {"Limit": limit}

            if last_evaluated_key:
                scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

            response = self.table.scan(**scan_kwargs)

            users = [User.model_validate(item) for item in response.get("Items", [])]

            result = {
                "users": users,
                "count": len(users),
                "last_evaluated_key": response.get("LastEvaluatedKey"),
                "has_more": response.get("LastEvaluatedKey") is not None,
            }

            logger.info(f"Listed {len(users)} users (paginated)")
            return result

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            logger.error(
                f"DynamoDB ClientError listing users (paginated): {error_code} - {str(e)}"
            )

            raise BaseApplicationException(
                message_pt="Falha ao listar usuários com paginação",
                message_en="Failed to list users with pagination",
                details={
                    "error": str(e),
                    "error_code": error_code,
                    "limit": limit,
                },
                error_code="USER_LIST_PAGINATED_ERROR",
                status_code=500,
            )

        except Exception as e:
            logger.error(f"Unexpected error listing users (paginated): {str(e)}")

            raise BaseApplicationException(
                message_pt="Erro inesperado ao listar usuários com paginação",
                message_en="Unexpected error listing users with pagination",
                details={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "limit": limit,
                },
                error_code="USER_LIST_PAGINATED_UNEXPECTED_ERROR",
                status_code=500,
            )
