"""Provedor de IA utilizando a API oficial da OpenAI."""

from __future__ import annotations

import os

from core.exceptions import AIError
from core.logger import logger
from providers.base import BaseProvider, Message


class OpenAIProvider(BaseProvider):
    """Adapter para modelos OpenAI compatíveis com Chat Completions."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = (
            temperature
            if temperature is not None
            else float(os.getenv("AI_TEMPERATURE", "0.2"))
        )

        if not self.api_key:
            logger.warning("OPENAI_API_KEY não configurada.")

    def chat(self, messages: list[Message]) -> str:
        """Envia mensagens para a API da OpenAI e retorna o texto gerado."""
        if not self.api_key:
            raise AIError("Chave da OpenAI não configurada. Defina OPENAI_API_KEY.")

        try:
            import openai
        except ImportError as exc:
            raise AIError("Biblioteca 'openai' não instalada.") from exc

        client = openai.OpenAI(api_key=self.api_key)

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            return response.choices[0].message.content or "Sem resposta."
        except openai.AuthenticationError as exc:
            logger.exception("Falha de autenticação na OpenAI")
            raise AIError("Chave da OpenAI inválida ou expirada.") from exc
        except openai.RateLimitError as exc:
            logger.exception("Rate limit atingido na OpenAI")
            raise AIError("Limite de requisições atingido. Tente novamente.") from exc
        except Exception as exc:
            logger.exception("Erro inesperado na OpenAI")
            raise AIError(f"Erro ao consultar OpenAI: {exc}") from exc
