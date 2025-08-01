from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field

from core.entities.chat import Chat


class User(BaseModel):
    user_id: str = Field(
        default=str(uuid4()),
        title="User ID",
        description="Unique identifier for the user",
        alias="userId",
    )
    email: EmailStr = Field(
        ..., title="Email", description="Email address of the user", alias="email"
    )
    first_name: Optional[str] = Field(
        None, title="First Name", description="First name of the user", alias="firstName"
    )
    last_name: Optional[str] = Field(
        None, title="Last Name", description="Last name of the user", alias="lastName"
    )
    roles: Optional[List[str]] = Field(
        title="Roles",
        description="List of roles assigned to the user",
        alias="roles",
    )
    is_active: bool = Field(
        False,
        title="Active Status",
        description="Indicates if the user is active",
        alias="isActive",
    )
    org_id: Optional[str] = Field(
        None,
        title="Organization",
        description="Organization to which the user belongs",
        alias="org",
    )
    chats: Optional[List[Chat]] = Field(
        None,
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
        default_factory=lambda: datetime.now(),
        title="Creation Timestamp",
        description="Timestamp when the user was created",
        alias="createdAt",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        title="Update Timestamp",
        description="Timestamp when the user was last updated",
        alias="updatedAt",
    )
