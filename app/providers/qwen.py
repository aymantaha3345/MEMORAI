from app.providers.base import BaseProvider
from typing import Dict, Any, List
import httpx

class QwenProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert messages to Qwen format
        prompt_messages = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            prompt_messages.append({"role": role, "content": content})
        
        payload = {
            "model": kwargs.get("model", "qwen-max"),
            "input": {
                "messages": prompt_messages
            },
            "parameters": {
                "temperature": kwargs.get("temperature", 0.7),
            }
        }
        
        if kwargs.get("max_tokens"):
            payload["parameters"]["max_tokens"] = kwargs["max_tokens"]
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Qwen API error: {response.status_code} - {response.text}")
                
            result = response.json()
            return {
                "content": result["output"]["text"],
                "usage": result.get("usage", {}),
                "model": result["request_id"]
            }

    def validate_config(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)