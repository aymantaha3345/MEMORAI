from app.providers.openai import OpenAIProvider
from app.providers.base import BaseProvider
from app.core.config import settings

def get_provider(provider_name: str = None) -> BaseProvider:
    """Factory function to get the appropriate provider instance."""
    if not provider_name:
        provider_name = settings.DEFAULT_PROVIDER.lower()
    
    if provider_name == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")