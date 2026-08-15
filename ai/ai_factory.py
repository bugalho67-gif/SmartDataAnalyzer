"""Compatibilidade com a factory antiga de IA."""

from __future__ import annotations

from ai.llm_factory import available_providers, create_llm_provider
from providers.base import BaseProvider


class AIProviderFactory:
    """Facade compatível com versões anteriores da aplicação."""

    @classmethod
    def available_providers(cls) -> list[str]:
        """Retorna os provedores registrados."""
        return available_providers()

    @classmethod
    def register(cls, name: str, provider: type[BaseProvider]) -> None:
        """Mantido apenas por compatibilidade; use `ai.llm_factory` em código novo."""
        from ai.llm_factory import _PROVIDER_REGISTRY

        _PROVIDER_REGISTRY[name.lower()] = provider

    @classmethod
    def create(cls, provider_name: str | None = None) -> BaseProvider:
        """Cria uma instância do provedor escolhido."""
        return create_llm_provider(provider_name)


def get_provider(provider_name: str | None = None) -> BaseProvider:
    """Função auxiliar para manter a API legada simples."""
    return AIProviderFactory.create(provider_name)
