import logging
from typing import Any, Dict, List

from configs.load_env import settings
from core.entities.chat import Chat
from core.exceptions.base_exceptions import BaseApplicationException
from infraestructure.client_factory.aws import AWSClientFactory
from interface.chat.chat_interface import ChatInterface

logger = logging.getLogger(__name__)


class ChatRepository(ChatInterface):
    """Repositório de chats que implementa a interface ChatInterface"""

    def __init__(self, client_factory: AWSClientFactory = AWSClientFactory()):
        self.table_name = f"{settings.app_prefix}-{settings.environment}-chats"
        self.aws_factory = client_factory

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

    def create_chat(self, chat_data: Chat) -> Chat:
        try:
            self.table.put_item(Item={
                "chatId": chat_data.chat_id,
                "userId": chat_data.user_id,
                "isActive": chat_data.is_active,
                "messages": chat_data.messages,
            })
            logger.info(f"Chat created successfully: {chat_data.chat_id}")
            
            return chat_data
        except Exception as e:
            logger.error(f"Failed to create chat: {str(e)}")
            raise

    def get_chats(self, chat_id: str) -> Chat:
        try:
            response = self.table.get_item(Key={"chatId": chat_id})
            if "Item" not in response:
                logger.warning(f"Chat not found: {chat_id}")
                return None
            chat_data = response["Item"]
            chat = Chat(**chat_data)
            logger.info(f"Chat retrieved successfully: {chat.chat_id}")
            return chat
        except Exception as e:
            logger.error(f"Failed to retrieve chat: {str(e)}")
            raise BaseApplicationException(
                message_pt="Erro ao recuperar chat",
                message_en="Error retrieving chat",
                details={"chat_id": chat_id},
                error_code="CHAT_RETRIEVAL_ERROR",
            )

    def delete_chat(self, chat_id: str) -> bool:
        try:
            response = self.table.delete_item(Key={"chatId": chat_id})
            if "Attributes" not in response:
                logger.warning(f"Chat not found for deletion: {chat_id}")
                return False
            logger.info(f"Chat deleted successfully: {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete chat: {str(e)}")
            raise BaseApplicationException(
                message_pt="Erro ao deletar chat",
                message_en="Error deleting chat",
                details={"chat_id": chat_id},
                error_code="CHAT_DELETION_ERROR",
            )

    def update_chat(self, chat_id: str, chat_data: Chat) -> Chat:
        try:
            update_expression = "SET isActive = :isActive, messages = :messages"
            expression_values = {
                ":isActive": chat_data.is_active,
                ":messages": chat_data.messages,
            }

            response = self.table.update_item(
                Key={"chatId": chat_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW",
            )

            if "Attributes" not in response:
                logger.warning(f"Chat not found for update: {chat_id}")
                return None

            updated_chat_data = response["Attributes"]
            updated_chat = Chat(**updated_chat_data)
            logger.info(f"Chat updated successfully: {chat_id}")
            return updated_chat

        except Exception as e:
            logger.error(f"Failed to update chat: {str(e)}")
            raise BaseApplicationException(
                message_pt="Erro ao atualizar chat",
                message_en="Error updating chat",
                details={"chat_id": chat_id},
                error_code="CHAT_UPDATE_ERROR",
            )