from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    QWEN_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./memorai.db"
    
    # Redis (optional)
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    
    # Server
    DEFAULT_PROVIDER: str = "openai"
    MAX_CONTEXT_TOKENS: int = 8000
    MEMORY_RETENTION_DAYS: int = 30
    LOG_LEVEL: str = "INFO"
    
    # CORS
    ALLOWED_ORIGINS: str = "*"
    
    class Config:
        env_file = ".env"

settings = Settings()