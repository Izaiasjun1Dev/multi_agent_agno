from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Modelo padrão de resposta da API"""

    success: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    message: Optional[str] = Field(None, description="Mensagem adicional")
    data: Optional[T] = Field(None, description="Dados da resposta")
    error: Optional[str] = Field(None, description="Mensagem de erro, se houver")
    error_code: Optional[str] = Field(None, description="Código do erro, se houver")
    status_code: int = Field(..., description="Código de status HTTP")


class UserResponse(ApiResponse[Dict[str, Any]]):
    """Resposta específica para operações de usuário"""

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operação realizada com sucesso",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "first_name": "João",
                    "last_name": "Silva",
                },
                "status_code": 200,
            }
        }


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""

    detail: str = Field(..., description="Detalhes do erro")

    class Config:
        json_schema_extra = {"example": {"detail": "Usuário não encontrado"}}
        
        
class NotFoundResponse(ApiResponse[None]):
    """Resposta para recursos não encontrados"""

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Recurso não encontrado",
                "error": "Usuário não encontrado",
                "error_code": "USER_NOT_FOUND",
                "status_code": 404,
            }
        }
        
        
class ConflictResponse(ApiResponse[None]):
    """Resposta para conflitos de recursos"""

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Conflito ao criar o recurso",
                "error": "Usuário já existe",
                "error_code": "USER_ALREADY_EXISTS",
                "status_code": 409,
            }
        }
        
        
class CreateChatResponse(ApiResponse[Dict[str, Any]]):
    """Resposta para criação de chat"""

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Chat criado com sucesso",
                "data": {
                    "chat_id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Novo Chat",
                    "created_at": "2023-10-01T12:00:00Z",
                },
                "status_code": 201,
            }
        }
