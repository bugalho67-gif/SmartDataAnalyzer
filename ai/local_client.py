from ai.ai_client import AIClient


class LocalAIClient(AIClient):

    def ask(
        self,
        question: str,
        context: str
    ) -> str:

        return f"""
Pergunta:
{question}

Contexto recebido:

{context}

Nenhum provedor de IA foi configurado.

Configure OpenAI, Gemini, Claude ou outro modelo
para obter respostas inteligentes.
"""
