from app.providers.base import BaseProvider
from typing import Dict, Any, List
import httpx

class DeepSeekProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.deepseek.com/chat/completions"
        
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": kwargs.get("model", "deepseek-chat"),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
        }
        
        if kwargs.get("max_tokens"):
            payload["max_tokens"] = kwargs["max_tokens"]
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")
                
            result = response.json()
            return {
                "content": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "model": result["model"]
            }

    def validate_config(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)