from ai.ai_client import AIClient


class LocalAIClient(AIClient):
    """
    Cliente local.

    Utilizado quando nenhuma IA
    estiver configurada.
    """

    def ask(self, question: str, context: str) -> str:

        resposta = f"""
### Pergunta

{question}

---

Nenhum provedor de IA foi configurado.

O contexto abaixo seria enviado para um modelo de IA.

{context}

Configure um cliente OpenAI, Gemini, Claude
ou Ollama para obter respostas inteligentes.
"""

        return resposta
