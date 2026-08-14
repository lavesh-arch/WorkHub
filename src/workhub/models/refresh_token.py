import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

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
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )

    token_hash: str = Field(
        sa_column=Column(
            String,
            nullable=False,
            unique=True,
        ),
    )

    expires_at: datetime = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
        ),
    )

    revoked_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime,
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