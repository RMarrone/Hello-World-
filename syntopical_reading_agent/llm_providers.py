"""
LLM Provider Abstraction Layer

Supports multiple LLM backends with a unified interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import os


class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        """Generate a completion from the LLM."""
        pass

    @abstractmethod
    def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a completion with conversation context."""
        pass


class ClaudeProvider(LLMProvider):
    """Anthropic Claude API provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude provider.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use (default: claude-sonnet-4-20250514)
        """
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY or pass api_key parameter")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        """Generate completion from Claude."""
        max_tokens = kwargs.get("max_tokens", 4096)
        temperature = kwargs.get("temperature", 1.0)

        message_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system:
            message_params["system"] = system

        response = self.client.messages.create(**message_params)
        return response.content[0].text

    def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion with conversation context."""
        max_tokens = kwargs.get("max_tokens", 4096)
        temperature = kwargs.get("temperature", 1.0)
        system = kwargs.get("system")

        message_params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system:
            message_params["system"] = system

        response = self.client.messages.create(**message_params)
        return response.content[0].text


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4-turbo-preview)
        """
        try:
            import openai
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set OPENAI_API_KEY or pass api_key parameter")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        """Generate completion from OpenAI."""
        max_tokens = kwargs.get("max_tokens", 4096)
        temperature = kwargs.get("temperature", 1.0)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content

    def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate completion with conversation context."""
        max_tokens = kwargs.get("max_tokens", 4096)
        temperature = kwargs.get("temperature", 1.0)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content


def get_provider(provider_name: str = "claude", **kwargs) -> LLMProvider:
    """
    Factory function to get an LLM provider.

    Args:
        provider_name: Name of provider ("claude" or "openai")
        **kwargs: Additional arguments for the provider

    Returns:
        LLMProvider instance
    """
    providers = {
        "claude": ClaudeProvider,
        "openai": OpenAIProvider,
    }

    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_name}. Available: {list(providers.keys())}")

    return provider_class(**kwargs)
