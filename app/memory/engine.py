from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.models.user import User
from app.models.chat import ChatMessage
from datetime import datetime, timedelta
from typing import List
import uuid

class MemoryEngine:
    def __init__(self, db: Session):
        self.db = db
    
    def get_relevant_memories(self, user_id: str, current_query: str) -> List[Memory]:
        """Retrieve relevant memories for the current query."""
        # For now, return recent memories - in a real implementation, 
        # we would use semantic search or other techniques
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        memories = self.db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.created_at >= cutoff_date
        ).order_by(Memory.created_at.desc()).limit(10).all()
        
        return memories
    
    def store_conversation_memory(self, user_id: str, user_message: str, assistant_response: str):
        """Store conversation parts as memory."""
        # Store user message as memory
        user_memory = Memory(
            user_id=user_id,
            memory_type="short_term",
            content=f"User said: {user_message}",
            relevance_score=5,
            tags=["conversation", "user_input"]
        )
        
        # Store assistant response as memory
        assistant_memory = Memory(
            user_id=user_id,
            memory_type="short_term",
            content=f"Assistant replied: {assistant_response}",
            relevance_score=5,
            tags=["conversation", "assistant_response"]
        )
        
        self.db.add(user_memory)
        self.db.add(assistant_memory)
        self.db.commit()
    
    def summarize_conversation(self, user_id: str, conversation_history: List[dict]) -> str:
        """Summarize a conversation for long-term memory."""
        # In a real implementation, this would call an LLM to create a summary
        # For now, return a simple concatenation
        summary = "Summary of conversation: "
        for msg in conversation_history[-5:]:  # Last 5 messages
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:100]  # First 100 chars
            summary += f"{role}: {content}... "
        
        return summary
    
    def store_summary_memory(self, user_id: str, summary: str):
        """Store a summary as long-term memory."""
        summary_memory = Memory(
            user_id=user_id,
            memory_type="long_term",
            content=summary,
            relevance_score=8,
            tags=["summary", "long_term"]
        )
        
        self.db.add(summary_memory)
        self.db.commit()
    
    def prune_old_memory(self, user_id: str, retention_days: int = 30) -> int:
        """Remove old memories based on retention policy."""
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        deleted_count = self.db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.created_at < cutoff_date
        ).delete()
        
        self.db.commit()
        return deleted_count