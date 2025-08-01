from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class Org(BaseModel):
    org_id: str = Field(
        ...,
        title="Organization ID",
        description="Unique identifier for the organization",
        alias="orgId"
    )
    name: str = Field(
        ...,
        title="Organization Name",
        description="Name of the organization",
        alias="name"
    )
    domain: Optional[str] = Field(
        None,
        title="Domain",
        description="Domain name of the organization",
        alias="domain"
    )
    slug: Optional[str] = Field(
        None,
        title="Slug",
        description="URL-friendly identifier for the organization",
        alias="slug"
    )
    is_active: bool = Field(
        True,
        title="Active Status",
        description="Indicates if the organization is active",
        alias="isActive"
    )
    users: List[str] = Field(
        default_factory=list,
        title="Users",
        description="List of user IDs associated with the organization",
    )
    admins: List[str] = Field(
        default_factory=list,
        title="Admins",
        description="List of admin user IDs for the organization",
        alias="admins"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        title="Creation Timestamp",
        description="Timestamp when the organization was created",
        alias="createdAt"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        title="Update Timestamp",
        description="Timestamp when the organization was last updated",
        alias="updatedAt"
    )