from .base import BaseProvider


class LocalProvider(BaseProvider):

    def ask(
        self,
        question,
        context
    ):

        return f"""
### Pergunta

{question}

---

Nenhuma IA foi configurada.

Contexto recebido:

{context}
"""
