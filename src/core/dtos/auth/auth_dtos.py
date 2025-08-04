from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class LoginDto(BaseModel):
    email: str = Field(..., description="The email of the user")
    password: str = Field(..., description="The password of the user")
    
    
    