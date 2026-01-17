from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.models.user import User
from typing import List, Optional
from uuid import UUID

class MemoryStorage:
    def __init__(self, db: Session):
        self.db = db

    def save_memory(self, user_id: UUID, content: str, memory_type: str = "short_term", 
                   importance_score: int = 5, topic: Optional[str] = None) -> Memory:
        """Save a new memory entry"""
        memory = Memory(
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            importance_score=importance_score,
            topic=topic
        )
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory

    def get_memories_by_user(self, user_id: UUID, memory_types: List[str] = None, 
                           limit: int = 10) -> List[Memory]:
        """Retrieve memories for a user"""
        query = self.db.query(Memory).filter(Memory.user_id == user_id)
        
        if memory_types:
            query = query.filter(Memory.memory_type.in_(memory_types))
        
        # Order by importance score descending, then by creation date descending
        memories = query.order_by(
            Memory.importance_score.desc(),
            Memory.created_at.desc()
        ).limit(limit).all()
        
        return memories

    def get_recent_memories(self, user_id: UUID, days: int = 7, limit: int = 10) -> List[Memory]:
        """Get recent memories for a user"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        memories = self.db.query(Memory)\
            .filter(
                Memory.user_id == user_id,
                Memory.created_at >= cutoff_date
            )\
            .order_by(Memory.created_at.desc())\
            .limit(limit)\
            .all()
        
        return memories

    def update_memory_importance(self, memory_id: UUID, importance_score: int):
        """Update the importance score of a memory"""
        memory = self.db.query(Memory).filter(Memory.id == memory_id).first()
        if memory:
            memory.importance_score = importance_score
            self.db.commit()

    def delete_memory(self, memory_id: UUID):
        """Delete a memory entry"""
        memory = self.db.query(Memory).filter(Memory.id == memory_id).first()
        if memory:
            self.db.delete(memory)
            self.db.commit()

    def prune_old_memories(self, user_id: UUID, days_to_keep: int = 30, min_importance: int = 3):
        """Remove old memories that are below the importance threshold"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        # Delete memories older than cutoff date with importance below threshold
        deleted_count = self.db.query(Memory)\
            .filter(
                Memory.user_id == user_id,
                Memory.created_at < cutoff_date,
                Memory.importance_score < min_importance
            )\
            .delete()
        
        self.db.commit()
        return deleted_count