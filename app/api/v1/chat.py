from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.providers.factory import get_provider
from app.memory.engine import MemoryEngine
from app.models.user import User
from app.models.chat import ChatMessage
from app.models.memory import Memory
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    provider: Optional[str] = None
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

class ChatResponse(BaseModel):
    id: str
    user_id: str
    message: str
    timestamp: str
    tokens_used: int
    memory_injected: bool

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Load or create user
        user = db.query(User).filter(User.user_id == request.user_id).first()
        if not user:
            user = User(user_id=request.user_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Update last active
        user.last_active = datetime.utcnow()
        db.commit()
        
        # Initialize memory engine
        memory_engine = MemoryEngine(db)
        
        # Retrieve relevant memories
        relevant_memories = memory_engine.get_relevant_memories(request.user_id, request.message)
        
        # Build system prompt with memory
        system_prompt_parts = []
        if user.system_prompt:
            system_prompt_parts.append(user.system_prompt)
        
        if user.profile:
            if user.profile.get('name'):
                system_prompt_parts.append(f"User name: {user.profile['name']}")
            if user.profile.get('language'):
                system_prompt_parts.append(f"Preferred language: {user.profile['language']}")
            if user.profile.get('custom_instructions'):
                system_prompt_parts.append(user.profile['custom_instructions'])
        
        if relevant_memories:
            memory_context = "\n".join([mem.content for mem in relevant_memories])
            system_prompt_parts.append(f"\nRelevant context from previous conversations:\n{memory_context}")
        
        system_prompt = "\n".join(system_prompt_parts) if system_prompt_parts else "You are a helpful AI assistant."
        
        # Prepare messages for the LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]
        
        # Get response from provider
        provider = get_provider(request.provider)
        response_data = await provider.chat_completion(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Save the conversation
        chat_message = ChatMessage(
            user_id=request.user_id,
            role="user",
            content=request.message
        )
        assistant_message = ChatMessage(
            user_id=request.user_id,
            role="assistant",
            content=response_data["message"],
            tokens_used=response_data["usage"]["total_tokens"]
        )
        
        db.add(chat_message)
        db.add(assistant_message)
        db.commit()
        
        # Update memory with the conversation
        memory_engine.store_conversation_memory(
            user_id=request.user_id,
            user_message=request.message,
            assistant_response=response_data["message"]
        )
        
        return ChatResponse(
            id=str(uuid.uuid4()),
            user_id=request.user_id,
            message=response_data["message"],
            timestamp=datetime.utcnow().isoformat(),
            tokens_used=response_data["usage"]["total_tokens"],
            memory_injected=len(relevant_memories) > 0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")