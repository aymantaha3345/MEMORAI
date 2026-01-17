from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat, user, memory
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MEMORAI - Persistent AI Memory Server",
    description="A middleware server that provides persistent memory for AI interactions",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(user.router, prefix="/api/v1", tags=["user"])
app.include_router(memory.router, prefix="/api/v1", tags=["memory"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "providers": ["openai"],  # Could expand based on config
        "database": "connected",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)