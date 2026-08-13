"""Factory unificada de provedores LLM."""

from __future__ import annotations

import os

from providers.azure_openai import AzureOpenAIProvider
from providers.base import BaseProvider
from providers.claude import ClaudeProvider
from providers.gemini import GeminiProvider
from providers.local import LocalProvider
from providers.ollama import OllamaProvider
from providers.openai import OpenAIProvider

_PROVIDER_REGISTRY: dict[str, type[BaseProvider]] = {
    "local": LocalProvider,
    "openai": OpenAIProvider,
    "azure_openai": AzureOpenAIProvider,
    "azure-openai": AzureOpenAIProvider,
    "gemini": GeminiProvider,
    "claude": ClaudeProvider,
    "anthropic": ClaudeProvider,
    "ollama": OllamaProvider,
}


def available_providers() -> list[str]:
    """Lista provedores disponíveis na factory."""
    return sorted(_PROVIDER_REGISTRY)


def create_llm_provider(provider_name: str | None = None) -> BaseProvider:
    """Cria o provedor configurado por argumento ou variável `LLM_PROVIDER`."""
    selected_provider = (provider_name or os.getenv("LLM_PROVIDER") or os.getenv("AI_PROVIDER") or "local")
    provider_class = _PROVIDER_REGISTRY.get(selected_provider.lower(), LocalProvider)
    return provider_class()
