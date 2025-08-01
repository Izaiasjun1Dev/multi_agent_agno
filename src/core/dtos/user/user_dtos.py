from uuid import uuid4
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

class CreateUserDto(BaseModel):
    user_id: Optional[str] = Field(default=str(uuid4()), alias="id")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
