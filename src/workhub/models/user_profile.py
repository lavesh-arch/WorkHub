import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profile"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(
            UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=False,
            unique=True,
        )
    )

    avatar_url: str | None = Field(
        default=None,
        sa_column=Column(
            String,
            nullable=True,
        ),
    )

    bio: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            nullable=False,
            onupdate=datetime.utcnow,
        ),
    )