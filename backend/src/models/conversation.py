from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class ConversationBase(SQLModel):
    """Base model for conversations"""
    pass

class Conversation(ConversationBase, table=True):
    """Conversation model for storing chat sessions"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

    __tablename__ = "conversations"


class MessageBase(SQLModel):
    """Base model for messages"""
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=10000)

class Message(MessageBase, table=True):
    """Message model for storing chat messages"""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    __tablename__ = "messages"
