from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def ask(
        self,
        question: str,
        context: str
    ) -> str:
        pass
