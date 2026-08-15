from __future__ import annotations

from ai.ai_client import AIClient


class OpenAIClient(AIClient):
    """
    Cliente OpenAI.

    A implementação ficará pronta
    quando a API for configurada.
    """

    def __init__(self, api_key: str):

        self.api_key = api_key

    def ask(self, question: str, context: str) -> str:

        raise NotImplementedError("Integração OpenAI ainda não implementada.")
