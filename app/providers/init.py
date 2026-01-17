from app.providers.openai import OpenAIProvider
from app.providers.qwen import QwenProvider
from app.providers.deepseek import DeepSeekProvider
from app.models.schemas import Provider

def get_provider(provider_type: Provider, api_key: str):
    providers = {
        Provider.openai: OpenAIProvider,
        Provider.qwen: QwenProvider,
        Provider.deepseek: DeepSeekProvider,
    }
    
    if provider_type not in providers:
        raise ValueError(f"Unsupported provider: {provider_type}")
    
    return providers[provider_type](api_key)