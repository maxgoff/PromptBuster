from abc import ABC, abstractmethod
from typing import Optional
import openai
import anthropic
import requests
from .models import LLMConfig, LLMProvider


class BaseLLMProvider(ABC):
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = openai.OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = anthropic.Anthropic(api_key=config.api_key)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class LocalProvider(BaseLLMProvider):
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        payload = {
            "prompt": prompt,
            "system": system_prompt,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        response = requests.post(
            f"{self.config.base_url}/generate",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]


def create_provider(config: LLMConfig) -> BaseLLMProvider:
    if config.provider == LLMProvider.OPENAI:
        return OpenAIProvider(config)
    elif config.provider == LLMProvider.ANTHROPIC:
        return AnthropicProvider(config)
    elif config.provider == LLMProvider.LOCAL:
        return LocalProvider(config)
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")