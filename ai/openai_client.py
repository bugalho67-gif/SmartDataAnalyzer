from ai.ai_client import AIClient


class OpenAIClient(AIClient):

    def __init__(self, api_key: str):

        self.api_key = api_key

    def ask(
        self,
        question: str,
        context: str
    ) -> str:

        # Aqui ficará a integração
        # com a API futuramente.

        raise NotImplementedError(
            "Integração com OpenAI ainda não implementada."
        )
