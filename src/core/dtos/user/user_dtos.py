from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateRequestUserDto(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "senha123",
                "first_name": "João",
                "last_name": "Silva",
            }
        },
    )

    user_id: Optional[str] = Field(default_factory=lambda: str(uuid4()), alias="id")
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(
        ..., min_length=8, max_length=128, description="Senha do usuário"
    )
    first_name: Optional[str] = Field(None, description="Primeiro nome do usuário")
    last_name: Optional[str] = Field(None, description="Último nome do usuário")


class ReponseUserDto(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "first_name": "João",
                "last_name": "Silva",
            }
        },
    )

    user_id: str = Field(..., alias="id", description="ID único do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    first_name: Optional[str] = Field(None, description="Primeiro nome do usuário")
    last_name: Optional[str] = Field(None, description="Último nome do usuário")
