from typing import List, Dict, Any
from uuid import UUID
from app.memory.storage import MemoryStorage
from app.models.memory import Memory
from app.models.user import User
from app.providers import get_provider
from app.models.schemas import Provider as ProviderEnum
from app.core.config import settings
import re

class MemoryManager:
    def __init__(self, db_session):
        self.storage = MemoryStorage(db_session)
        self.db = db_session

    def analyze_relevance(self, message: str, memories: List[Memory]) -> List[Memory]:
        """Analyze which memories are relevant to the current message"""
        relevant_memories = []
        message_lower = message.lower()
        
        for memory in memories:
            # Simple keyword matching for now, could be enhanced with semantic similarity
            memory_content_lower = memory.content.lower()
            
            # Check if message contains keywords from memory or vice versa
            if any(word in memory_content_lower for word in message_lower.split()[:10]):
                relevant_memories.append(memory)
            elif any(word in message_lower for word in memory_content_lower.split()[:10]):
                relevant_memories.append(memory)
        
        return relevant_memories

    def build_context(self, user_id: UUID, message: str, max_tokens: int = 3000) -> List[Dict[str, str]]:
        """Build the context with relevant memories for the LLM"""
        # Get user profile
        user = self.db.query(User).filter(User.id == user_id).first()
        
        # Start with system prompt
        context = []
        
        # Add user-specific system prompt if available
        if user and user.system_prompt:
            context.append({
                "role": "system",
                "content": user.system_prompt
            })
        
        # Add user preferences as additional context
        if user:
            user_context = f"User preferences:\n- Language: {user.language_preference}\n"
            if user.tone_style_preference:
                user_context += f"- Tone: {user.tone_style_preference}\n"
            if user.custom_instructions:
                user_context += f"- Instructions: {user.custom_instructions}\n"
            
            if len(context) == 0:
                context.append({
                    "role": "system",
                    "content": user_context
                })
            else:
                # Append to existing system message
                context[0]["content"] += "\n\n" + user_context
        
        # Get relevant memories
        all_memories = self.storage.get_memories_by_user(user_id, limit=20)
        relevant_memories = self.analyze_relevance(message, all_memories)
        
        # Add relevant memories to context
        for memory in relevant_memories:
            memory_text = f"[{memory.memory_type.upper()}] {memory.topic}: {memory.content}"
            context.append({
                "role": "system",
                "content": memory_text
            })
        
        # Add the user's current message
        context.append({
            "role": "user",
            "content": message
        })
        
        # TODO: Implement token counting to ensure we don't exceed max_tokens
        # For now, return the full context
        
        return context

    def update_memories(self, user_id: UUID, input_message: str, response: str):
        """Update memories based on the conversation"""
        # Save the input message as a memory
        self.storage.save_memory(
            user_id=user_id,
            content=input_message,
            memory_type="short_term",
            importance_score=self._calculate_importance(input_message),
            topic=self._extract_topic(input_message)
        )
        
        # Save the response as a memory
        self.storage.save_memory(
            user_id=user_id,
            content=response,
            memory_type="short_term",
            importance_score=self._calculate_importance(response),
            topic=self._extract_topic(response)
        )
        
        # Update user's message count
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.message_count += 1
            self.db.commit()

    def _calculate_importance(self, text: str) -> int:
        """Calculate importance score for a piece of text (1-10)"""
        # Simple heuristics for importance calculation
        score = 5  # Base score
        
        # Increase score for longer texts (likely more detailed information)
        if len(text) > 100:
            score += 1
        if len(text) > 500:
            score += 1
            
        # Increase score if text contains certain keywords indicating importance
        important_keywords = ['important', 'remember', 'critical', 'essential', 'key', 'crucial']
        for keyword in important_keywords:
            if keyword.lower() in text.lower():
                score += 1
                
        # Cap at 10
        return min(score, 10)

    def _extract_topic(self, text: str) -> str:
        """Extract a topic from text"""
        # Simple topic extraction - just take first few words as topic
        words = text.split()[:5]
        return " ".join(words) if words else "General"

    def summarize_conversation(self, user_id: UUID, messages: List[Dict[str, str]]) -> str:
        """Summarize a conversation for long-term storage"""
        # For now, create a simple summary
        # In a real implementation, this would call an LLM to create a proper summary
        summary_parts = []
        for msg in messages[-10:]:  # Last 10 messages
            role = msg['role'].upper()
            content = msg['content'][:100]  # First 100 chars
            summary_parts.append(f"{role}: {content}")
        
        summary = " | ".join(summary_parts)
        
        # Save as a long-term memory
        self.storage.save_memory(
            user_id=user_id,
            content=summary,
            memory_type="summary",
            importance_score=7,  # Summaries tend to be important
            topic="Conversation Summary"
        )
        
        return summary