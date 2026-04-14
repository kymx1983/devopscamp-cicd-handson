from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Text, TIMESTAMP, text
from sqlmodel import Field, SQLModel


class NoteCreate(SQLModel):
    title: str = Field(max_length=100)
    content: str


class Note(SQLModel, table=True):
    __tablename__ = "notes"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str = Field(sa_column=Column(Text, nullable=False))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
    )