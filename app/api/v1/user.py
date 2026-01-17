from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserProfile(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    tone_preference: Optional[str] = None
    custom_instructions: Optional[str] = None

class UserPreferencesUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    tone_preference: Optional[str] = None
    custom_instructions: Optional[str] = None

@router.get("/user/{user_id}")
async def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.user_id,
        "profile": user.profile or {},
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_active": user.last_active.isoformat() if user.last_active else None
    }

@router.post("/user/{user_id}/preferences")
async def update_user_preferences(
    user_id: str, 
    preferences: UserPreferencesUpdate, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(user_id=user_id)
        db.add(user)
    
    # Update profile
    if not user.profile:
        user.profile = {}
    
    if preferences.name is not None:
        user.profile["name"] = preferences.name
    if preferences.language is not None:
        user.profile["language"] = preferences.language
    if preferences.tone_preference is not None:
        user.profile["tone_preference"] = preferences.tone_preference
    if preferences.custom_instructions is not None:
        user.profile["custom_instructions"] = preferences.custom_instructions
    
    db.commit()
    db.refresh(user)
    
    return {
        "user_id": user.user_id,
        "profile": user.profile,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }