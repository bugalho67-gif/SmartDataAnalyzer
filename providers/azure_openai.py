"""Provedor Azure OpenAI compatível com Chat Completions."""

from __future__ import annotations

import os

from core.exceptions import AIError
from core.logger import logger
from providers.base import BaseProvider, Message


class AzureOpenAIProvider(BaseProvider):
    """Adapter para deployments do Azure OpenAI."""

    def __init__(self) -> None:
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.2"))

    def chat(self, messages: list[Message]) -> str:
        """Envia mensagens ao deployment configurado no Azure OpenAI."""
        if not self.api_key or not self.endpoint:
            raise AIError("Configure AZURE_OPENAI_API_KEY e AZURE_OPENAI_ENDPOINT.")

        try:
            import openai
        except ImportError as exc:
            raise AIError("Biblioteca 'openai' não instalada.") from exc

        client = openai.AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
        )
        try:
            response = client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=self.temperature,
            )
            return response.choices[0].message.content or "Sem resposta."
        except Exception as exc:
            logger.exception("Erro inesperado no Azure OpenAI")
            raise AIError(f"Erro ao consultar Azure OpenAI: {exc}") from exc
