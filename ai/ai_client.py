from abc import ABC, abstractmethod
from typing import Any


class AIClient(ABC):
    """
    Classe base para qualquer provedor de IA.
    """

    @abstractmethod
    def ask(
        self,
        question: str,
        context: str
    ) -> str:
        """
        Recebe uma pergunta e um contexto
        e devolve uma resposta.
        """
        raise NotImplementedError
