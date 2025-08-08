from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GetUserDetailsDto(BaseModel):
    token: str = Field(..., description="The authentication token of the user")


class UserDetailsResponseDto(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    user_sub: str = Field(
        ..., description="User sub (same as user_id for compatibility)"
    )
    email: str = Field(..., description="Email address of the user")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    name: Optional[str] = Field(None, description="Full name of the user")
    email_verified: bool = Field(True, description="Indicates if email is verified")
    is_active: bool = Field(..., description="Indicates if the user is active")


class LoginDto(BaseModel):
    email: str = Field(
        default="solucaoprogramer@gmail.com",
        description="The email of the user",
        title="User Email",
    )
    password: str = Field(
        default="1213@Cronicas",
        description="The password of the user",
        title="User Password",
    )


class ConfirmEmailDto(BaseModel):
    email: str = Field(..., description="The email of the user to confirm")
    confirmation_token: str = Field(
        ..., description="The confirmation token sent to the user's email"
    )
