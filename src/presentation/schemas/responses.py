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
