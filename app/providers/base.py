from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator

class BaseProvider(ABC):
    @abstractmethod
    async def chat_completion(self, messages: list, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def stream_completion(self, messages: list, **kwargs) -> AsyncGenerator[str, None]:
        pass