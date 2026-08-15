"""Contrato unificado para provedores de IA."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

Message = dict[str, str]


class BaseProvider(ABC):
    """Interface base para adapters de LLM usados pela aplicação."""

    @abstractmethod
    def chat(self, messages: list[Message]) -> str:
        """Envia uma lista de mensagens e retorna a resposta do modelo."""

    def ask(self, question: str, context: str) -> str:
        """Mantém compatibilidade com o fluxo legado de pergunta + contexto."""
        return self.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Você é um analista de dados. Responda em português "
                        "usando apenas o contexto fornecido."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Contexto dos dados:\n{context}\n\nPergunta: {question}",
                },
            ]
        )

    def generate_insights(self, data_summary: str) -> str:
        """Gera insights automáticos a partir de um resumo estruturado dos dados."""
        return self.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Você é um cientista de dados sênior. Gere de 3 a 5 "
                        "insights objetivos, úteis e em português."
                    ),
                },
                {"role": "user", "content": data_summary},
            ]
        )

    def explain_chart(self, chart_data: dict[str, Any] | str) -> str:
        """Explica um gráfico ou especificação de gráfico em linguagem natural."""
        return self.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Explique o gráfico como um analista de dados, destacando "
                        "padrões, possíveis causas e cautelas de interpretação."
                    ),
                },
                {"role": "user", "content": str(chart_data)},
            ]
        )
