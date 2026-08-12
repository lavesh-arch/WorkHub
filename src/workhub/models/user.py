import uuid
from enum import Enum
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime, Enum as SQLenum
from sqlalchemy.dialects.postgresql import UUID


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
    )

    email: str = Field(
        sa_column=Column(
            String,
            nullable=False,
            unique=True,
        )
    )

    full_name: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )

    password_hash: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )

    role: UserRole = Field(
        sa_column=Column(
            SQLenum(UserRole),
            nullable=False,
        )
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
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