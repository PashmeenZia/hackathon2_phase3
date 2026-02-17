from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID or None for new conversation")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    conversation_id: str = Field(..., description="Conversation ID")
    response: str = Field(..., description="AI assistant response")
    timestamp: str = Field(..., description="Response timestamp in ISO format")


class MessageSchema(BaseModel):
    """Schema for individual message"""
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")
    created_at: str = Field(..., description="Message timestamp")


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history"""
    conversation_id: str
    messages: list[MessageSchema]
