from sqlalchemy import Column, String, DateTime, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class Memory(Base):
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, index=True, nullable=False)
    memory_type = Column(String, index=True)  # short_term, long_term, summary
    content = Column(Text)
    relevance_score = Column(Integer, default=0)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)