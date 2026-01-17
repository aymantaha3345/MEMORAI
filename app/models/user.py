from sqlalchemy import Column, String, DateTime, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, unique=True, index=True, nullable=False)
    profile = Column(JSON, default={})
    system_prompt = Column(Text, default="")
    conversation_state = Column(JSON, default={})
    memory = Column(JSON, default={})
    favorites = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)