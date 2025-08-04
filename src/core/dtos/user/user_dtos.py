from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateRequestUserDto(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "izaias.junior@inner.com",
                "password": "1213@Cronicas",
                "first_name": "Izaias",
                "last_name": "Henrique",
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
                "User_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "izaias.junior@inner.com",
                "first_name": "Izaias",
                "last_name": "Henrique",
            }
        },
    )

    user_id: str = Field(..., alias="id", description="ID único do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    first_name: Optional[str] = Field(None, description="Primeiro nome do usuário")
    last_name: Optional[str] = Field(None, description="Último nome do usuário")
