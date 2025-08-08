from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    field_serializer,
)

from core.entities.chat import Chat


class User(BaseModel):
    model_config = ConfigDict(
        # Permite uso de alias nos campos
        populate_by_name=True
    )

    user_id: str = Field(
        default_factory=lambda: str(uuid4()),  # Mudado de default para default_factory
        title="User ID",
        description="Unique identifier for the user",
        alias="userId",
    )
    email: EmailStr = Field(
        default="",
        title="Email",
        description="Email address of the user",
        alias="email",
    )
    first_name: Optional[str] = Field(
        default=None,
        title="First Name",
        description="First name of the user",
        alias="firstName",
    )
    last_name: Optional[str] = Field(
        default=None,
        title="Last Name",
        description="Last name of the user",
        alias="lastName",
    )
    is_active: bool = Field(
        False,
        title="Active Status",
        description="Indicates if the user is active",
        alias="isActive",
    )
    chats: Optional[List[Chat]] = Field(
        default=None,
        title="Chats",
        description="List of chats associated with the user",
        alias="chats",
    )
    slug: Optional[str] = Field(
        None,
        title="Slug",
        description="URL-friendly identifier for the user",
        alias="slug",
    )
    avatar_url: Optional[str] = Field(
        None,
        title="Avatar URL",
        description="URL of the user's avatar image",
        alias="avatarUrl",
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,  # Simplificado
        title="Creation Timestamp",
        description="Timestamp when the user was created",
        alias="createdAt",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,  # Simplificado
        title="Update Timestamp",
        description="Timestamp when the user was last updated",
        alias="updatedAt",
    )

    @computed_field
    @property
    def name(self) -> Optional[str]:
        """Retorna o nome completo combinando first_name e last_name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return None

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: Optional[datetime], _info):
        """Serializa datetime para ISO format string"""
        if dt:
            return dt.isoformat()
        return None
