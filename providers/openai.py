"""Provedor de IA utilizando a API oficial da OpenAI."""

from __future__ import annotations

import os

from core.exceptions import AIError
from core.logger import logger
from providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    Provedor de IA que consome a API da OpenAI.

    Parameters
    ----------
    api_key : str, optional
        Chave de API da OpenAI. Se não informada, lê da variável
        de ambiente ``OPENAI_API_KEY``.
    model : str, optional
        Modelo a ser utilizado. Padrão: ``gpt-4o-mini``.
    temperature : float, optional
        Temperatura de amostragem. Padrão: ``0.2``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature

        if not self.api_key:
            logger.warning(
                "OPENAI_API_KEY não configurada. "
                "O provedor OpenAI não funcionará."
            )

    def ask(self, question: str, context: str) -> str:
        """
        Envia a pergunta + contexto para a API da OpenAI.

        Parameters
        ----------
        question : str
            Pergunta do usuário.
        context : str
            Contexto dos dados (resumo, estatísticas, etc.).

        Returns
        -------
        str
            Resposta gerada pelo modelo.

        Raises
        ------
        AIError
            Se a API retornar erro ou a chave não estiver configurada.
        """
        if not self.api_key:
            raise AIError(
                "Chave da OpenAI não configurada. "
                "Defina OPENAI_API_KEY no arquivo .env"
            )

        try:
            import openai
        except ImportError as exc:
            raise AIError(
                "Biblioteca 'openai' não instalada. "
                "Execute: pip install openai"
            ) from exc

        client = openai.OpenAI(api_key=self.api_key)

        system_prompt = (
            "Você é um assistente de análise de dados. "
            "Responda em português do Brasil de forma clara e objetiva. "
            "Use o contexto dos dados fornecido para fundamentar suas respostas."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contexto dos dados:\n{context}\n\nPergunta: {question}"},
        ]

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
            raise AIError("Limite de requisições atingido. Tente novamente em alguns segundos.") from exc
        except Exception as exc:
            logger.exception("Erro inesperado na OpenAI")
            raise AIError(f"Erro ao consultar OpenAI: {exc}") from exc
