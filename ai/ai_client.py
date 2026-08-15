from __future__ import annotations

from abc import ABC, abstractmethod


class AIClient(ABC):
    """
    Interface para qualquer modelo de IA.
    """

    @abstractmethod
    def ask(self, question: str, context: str) -> str:
        """
        Recebe uma pergunta e o contexto
        dos dados e devolve uma resposta.
        """
        pass
