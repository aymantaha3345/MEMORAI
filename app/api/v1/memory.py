from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.memory.engine import MemoryEngine
from pydantic import BaseModel

router = APIRouter()

class PruneRequest(BaseModel):
    user_id: str
    retention_days: int = 30

@router.post("/memory/prune")
async def prune_memory(request: PruneRequest, db: Session = Depends(get_db)):
    memory_engine = MemoryEngine(db)
    pruned_count = memory_engine.prune_old_memory(
        user_id=request.user_id,
        retention_days=request.retention_days
    )
    
    return {
        "status": "success",
        "pruned_count": pruned_count,
        "retention_days": request.retention_days
    }