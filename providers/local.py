"""Provedor local fallback, sem chamada externa."""

from __future__ import annotations

from providers.base import BaseProvider, Message


class LocalProvider(BaseProvider):
    """Retorna respostas explicativas quando nenhum LLM externo está configurado."""

    def chat(self, messages: list[Message]) -> str:
        """Mostra o payload que seria enviado a um provedor real."""
        last_message = messages[-1]["content"] if messages else ""
        return f"""
### Modo local

Nenhum provedor de IA externo foi configurado.

O conteúdo abaixo seria enviado para o modelo selecionado:

{last_message}
""".strip()
