from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

class Provider(str, Enum):
    openai = "openai"
    qwen = "qwen"
    deepseek = "deepseek"
    pollinations = "pollinations"

class ChatRequest(BaseModel):
    user_id: UUID
    message: str
    provider: Provider = Provider.openai
    temperature: float = 0.7
    max_tokens: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    tokens_used: Optional[dict] = None

class UserPreferences(BaseModel):
    name: Optional[str] = None
    language_preference: Optional[str] = None
    tone_style_preference: Optional[str] = None
    custom_instructions: Optional[str] = None
    system_prompt: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    name: Optional[str]
    language_preference: str
    tone_style_preference: Optional[str]
    custom_instructions: Optional[str]
    system_prompt: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: int
    last_active: datetime

class MemoryEntry(BaseModel):
    id: UUID
    user_id: UUID
    memory_type: str
    content: str
    importance_score: int
    topic: Optional[str]
    is_favorited: bool
    created_at: datetime
    updated_at: datetime
    last_accessed: datetime

class PruneRequest(BaseModel):
    user_id: UUID
    days_to_keep: int = 30
    min_importance: int = 3