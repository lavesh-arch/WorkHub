import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from workhub.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    role: UserRole | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserProfileUpdate(BaseModel):
    avatar_url: str | None = None
    bio: str | None = Field(default=None, max_length=1000)


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    avatar_url: str | None
    bio: str | None
    created_at: datetime
    updated_at: datetime