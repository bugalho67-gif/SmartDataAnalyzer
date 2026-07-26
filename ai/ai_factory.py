from __future__ import annotations

import os

from ai.providers.base import BaseProvider
from ai.providers.local import LocalProvider

# Descomente quando implementar os provedores
#
# from ai.providers.openai_provider import OpenAIProvider
# from ai.providers.gemini_provider import GeminiProvider
# from ai.providers.ollama_provider import OllamaProvider


class AIProviderFactory:
    """
    Responsável por instanciar o provedor de IA
    configurado na aplicação.
    """

    _providers = {

        "local": LocalProvider,

        # "openai": OpenAIProvider,
        # "gemini": GeminiProvider,
        # "ollama": OllamaProvider,

    }

    @classmethod
    def available_providers(cls) -> list[str]:
        """
        Retorna os provedores registrados.
        """

        return sorted(cls._providers.keys())

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[BaseProvider]
    ) -> None:
        """
        Permite registrar novos provedores
        dinamicamente.
        """

        cls._providers[name.lower()] = provider

    @classmethod
    def create(
        cls,
        provider_name: str | None = None
    ) -> BaseProvider:
        """
        Cria uma instância do provedor escolhido.

        Caso nenhum seja informado, utiliza a variável
        de ambiente AI_PROVIDER.

        Se o provedor não existir, utiliza LocalProvider.
        """

        if provider_name is None:

            provider_name = os.getenv(
                "AI_PROVIDER",
                "local"
            )

        provider_name = provider_name.lower()

        provider_class = cls._providers.get(
            provider_name,
            LocalProvider
        )

        return provider_class()


def get_provider(
    provider_name: str | None = None
) -> BaseProvider:
    """
    Função auxiliar para manter a API simples.

    Exemplo:

    provider = get_provider()

    ou

    provider = get_provider("gemini")
    """

    return AIProviderFactory.create(
        provider_name
    )
