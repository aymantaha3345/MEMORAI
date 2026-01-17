from app.providers.base import BaseProvider
from typing import Dict, Any, AsyncGenerator
from openai import AsyncOpenAI
from app.core.config import settings

class OpenAIProvider(BaseProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def chat_completion(self, messages: list, **kwargs) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                messages=messages,
                **kwargs
            )
            
            return {
                "id": response.id,
                "message": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            raise Exception(f"OpenAI API Error: {str(e)}")
    
    async def stream_completion(self, messages: list, **kwargs) -> AsyncGenerator[str, None]:
        try:
            stream = await self.client.chat.completions.create(
                messages=messages,
                stream=True,
                **kwargs
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(f"OpenAI Stream Error: {str(e)}")